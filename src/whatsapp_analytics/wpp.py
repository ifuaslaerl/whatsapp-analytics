""" Module containing the WhatsApp processing class. """

import re
import typing
import pathlib
from collections import Counter
import pandas as pd

class Whatsapp:
    """ Class used to process WhatsApp chat exports. """

    def __init__(self, path: typing.Union[str, pathlib.Path] = "WppFolder/chat.txt"):
        """
        Initialize the Whatsapp analyzer.

        Args:
            path (str | Path): Path to the WhatsApp chat export text file.
        """
        self.path = pathlib.Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"Chat file not found at: {self.path}")

        self.df = pd.DataFrame()
        self.data = self._load_data()
        
        # Initialize self.df with unique users
        self.df["User"] = self.data["User"].unique()

    def _load_data(self) -> pd.DataFrame:
        """ Helper method to load and parse the chat text file. """
        with open(self.path, encoding="UTF-8") as f:
            chat_content = f.read().lower()
        
        # Regex to match: Date Time - User: Message
        # Format example: 12/05/2023 14:30 - John Doe: Hello world
        line_format = r'(\d{1,2}\/\d{1,2}\/\d{1,4}) (\d{1,2}:\d{1,2}) - (.+?): (.*)'
        pattern = re.compile(line_format)
        matches = pattern.findall(chat_content)
        
        data = pd.DataFrame(matches, columns=["Day", "Hour", "User", "Message"])
        
        # Create a proper Datetime column
        data["Datetime"] = pd.to_datetime(
            data["Day"] + " " + data["Hour"], 
            format="%d/%m/%Y %H:%M"
        )
        
        # Drop intermediate columns and reorder
        return data[["Datetime", "User", "Message"]]

    def __len__(self) -> int:
        return len(self.data)

    def rename_user(self, user: str, new_name: str) -> None:
        """ Rename a user in the dataframe (e.g. to fix nicknames). """
        self.data["User"] = self.data["User"].replace(user, new_name)
        # Update the summary dataframe as well if it exists
        if "User" in self.df.columns:
            self.df["User"] = self.df["User"].replace(user, new_name)

    def ranking(self) -> typing.Tuple[pd.DataFrame, str]:
        """ Gets the ranking of who sends the maximum amount of messages. """
        # Count messages per user
        message_frame = self.data["User"].value_counts().reset_index()
        message_frame.columns = ["User", "MessageCount"]

        # Count characters per user
        char_frame = self.data.groupby("User")["Message"].apply(
            lambda x: x.str.len().sum()
        ).reset_index()
        char_frame.columns = ["User", "TotalCharacters"]

        ranking = pd.merge(message_frame, char_frame, on="User")
        
        # Merge results into the main summary df
        self.df = pd.merge(self.df, ranking, on="User", how="left")

        return ranking, "Ranking"

    def emoji_count(self) -> typing.Tuple[pd.DataFrame, str]:
        """ Get frequency of all emojis. """
        # Regex range for common emojis and symbols
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # Faces
            "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
            "\U0001F680-\U0001F6FF"  # Transport
            "\U0001F1E0-\U0001F1FF"  # Flags
            "\U00002700-\U000027BF"  # Dingbats
            "\U000024C2-\U0001F251"  # Misc
            "]+"
        )
        
        all_emojis = []
        for message in self.data["Message"]:
            found_emojis = emoji_pattern.findall(str(message))
            for emoji_group in found_emojis:
                all_emojis.extend(list(emoji_group))

        emoji_counts = Counter(all_emojis)
        
        frame = pd.DataFrame(emoji_counts.items(), columns=["Emoji", "Count"])
        frame.sort_values(by="Count", ascending=False, inplace=True)
        frame.reset_index(drop=True, inplace=True)

        return frame, "Emojis"

    def week_chart(self) -> typing.Tuple[pd.DataFrame, str]:
        """ Get amount of messages broken down by days of the week. """
        frame = pd.DataFrame()
        frame["User"] = self.data["User"]
        frame["WeekDay"] = self.data["Datetime"].dt.strftime('%A')

        # Pivot table: Users as rows, Days as columns
        pivot = frame.groupby(['User', 'WeekDay']).size().unstack(fill_value=0)
        pivot.columns.name = None
        pivot.reset_index(inplace=True)

        # Ensure all days are present and ordered
        days_order = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        # Add missing days as 0
        for day in days_order:
            if day not in pivot.columns:
                pivot[day] = 0
        
        pivot = pivot[["User"] + days_order]

        # Add "AllUsers" row
        sum_row = pivot.drop(columns="User").sum(numeric_only=True)
        pivot.loc[len(pivot)] = ["AllUsers"] + sum_row.tolist()

        self.df = pd.merge(self.df, pivot, on="User", how="left")

        return pivot, "WeekFrequency"

    def repeated_message(self, find: str) -> typing.Tuple[pd.DataFrame, str]:
        """ Get frequency of a specific string in messages. """
        target = find.lower()
        
        # Check if target is in message
        has_word = self.data["Message"].apply(lambda x: target in str(x).lower())
        
        frame = pd.DataFrame({
            "User": self.data["User"],
            f"{find}_Frequency": has_word.astype(int)
        })

        result = frame.groupby("User")[f"{find}_Frequency"].sum().reset_index()
        self.df = pd.merge(self.df, result, on="User", how="left")

        return result, f"{find}_Frequency"

    def word_count(self) -> typing.Tuple[pd.DataFrame, str]:
        """ Creates a DataFrame of word frequency per user. """
        contador_usuarios = {}

        for usuario, messages in self.data.groupby("User")["Message"]:
            text = ' '.join(messages).lower()
            # Simple split by whitespace
            word_counts = Counter(text.split())
            contador_usuarios[usuario] = word_counts

        frame = pd.DataFrame.from_dict(contador_usuarios, orient='index').fillna(0).astype(int)

        # Sort users (rows) by total word count
        frame = frame.loc[frame.sum(axis=1).sort_values(ascending=False).index]
        
        # Sort words (columns) by total frequency across all users
        frame = frame[frame.sum(axis=0).sort_values(ascending=False).index]

        return frame, "WordFrequency"
