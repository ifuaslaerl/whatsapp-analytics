"""
Example 2: Visualization
This script demonstrates how to generate Bar and Pie charts.
"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from whatsapp_analytics import Whatsapp, Graphical

def main():
    chat_path = "WppFolder/chat.txt"
    
    try:
        wpp = Whatsapp(path=chat_path)
    except FileNotFoundError:
        print(f"File not found: {chat_path}")
        return

    # --- Scenario A: Emoji Analysis ---
    emoji_df, title = wpp.emoji_count()
    
    # Filter to top 10 emojis to keep the chart readable
    top_emojis = emoji_df.head(10)
    
    print(f"Plotting {title}...")
    plots = Graphical(top_emojis, title, save_path="../Grafic", show=True)
    
    # Create a Bar Plot of top emojis
    plots.bar_plot(x_col="Emoji", y_col="Count")

    # --- Scenario B: Specific Word Frequency ---
    target_word = "Bom dia"  # "Good morning"
    word_df, title = wpp.repeated_message(target_word)
    
    print(f"Plotting {title}...")
    plots_word = Graphical(word_df, title, save_path="../Grafic", show=True)
    
    # Create a Pie Plot showing who says "Bom dia" the most
    plots_word.pie_plot(label_col="User", value_col=f"{target_word}_Frequency")

if __name__ == "__main__":
    main()
