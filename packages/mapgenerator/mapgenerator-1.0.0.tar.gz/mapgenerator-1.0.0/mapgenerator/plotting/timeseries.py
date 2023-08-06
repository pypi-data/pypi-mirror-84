from ast import parse
import math
import os
import logging
from matplotlib.dates import date2num, num2date

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.dates as mdates
import netCDF4

from mapgenerator.plotting.definitions import MapGenerator

logger = logging.getLogger(__name__)

class PlotSeries(MapGenerator):
    """ Main class for plotting time series """

    def __init__(self, loglevel='WARNING', **kwargs):
        """ Initialize class with attributes """
        super().__init__(loglevel=loglevel, kwargs=kwargs)
        self._current_fig = None
        self.scalex = kwargs.get('scalex', None)
        self.scaley = kwargs.get('scaley', None)
        self.suptitle_fontsize = kwargs.get('suptitle_fontsize', 24)
        self.title_fontsize = kwargs.get('title_fontsize', 16)
        self.axis_fontsize = kwargs.get('axis_fontsize', 12)
        self.plot_size = kwargs.get("plot_size", (8.0, 6.0))

    def _close(self):
        plt.close(self._current_fig)
        self._current_fig = None

    def plot_cube(self, cube, coord=None, **kwargs):
        if coord:
            coord = cube.coord(coord)
        if not coord and cube.dim_coords:
            coord = cube.dim_coords[0]
        if not coord and cube.dim_coords:
            coord = cube.aux_coords[0]

        if coord.units.calendar:
            points = date2num(coord.units.num2date(coord.points))
        else:
            points = coord.points

        if 'xlabel' not in kwargs:
            kwargs['xlabel'] = self._get_default_title(cube)
        self._current_fig = plt.figure(figsize=self.plot_size)
        self._plot_array(
            points,
            cube.data,
            title=self._get_default_title(cube),
            **kwargs,
        )
        self._set_time_axis(coord)
        self._current_fig.tight_layout()
        suptitle = kwargs.pop('suptitle', None)
        if suptitle:
            plt.suptitle(suptitle, y=1.08, fontsize=self.suptitle_fontsize)
        self._save_fig(self.img_template)
        self._close()

    def _plot_array(self, x, y, **kwargs):
        invertx = kwargs.pop('invertx', False)
        inverty = kwargs.pop('inverty', False)
        xlabel = kwargs.pop('xlabel', None)
        ylabel = kwargs.pop('ylabel', None)
        xlimits = kwargs.pop('xlimits', None)
        ylimits = kwargs.pop('ylimits', None)
        title = kwargs.pop('title', None)
        plt.plot(x, y)
        ax = plt.gca()
        if xlabel:
            ax.set_xlabel(xlabel, fontsize=self.axis_fontsize)
        if ylabel:
            ax.set_ylabel(ylabel, fontsize=self.axis_fontsize)
        if title:
            ax.set_title(title, fontsize=self.title_fontsize, y=1.04)
        if invertx:
            logger.debug('Invert x axis')
            ax.invert_xaxis()
        if inverty:
            logger.debug('Invert y axis')
            ax.invert_yaxis()
        if self.scalex:
            ax.set_xscale(self.scalex)
        if self.scaley:
            ax.set_yscale(self.scaley)
        if xlimits:
            if xlimits == 'tight':
                ax.set_xlim(left=x.min(), right=x.max())
            elif xlimits == 'auto':
               ax.set_autoscalex_on(True)
            else:
                ax.set_xlim(left=xlimits[0], right=xlimits[1])
        if ylimits:
            if ylimits == 'tight':
                ax.set_ylim(left=y.min(), right=y.max())
            elif ylimits == 'auto':
               ax.set_autoscaley_on(True)
            else:
                ax.set_ylim(left=ylimits[0], right=ylimits[1])
        ax.grid(b=True, which='major', axis='both', alpha=0.6)
        ax.grid(b=True, which='minor', axis='both', alpha=0.3)
        ax.tick_params(axis='both', which='major', labelsize=self.axis_fontsize)


    def multiplot_cube(self, cube, coord, multi_coord, ncols=2, invert=False,  **kwargs):
        coord = cube.coord(coord)
        multi_coord = cube.coord(multi_coord)
        if multi_coord.shape[0] == 1:
            self.plot_cube(cube, coord, **kwargs)
            return
        sharex = kwargs.get('sharex', False)
        sharey = kwargs.get('sharey', False)

        self._current_fig = plt.figure(
            figsize=(
                ncols * self.plot_size[0],
                math.ceil(multi_coord.shape[0] / ncols) * self.plot_size[1])
        )
        suptitle = kwargs.pop('suptitle', '')
        if suptitle:
            suptitle =  f"{suptitle}\n\n{self._get_default_title(cube)}"
        else:
            suptitle =  self._get_default_title(cube)
        self._current_fig.suptitle(
            suptitle, y=1.0, fontsize=self.suptitle_fontsize
        )
        gs = GridSpec(math.ceil(multi_coord.shape[0] / ncols), ncols)
        for i, plot_cube in enumerate(cube.slices_over(multi_coord)):
            if i == 0 or not (sharex or sharey):
                self._current_fig.add_subplot(gs[i])
            elif sharex:
                if sharey:
                    self._current_fig.add_subplot(gs[i], sharex=plt.gca(), sharey=plt.gca())
                    kwargs.pop('invertx', None)
                    kwargs.pop('inverty', None)
                else:
                    self._current_fig.add_subplot(gs[i], sharex=plt.gca())
                    kwargs.pop('invertx', None)
            elif sharey:
                self._current_fig.add_subplot(gs[i], sharey=plt.gca())
                kwargs.pop('inverty', None)
            title = plot_cube.coord(multi_coord).cell(0).point
            if isinstance(title, bytes):
                title = title.decode()
            plt.title(
                title,
                fontsize=self.title_fontsize
            )
            if coord.units.calendar:
                points = date2num(coord.units.num2date(coord.points))
            else:
                points = coord.points
            if invert:
                x = plot_cube.data
                y = points
                if 'ylabel' not in kwargs:
                    kwargs['ylabel'] = self._get_default_title(coord)
            else:
                x = points
                y = plot_cube.data
                if 'xlabel' not in kwargs:
                    kwargs['xlabel'] = self._get_default_title(coord)

            self._plot_array(
                x, y, **kwargs,
            )
            self._set_time_axis(coord)

        self._current_fig.tight_layout(pad=2.0)
        self._save_fig(self.img_template)
        self._close()

    def _save_fig(self, name):
        fullname = os.path.join(self.outdir ,f"{name}.{self.filefmt}")
        self._current_fig.savefig(fullname, bbox_inches='tight', pad_inches=.2, dpi=self.dpi)

    

    @staticmethod
    def _set_time_axis(coord):
        if not coord.units.calendar:
            return
        axis = plt.gca().xaxis
        years = coord.cell(-1).point.year - coord.cell(0).point.year
        if years < 10:
            major_locator = 1
            minor_locator = None
        elif years < 50:
            major_locator = 5
            minor_locator = 1
        elif years < 100:
            major_locator = 10
            minor_locator = 2
        else:
            major_locator = 20
            minor_locator = 5
        axis.set_major_locator(mdates.YearLocator(major_locator))
        if minor_locator:
            axis.set_minor_locator(mdates.YearLocator(minor_locator))
        axis.set_major_formatter(mdates.DateFormatter('%Y'))
        axis.label._text = f"{coord.name()} (years)"

