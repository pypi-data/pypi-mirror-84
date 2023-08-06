"""
Module to visualize arrival directions or heatmaps on the sphere.
"""

import healpy as hp
import matplotlib.pyplot as plt
import numpy as np

from astrotools import coord, healpytools as hpt


def scatter(v, c=None, cblabel='log$_{10}$(Energy / eV)', opath=None, fig=None, **kwargs):
    """
    Scatter plot of events with arrival directions x,y,z and colorcoded energies.

    :param v: array of shape (3, n) pointing into directions of the events
    :param c: quantity that is supposed to occur in colorbar, e.g. energy of the cosmic rays
    :param cblabel: colorbar label
    :param opath: if not None, saves the figure to the given opath (no returns)
    :param fig: figure to plot in, creates new figure if None
    :param kwargs: additional named keyword arguments

           - figsize: figure size as input for plt.figure()
           - cmap: colormap
           - cbar: if True includes a colobar
           - cticks: sets ticks of colormap
           - mask_alpha: alpha value for maskcolor
           - fontsize: scale the general fontsize
           - dark_grid: if True paints a dark grid (useful for bright maps)
           - gridcolor: Color of the grid.
           - gridalpha: Transparency value of the gridcolor.
           - tickcolor: Color of the ticks.
           - tickalpha: Transparency of the longitude ticks.
           - plane: plots 'SGP' or 'GP' or both (list) into plot
           - planecolor: color of plane
           - coord_system: default galactic ('gal') / equatorial ('eq')
    :return: figure, axis of the scatter plot
    """

    lons, lats = coord.vec2ang(v)

    fontsize = kwargs.pop('fontsize', 26)
    kwargs.setdefault('s', 8)
    if 'marker' not in kwargs:
        kwargs.setdefault('lw', 0)
    cbar = kwargs.pop('cbar', True) and isinstance(c, (list, tuple, np.ndarray))
    if cbar:
        vmin = kwargs.pop('vmin', smart_round(np.min(c[np.isfinite(c)]), upper_border=False))
        vmax = kwargs.pop('vmax', smart_round(np.max(c[np.isfinite(c)]), upper_border=True))
        step = smart_round((vmax - vmin) / 5., order=1)
        cticks = kwargs.pop('cticks', np.round(np.arange(vmin, vmax, step), int(np.round(-np.log10(step), 0))))
        clabels = kwargs.pop('clabels', cticks)

    # read keyword arguments for the grid
    dark_grid = kwargs.pop('dark_grid', True)
    gridcolor = kwargs.pop('gridcolor', 'lightgray' if dark_grid is None else 'black')
    gridalpha = kwargs.pop('gridalpha', 0.5 if dark_grid is None else 0.4)
    tickcolor = kwargs.pop('tickcolor', 'lightgray' if dark_grid is None else 'black')
    tickalpha = kwargs.pop('tickalpha', 0.5 if dark_grid is None else 1)
    planecolor = kwargs.pop('planecolor', 'darkgray')
    plane = kwargs.pop('plane', None)
    coord_system = kwargs.pop('coord_system', 'gal')

    if coord_system == 'eq':
        lons, lats = coord.vec2ang(coord.gal2eq(coord.ang2vec(lons, lats)))

    # mimic astronomy convention: positive longitudes evolving to the left with respect to GC
    lons = -lons

    # plot the events
    fig = plt.figure(figsize=kwargs.pop('figsize', [12, 6])) if fig is None else fig
    ax = fig.add_axes([0.1, 0.1, 0.85, 0.9], projection="hammer")
    events = ax.scatter(lons, lats, c=c, **kwargs)

    if cbar:
        cbar = plt.colorbar(events, orientation='horizontal', shrink=0.85, pad=0.05, aspect=30, ticks=cticks)
        cbar.set_label(cblabel, fontsize=fontsize)
        events.set_clim(vmin, vmax)
        cbar.ax.tick_params(labelsize=fontsize - 4)
        cbar.set_ticklabels(clabels)
        cbar.draw_all()

    # Setup the grid
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    plot_grid(gridcolor=gridcolor, gridalpha=gridalpha, tickalpha=tickalpha, tickcolor=tickcolor, fontsize=fontsize)

    if plane is not None:
        plot_plane(planecolor, coord_system, plane)

    if opath is not None:
        plt.savefig(opath, bbox_inches='tight')
        plt.clf()

    return fig, ax


def heatmap(m, opath=None, label='entries', mask=None, maskcolor='white', **kwargs):
    """
    Heatmap plot of binned data m. For exmaple usage see: cosmic_rays.plot_healpy_map()

    :param m: Array with size npix for an arbitrary healpy nside.
    :param opath: if not None, saves the figure to the given opath (no returns)
    :param label: label for the colormap
    :param mask: either boolean mask that paints certain pixels different or condition for m
    :param maskcolor: which color to paint the mask
    :param kwargs: additional named keyword arguments (non-listed keywords are passed to matplotlib.pcolormesh)

           - figsize: figure size as input for plt.figure()
           - cmap: colormap
           - vmin: Lower cut of the colorbar scale
           - vmax: Upper cut of the colorbar scale
           - cbticks: Ticks of the colorbar
           - mask_alpha: alpha value for maskcolor
           - fontsize: scale the general fontsize
           - xresolution: Scales the resolution of the plot (default: 800)
           - dark_grid: if True paints a dark grid (useful for bright maps)
           - gridcolor: Color of the grid.
           - gridalpha: Transparency value of the gridcolor.
           - tickcolor: Color of the ticks.
           - tickalpha: Transparency of the longitude ticks.
           - plane: plots 'SGP' or 'GP' or both (list) into plot
           - planecolor: color of plane
           - coord_system: default galactic ('gal') / equatorial ('eq')
    :return: figure of the heatmap, colorbar
    """

    # read general keyword arguments
    fontsize = kwargs.pop('fontsize', 26)

    # create the meshgrid and project the map to a rectangular matrix (xresolution x yresolution)
    xresolution = kwargs.pop('xresolution', 800)
    yresolution = xresolution // 2
    theta = np.linspace(np.pi, 0, yresolution)
    phi = np.linspace(-np.pi, np.pi, xresolution)
    longitude = np.deg2rad(np.linspace(-180, 180, xresolution))
    latitude = np.deg2rad(np.linspace(-90, 90, yresolution))

    phi_grid, theta_grid = np.meshgrid(phi, theta)
    grid_pix = hp.ang2pix(hp.get_nside(m), theta_grid, phi_grid)

    # management of the colormap
    cmap = kwargs.pop('cmap', 'viridis')
    coord_system = kwargs.pop('coord_system', 'gal')
    planecolor = kwargs.pop('planecolor', 'darkred')
    plane = kwargs.pop('plane', None)

    if isinstance(cmap, str):
        cmap = plt.cm.get_cmap(cmap)
    if mask is not None:
        if not hasattr(mask, 'size'):
            mask = m == mask
        m = np.ma.masked_where(mask, m)
        cmap.set_bad(maskcolor, alpha=kwargs.pop('mask_alpha', 1))

    if coord_system == 'eq':
        hrot = hp.Rotator(coord=['G', 'C'], inv=True)
        theta, phi = hp.pix2ang(hpt.get_nside(m), np.arange(len(m)))
        g0, g1 = hrot(theta, phi)
        pix0 = hp.ang2pix(hpt.get_nside(m), g0, g1)
        m = m[pix0]
    grid_map = m[grid_pix]

    finite = np.isfinite(m)
    vmin = kwargs.pop('vmin', smart_round(np.min(m[finite]), upper_border=False))
    vmax = kwargs.pop('vmax', smart_round(np.max(m[finite]), upper_border=True))
    cbticks = kwargs.pop('cbticks', [vmin, (vmin + vmax) / 2, vmax])

    # read keyword arguments for the grid
    dark_grid = kwargs.pop('dark_grid', None)
    gridcolor = kwargs.pop('gridcolor', 'lightgray' if dark_grid is None else 'black')
    gridalpha = kwargs.pop('gridalpha', 0.5 if dark_grid is None else 0.4)
    tickcolor = kwargs.pop('tickcolor', 'lightgray' if dark_grid is None else 'black')
    tickalpha = kwargs.pop('tickalpha', 0.5 if dark_grid is None else 1)

    # Start plotting
    fig = plt.figure(figsize=kwargs.pop('figsize', (12, 12)))
    fig.add_subplot(111, projection='hammer')
    # flip longitude to the astro convention
    # rasterized makes the map bitmap while the labels remain vectorial
    image = plt.pcolormesh(longitude[::-1], latitude, grid_map, rasterized=True, vmin=vmin, vmax=vmax, cmap=cmap,
                           edgecolor='face', shading='auto', **kwargs)
    cb = fig.colorbar(image, ticks=cbticks, orientation='horizontal', aspect=30, shrink=0.9, pad=0.05)
    cb.solids.set_edgecolor("face")
    cb.set_label(label, fontsize=fontsize)
    cb.ax.tick_params(axis='x', direction='in', size=3, labelsize=fontsize - 4)

    if plane is not None:
        plot_plane(planecolor, coord_system, plane)

    # Setup the grid
    plot_grid(gridcolor=gridcolor, gridalpha=gridalpha, tickalpha=tickalpha, tickcolor=tickcolor, fontsize=fontsize)

    if opath is not None:
        plt.savefig(opath, bbox_inches='tight')
        plt.clf()

    return fig, cb


def plot_grid(lon_ticks=None, lat_ticks=None, lon_grid=30, lat_grid=30, fontsize=26, **kwargs):
    """
    Plot a grid on the skymap.

    :param lon_ticks: Set the label ticks for the longitudes (default: [90, 0, -90]).
    :param lat_ticks: Set the label ticks for the latitude (default: [-60, -30, 0, 30, 60]).
    :param lon_grid: Distances between the grid lines in longitude in degrees (default: 30 deg).
    :param lat_grid: Distances between the grid lines in latitude in degrees (default: 30 deg).
    :param kwargs: additional named keyword arguments

            - gridcolor: Color of the grid.
            - gridalpha: Transparency value of the gridcolor.
            - tickcolor: Color of the ticks.
            - tickalpha: Transparency of the longitude ticks.
    """
    lon_ticks = [90, 0, -90] if lon_ticks is None else lon_ticks
    lat_ticks = [-60, -30, 0, 30, 60] if lat_ticks is None else lat_ticks
    plt.gca().set_longitude_grid(lon_grid)
    plt.gca().set_latitude_grid(lat_grid)
    plt.gca().set_longitude_grid_ends(89)

    plt.grid(alpha=kwargs.pop('gridalpha', 0.5), color=kwargs.pop('gridcolor', 'lightgray'))
    plt.gca().set_xticklabels(np.append(np.hstack([(r'', r'', r'%d$^{\circ}$' % l) for l in lon_ticks]), [r'', r'']),
                              alpha=kwargs.pop('tickalpha', 0.5), fontsize=fontsize)
    plt.gca().tick_params(axis='x', colors=kwargs.pop('tickcolor', 'lightgray'))
    plt.gca().set_yticklabels([r'%d$^{\circ}$' % lat for lat in lat_ticks], fontsize=fontsize)


def plot_plane(planecolor=0.5, coord_system='gal', plane='SGP', **kwargs):
    """
    Plot a the supergalactic plane onto skymap.

    :param planecolor: color of plane
    :param coord_system: default galactic ('gal') / equatorial ('eq')
    :param plane: plots 'SGP' or 'GAL' or both (list) into plot
    :param kwargs: additional named keyword arguments passed to plt.plot()
    """
    phi0 = np.linspace(0, 2*np.pi, 100)
    if coord_system.upper() == 'GAL':
        # only plotting the SGP makes sense
        phi, theta = coord.vec2ang(coord.sgal2gal(coord.ang2vec(phi0, np.zeros_like(phi0))))
        kwargs.setdefault('color', planecolor)
        plt.plot(-np.sort(phi), theta[np.argsort(phi)], **kwargs)

    elif coord_system.upper() == 'EQ':
        if 'SGP' in plane:
            phi, theta = coord.vec2ang(coord.gal2eq(coord.sgal2gal(coord.ang2vec(phi0, np.zeros_like(phi0)))))
            kwargs.setdefault('color', planecolor)
            plt.plot(-np.sort(phi), theta[np.argsort(phi)], **kwargs)
        if 'GAL' in plane:
            phi, theta = coord.vec2ang(coord.gal2eq(coord.ang2vec(phi0, np.zeros_like(phi0))))
            kwargs.setdefault('color', '0.5')
            plt.plot(-np.sort(phi), theta[np.argsort(phi)], **kwargs)
        else:
            raise Exception("plane type not understood, use GP or SGP or list!")
    else:
        raise Exception("coord system not understood, use eq or gal!")


def plot_tissot(vec_c, r, res=1e-2, **kwargs):
    """
    Plot a circle onto skymap.

    :param vec_c: vector pointing to the center of the circle
    :param r: radius of the circle
    :param res: resolution of the circle approximation (in radian)
    :param kwargs: additional named keyword arguments passed to plt.plot()
    """
    lon, lat = coord.vec2ang(vec_c)
    vec_ref = coord.rotate(vec_c, coord.sph_unit_vectors(lon, lat)[2], r)
    psis = np.arange(0, 2*np.pi, res)
    lons, lats = coord.vec2ang(coord.rotate(vec_ref, vec_c, psis))
    plt.plot(-lons, lats, **kwargs)


def smart_round(v, order=2, upper_border=True):
    """
    Rounds a value v such that it can be used e.g. for colorbars

    :param v: scalar value which should be rounded
    :type v: int, float
    :param upper_border: round such that the value can be used as an upper border of an interval, default=True
    :param order: number of digits to round to, default=2
    :return: rounded value
    :rtype: int, float

    This function has been tested on the following numbers (with all upper_border presented here):

    .. code-block:: python

        :linenos:
        >> from astrotools.skymap import smart_round
        >> smart_round(100000), smart_round(100000, upper_border=False)
        100000.0, 100000.0
        >> smart_round(100001), smart_round(100001, upper_border=False)
        101000.0, 100000.0
        >> smart_round(-100001), smart_round(-100001, upper_border=False)
        -100000.0, -100000.0
        >> smart_round(2.23), smart_round(2.23, upper_border=False)
        2.23, 2.23
        >> smart_round(2.230), smart_round(2.230, upper_border=False)
        2.23, 2.23
        >> smart_round(2.231), smart_round(2.231, upper_border=False)
        2.24, 2.23
        >> smart_round(-2.230), smart_round(-2.230, upper_border=False)
        -2.23, -2.23
        >> smart_round(-2.231), smart_round(-2.231, upper_border=False)
        -2.23, -2.24
        >> smart_round(0.930001), smart_round(0.930001, upper_border=False)
        0.94, 0.93
        >> smart_round(-0.930001), smart_round(-0.930001, upper_border=False)
        -0.93, -0.94
    """
    if v == 0:
        return 0
    o = np.log10(np.fabs(v))
    f = 10 ** (-int(o) + order)
    if upper_border:
        return np.ceil(v * f) / f
    return np.floor(v * f) / f


def skymap(m, **kwargs):
    """ Deprecated funcion -> See heatmap() """
    print("User warning: function skymap() is deprecated and will stop existing in v2.0.0. \
            Please use heatmap() in future!")
    return heatmap(m, **kwargs)


def healpy_map(m, **kwargs):
    """ Forwards to function heatmap() """
    return heatmap(m, **kwargs)


def eventmap(v, **kwargs):
    """ Forwards to function scatter() """
    return scatter(v, **kwargs)


class PlotSkyPatch:

    """
    Class to plot a close-up look of a region of interest (ROI) in the sky.
    To use this class you need to install the Basemap package:
    https://matplotlib.org/basemap/users/installing.html

    .. code-block:: python

        from astrotools.skymap import PlotSkyPatch
        patch = PlotSkyPatch(lon0, lat0, r_roi, title='My Skypatch')
        mappable = patch.plot_crs("/path/to/cosmic_rays.CosmicRaysSets.npz", set_idx=0)
        patch.mark_roi()
        patch.plot_grid()
        patch.colorbar(mappable)
        patch.savefig("/tmp/test-skypatch.png")
    """

    def __init__(self, lon_roi, lat_roi, r_roi, ax=None, title=None, **kwargs):
        """
        :param lon_roi: Longitude of center of ROI in radians (0..2*pi)
        :param lat_roi: Latitude of center of ROI in radians (0..2*pi)
        :param r_roi: Radius of ROI to be plotted (in radians)
        :param ax: Matplotlib axes in case you want to plot on certain axes
        :param title: Optional title of plot (plotted in upper left corner)
        :param kwargs: keywords passed to matplotlib.figure()
        """
        from mpl_toolkits.basemap import Basemap    # pylint: disable=import-error,no-name-in-module
        import matplotlib as mpl

        with_latex_style = {
            "text.usetex": True,
            "font.family": "serif",
            "axes.labelsize": 30,
            "font.size": 30,
            "legend.fontsize": 30,
            "xtick.labelsize": 26,
            "ytick.labelsize": 26,
            "legend.fancybox": False,
            "lines.linewidth": 3.0,
            "patch.linewidth": 3.0}

        mpl.rcParams.update(with_latex_style)

        assert (isinstance(lon_roi, (float, int))) and (isinstance(lat_roi, (float, int))) and \
            (isinstance(r_roi, (float, int))), "Keywords 'lon_roi', 'lat_roi' and 'r_roi' have to be floats or ints!"

        self.vec_0 = coord.ang2vec(lon_roi, lat_roi)
        self.lon_0 = np.rad2deg(lon_roi)
        self.lat_0 = np.rad2deg(lat_roi)
        self.r_roi = r_roi

        self.scale = 5500000 * (r_roi / 0.3)

        self.fig = None
        self.ax = ax
        if ax is None:
            kwargs.setdefault('figsize', [8, 8])
            self.fig = plt.figure(**kwargs)
            self.ax = plt.axes()

        self.title = title
        if title is not None:
            self.text(0.02, 0.98, title, verticalalignment='top', fontsize=36)

        self.m = Basemap(width=self.scale, height=self.scale, resolution='l', projection='stere', celestial=True,
                         lat_0=self.lat_0, lon_0=-360 - self.lon_0 if self.lon_0 < 0 else -self.lon_0, ax=ax)

    def plot_crs(self, crs, set_idx=0, zorder=0, cmap='viridis', **kwargs):
        """
        Plot cosmic ray events in the sky.

        :param crs: Either cosmic_rays.CosmicRaysBase or cosmic_rays.CosmicRaysSets object (or path) or dict object
        :param set_idx: In case of CosmicRaysSets object, chose the respective set index
        :param zorder: Usual matplotlib zorder keyword (order of plotting)
        :param cmap: Matplotlib colormap object or string
        """
        if isinstance(crs, str):
            from astrotools import cosmic_rays
            try:
                crs = cosmic_rays.CosmicRaysBase(crs)
            except AttributeError:
                crs = cosmic_rays.CosmicRaysSets(crs)

        if hasattr(crs, 'type') and (crs.type == "CosmicRaysSet"):
            crs = crs[set_idx]

        if 'log10e' in crs.keys():
            log10e = crs['log10e']
            assert np.all(log10e < 25), "Input energies ('log10e' key) are too high for being plotted"
            kwargs.setdefault('s', 10**(log10e - 18.))
            kwargs.setdefault('c', log10e)
        kwargs.setdefault('lw', 0)

        return self.scatter(crs['lon'], crs['lat'], zorder=zorder, cmap=cmap, **kwargs)

    def plot(self, lons, lats, **kwargs):
        """ Replaces matplotlib.pyplot.plot() function """
        kwargs.setdefault('rasterized', True)
        x, y = self.m(np.rad2deg(lons), np.rad2deg(lats))
        return self.m.plot(x, y, **kwargs)

    def scatter(self, lons, lats, **kwargs):
        """ Replaces matplotlib.pyplot.scatter() function """
        kwargs.setdefault('rasterized', True)
        x, y = self.m(np.rad2deg(lons), np.rad2deg(lats))
        return self.m.scatter(x, y, **kwargs)

    def tissot(self, lon, lat, radius, npts=1000, **kwargs):
        """ Replaces the Basemap tissot() function (plot circles) """
        kwargs.setdefault('fill', False)
        kwargs.setdefault('lw', 1)
        kwargs.setdefault('color', 'grey')
        return self.m.tissot(np.rad2deg(lon), np.rad2deg(lat), np.rad2deg(radius), npts, **kwargs)

    def mark_roi(self, alpha=0.4, **kwargs):
        """
        Marks the ROI by a circle ans shades cosmic rays outside the ROI.

        :param kwargs: Passed to Basemaps tissot() function
        """
        from matplotlib import path, collections
        kwargs.setdefault('lw', 2)
        kwargs.setdefault('zorder', 3)
        try:
            t = self.tissot(np.deg2rad(self.lon_0), np.deg2rad(self.lat_0), self.r_roi, **kwargs)
            xyb = np.array([[0., 0.], [1., 0.], [1., 1.], [0., 1.], [0., 0.]]) * self.scale

            p = path.Path(np.concatenate([xyb, t.get_xy()[::-1]]))
            p.codes = np.ones(len(p.vertices), dtype=p.code_type) * p.LINETO
            p.codes[0] = path.Path.MOVETO
            p.codes[4] = path.Path.CLOSEPOLY
            p.codes[5] = path.Path.MOVETO
            p.codes[-1] = path.Path.CLOSEPOLY
            col = collections.PathCollection([p], facecolor='white', alpha=alpha, zorder=1)
            self.ax.add_collection(col)
        except ValueError:
            print("Warning: Could not plot ROI circle due to undefined inverse geodesic!")

        self.mark_roi_center()

    def mark_roi_center(self, **kwargs):
        """
        Mark the ROI center

        :param kwargs: keywords for matplotlib.pyplot.plot() function
        """
        kwargs.setdefault('marker', '+')
        kwargs.setdefault('markersize', 20)
        kwargs.setdefault('color', 'k')
        kwargs.setdefault('lw', 2)
        x, y = self.m(self.lon_0, self.lat_0)
        self.m.plot((x), (y), **kwargs)

    def plot_grid(self, meridians=None, parallels=None, mer_labels=None, par_labels=None):
        """ Plot the longitude and latitude grid in the skypatch """
        if meridians is None:
            meridians = np.arange(-180, 181, 60) if abs(self.lat_0) > 60 else np.arange(-180, 181, 20)
        if parallels is None:
            parallels = np.arange(-90, 91, 15) if abs(self.lat_0) > 60 else np.arange(-90, 91, 20)

        self.m.drawmeridians(meridians, labels=[False, False, True, False] if mer_labels is None else mer_labels)
        self.m.drawparallels(parallels, labels=[True, True, False, False] if par_labels is None else par_labels)

    def plot_thrust(self, n, t, **kwargs):
        """
        Visualize the thrust observables in the ROI.

        :param n: Thrust axis as given by astrotools.obs.thrust()[1]
        :param t: Thrust values as returned by astrotools.obs.thrust()[0]
        :param kwargs: Keywords passed to matplotlib.pyplot.plot() for axis visualization
        """
        kwargs.setdefault('c', 'red')
        linestyle_may = kwargs.pop('linestyle', 'solid')
        alpha_may = kwargs.pop('alpha', 0.5)

        lon, lat = coord.vec2ang(n[0])
        # fill thrust array (unit vector phi runs in negative lon direction)
        e_phi = coord.sph_unit_vectors(lon, lat)[1]
        sign = np.sign(e_phi[2] - n[1][2])
        phi_major = sign * coord.angle(e_phi, n[1])[0]
        phi_minor = sign * coord.angle(e_phi, n[2])[0]
        if np.abs(phi_major - phi_minor) < 0.99 * np.pi / 2.:
            phi_minor = 2*np.pi - phi_minor
        t23_ratio = t[1] / t[2]

        # mark the principal axes n3
        u = np.array(np.cos(phi_minor))
        v = -1. * np.array(np.sin(phi_minor))
        urot, vrot, x, y = self.m.rotate_vector(u, v, np.rad2deg(lon), np.rad2deg(lat), returnxy=True)
        _phi = np.arctan2(vrot, urot)
        s = self.r_roi * (t[1] / 0.15) * self.scale / t23_ratio
        self.m.plot([x - np.cos(_phi) * s, x + np.cos(_phi)*s],
                    [y - np.sin(_phi) * s, y + np.sin(_phi)*s], linestyle='dashed', alpha=0.5, **kwargs)

        # mark the principal axes n2
        u = np.array(np.cos(phi_major))
        v = -1. * np.array(np.sin(phi_major))
        urot, vrot, x, y = self.m.rotate_vector(u, v, np.rad2deg(lon), np.rad2deg(lat), returnxy=True)
        _phi = np.arctan2(vrot, urot)
        s = self.r_roi * (t[1] / 0.15) * self.scale
        self.m.plot([x - np.cos(_phi) * s, x + np.cos(_phi)*s],
                    [y - np.sin(_phi) * s, y + np.sin(_phi)*s], linestyle=linestyle_may, alpha=alpha_may, **kwargs)

        # mark the center point
        self.m.plot((x), (y), 'o', color=kwargs.pop('c'), markersize=10)

    def colorbar(self, mappable, cblabel='Energy [eV]', labelsize=12, ticks=None, **kwargs):
        """
        Adds a colorbar to a mappable in matplotlib. Replaces matplotlib colorbar() function.
        Use e.g:

        patch = PlotSkyPatch(...)
        mappable = patch.plot_crs(crs)
        patch.colorbar(mappable)

        :param mappable: Mappable in matplotlib.
        :param clabel: Label for the colorbar
        :param ticks: Ticks for the colorbar (either array-like or integer for number of ticks)
        :param kwargs: Keywords passed to matplotlib colorbar() function
        """
        # add a colorbar
        try:
            kwargs.setdefault('location', 'bottom')
            cb = self.m.colorbar(mappable, **kwargs)
            if (ticks is None) or isinstance(ticks, (int, float)):
                vmin, vmax = mappable.get_clim()
                vmin, vmax = smart_round(vmin), smart_round(vmax)
                n_ticks = float(3) if ticks is None else float(ticks)
                step = smart_round((vmax - vmin) / n_ticks, order=1)
                ticks = np.arange(vmin, vmax, step)
                ticks = ticks[(ticks >= vmin) & (ticks <= vmax)]
            cb.set_ticks(ticks)
            cb.set_label(cblabel, fontsize=3*labelsize)
            t = ['$10^{%.1f}$' % (f) for f in ticks]
            cb.ax.set_xticklabels(t, fontsize=int(max(0.8 * 3 * labelsize, 1)))
        except KeyError:
            print("Can not plot colorbar on axis.")

    def text(self, x, y, s, **kwargs):
        """ Substitudes matplotlib.pyplot.text() function """
        kwargs.setdefault('transform', self.ax.transAxes)
        self.ax.text(x, y, s, **kwargs)

    def savefig(self, path, **kwargs):
        """ Substitudes matplotlib savefig() function """
        kwargs.setdefault('dpi', 150)
        kwargs.setdefault('bbox_inches', 'tight')
        self.fig.savefig(path, **kwargs)
