# -*- coding: utf-8 -*-
"""
Contains the cosmic rays base class which allows to store arbitrary properties for the cosmic rays and
makes them accesseble via key or getter function.
The second class describes sets of cosmic rays as needed for larger studies.
"""
import matplotlib.pyplot as plt
import numpy as np

from astrotools import container, coord, healpytools as hpt, obs, skymap

DTYPE_TEMPLATE = []
PHYS_ENERGIES = ['e', 'log10e', 'energy', 'E']
PHYS_DIRECTIONS = ['vecs', 'lon', 'lat', 'pixel', 'pix']
SHAPE_FLEXIBLE = ['charge'] + PHYS_ENERGIES


def plot_eventmap(crs, opath=None, **kwargs):  # pragma: no cover
    """
    Function to plot a scatter skymap of the cosmic rays

    :param crs: CosmicRaysBase object
    :param opath: Output path for the image, default is None
    :type opath: str
    :param kwargs:

           - c: quantity that is supposed to occur in colorbar, e.g. energy of the cosmic rays
           - cblabel: label for the colorbar
           - nside: Healpy resolution of the 'pixel' array in the cosmic ray class
           - additional named keywords passed to matplotlib.scatter
           - fontsize: Scales the fontsize in the image
    :return: figure, axis of the scatter plot
    """
    vecs = crs['vecs']
    c = kwargs.pop('c', crs['log10e'] if len(set(PHYS_ENERGIES) & set(crs.keys())) > 0 else None)
    cmap = kwargs.pop('cmap', "viridis" if len(set(PHYS_ENERGIES) & set(crs.keys())) > 0 else None)
    return skymap.scatter(vecs, c=c, cmap=cmap, opath=opath, **kwargs)


def plot_heatmap(crs, opath=None, **kwargs):  # pragma: no cover
    """
    Function to plot a scatter skymap of the cosmic rays

    :param crs: CosmicRaysBase object
    :param opath: Output path for the image, default is None
    :type opath: str
    :param kwargs:

           - nside: Healpy resolution of the 'pixel' array in the cosmic ray class
           - additional named keywords passed to matplotlib.pcolormesh
    :return: figure of the heatmap, colorbar
    """
    nside = crs['nside'] if 'nside' in crs.keys() else kwargs.pop('nside', 64)
    pixel = crs['pixel']

    count = np.bincount(pixel, minlength=hpt.nside2npix(nside))
    return skymap.heatmap(count, opath=opath, **kwargs)


def plot_energy_spectrum(crs, xlabel='log$_{10}$(Energy / eV)', ylabel='entries', fontsize=16, bw=0.05,
                         opath=None, **kwargs):  # pragma: no cover
    """
    Function to plot the energy spectrum of the cosmic ray set

    :param crs: CosmicRaysBase object
    :param xlabel: label for the x-axis
    :type xlabel: str
    :param ylabel: label for the y-axis
    :type ylabel: str
    :param fontsize: Scales the fontsize in the image.
    :type fontsize: int
    :param bw: bin width for the histogram
    :type bw: float
    :param opath: Output path for the image, default is None
    :type opath: str
    :param kwargs: additional named keywords passed to matplotlib.pyplot.hist
    :return: bins of the histogram
    """
    log10e = crs['log10e']
    if 'bins' not in kwargs:
        bins = np.arange(17., 20.6, bw)
        bins = bins[(bins >= np.min(log10e) - 0.1) & (bins <= np.max(log10e) + 0.1)]
        kwargs['bins'] = bins

    kwargs.setdefault('color', 'k')
    kwargs.setdefault('fill', None)
    kwargs.setdefault('histtype', 'step')
    plt.hist(log10e, **kwargs)

    plt.xticks(fontsize=fontsize - 4)
    plt.yticks(fontsize=fontsize - 4)
    plt.xlabel(xlabel, fontsize=fontsize)
    plt.ylabel(ylabel, fontsize=fontsize)
    if opath is not None:
        plt.savefig(opath, bbox_inches='tight')
        plt.clf()
    return bins


# TODO: Do not allow names with leading underscore (if before self.__dict__.update)
class CosmicRaysBase(container.DataContainer):
    """ Cosmic rays base class meant for inheritance """

    def __init__(self, initializer=None, coord_system='gal'):
        # Inherits all functionalities from container.DataContainer object
        super(CosmicRaysBase, self).__init__(initializer)
        self.type = "CosmicRays"
        self.coord_system = coord_system

    def __getitem__(self, key):

        if isinstance(key, (int, np.integer, np.ndarray, slice)):
            crs = CosmicRaysBase(self.shape_array[key])
            for k in self.general_object_store.keys():
                to_copy = self.get(k)
                if isinstance(to_copy, (np.ndarray, list)):
                    if len(to_copy) == self.ncrs:
                        to_copy = to_copy[key]
                if (k == 'vecs'):
                    to_copy = to_copy[:, key]
                crs.__setitem__(k, to_copy)
            return crs
        if key in self.general_object_store.keys():
            if key in SHAPE_FLEXIBLE:
                return self.general_object_store[key] * np.ones(self.ncrs, dtype='int')
            return self.general_object_store[key]
        if key in self.shape_array.dtype.names:
            return self.shape_array[key]

        if len(self._similar_key(key)) > 0:
            return self._get_values_similar_key(self._similar_key(key).pop(), key)

        raise ValueError("Key '%s' does not exist, no info stored under similar keys was found" % key)

    def __setitem__(self, key, value):
        if key in self.shape_array.dtype.names:
            self.shape_array[key] = value
            if len(self._similar_key(key)) > 1:
                print("Warning: Your cosmic rays object contains data stored under a key similar to %s. "
                      "Changing one without the other may lead to problems." % key)
            return
        super(CosmicRaysBase, self).__setitem__(key, value)

    def __add__(self, other):
        return CosmicRaysBase([self, other])

    def _similar_key(self, key):
        """
        Helper function to check for keys describing the same physical data eg. 'vecs' and 'pixel'.
        """
        key_list = self.keys()
        common_keys = []
        if key in PHYS_DIRECTIONS:
            common_keys = set(PHYS_DIRECTIONS) & set(key_list)
            if ('pix' in key) and (('pix' in key_list) or ('pixel' in key_list)):
                return ["pix"] if key == "pixel" else ["pixel"]
            elif key not in ['lon', 'lat']:
                if ('lon' in common_keys) and ('lat' not in common_keys):
                    common_keys.discard('lon')
                if ('lat' in common_keys) and ('lon' not in common_keys):
                    common_keys.discard('lat')
                common_keys = sorted(common_keys, key=PHYS_DIRECTIONS.index, reverse=True)
        elif key in PHYS_ENERGIES:
            common_keys = set(PHYS_ENERGIES) & set(key_list)
        return common_keys

    def _get_values_similar_key(self, similar_key, orig_key):
        """
        Helper function to get values stored under a different physical key in the correctly
        transformed way, together with _similar_key()
        """
        store = self.shape_array if similar_key in list(self.shape_array.dtype.names) else self.general_object_store
        if orig_key in ['e', 'energy', 'E']:
            if similar_key in ['e', 'energy', 'E']:
                return store[similar_key]
            return 10**np.array(store[similar_key])
        if orig_key == 'log10e':
            return np.log10(store[similar_key])
        return self._direction_transformation(similar_key, orig_key)

    def _direction_transformation(self, similar_key, orig_key):
        """
        Helper function to get values stored under a different physical key in the correctly
        transformed way specifically only for directions
        """
        nside = self.general_object_store['nside'] if 'nside' in self.keys() else 64
        store = self.shape_array if similar_key in list(self.shape_array.dtype.names) else self.general_object_store
        if orig_key == 'vecs':
            if ('lon' in similar_key) or ('lat' in similar_key):
                return hpt.ang2vec(store['lon'], store['lat'])
            return hpt.pix2vec(nside, store[similar_key])
        if ('pix' in orig_key):
            if 'pix' in similar_key:
                return store[similar_key]
            if similar_key == 'vecs':
                return hpt.vec2pix(nside, store['vecs'])
            return hpt.ang2pix(nside, store['lon'], store['lat'])
        if similar_key == 'vecs':
            lon, lat = hpt.vec2ang(store['vecs'])
        else:
            lon, lat = hpt.pix2ang(nside, store[similar_key])
        return lon if orig_key == 'lon' else lat

    def add_cosmic_rays(self, crs):
        """
        Function to add cosmic rays to the already existing set of cosmic rays

        :param crs: numpy array with cosmic rays. The cosmic rays must not contain
                    all original keys. Missing keys are set to zero. If additional
                    keys are provided, they are ignored.
        """
        if not isinstance(crs, CosmicRaysBase):
            raise Exception("You need to add a CosmicRaysBase object!")
        self.add_shape_array(crs.get_array())

    def sensitivity_2pt(self, niso=1000, bins=180, **kwargs):
        """
        Function to calculate the sensitivity by the 2pt-auto-correlation over a scrambling
        of the right ascension coordinates.

        :param niso: Number of isotropic sets to calculate.
        :param bins: Number of angular bins, 180 correspond to 1 degree binning (np.linspace(0, np.pi, bins+1).
        :param kwargs: additional named arguments passed to obs.two_pt_auto()
        :return: pvalues in the shape (bins)
        """
        kwargs.setdefault('cumulative', True)
        vec_crs = self.get('vecs')
        _, dec = coord.vec2ang(coord.gal2eq(vec_crs))

        # calculate auto correlation for isotropic scrambled data
        _ac_iso = np.zeros((niso, bins))
        for i in range(niso):
            _vecs = coord.ang2vec(coord.rand_phi(self.ncrs), dec)
            _ac_iso[i] = obs.two_pt_auto(_vecs, bins, **kwargs)

        # calculate p-value by comparing the true sets with the isotropic ones
        _ac_crs = obs.two_pt_auto(vec_crs, bins, **kwargs)
        pvals = np.sum(_ac_iso >= _ac_crs[np.newaxis], axis=0) / float(niso)
        return pvals

    def plot_eventmap(self, **kwargs):  # pragma: no cover
        """
        Function to plot a scatter skymap of the cosmic rays

        :param kwargs: additional named arguments passed to plot_eventmap().
        """
        return plot_eventmap(self, **kwargs)

    def plot_heatmap(self, **kwargs):  # pragma: no cover
        """
        Function to plot a healpy skymap of the cosmic rays

        :param kwargs: additional named arguments passed to plot_healpy_map().
        """
        return plot_heatmap(self, **kwargs)

    def plot_healpy_map(self, **kwargs):  # pragma: no cover
        """ Forwards to function plot_heatmap() """
        return self.plot_heatmap(**kwargs)

    def plot_energy_spectrum(self, **kwargs):  # pragma: no cover
        """
        Function to plot the energy spectrum of the cosmic rays

        :param kwargs: additional named arguments passed to plot_energy_spectum().
        """
        return plot_energy_spectrum(self, **kwargs)


class CosmicRaysSets(CosmicRaysBase):
    """Set of cosmic rays """

    def __init__(self, nsets=None, ncrs=None):
        self.type = "CosmicRaysSet"
        if nsets is None:
            CosmicRaysBase.__init__(self, initializer=None)
            self.type = "CosmicRaysSet"

        # noinspection PyUnresolvedReferences
        elif isinstance(nsets, str):
            self.load(nsets)
        elif isinstance(nsets, (tuple, float, int, np.integer)):
            self.nsets = nsets[0] if isinstance(nsets, tuple) else nsets
            ncrs = nsets[1] if isinstance(nsets, tuple) else ncrs

            # Set the shape first as this is required for __setitem__ used by copy from CosmicRaysBase
            CosmicRaysBase.__init__(self, initializer=ncrs * self.nsets)
            # this number has to be set again as it is overwritten by the init function.
            # It is important to set it before adding the index
            self.type = "CosmicRaysSet"
            self.ncrs = ncrs
            self.shape = (int(self.nsets), int(self.ncrs))
            self.general_object_store["shape"] = self.shape
        elif isinstance(nsets, (list, np.ndarray)):
            self._from_list(nsets)
        else:
            # copy case of a cosmic rays set
            try:
                if nsets.type == self.type:
                    self.general_object_store = {}
                    self.shape = nsets.shape
                    self.copy(nsets)
                    self._create_access_functions()
                    # _create_access_functions and the __setitem__ function from the CosmicRaysBase overwrite self.shape
                    self.shape = nsets.shape
            except AttributeError as e:
                raise AttributeError(str(e))
                # raise NotImplementedError("Trying to instantiate the CosmicRaysSets class with a non "
                #                           "supported type of cosmic_rays")

    def load(self, filename, **kwargs):
        """ Loads cosmic rays from a filename

        :param filename: filename from where to load
        :type filename: str
        :param kwargs: additional keyword arguments passed to numpy / pickle load functions
        """
        CosmicRaysBase.load(self, filename, **kwargs)
        self._create_access_functions()
        if (len(self.shape) == 1) or len(self.general_object_store["shape"]) == 1:
            raise AttributeError("Loading a CosmicRaysBase() object with the CosmicRaysSets() class. Use function "
                                 "cosmic_rays.CosmicRaysBase() instead.")
        self.ncrs = self.shape[1]
        self.nsets = self.shape[0]

    def _create_access_functions(self):
        super(CosmicRaysSets, self)._create_access_functions()
        if "shape" in self.general_object_store.keys():
            self.shape = self.general_object_store["shape"]

    def _from_list(self, l):
        types = np.array([type(elem) for elem in l])
        if np.all(types == CosmicRaysBase):
            _nsets, _ncrs = len(l), len(l[0])
        elif np.all(types == CosmicRaysSets):
            _nsets, _ncrs = sum([len(elem) for elem in l]), l[0].ncrs
        else:
            raise TypeError("All elements must be either of type CosmicRays or of type CosmicRaysSets")

        ncrs_each = np.array([elem.ncrs for elem in l])
        if not np.all(ncrs_each == _ncrs):
            raise ValueError("The number of cosmic rays must be the same in each set")

        keys = [sorted(elem.shape_array.dtype.names) for elem in l]
        joint_keys = np.array(["-".join(elem) for elem in keys])
        gos_keys = [sorted(elem.general_object_store.keys()) for elem in l]
        joint_gos_keys = np.array(["-".join(elem) for elem in gos_keys])
        if not np.all(joint_keys == joint_keys[0]) or not np.all(joint_gos_keys == joint_gos_keys[0]):
            raise AttributeError("All cosmic rays must have the same properties array and general object store")

        self.__init__(_nsets, _ncrs)
        for key in keys[0]:
            value = np.array([cr[key] for cr in l]).reshape(self.shape)
            self.__setitem__(key, value)
        for key in gos_keys[0]:
            if key == 'shape':
                continue
            try:
                value = np.array([cr[key] for cr in l])
            except ValueError:
                if np.all(l[i][key] == l[0][key] for i in range(len(l))):
                    value = l[0][key]
                else:
                    print('Deleted key %s because of shape (%s) problems' % (key, np.shape(l[0][key])))
            if key == 'vecs':
                value = np.swapaxes(value, 0, 1).reshape(3, -1, _ncrs)
            if np.all(value == value[0]):
                value = value[0]
            self.general_object_store[key] = value
        self.general_object_store["shape"] = self.shape

    def __setitem__(self, key, value):
        # casting into int is required to get python3 compatibility
        v = value.reshape(int(self.nsets * self.ncrs)) if np.shape(value) == self.shape else value
        # to avoid the overwriting we use this hack
        self.ncrs = self.ncrs * self.nsets
        super(CosmicRaysSets, self).__setitem__(key, v)
        # this number has to be set again as it is overwritten by the init function
        self.ncrs = int(self.ncrs / int(self.nsets))

    def __getitem__(self, key):
        # noinspection PyUnresolvedReferences
        if isinstance(key, (int, np.integer)):
            crs = CosmicRaysBase(self.shape_array.dtype)
            crs.shape_array = self.shape_array[int(key * self.ncrs):int((key + 1) * self.ncrs)]
            for k in self.general_object_store.keys():
                if (k == 'shape'):
                    continue
                to_copy = self.get(k)
                if isinstance(to_copy, (np.ndarray, list)):
                    if len(to_copy) == self.nsets:
                        to_copy = to_copy[key]
                    elif np.shape(to_copy) == (3, self.nsets, self.ncrs):
                        to_copy = to_copy[:, key]   # check for vectors which belong to cosmic rays
                crs.__setitem__(k, to_copy)
            # The order is important
            crs.ncrs = self.ncrs
            crs.shape = (self.ncrs, )
            return crs
        if isinstance(key, (np.ndarray, slice)):
            return self._masking(key)
        if key in self.general_object_store.keys():
            if key in SHAPE_FLEXIBLE:
                return self.general_object_store[key] * np.ones((self.nsets, self.ncrs), dtype='int')
            return self.general_object_store[key]
        try:
            # casting into int is required to get python3 compatibility
            return np.reshape(self.shape_array[key], self.shape)
        except ValueError as e:
            if len(self._similar_key(key)) > 0:
                value = self._get_values_similar_key(self._similar_key(key).pop(), key)
                if value.size in (np.prod(self.shape), 3*np.prod(self.shape)):
                    shape = self.shape if value.size == np.prod(self.shape) else (-1,)+self.shape
                    return np.reshape(value, shape)
                raise Exception("Weird error occured, please report this incident with a minimal example!")

            raise ValueError("The key %s does not exist and the error message was %s" % (key, str(e)))

    def __len__(self):
        return int(self.nsets)

    def __add__(self, other):
        return CosmicRaysSets([self, other])

    def __iter__(self):
        self._current_idx = 0
        return self

    def __next__(self):
        return self.next()

    def next(self):
        """returns next element when iterating over all elements"""
        self._current_idx += 1
        if self._current_idx > self.nsets:
            raise StopIteration
        return self.__getitem__(self._current_idx - 1)

    def _masking(self, sl):
        mask = np.zeros(self.shape, dtype=bool)
        if isinstance(sl, slice):
            mask[sl] = True
            sl = mask
        if sl.dtype == bool:
            if sl.shape == (self.nsets,):
                nsets = np.sum(sl)
                ncrs = self.ncrs
                mask[sl, :] = True
                sl = np.where(mask)
            elif sl.shape == self.shape:
                ncrs_in_nsets = np.sum(sl, axis=1)
                ncrs = np.amax(ncrs_in_nsets)
                assert self.nsets == np.sum(ncrs_in_nsets == ncrs) + np.sum(ncrs_in_nsets == 0)
                nsets = np.sum(ncrs_in_nsets > 0)
                sl = np.where(sl)
            else:
                raise AssertionError("Slicing dimension is neither (nsets) nor (nsets, ncrs)")
        elif sl.dtype == int:
            assert (np.amin(sl) >= 0) & (np.amax(sl) < self.nsets)
            nsets = len(sl)
            ncrs = self.ncrs
        else:
            raise ValueError("Dtype of slicing ndarray not understood: %s" % (sl.dtype))

        crs = CosmicRaysSets(nsets, ncrs)
        for key_copy in self.keys():
            if key_copy not in crs.keys():
                to_copy = self.get(key_copy)
                # check if array needs to be sliced
                if isinstance(to_copy, np.ndarray):
                    if to_copy.shape == self.shape:
                        to_copy = to_copy[sl]
                    elif to_copy.shape == (self.nsets, ):
                        _sl = np.unique(sl[0]) if isinstance(sl, tuple) else sl
                        to_copy = to_copy[_sl]
                crs.__setitem__(key_copy, to_copy)
        return crs

    def _update_attributes(self):
        self.ncrs = self.shape[1]
        self.nsets = self.shape[0]

    def save_readable(self, fname, use_keys=None, **kwargs):
        """
        Saves cosmic ray class as ASCII file with general object store written to header.

        :param fname: file name of the outfile
        :type fname: str
        :param use_keys: list or tuple of keywords that will be used for the saved file
        :param kwargs: additional named keyword arguments passed to numpy.savetxt()
        """
        dump, header, fmt = self._prepare_readable_output(use_keys)
        dump = container.join_struct_arrays([np.repeat(np.arange(self.nsets), self.ncrs), dump])
        header_parts = header.split("\n")
        header_parts[-1] = ('\n' if len(header_parts) > 1 else '') + 'setID\t' + header_parts[-1]
        fmt.insert(0, '%i')
        kwargs.setdefault('header', "\n".join(header_parts))
        kwargs.setdefault('fmt', fmt)
        kwargs.setdefault('delimiter', '\t')
        np.savetxt(fname, dump, **kwargs)

    def sensitivity_2pt(self, set_idx=None, niso=1000, bins=180, **kwargs):
        """
        Function to calculate the sensitivity by the 2pt-auto-correlation over a scrambling
        of the right ascension coordinates.

        :param set_idx: If set, only this set number will be evaluated
        :param niso: Number of isotropic sets to calculate
        :param bins: Number of angular bins, 180 correspond to 1 degree binning (np.linspace(0, np.pi, bins+1).
        :param kwargs: additional named arguments passed to obs.two_pt_auto()
        :return: pvalues in the shape (self.nsets, bins)
        """
        kwargs.setdefault('cumulative', True)
        vec_crs = self.get('vecs')
        _, dec = coord.vec2ang(coord.gal2eq(np.reshape(vec_crs, (3, -1))))

        # calculate auto correlation for isotropic scrambled data
        _ac_iso = np.zeros((niso, bins))
        for i in range(niso):
            _vecs = coord.ang2vec(coord.rand_phi(self.ncrs), np.random.choice(dec, size=self.ncrs))
            _ac_iso[i] = obs.two_pt_auto(_vecs, bins, **kwargs)

        # calculate p-value by comparing the true sets with the isotropic ones
        set_idx = np.arange(self.nsets) if set_idx is None else [set_idx]
        pvals = np.zeros((len(set_idx), bins))
        for i, idx in enumerate(set_idx):
            _ac_crs = obs.two_pt_auto(vec_crs[:, idx], bins, **kwargs)
            pvals[i] = np.sum(_ac_iso >= _ac_crs[np.newaxis], axis=0) / float(niso)
        return pvals

    def add_cosmic_rays(self, crs):
        """
        Function to add cosmic rays to the already existing sets of cosmic rays.
        Number of sets must be equal.

        :param crs: CosmicRaysSet instance. The cosmic rays must not contain
                    all original keys. Missing keys are set to zero. If additional
                    keys are provided, they are ignored.
        """
        if not isinstance(crs, CosmicRaysSets):
            raise Exception("You need to add a CosmicRaysSet object!")
        if not self.nsets == crs.nsets:
            raise Exception("Adding CRs to existing CosmicRaysSet instance is only \
                             possible if they have same number of sets!")
        self.add_shape_array(crs.get_array())
        self.ncrs = self.ncrs + crs.ncrs
        self.shape = (self.nsets, self.ncrs)

    def plot_eventmap(self, setid=0, **kwargs):  # pragma: no cover
        """
        Function to plot a scatter skymap of the cosmic rays

        :param setid: id of the set which is plotted (default: 0)
        :type setid: int
        :param kwargs: additional named arguments passed to plot_eventmap().
        """
        # noinspection PyTypeChecker
        return plot_eventmap(self.get(setid), **kwargs)

    def plot_heatmap(self, setid=0, **kwargs):  # pragma: no cover
        """
        Function to plot a healpy map of the cosmic ray set

        :param setid: id of the set which is plotted (default: 0)
        :type setid: int
        :param kwargs: additional named arguments pased to plot_healpy_map().
        """
        # noinspection PyTypeChecker
        return plot_heatmap(self.get(setid), **kwargs)

    def plot_healpy_map(self, setid=0, **kwargs):  # pragma: no cover
        """ Forwards to function plot_heatmap() """
        self.plot_heatmap(setid, **kwargs)

    def plot_energy_spectrum(self, setid=0, **kwargs):  # pragma: no cover
        """
        Function to plot the energy spectrum of the cosmic ray set

        :param setid: id of the set which is plotted (default: 0)
        :type setid: int
        :param kwargs: additional named arguments pased to plot_energy_spectrum().
        """
        # noinspection PyTypeChecker
        crs = self.get(setid)
        return plot_energy_spectrum(crs, **kwargs)

    def shuffle_events(self):
        """
        Independently shuffle the cosmic rays of each set.
        """
        # This function can be simplified in the future using np.take_along_axis()
        shuffle_ids = np.random.permutation(np.prod(self.shape)).reshape(self.shape)
        shuffle_ids = np.argsort(shuffle_ids, axis=1)
        sets_ids = np.repeat(np.arange(self.nsets), self.ncrs).reshape(self.shape)
        for _key in self.shape_array.dtype.names:
            self.__setitem__(_key, self.__getitem__(_key)[sets_ids, shuffle_ids])
        sets_ids_3d = np.repeat(np.arange(3), np.prod(self.shape)).reshape((3,) + self.shape)
        self.__setitem__('vecs', self.__getitem__('vecs')[sets_ids_3d, sets_ids, np.stack([shuffle_ids] * 3)])
