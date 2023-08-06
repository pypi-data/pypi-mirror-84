"""
Extensions to healpy that covers:
-> pixel, vector, angular transformations
-> drawing vectors uniformly in pixel
-> various probability density functions (exposure, fisher, dipole)
"""

import healpy as hp
# noinspection PyUnresolvedReferences
from healpy import *    # keep namespace of healpy
import numpy as np

from astrotools import coord


def rand_pix_from_map(healpy_map, n=1):
    """
    Draw n random pixels from a HEALpix map.

    :param healpy_map: healpix map (not necessarily normalized)
    :param n: number of pixels that are drawn from the map
    :return: an array of pixels with size n, that are drawn from the map
    """
    p = np.cumsum(healpy_map)
    return p.searchsorted(np.random.rand(n) * p[-1])


def rand_vec_from_map(healpy_map, n=1, nest=False):
    """
    Draw n random vectors from a HEALpix map.

    :param healpy_map: healpix map (not necessarily normalized)
    :param n: number of pixels that are drawn from the map
    :param nest: set True in case you work with healpy's nested scheme
    :return: an array of vectors with size n, that are drawn from the map
    """
    pix = rand_pix_from_map(healpy_map, n)
    nside = hp.get_nside(healpy_map)
    return rand_vec_in_pix(nside, pix, nest)


def rand_vec_in_pix(nside, ipix, nest=False):
    """
    Draw vectors from a uniform distribution within a HEALpixel.

    :param nside: nside of the healpy pixelization
    :param ipix: pixel number(s)
    :param nest: set True in case you work with healpy's nested scheme
    :return: vectors containing events from the pixel(s) specified in ipix
    """
    if not nest:
        ipix = hp.ring2nest(nside, ipix=ipix)

    n_order = nside2norder(nside)
    n_up = 29 - n_order
    i_up = ipix * 4 ** n_up
    i_up += np.random.randint(0, 4 ** n_up, size=np.size(ipix))

    v = pix2vec(nside=2 ** 29, ipix=i_up, nest=True)
    return np.array(v)


def rand_exposure_vec_in_pix(nside, ipix, a0=-35.25, zmax=60, coord_system='gal', deviation=0.5, nest=False):
    """
    Draw vectors from a distribution within a HEALpixel that follow the exposure
    distribution within the pixel. It is much slower than rand_vec_in_pix() and
    should therefore only be used for problematic pixels (close to zero exposure).

    :param nside: nside of the healpy pixelization
    :param ipix: pixel number(s)
    :param a0: latitude of detector (-90, 90) in degrees (default: Auger)
    :param zmax: maximum acceptance zenith angle (0, 90) degrees
    :param coord_system: choose between different coordinate systems - gal, eq, sgal, ecl
    :param deviation: maximum relative deviation between exposure values in pixel corners
    :param nest: set True in case you work with healpy's nested scheme
    :return: vectors containing events from the pixel(s) specified in ipix
    """
    ipix = np.atleast_1d(ipix)
    vecs = np.zeros((3, ipix.size))
    mask = check_problematic_pixel(nside, ipix, a0, zmax, deviation)
    vecs[:, ~mask] = rand_vec_in_pix(nside, ipix[~mask], nest)
    if not nest:
        ipix = hp.ring2nest(nside, ipix=ipix)

    for pix in np.unique(ipix[mask]):
        n = np.sum(ipix == pix)
        # increase resolution of healpy schemes cooresponding to number of crs per pixel
        n_up = max(3, int(np.ceil(np.log10(10*n) / np.log10(4))))
        pix_new = pix * 4 ** n_up + np.arange(4 ** n_up)
        v = pix2vec(nside=nside * 2**n_up, ipix=pix_new, nest=True)
        if coord_system != 'eq':
            v = getattr(coord, '%s2eq' % coord_system)(v)
        p = coord.exposure_equatorial(coord.vec2ang(v)[1], a0, zmax)
        pixel = np.random.choice(pix_new, size=n, replace=False, p=p/np.sum(p))
        vecs[:, ipix == pix] = pix2vec(nside=nside * 2**n_up, ipix=pixel, nest=True)

    return np.array(vecs)


def check_problematic_pixel(nside, ipix, a0, zmax, deviation=0.5, coord_system='gal'):
    """
    Checks input pixel for exposure deviation within the corner points from more than certain
    threshold (default: 0.5).

    :param nside: nside of the healpy pixelization
    :param ipix: pixel number(s)
    :param a0: latitude of detector (-90, 90) in degrees (default: Auger)
    :param zmax: maximum acceptance zenith angle (0, 90) degrees
    :param deviation: maximum deviation between exposure values in pixel corners
    :param coord_system: choose between different coordinate systems - gal, eq, sgal, ecl
    """
    npix = hp.nside2npix(nside)
    v = np.swapaxes(hp.boundaries(nside, np.arange(npix), step=1), 0, 1).reshape(3, -1)
    if coord_system != 'eq':
        v = getattr(coord, '%s2eq' % coord_system)(v)
    # exposure values of corner points
    exposure = coord.exposure_equatorial(coord.vec2ang(v)[1], a0, zmax).reshape((npix, 4))
    # check for maximal deviation of corner points
    _min, _max = np.min(exposure, axis=-1), np.max(exposure, axis=-1)
    mask = _max > 0
    eps = np.min(_min[_min > 0]) / 2.
    _min[_min < eps] = eps
    mask = mask * (_max / _min > (1 + deviation))
    return mask[ipix]


def pix2map(nside, ipix):
    """
    Converts healpy pixel to healpix map

    :param nside: nside of the healpy pixelization
    :param ipix: pixel number(s) in nside scheme
    :return: healpix map of size npix
    """
    npix = hp.nside2npix(nside)
    ipix = np.atleast_1d(ipix)
    assert (ipix < npix).all(), "Nside does not match the given pixel(s)!"
    return np.bincount(ipix, minlength=npix)


def pix2vec(nside, ipix, nest=False):
    """
    Convert HEALpixel ipix to cartesian vector
    Substitutes hp.pix2vec

    :param nside: nside of the healpy pixelization
    :param ipix: pixel number(s)
    :param nest: set True in case you work with healpy's nested scheme
    :return: vector of the pixel center(s)
    """
    v = hp.pix2vec(nside, ipix, nest=nest)
    return np.asarray(v)


def pix2ang(nside, ipix, nest=False):
    """
    Convert HEALpixel ipix to spherical angles (astrotools definition)
    Substitutes hp.pix2ang

    :param nside: nside of the healpy pixelization
    :param ipix: pixel number(s)
    :param nest: set True in case you work with healpy's nested scheme
    :return: angles (phi, theta) in astrotools definition
    """
    v = pix2vec(nside, ipix, nest=nest)
    phi, theta = coord.vec2ang(v)

    return phi, theta


def ang2vec(phi, theta):
    """
    Substitutes healpy.ang2vec() to use our angle convention

    :param phi: longitude, range (pi, -pi), 0 points in x-direction, pi/2 in y-direction
    :param theta: latitude, range (pi/2, -pi/2), pi/2 points in z-direction
    :return: vector of shape (3, n)
    """
    return coord.ang2vec(phi, theta)


def ang2pix(nside, phi, theta, nest=False):
    """
    Convert spherical angle (astrotools definition) to HEALpixel ipix
    Substitutes hp.ang2pix

    :param nside: nside of the healpy pixelization
    :param phi: longitude in astrotools definition
    :param theta: latitude in astrotools definition
    :param nest: set True in case you work with healpy's nested scheme
    :return: pixel number(s)
    """
    v = ang2vec(phi, theta)
    # mimic ValueError behavior from healpys function ang2pix()
    if not np.all(hp.isnsideok(nside)):
        raise ValueError("%s is not a valid nside parameter (must be a power of 2, less than 2**30)" % str(nside))
    ipix = hp.vec2pix(nside, *v, nest=nest)

    return ipix


def vec2ang(v):
    """
    Substitutes healpy.vec2ang() to use our angle convention.

    :param v: vector(s) of shape (3, n)
    :return: tuple consisting of

             - phi [range (pi, -pi), 0 points in x-direction, pi/2 in y-direction],
             - theta [range (pi/2, -pi/2), pi/2 points in z-direction]
    """
    return coord.vec2ang(v)


def vec2pix(nside, v, y=None, z=None, nest=False):
    """
    Convert HEALpixel ipix to spherical angles (astrotools definition)
    Substitutes hp.vec2pix

    :param nside: nside of the healpy pixelization
    :param v: either (x, y, z) vector of the pixel center(s) or only x-coordinate
    :param y: y-coordinate(s) of the center
    :param z: z-coordinate(s) of the center
    :param nest: set True in case you work with healpy's nested scheme
    :return: vector of the pixel center(s)
    """
    if y is None and z is None:
        v, y, z = v
    ipix = hp.vec2pix(nside, v, y, z, nest=nest)
    return ipix


def query_disc(nside, v, radius, nest=False, **kwargs):
    """
    Substitutes hp.query_disc but supports also pixel number input

    :param nside: nside of the healpy pixelization
    :param v: either (x, y, z) vector of the pixel center or healpy pixel
    :param radius: radius of disk in radians
    :param nest: set True in case you work with healpy's nested scheme
    :return: pixels thay lie within radius from center v
    """
    if isinstance(v, (int, np.int32, np.int64)):
        v = pix2vec(nside, v, nest=nest)
    return hp.query_disc(nside, v, radius, nest=nest, **kwargs)


def angle(nside, ipix, jpix, nest=False, each2each=False):
    """
    Give the angular distance between two pixel arrays.

    :param nside: nside of the healpy pixelization
    :param ipix: healpy pixel i (either int or array like int)
    :param jpix: healpy pixel j (either int or array like int)
    :param nest: use the nesting scheme of healpy
    :param each2each: if true, calculates every combination of the two lists v1, v2
    :return: angular distance in radians
    """
    v1 = pix2vec(nside, ipix, nest)
    v2 = pix2vec(nside, jpix, nest)
    return coord.angle(v1, v2, each2each=each2each)


def rotate_map(healpy_map, rotation_axis, rotation_angle):
    """
    Perform rotation of healpy map for given rotation axis and angle(s).

    :param healpy_map: healpix map to be rotated
    :param rotation_axis: rotation axis, either np.array([x, y, z]) or ndarray with shape (3, n)
    :param rotation_angle: rotation angle in radians, either float or array size n
    :return: rotated healpy map, same shape as input healpy map or shape (n, npix)
    """
    rotation_axis = coord.atleast_kd(rotation_axis, 2)
    nside, npix = hp.get_nside(healpy_map), len(healpy_map)
    n_ang, n_ax = np.size(rotation_angle), np.shape(rotation_axis)[-1]
    assert (n_ang == n_ax) or (np.min([n_ang, n_ax]) == 1), "Rotation axes and angles dimensions not compatible."
    n = np.max([n_ang, n_ax])
    rotation_vectors = pix2vec(nside, np.arange(npix))
    if n > 1:
        rotation_vectors = np.tile(rotation_vectors, n)
        rotation_axis = np.repeat(rotation_axis, npix*((n_ax == 1) * n + (n_ax > 1)), axis=1)
        rotation_angle = np.repeat(rotation_angle, npix*((n_ang == 1) * n + (n_ang > 1)))
    _vecs = coord.rotate(rotation_vectors, rotation_axis, -rotation_angle)
    _phi, _theta = vec2ang(np.squeeze(_vecs.reshape(3, -1, npix)))
    return hp.get_interp_val(healpy_map, np.pi / 2. - _theta, _phi)


def norder2npix(norder):
    """
    Give the number of pixel for the given HEALpix order.

    :param norder: norder of the healpy pixelization
    :return: npix, number of pixels of the healpy pixelization
    """
    return 12 * 4 ** norder


def npix2norder(npix):
    """
    Give the HEALpix order for the given number of pixel.

    :param npix: number of pixels of the healpy pixelization
    :return: norder, norder of the healpy pixelization
    """
    norder = np.log(npix / 12) / np.log(4)
    if not (norder.is_integer()):
        raise ValueError('Wrong pixel number (it is not 12*4**norder)')
    return int(norder)


def norder2nside(norder):
    """
    Give the HEALpix nside parameter for the given HEALpix order.

    :param norder: norder of the healpy pixelization
    :return: nside, nside of the healpy pixelization
    """
    return 2 ** norder


def nside2norder(nside):
    """
    Give the HEALpix order for the given HEALpix nside parameter.

    :param nside: nside of the healpy pixelization
    :return: norder, norder of the healpy pixelization
    """
    norder = np.log2(nside)
    if not (norder.is_integer()):
        raise ValueError('Wrong nside number (it is not 2**norder)')
    return int(norder)


def statistic(nside, v, y=None, z=None, statistics='count', vals=None):
    """
    Create HEALpix map of count, frequency or mean or rms value.

    :param nside: nside of the healpy pixelization
    :param v: either (x, y, z) vector of the pixel center(s) or only x-coordinate
    :param y: y-coordinate(s) of the center
    :param z: z-coordinate(s) of the center
    :param statistics: keywords 'count', 'frequency', 'mean' or 'rms' possible
    :param vals: values (array like) for which the mean or rms is calculated
    :return: either count, frequency, mean or rms maps
    """
    npix = hp.nside2npix(nside)
    pix = vec2pix(nside, v, y, z)
    n_map = np.bincount(pix, minlength=npix)

    if statistics == 'count':
        v_map = n_map.astype('float')
    elif statistics == 'frequency':
        v_map = n_map.astype('float')
        v_map /= max(n_map)  # frequency [0,1]
    elif statistics == 'mean':
        if vals is None:
            raise ValueError
        v_map = np.bincount(pix, weights=vals, minlength=npix)
        v_map /= n_map  # mean
    elif statistics == 'rms':
        if vals is None:
            raise ValueError
        v_map = np.bincount(pix, weights=vals ** 2, minlength=npix)
        v_map = (v_map / n_map) ** .5  # rms
    else:
        raise NotImplementedError("Unknown keyword")

    return v_map


def skymap_mean_quantile(skymap, quantile=0.68):
    """
    Calculates mean direction and quantile from an arbitrary healpy skymap

    :param skymap: healpy skymap of valid healpy size
    :param quantile: quantile for which the scatter angle is calculated
    :return: either count, frequency, mean or rms maps
    """
    npix = len(skymap)
    nside = hp.npix2nside(npix)
    norm = np.sum(skymap)
    assert norm > 0
    skymap /= norm

    # calculate mean vector
    vecs = pix2vec(nside, range(npix))
    vec_mean = np.sum(vecs * skymap[np.newaxis], axis=1)
    vec_mean /= np.sqrt(np.sum(vec_mean**2))

    # calculate alpha
    alpha = np.arccos(np.sum(vecs * vec_mean[:, np.newaxis], axis=0))
    srt = np.argsort(alpha)
    idx = np.searchsorted(np.cumsum(skymap[srt]), quantile)
    alpha_quantile = alpha[srt][idx]

    return vec_mean, alpha_quantile


def exposure_pdf(nside=64, a0=-35.25, zmax=60, coord_system='gal', pdf=True):
    """
    Exposure (type: density function) of an experiment located at equatorial
    declination a0 and measuring events with zenith angles up to zmax degrees.

    :param nside: nside of the output healpy map
    :param a0: equatorial declination [deg] of the experiment (default: AUGER, a0=-35.25 deg)
    :param zmax: maximum zenith angle [deg] for the events
    :param coord_system: choose between different coordinate systems - gal, eq, sgal, ecl
    :param pdf: if false, return relative exposure
    :return: weights of the exposure map
    """
    npix = hp.nside2npix(nside)
    v = pix2vec(nside, range(npix))
    if coord_system != 'eq':
        v = getattr(coord, '%s2eq' % coord_system)(v)
    _, theta = vec2ang(v)
    exposure = coord.exposure_equatorial(theta, a0, zmax)
    if pdf is True:
        exposure /= exposure.sum()
    return exposure


def fisher_pdf(nside, v, y=None, z=None, k=None, threshold=4, sparse=False, pdf=True):
    """
    Probability density function of a fisher distribution of healpy pixels with mean direction (x, y, z) and
    concentration parameter kappa; normalized to 1.

    :param nside: nside of the healpy map
    :param v: either (x, y, z) vector of the center or only x-coordinate
    :param y: y-coordinate of the center
    :param z: z-coordinate of the center
    :param k: kappa for the fisher distribution, 1 / sigma**2
    :param threshold: Threshold in sigma up to where the distribution should be calculated
    :param sparse: returns the map in the form (pixels, weights); this may be meaningfull for small distributions
    :param pdf: if false, return values with maximum 1
    :return: pixels, weights at pixels if sparse else a full map with length nside2npix(nside)
    """
    assert k is not None, "Concentration parameter 'k' for fisher_pdf() must be set!"
    sigma = 1. / np.sqrt(k)  # in radians

    if (y is not None) and (z is not None):
        v = np.array([v, y, z])
    elif (y is None and z is not None) or (z is None and y is not None):
        raise ValueError("Either 'y' and 'z' are set to None or both are not None. No mixture allowed.")
    v = np.squeeze(v)
    assert v.shape[0] == 3, "Input vector v does not have proper shape (3, ...)"
    # if alpha_max is larger than a reasonable np.pi than query disk takes care of using only
    # np.pi as maximum range.
    alpha_max = threshold * sigma

    pixels = np.array(hp.query_disc(nside, v, alpha_max))
    if len(pixels) == 0:
        # If sigma is too small, the pixel sequence will be empty
        pixels = np.array([vec2pix(nside, v)])
        weights = np.array([1.])
    else:
        pvec = pix2vec(nside, pixels)
        length = np.sum(v ** 2, axis=0) ** 0.5
        d = np.sum(v[:, np.newaxis] * pvec, axis=0) / length
        # for large values of kappa exp(k * d) goes to infinity which is meaningless. So we use the trick to write:
        # exp(k * d) = exp(k * d + k - k) = exp(k) * exp(k * (d-1)). As we normalize the function to one in the end,
        # we can leave out the first factor exp(k)
        weights = np.exp(k * (d - 1)) if k > 30 else np.exp(k * d)

    weights = weights / np.sum(weights) if pdf is True else weights / np.max(weights)
    if sparse:
        return pixels, weights

    fisher_map = np.zeros(hp.nside2npix(nside))
    fisher_map[pixels] = weights
    return fisher_map


def dipole_pdf(nside, a, v, y=None, z=None, pdf=True):
    """
    Probability density function of a dipole. Returns 1 + a * cos(theta) for all pixels in hp.nside2npix(nside).

    :param nside: nside of the healpy map
    :param a: amplitude of the dipole, 0 <= a <= 1, automatically clipped
    :param v: either (x, y, z) vector of the pixel center(s) or only x-coordinate
    :param y: y-coordinate(s) of the center
    :param z: z-coordinate(s) of the center
    :param pdf: if false, return unnormalized map (modulation around 1)
    :return: weights
    """
    assert (a >= 0.) and (a <= 1.), "Dipole amplitude must be between 0 and 1"
    a = np.clip(a, 0., 1.)
    if y is not None and z is not None:
        v = np.array([v, y, z], dtype=np.float)

    # normalize to one
    direction = v / np.sqrt(np.sum(v ** 2))
    npix = hp.nside2npix(nside)
    v = np.array(pix2vec(nside, np.arange(npix)))
    cos_angle = np.sum(v.T * direction, axis=1)
    dipole_map = 1 + a * cos_angle

    if pdf is True:
        dipole_map /= np.sum(dipole_map)

    return dipole_map
