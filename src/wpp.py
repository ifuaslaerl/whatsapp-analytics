""" Module containing whatsapp processing class. """

import re
import typing
from collections import Counter
import pandas as pd

class Whatsapp:
    """ Class used to process whatsapp chat. """

    def __init__(self, path="WppFolder/chat.txt"):
        self.path = path
        self.df = pd.DataFrame()
        with open(path,encoding="UTF-8") as f:
            self.chat = f.read().lower()
            line_format = \
                r'(\d{1,2}\/\d{1,2}\/\d{1,4}) (\d{1,2}:\d{1,2}) - (.+?): (.*)'
            pattern = re.compile(line_format)
            data = pattern.findall(self.chat)
            self.data = pd.DataFrame(data, columns=["Day", "Hour", "User", "Message"])

            self.data["Datetime"] = pd.to_datetime(self.data["Day"] + " " + self.data["Hour"],
                                                    format="%d/%m/%Y %H:%M")

            self.data.drop(columns=["Day", "Hour"], inplace=True)
            self.data = self.data[["Datetime", "User", "Message"]]
            self.data["Message"] = self.data["Message"]
        self.df["User"] = self.data["User"].unique()

    def __len__(self) -> int:
        return len(self.data)

    def rename_user(self, user: str, new_name: str) -> None:
        """ Rename user to new_name. """
        self.data["User"] = self.data["User"].replace(user,new_name)
        self.df["User"] = self.df["User"].replace(user,new_name)

    def ranking(self) -> typing.Tuple[pd.DataFrame , str]:
        """ Gets the ranking of who sends the maximum amount of messages. """
        message_frame = self.data["User"].value_counts().reset_index()
        message_frame.columns = ["User", "MessageCount"]

        char_frame = self.data.groupby("User")["Message"].\
            apply(lambda x: x.str.len().sum()).reset_index()

        char_frame.columns = ["User", "TotalCharacters"]

        ranking = pd.merge(message_frame, char_frame)

        ranking = ranking[["User", "MessageCount", "TotalCharacters"]]

        self.df = pd.merge(ranking, self.df)

        return ranking, "Ranking"

    def emoji_count(self) -> typing.Tuple[pd.DataFrame , str]:
        """ Get frequency of all emojis. """

        emoji_pattern = re.compile(
            "[" 
            "\U0001F600-\U0001F64F"  # Emojis de rosto
            "\U0001F300-\U0001F5FF"  # Símbolos e pictogramas
            "\U0001F680-\U0001F6FF"  # Transporte e mapas
            "\U0001F1E0-\U0001F1FF"  # Bandeiras
            "\U00002700-\U000027BF"  # Diversos símbolos adicionais
            "\U000024C2-\U0001F251"  # Símbolos diversos
            "]+"
        )
        all_emojis = []

        for message in self.data["Message"]:
            found_emojis = emoji_pattern.findall(message)

            for emoji in found_emojis:
                all_emojis.extend(list(emoji))

        emoji_counts = Counter(all_emojis)

        frame = pd.DataFrame(emoji_counts.items(), columns=["Emoji", "Count"])
        frame.sort_values(by="Count", ascending=False, inplace=True)

        frame.reset_index(drop=True, inplace=True)

        return frame, "Emojis"

    def week_chart(self) -> typing.Tuple[pd.DataFrame , str]:
        """ Get amount of messages in days of week. """

        frame = pd.DataFrame()
        frame["User"] = self.data["User"]
        frame["WeekDay"] = self.data["Datetime"].dt.strftime('%A')

        frame = frame.groupby(['User', 'WeekDay']).size().unstack(fill_value=0)

        frame.columns.name = None
        frame.reset_index(inplace=True)

        frame = frame[["User", "Sunday", "Monday", "Tuesday",\
                        "Wednesday", "Thursday", "Friday", "Saturday"]]

        frame.loc["AllUsers"] = frame.sum(numeric_only=True)
        frame.loc["AllUsers","User"] = "AllUsers"

        self.df = pd.merge(self.df, frame)

        return frame , "WeekFrequency"

    def repeated_message(self, find: str) -> typing.Tuple[pd.DataFrame , str]:
        """ Get amount of repetition os string in messages. """

        frame = pd.DataFrame()
        frame[f"{find}_Frequency"] = self.data["Message"].apply(lambda x: find.lower() in str(x).lower())
        # frame[f"{find}_Frequency"] = self.data["Message"].str.count(find)
        frame["User"] = self.data["User"]

        frame = frame.groupby("User")[f"{find}_Frequency"].sum().reset_index()

        self.df = pd.merge(self.df, frame)

        return frame , f"{find}_Frequency"

    def word_count(self)-> typing.Tuple[pd.DataFrame , str]:
        """ Cria um DataFrame que representa a quantidade de vezes que
            cada usuário digitou cada palavra.
        """
        contador_usuarios = {}

        for usuario, mensagens in self.data.groupby("User")["Message"]:
            texto = ' '.join(mensagens).lower()
            palavras_contadas = Counter(texto.split())
            contador_usuarios[usuario] = palavras_contadas

        frame = pd.DataFrame.from_dict(contador_usuarios, orient='index').\
                fillna(0).astype(int)

        frame = frame.loc[frame.sum(axis=1).sort_values(ascending=False).index]

        frame = frame[frame.sum(axis=0).sort_values(ascending=False).index]

        return frame, "WordFrequency"

def main():
    """ Debugging function. """

    wpp = Whatsapp()

    #wpp.ranking()
    #wpp.repeated_message("dias")
    frame , title = wpp.week_chart()
    print(frame)
    #wpp.df.to_csv("tortilha.csv")

    frame, title = wpp.emoji_count()
    #frame.to_csv(f"{title}.csv")

    frame , title = wpp.word_count()
    #frame.to_csv(f"{title}.csv")

if __name__ == "__main__":
    main()
