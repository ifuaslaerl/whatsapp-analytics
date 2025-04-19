""" Module providing Grafical tools. """

import os
import typing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Grafical:
    """ Class representing grafical data. """

    def __init__(self, data: pd.DataFrame, title: str,\
                color: typing.Optional[str] = "tab20",
                save_path: typing.Optional[str] = None,
                show: typing.Optional[bool] = True,
                fig_size: typing.Optional[typing.Tuple[int, int]] = (5, 5)):
        self.title = title
        self.save_path = save_path
        self.show = show
        self.data = data
        self.fig_size = fig_size

        colormap = plt.cm.get_cmap(color)
        self.cmap = tuple( [mcolors.to_hex(colormap(i)) for i in range(colormap.N)] )

    def __end_plot(self, title: str) -> None:
        plt.title(self.title + " | " + title)
        if self.save_path:
            plt.savefig(os.path.join(self.save_path,self.title+title))
        if self.show:
            plt.show()
        plt.close()

    def bar_plot(self, x: str, y: str) -> None:
        """ Plot bar grafic. """

        plt.xlabel(x)
        plt.ylabel(y)
        plt.bar(self.data[x], self.data[y], color=self.cmap)
        self.__end_plot("Bar")

    def pie_plot(self, x: str, y: str) -> None:
        """ Plot Pie Grafic. """

        plt.pie(self.data[y], labels=self.data[x], autopct='%.1f%%', colors=self.cmap)
        self.__end_plot("Pie")

    def radar_chart(self, x, y) -> None:
        """ Plot Radar chart. """

        labels = list(x)
        values = list(y)

        num_vars = len(labels)

        fig, ax = plt.subplots(subplot_kw=dict(polar=True))

        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        values.append(values[0])
        angles.append(angles[0])


        ax.plot(angles, values, linewidth=1, linestyle='solid', label='Data 1')
        ax.fill(angles, values, alpha=0.25)

        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        self.__end_plot("Radar")
