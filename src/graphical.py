""" Module providing Graphical visualization tools. """

import os
import typing
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

class Graphical:
    """ Class representing graphical data visualization. """

    def __init__(self, data: pd.DataFrame, title: str,
                 color: typing.Optional[str] = "tab20",
                 save_path: typing.Optional[str] = None,
                 show: typing.Optional[bool] = True,
                 fig_size: typing.Tuple[int, int] = (6, 6)):
        
        self.title = title
        self.save_path = save_path
        self.show = show
        self.data = data
        self.fig_size = fig_size

        # Handle colormap retrieval safely
        if hasattr(plt, 'get_cmap'):
            colormap = plt.get_cmap(color)
        else:
            colormap = plt.cm.get_cmap(color)
            
        self.cmap = tuple([mcolors.to_hex(colormap(i)) for i in range(colormap.N)])

    def _end_plot(self, subtitle: str) -> None:
        """ Finalize the plot with title, save, and show options. """
        plt.title(f"{self.title} | {subtitle}")
        plt.tight_layout()
        
        if self.save_path:
            os.makedirs(self.save_path, exist_ok=True)
            filename = f"{self.title}_{subtitle}.png".replace(" ", "_")
            plt.savefig(os.path.join(self.save_path, filename))
            
        if self.show:
            plt.show()
        plt.close()

    def bar_plot(self, x_col: str, y_col: str) -> None:
        """ Plot a Bar graphic. """
        plt.figure(figsize=self.fig_size)
        plt.xlabel(x_col)
        plt.ylabel(y_col)
        
        # Ensure we have enough colors or cycle them
        colors = self.cmap[:len(self.data)] if len(self.data) <= len(self.cmap) else self.cmap
        
        plt.bar(self.data[x_col], self.data[y_col], color=colors)
        self._end_plot("Bar")

    def pie_plot(self, label_col: str, value_col: str) -> None:
        """ Plot a Pie graphic. """
        plt.figure(figsize=self.fig_size)
        
        # Ensure we have enough colors
        colors = self.cmap[:len(self.data)] if len(self.data) <= len(self.cmap) else self.cmap

        plt.pie(self.data[value_col], labels=self.data[label_col], 
                autopct='%.1f%%', colors=colors)
        self._end_plot("Pie")

    def radar_chart(self, label_col: str, value_col: str) -> None:
        """ Plot a Radar chart. """
        labels = list(self.data[label_col])
        values = list(self.data[value_col])

        num_vars = len(labels)

        # Compute angle for each axis
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Complete the loop
        values.append(values[0])
        angles.append(angles[0])

        fig, ax = plt.subplots(figsize=self.fig_size, subplot_kw=dict(polar=True))

        ax.plot(angles, values, linewidth=1, linestyle='solid', label='Data')
        ax.fill(angles, values, alpha=0.25)

        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)

        self._end_plot("Radar")
