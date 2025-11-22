""" Module providing main archive. """

import sys
# Ensure src is in path if running directly from root without install
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from whatsapp_analytics.wpp import Whatsapp
from whatsapp_analytics.graphical import Graphical

def main():
    # 1. Initialize Processor
    try:
        # Ensure WppFolder/chat.txt exists or pass the correct path
        wpp = Whatsapp(path="WppFolder/chat.txt")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Please create a 'WppFolder' and place your 'chat.txt' inside it.")
        return

    # 2. Data Cleaning (Optional Renaming)
    # Example: wpp.rename_user("old_name", "New Name")
    wpp.rename_user("mô 🤓❤️", "Maria")
    wpp.rename_user("luís rafael sena", "Luís")

    # 3. Analysis: Repeated Message Frequency
    word_to_find = "Péssimo"
    df_result, title = wpp.repeated_message(word_to_find)

    print(f"--- Analysis: {title} ---")
    print(df_result)

    # 4. Visualization
    # Create a folder 'Grafic' if you want to save output automatically
    plots = Graphical(df_result, title, save_path="Grafic", show=True)
    
    # Generate Plots
    plots.bar_plot(x_col="User", y_col=f"{word_to_find}_Frequency")
    plots.pie_plot(label_col="User", value_col=f"{word_to_find}_Frequency")

    # 5. Other Examples (Commented out)
    # frame, title = wpp.week_chart()
    # print(frame)
    # frame, title = wpp.emoji_count()
    # print(frame.head())

if __name__ == "__main__":
    main()
