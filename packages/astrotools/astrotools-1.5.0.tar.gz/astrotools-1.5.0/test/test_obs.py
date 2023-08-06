import unittest

import numpy as np
from astrotools import auger, coord, healpytools as hpt, obs
np.random.seed(0)


def setup_roi(nside=256, ncrs=2000, roi_size=0.25, energy_spectrum='uniform', energy_ordering=False, emin=19):

        npix = hpt.nside2npix(nside)
        roipix = 0

        angles_pix_to_roi = hpt.angle(nside, roipix, np.arange(npix))
        iso_map = np.zeros(npix)
        iso_map[angles_pix_to_roi < roi_size] = 1
        p = np.cumsum(iso_map)
        pix = np.sort(p.searchsorted(np.random.rand(ncrs) * p[-1]))

        if energy_spectrum == 'auger':
            energies = auger.rand_energy_from_auger(ncrs, emin)
        elif energy_spectrum == 'uniform':
            energies = np.random.uniform(10, 20, ncrs)
        if energy_ordering:
            energies = np.sort(energies)[::-1]

        return pix, energies


def setup_roi_same_ncrs_in_bins(nside=62, ncrs=4, nbins=2, alpha_max=0.25, bin_type='area'):
    bins = np.arange(nbins+1).astype(np.float)
    if bin_type == 'lin':
        alpha_bins = alpha_max * bins / nbins
    else:
        alpha_bins = 2 * np.arcsin(np.sqrt(bins/nbins) * np.sin(alpha_max/2))

    npix = hpt.nside2npix(nside)
    roipix = 0
    angles_pix_to_roi = hpt.angle(nside, roipix, np.arange(npix))
    pixel = np.zeros(ncrs, dtype=int)

    for a in range(nbins):
        iso_map_bin = np.zeros(npix)
        mask_bin = (angles_pix_to_roi >= alpha_bins[a]) * (angles_pix_to_roi < alpha_bins[a + 1])
        iso_map_bin[mask_bin] = 1
        iso_map_bin /= np.sum(iso_map_bin)
        ratio = int(ncrs / nbins)
        pixel[ratio * a: ratio * (a + 1)] = np.random.choice(np.arange(npix), ratio, p=iso_map_bin)

    return pixel


class TestThrust(unittest.TestCase):

    def setUp(self):
        _n2 = 1. / np.sqrt(2)
        self.vecs1 = np.array([[4/5., 4/5., _n2, _n2],
                               [3/5., -3/5., _n2, -_n2],
                               [0, 0, 0, 0]])
        self.vecs2 = np.array([[4/5., 4/5., _n2, _n2],
                               [0, 0, _n2, -_n2],
                               [3/5., -3/5., 0, 0]])
        self.w = np.array([1.2, 1.2, 0.8, 0.8])

    def test_01_point(self):
        p = np.array([1., 0., 0.])[:, np.newaxis]
        T, N = obs.thrust(p, weights=None)
        self.assertTrue(T[0] == 1.)
        self.assertTrue(T[1] == 0.)
        self.assertTrue(T[2] == 0.)

    def test_02_line(self):
        ncrs = 1000
        roi_size = 0.25
        lat = np.zeros(ncrs)
        lon = np.linspace(-roi_size, roi_size, ncrs)
        p = coord.ang2vec(lon, lat)
        T, N = obs.thrust(p, weights=None)
        self.assertTrue(np.abs(T[1] - 0.5 * roi_size) < 1e-3)
        self.assertTrue(np.abs(T[2]) < 1e-3)

    def test_03_iso(self):

        nside = 256
        roi_size = 0.25
        pix, _ = setup_roi(nside=nside, roi_size=roi_size)
        p = hpt.rand_vec_in_pix(nside, pix)
        T, N = obs.thrust(p, weights=None)
        self.assertTrue(np.abs(T[1] - 4./(3. * np.pi) * roi_size) < 1e-2)
        self.assertTrue(T[2] < T[1])
        self.assertTrue(np.abs(T[2] - T[1]) < 1e-2)

    def test_04_toy(self):
        t, n = obs.thrust(self.vecs1, self.w, ntry=5000)
        self.assertTrue(np.allclose(n[0], np.array([1, 0, 0])))
        self.assertTrue(np.allclose(n[1], [0, 1, 0], atol=1e-3) or np.allclose(n[1], [0, -1, 0], atol=1e-3))
        self.assertTrue(np.allclose(n[2], [0, 0, 1], atol=1e-3) or np.allclose(n[2], [0, 0, -1], atol=1e-3))
        for i in range(3):
            _t = np.sum(np.abs(self.w * np.sum(self.vecs1 * n[i][:, np.newaxis], axis=0))) / np.sum(np.abs(self.w))
            self.assertAlmostEqual(_t, t[i], places=10)

    def test_04_toy_minimize_distance(self):
        t, n = obs.thrust(self.vecs1, self.w, minimize_distances=True, ntry=5000)
        self.assertTrue(t[1] < t[2])
        self.assertTrue(np.allclose(n[0], np.array([1, 0, 0])))
        self.assertTrue(np.allclose(n[1], [0, 1, 0], atol=1e-3) or np.allclose(n[1], [0, -1, 0], atol=1e-3))
        self.assertTrue(np.allclose(n[2], [0, 0, 1], atol=1e-3) or np.allclose(n[2], [0, 0, -1], atol=1e-3))
        t1 = np.sum(np.abs(self.w * np.sum(self.vecs1 * n[0][:, np.newaxis], axis=0))) / np.sum(np.abs(self.w))
        self.assertAlmostEqual(t1, t[0], places=10)
        for i in range(2):
            _t = np.sum(np.abs(self.w * np.sum(self.vecs1 * n[1+i][:, np.newaxis], axis=0))) / np.sum(np.abs(self.w))
            self.assertAlmostEqual(_t, t[2-i], places=10)


class Test2PT(unittest.TestCase):

    def setUp(self):
        self.nside, self.stat, self.nbins = 64, 1000, 180
        self.npix = hpt.nside2npix(self.nside)
        self.vecs = hpt.rand_vec_in_pix(self.nside, np.random.choice(self.npix, self.stat))

    def test_01_number_correlations(self):

        ac = obs.two_pt_auto(self.vecs, bins=self.nbins, cumulative=True)
        # Check if cumulative value is in upper triangle matrix (100 x 100) without diagonal
        self.assertEqual(ac[-1], int(int(self.stat**2 - self.stat) / 2))

    def test_02_isotropy_peak_90(self):
        ac = obs.two_pt_auto(self.vecs, bins=self.nbins, cumulative=False, normalized=True)
        # Check if isotropy peaks at 90 degree
        self.assertTrue(np.abs(np.argmax(ac) - 90) < 20)

    def test_03_isotropy_in_omega(self):
        ac = obs.two_pt_auto(self.vecs, bins=self.nbins, cumulative=True, normalized=True)
        theta_bins = np.linspace(0, np.pi, self.nbins + 1)
        expectation = np.sin(theta_bins / 2)**2
        # Check if number of events within opening angle scales with expectation
        # as only 1000 cosmic rays: exclude first 15 bins (starting at 15 deg)
        self.assertTrue(np.allclose(ac[15:], expectation[16:], rtol=5e-2))

    def test_04_clustering(self):
        radius = 0.1
        pix_choice = hpt.query_disc(self.nside, np.array([0, 0, 1]), radius)
        vecs = hpt.rand_vec_in_pix(self.nside, np.random.choice(pix_choice, self.stat))
        ac = obs.two_pt_auto(vecs, bins=self.nbins, cumulative=False)
        theta_bins = np.linspace(0, np.pi, self.nbins + 1)
        # no event with correlation higher than 2 * radius
        self.assertTrue(np.sum(ac[theta_bins[1:] > 2.1 * radius]) == 0)
        # all events within 2 * radius
        self.assertTrue(np.sum(ac[theta_bins[1:] < 2.1 * radius]) == np.sum(ac))
        # check if maximum is close to radius
        self.assertTrue(ac[np.argmin(np.abs(theta_bins[1:] - radius))] > 0.9 * max(ac))

    def test_05_inariant_rotation(self):
        ac = obs.two_pt_auto(self.vecs, bins=self.nbins, cumulative=True, normalized=True)
        vecs_rotated = coord.gal2eq(self.vecs)
        self.assertTrue(np.mean(coord.angle(self.vecs, vecs_rotated)) > 0.1)
        ac_rotated = obs.two_pt_auto(vecs_rotated, bins=self.nbins, cumulative=True, normalized=True)
        self.assertTrue(np.allclose(ac, ac_rotated))

    def test_06_two_pt_cross(self):
        cc = obs.two_pt_cross(self.vecs, self.vecs, cumulative=False)
        self.assertTrue(np.sum(cc) == self.stat**2)


class TestEEC(unittest.TestCase):

    def test_01_bin_type(self):
        nside, ncrs = 256, 2000
        nbins = 5
        vec_roi = hpt.pix2vec(nside, 0)
        pixel_0, energies_0 = setup_roi(nside, ncrs=ncrs)
        vecs_0 = np.array(hpt.pix2vec(nside, pixel_0))

        omega, bins, ncr_bin = obs.energy_energy_correlation(vecs_0, energies_0, vec_roi, nbins=nbins, bin_type='area')
        close_to_one = nbins * ncr_bin / ncrs
        self.assertTrue(np.allclose(close_to_one, np.ones(nbins), rtol=0.2))

        omega, bins, ncr_bin = obs.energy_energy_correlation(vecs_0, energies_0, vec_roi, nbins=nbins, bin_type='lin')
        constant = ncr_bin / np.arange(0.5, nbins, 1)
        close_to_one = constant / np.mean(constant)
        self.assertTrue(np.allclose(close_to_one, np.ones(nbins), rtol=0.4))

    def test_02_four_crs_one_bin(self):
        nside = 64
        ncrs = 4
        nbins = 1
        alpha_max = 0.25
        vec_roi = hpt.pix2vec(nside, 0)

        pixel = setup_roi_same_ncrs_in_bins(nside=nside, ncrs=ncrs, nbins=nbins, alpha_max=alpha_max, bin_type='area')
        energies = np.array([7., 5., 3., 1.])
        vecs = np.array(hpt.pix2vec(nside, pixel))

        omega, bins, ncr_bin = obs.energy_energy_correlation(vecs, energies, vec_roi, nbins=nbins, e_ref='median')
        self.assertTrue(np.abs(omega + 0.16825397) < 1e-8)

    def test_03_four_crs_two_bins(self):
        nside = 64
        ncrs = 4
        nbins = 2
        alpha_max = 0.25
        vec_roi = hpt.pix2vec(nside, 0)

        pixel = setup_roi_same_ncrs_in_bins(nside=nside, ncrs=ncrs, nbins=nbins, alpha_max=alpha_max, bin_type='area')
        energies = np.array([7., 5., 3., 1.])
        vecs = np.array(hpt.pix2vec(nside, pixel))

        omega, bins, ncr_bin = obs.energy_energy_correlation(vecs, energies, vec_roi, nbins=nbins, e_ref='median')
        self.assertTrue(np.abs(omega[0] + 0.0031746) < 1e-7)
        self.assertTrue(np.abs(omega[1] + 0.1047619) < 1e-7)

    def test_04_refmode_roi(self):
        nside = 64
        ncrs = 4
        nbins = 2
        alpha_max = 0.25
        vec_roi = hpt.pix2vec(nside, 0)

        pixel = setup_roi_same_ncrs_in_bins(nside=nside, ncrs=ncrs, nbins=nbins, alpha_max=alpha_max, bin_type='area')
        energies = np.array([7., 5., 3., 1.])
        vecs = np.array(hpt.pix2vec(nside, pixel))

        omega, bins, ncr_bin = obs.energy_energy_correlation(vecs, energies, vec_roi, nbins=nbins, e_ref='median', ref_mode='roi')
        self.assertTrue(np.abs(omega[0] + 0.32063492) < 1e-8)
        self.assertTrue(np.abs(omega[1] + 0.01587302) < 1e-8)


if __name__ == '__main__':
    unittest.main()
