"""
Example 1: Basic Statistics
This script demonstrates how to load chat data and print text rankings.
"""

import sys
import os

# Add the src folder to path so we can import without installing
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from whatsapp_analytics import Whatsapp

def main():
    # Ensure you have your chat file at this path
    chat_path = "WppFolder/chat.txt"
    
    try:
        wpp = Whatsapp(path=chat_path)
    except FileNotFoundError:
        print(f"Could not find chat file at: {chat_path}")
        return

    print("--- Loading Chat Data ---")
    print(f"Total messages found: {len(wpp)}")

    # 1. Generate Ranking (Messages & Characters)
    ranking_df, title = wpp.ranking()
    
    print(f"\n--- {title} ---")
    print(ranking_df)

    # 2. Word Count Analysis (Frequency of words per user)
    word_df, title = wpp.word_count()
    print(f"\n--- {title} (Top 5 rows) ---")
    print(word_df.head(5))

if __name__ == "__main__":
    main()
