""" Module providing main archive. """

from src.wpp import Whatsapp
from src.grafical import Grafical

if __name__ == "__main__":

    wpp = Whatsapp()
    wpp.rename_user("mô 🤓❤️", "Maria")
    wpp.rename_user("luís rafael sena", "Luís")

    word = "Péssimo"
    df, title = wpp.repeated_message(word)

    print(df)
    plots = Grafical(df, title)
    plots.bar_plot("User", f"{word}_Frequency")
    plots.pie_plot("User", f"{word}_Frequency")