"""
Example 3: Radar Chart
This script demonstrates how to visualize weekly activity using a Radar Chart.
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
        return

    # Clean up user names if necessary
    wpp.rename_user("mom_cellphone", "Mom")

    # Get weekly data
    # Returns a dataframe with cols: User, Sunday, Monday, ..., Saturday
    week_df, title = wpp.week_chart()

    # We need to transform the data for the Radar chart.
    # The radar chart expects one row of data to plot against axis labels.
    
    # Let's plot the "AllUsers" aggregate to see group activity
    all_users_data = week_df[week_df["User"] == "AllUsers"]

    if all_users_data.empty:
        print("No data found.")
        return

    # Prepare data for plotting
    # Melt the dataframe to get two columns: 'Day' (labels) and 'Count' (values)
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    # Create a simple structure for the Graphical class
    # Note: The current Graphical.radar_chart expects the dataframe to have the columns we specify
    # We will create a temporary dataframe for the plot
    plot_data = {
        "Day": days,
        "Count": all_users_data.iloc[0][days].values.flatten()
    }
    import pandas as pd
    df_radar = pd.DataFrame(plot_data)

    print(f"Plotting {title} Radar Chart...")
    plots = Graphical(df_radar, "Weekly Activity Pattern", save_path="../Grafic", show=True)
    
    # Plot: Labels are Days, Values are Message Counts
    plots.radar_chart(label_col="Day", value_col="Count")

if __name__ == "__main__":
    main()
