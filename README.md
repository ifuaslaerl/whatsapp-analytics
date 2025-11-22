# WhatsApp Analytics

A Python tool to parse, analyze, and visualize WhatsApp chat exports.

## Features
- **Ranking**: See who sends the most messages and characters.
- **Emoji Analysis**: Count and rank emoji usage.
- **Activity Charts**: Visualize message frequency by day of the week.
- **Word Frequency**: Analyze word usage per user.
- **Visualization**: Generate Bar, Pie, and Radar charts.

## Installation

1. Clone the repository.
2. Install dependencies:
```bash
pip install .
# OR manually
pip install pandas matplotlib numpy
```

## Usage

1. **Export Chat**: Open a WhatsApp chat, go to **More > Export chat**, and choose "Without Media".
2. **Setup Folder**: Place the exported `.txt` file inside a folder named `WppFolder` (or specify the path in the code).
3. **Run the Script**:
```bash
python main.py
```

## Project Structure
- `src/whatsapp_analytics/wpp.py`: Core logic for parsing and analysis.
- `src/whatsapp_analytics/graphical.py`: Visualization tools using Matplotlib.
