import os
import sys
import numpy as np
import unittest

from astrotools import coord, gamale, healpytools as hpt
from astrotools.simulations import PATH, ObservedBound, SourceBound

nside = 64
ncrs = 1000
nsets = 10
np.random.seed(0)


class TestObservedBound(unittest.TestCase):

    def setUp(self):
        self.nside = 64
        self.nsets = 10
        self.ncrs = 1000
        self.shape = (self.nsets, self.ncrs)

    def test_01_n_cosmic_rays(self):
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        self.assertEqual(sim.ncrs, self.ncrs)

    def test_02_nsets(self):
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        self.assertEqual(sim.nsets, self.nsets)

    def test_03_keyword_setup(self):
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim.set_energy(log10e_min=19.)
        sim.set_charges(charge='mixed')
        sim.set_xmax('double')
        sim.set_sources(sources='sbg')
        sim.smear_sources(delta=0.1)
        sim.apply_exposure()
        sim.arrival_setup(fsig=0.4)
        crs = sim.get_data(convert_all=True)
        self.assertEqual(crs['pixel'].shape, crs['lon'].shape, crs['log10e'].shape)

    def test_04_set_energy_charge_arrays(self):
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        log10e = np.random.random(size=self.shape)
        charge = np.random.randint(0, 10, size=self.shape)
        sim.set_energy(log10e_min=log10e)
        sim.set_charges(charge=charge)
        crs = sim.get_data()
        self.assertTrue(np.allclose(crs['log10e'], log10e) and np.allclose(crs['charge'], charge))

        sim2 = ObservedBound(self.nside, self.nsets, self.ncrs)
        log10e = np.random.random(self.ncrs)
        charge = np.random.random(self.ncrs)
        sim2.set_energy(log10e)
        sim2.set_charges(charge)
        self.assertTrue(np.allclose(sim2.crs['log10e'], log10e) and np.allclose(sim2.crs['charge'], charge))

        sim3 = ObservedBound(self.nside, self.nsets, self.ncrs)
        log10e = np.random.random(self.nsets)
        charge = np.random.random(self.nsets)
        with self.assertRaises(Exception):
            sim3.set_energy(log10e)
            sim3.set_charges(log10e)

        sim4 = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim4.set_charges({'h': 0.5, 'he': 0.25, 'n': 0.24, 'si': 0.01})
        self.assertTrue(np.abs(np.sum(sim4.crs['charge'] == 1) / float(self.nsets * self.ncrs) - 0.5) < 0.02)
        self.assertTrue(np.abs(np.sum(sim4.crs['charge'] == 2) / float(self.nsets * self.ncrs) - 0.25) < 0.02)
        self.assertTrue(np.abs(np.sum(sim4.crs['charge'] == 7) / float(self.nsets * self.ncrs) - 0.25) < 0.02)
        self.assertTrue(np.abs(np.sum(sim4.crs['charge'] == 14) / float(self.nsets * self.ncrs) - 0.01) < 0.01)

    def test_05_set_n_random_sources(self):
        n = 5
        fluxes = np.random.random(n)
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim.set_sources(n, fluxes=fluxes)
        self.assertTrue(sim.sources.shape[1] == n)
        self.assertTrue(np.allclose(fluxes, sim.source_fluxes))

    def test_06_set_n_sources(self):
        v_src = np.random.rand(30).reshape((3, 10))
        fluxes = np.random.random(10)
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim.set_sources(v_src, fluxes=fluxes)
        self.assertTrue(np.allclose(v_src, sim.sources))
        self.assertTrue(np.allclose(fluxes, sim.source_fluxes))

    def test_07_smear_sources_dynamically(self):
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim.set_energy(log10e_min=19.)
        sim.set_charges('AUGER')
        sim.set_sources(1)
        sim.set_rigidity_bins(np.arange(17., 20.5, 0.02))
        sim.smear_sources(delta=0.1, dynamic=True)
        sim.arrival_setup(1.)
        crs = sim.get_data(convert_all=True)
        rigs = sim.rigidities
        rig_med = np.median(rigs)
        vecs1 = coord.ang2vec(crs['lon'][rigs >= rig_med], crs['lat'][rigs >= rig_med])
        vecs2 = coord.ang2vec(crs['lon'][rigs < rig_med], crs['lat'][rigs < rig_med])
        # Higher rigidities experience higher deflections
        self.assertTrue(np.mean(coord.angle(vecs1, sim.sources)) < np.mean(coord.angle(vecs2, sim.sources)))

    def test_08_isotropy(self):
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim.arrival_setup(0.)
        crs = sim.get_data(convert_all=True)
        x = np.abs(np.mean(crs['vecs'][0]))
        y = np.abs(np.mean(crs['vecs'][1]))
        z = np.abs(np.mean(crs['vecs'][2]))
        self.assertTrue((x < 0.03) & (y < 0.03) & (z < 0.03))

    def test_09_exposure(self):
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim.apply_exposure()
        sim.arrival_setup(0.)
        crs = sim.get_data(convert_all=True)
        vecs_eq = coord.gal2eq(coord.ang2vec(np.hstack(crs['lon']), np.hstack(crs['lat'])))
        lon_eq, lat_eq = coord.vec2ang(vecs_eq)
        self.assertTrue(np.abs(np.mean(lon_eq)) < 0.05)
        self.assertTrue((np.mean(lat_eq) < -0.5) & (np.mean(lat_eq) > - 0.55))

    def test_10_charge(self):
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        charge = 2
        sim.set_charges(charge)
        self.assertTrue(np.all(sim.crs['charge'] == charge))

    def test_11_xmax_setup(self):
        sim1 = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim1.set_energy(19.)
        sim1.set_charges(2)
        sim1.set_xmax('stable')
        check1 = (sim1.crs['xmax'] > 500) & (sim1.crs['xmax'] < 1200)

        sim2 = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim2.set_energy(19.)
        sim2.set_charges(2)
        sim2.set_xmax('stable')
        check2 = (sim2.crs['xmax'] > 500) & (sim2.crs['xmax'] < 1200)

        sim3 = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim3.set_energy(19.)
        sim3.set_charges(2)
        sim3.set_xmax('empiric')
        check3 = (sim3.crs['xmax'] > 500) & (sim3.crs['xmax'] < 1200)

        sim4 = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim4.set_energy(19.)
        sim4.set_charges(2)
        sim4.set_xmax('double')
        check4 = (sim4.crs['xmax'] > 500) & (sim4.crs['xmax'] < 1200)

        self.assertTrue(check1.all() and check2.all() and check3.all() and check4.all())

    def test_12_xmax_mass(self):
        sim1 = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim2 = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim1.set_energy(19.)
        sim2.set_energy(19.)
        sim1.set_charges('equal')
        sim2.set_charges(26)
        sim1.set_xmax('double')
        sim2.set_xmax('double')
        # Xmax of iron should be smaller (interact higher in atmosphere)
        self.assertTrue(np.mean(sim1.crs['xmax']) > np.mean(sim2.crs['xmax']))

    def test_13_xmax_energy(self):
        sim1 = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim2 = ObservedBound(self.nside, self.nsets, self.ncrs)
        sim1.set_energy(20. * np.ones(self.shape))
        sim2.set_energy(19. * np.ones(self.shape))
        sim1.set_charges(1)
        sim2.set_charges(1)
        sim1.set_xmax('double')
        sim2.set_xmax('double')
        # Xmax for higher energy is bigger
        self.assertTrue(np.mean(sim1.crs['xmax']) > np.mean(sim2.crs['xmax']))

    def test_14_lensing_map(self):
        lens_path = os.path.dirname(os.path.realpath(__file__)) + '/toy-lens/jf12-regular.cfg'
        toy_lens = gamale.Lens(lens_path)
        nside = toy_lens.nside
        sim = ObservedBound(nside, self.nsets, self.ncrs)
        sim.set_energy(19.*np.ones(self.shape))
        sim.set_charges(1)
        sim.set_xmax('empiric')
        sim.set_sources('gamma_agn')
        sim.lensing_map(toy_lens)
        # Xmax for higher energy is bigger
        self.assertTrue(sim.lensed)
        self.assertTrue(np.shape(sim.cr_map) == (1, sim.npix))
        self.assertAlmostEqual(np.sum(sim.cr_map), 1.)
        self.assertTrue(np.min(sim.cr_map) < np.max(sim.cr_map))

    def test_15_exposure(self):
        nsets = 100
        sim = ObservedBound(self.nside, nsets, self.ncrs)
        sim.apply_exposure(a0=-35.25, zmax=60)
        sim.arrival_setup(0.2)
        crs = sim.get_data(convert_all=True)
        lon, lat = np.hstack(crs['lon']), np.hstack(crs['lat'])
        ra, dec = coord.vec2ang(coord.gal2eq(coord.ang2vec(lon, lat)))
        exp = coord.exposure_equatorial(dec, a0=-35.25, zmax=60)
        self.assertTrue((exp > 0).all())

    def test_16_high_nside(self):
        nside_high = 256
        sim = ObservedBound(nside_high, nsets=self.nsets, ncrs=self.ncrs)
        self.assertTrue(sim.crs['nside'] == nside_high)
        self.assertTrue(sim.crs.nside() == nside_high)
        sim.arrival_setup(1.)
        self.assertTrue(np.max(sim.crs['pixel']) >= 0.8 * sim.npix)

    def test_17_energy_rigidity_set(self):
        ncrs = 100
        e = 19.5
        sim = ObservedBound(self.nside, self.nsets, ncrs)
        sim.set_energy(e * np.ones((self.nsets, ncrs)))
        sim.set_charges(2)
        sim.set_rigidity_bins(np.linspace(17., 20.48, 175))
        self.assertTrue((sim.crs['log10e'] == e).all())

    def test_18_energy_spectra(self):
        nsets = 100
        sim = ObservedBound(self.nside, nsets, self.ncrs)
        log10e_power_3 = sim.set_energy(log10e_min=19., log10e_max=21., energy_spectrum='power_law', gamma=-3)
        ebin = 0.1
        for e in np.arange(19.1, 20.1, ebin):
            sum_low = np.sum((log10e_power_3 >= e-ebin) & (log10e_power_3 < e))
            sum_high = np.sum((log10e_power_3 >= e) & (log10e_power_3 < e+ebin))
            self.assertTrue(sum_low > sum_high)
        sim2 = ObservedBound(self.nside, nsets, self.ncrs)
        log10e_power_4 = sim2.set_energy(log10e_min=19., log10e_max=21., energy_spectrum='power_law', gamma=-4)
        # higher energies for flatter spectrum
        self.assertTrue(np.mean(log10e_power_3) > np.mean(log10e_power_4))
        sim3 = ObservedBound(self.nside, nsets, self.ncrs)
        log10e_auger_fit = sim3.set_energy(log10e_min=19., log10e_max=21., energy_spectrum='auger_fit')
        self.assertTrue(np.mean(log10e_power_3) > np.mean(log10e_auger_fit))
        self.assertTrue(np.mean(log10e_power_4) < np.mean(log10e_auger_fit))

    def test_19_apply_uncertainties(self):
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        log10e = sim.set_energy(log10e_min=19., log10e_max=21., energy_spectrum='power_law', gamma=-3)
        sim.set_charges('mixed')
        xmax = sim.set_xmax()
        sim.set_sources(10)
        sim.set_rigidity_bins(np.arange(17., 20.5, 0.02))
        sim.smear_sources(delta=0.1, dynamic=True)
        sim.arrival_setup(1.)
        vecs = hpt.pix2vec(sim.nside, np.hstack(sim.crs['pixel']))
        sim.apply_uncertainties(err_e=0.1, err_a=1, err_xmax=10)
        # check that array are not equal but deviations are smaller than 5 sigma
        self.assertTrue(not (log10e == sim.crs['log10e']).all())
        self.assertTrue((np.abs(10**(log10e - 18) - 10**(sim.crs['log10e'] - 18)) < 5*0.1*10**(log10e - 18)).all())
        self.assertTrue(not (xmax == sim.crs['xmax']).all())
        self.assertTrue((np.abs(xmax - sim.crs['xmax']) < 50).all())
        vec_unc = coord.ang2vec(np.hstack(sim.crs['lon']), np.hstack(sim.crs['lat']))
        self.assertTrue(not (coord.angle(vecs, vec_unc) == 0).all())
        self.assertTrue((coord.angle(vecs, vec_unc) < np.deg2rad(10)).all())

    def test_20_exposure_issue(self):
        sim = ObservedBound(nside=4, nsets=nsets, ncrs=ncrs)
        sim.apply_exposure(a0=-35.25, zmax=60)
        sim.arrival_setup(0.)
        crs = sim.get_data(convert_all=True)
        _, dec = coord.vec2ang(coord.gal2eq(crs['vecs'].reshape(3, -1)))
        self.assertTrue(np.sum(coord.exposure_equatorial(dec, a0=-35.25, zmax=60) <= 0) == 0)

    def test_21_convert_all(self):
        sim = ObservedBound(nside=4, nsets=nsets, ncrs=ncrs)
        sim.arrival_setup(0.)
        crs = sim.get_data(convert_all=False)
        keys = crs.keys()
        self.assertTrue('vecs' not in keys and 'lon' not in keys and 'lat' not in keys)

        vecs = crs['vecs']  # automatic from pixel center
        sim.convert_pixel('angles')  # converts pixel to lon / lat
        crs = sim.get_data(convert_all=False)
        keys = crs.keys()
        self.assertTrue('vecs' not in keys and 'lon' in keys and 'lat' in keys)
        _lon, _lat = coord.vec2ang(vecs)
        self.assertTrue(np.mean(abs(crs['lon'] - _lon) < 0.5))
        self.assertTrue(np.mean(abs(crs['lat'] - _lat) < 0.5))
        self.assertTrue(np.mean(abs(crs['lon'] - _lon) > 0))
        self.assertTrue(np.mean(abs(crs['lat'] - _lat) > 0))

        sim = ObservedBound(nside=4, nsets=nsets, ncrs=ncrs)
        sim.apply_exposure(a0=-35.25, zmax=60)
        sim.arrival_setup(0.)
        crs = sim.get_data(convert_all=True)
        keys = crs.keys()
        self.assertTrue('vecs' in keys and 'lon' in keys and 'lat' in keys)

    def test_22_shuffle(self):
        sim = ObservedBound(self.nside, self.nsets, self.ncrs)
        src_vecs = np.array([1, 1, 1])
        src_pix = hpt.vec2pix(sim.nside, src_vecs)
        sim.set_sources(src_vecs[:, np.newaxis])

        sim.arrival_setup(fsig=0.1)
        crs = sim.get_data(convert_all=False, shuffle=True)
        self.assertTrue(np.all(src_pix == crs['pixel'][sim.signal_label]))
        self.assertTrue(np.all(src_pix == crs['pixel'][crs['signal_label'].astype(bool)]))


class TestSourceBound(unittest.TestCase):

    def setUp(self):
        self.nsets = 120
        self.ncrs = 1000
        self.shape = (self.nsets, self.ncrs)

    def test_01_init(self):
        sim = SourceBound(self.nsets, self.ncrs)
        self.assertEqual(sim.ncrs, self.ncrs)
        self.assertEqual(sim.nsets, self.nsets)
        self.assertEqual(sim.shape, (self.nsets, self.ncrs))

    def test_02_source_distance(self):
        sim = SourceBound(self.nsets, self.ncrs)
        sim.set_sources(source_density=1e-3)
        self.assertTrue((sim.universe.rmax > 20) & (sim.universe.rmax < 40))
        dmin = np.min(sim.universe.distances, axis=-1)
        self.assertTrue((np.median(dmin) > 3) & (np.median(dmin) < 10))

        sim = SourceBound(self.nsets, self.ncrs)
        sim.set_sources(source_density=1)
        dmin = np.min(sim.universe.distances, axis=-1)
        self.assertTrue((np.median(dmin) < 1))

        sim = SourceBound(self.nsets, self.ncrs)
        sim.set_sources(source_density=1e-6)
        dmin = np.min(sim.universe.distances, axis=-1)
        self.assertTrue((np.median(dmin) > 20))

        densities = np.array([1e-6, 1e-3, 1])
        n_each = 100
        sim = SourceBound(int(n_each * len(densities)), self.ncrs)
        sim.set_sources(source_density=np.repeat(densities, n_each))
        dmin = np.min(sim.universe.distances[:100], axis=-1)
        self.assertTrue((np.median(dmin) > 20))
        dmin = np.min(sim.universe.distances[100:200], axis=-1)
        self.assertTrue((np.median(dmin) > 3) & (np.median(dmin) < 10))
        dmin = np.min(sim.universe.distances[200:], axis=-1)
        self.assertTrue((np.median(dmin) < 1))

    @unittest.skipIf(sys.version_info < (3, 0), "Simulation libraries work only for python 3.")
    def test_03a_fluxes(self):
        sim = SourceBound(self.nsets, self.ncrs)
        sim.set_energy(gamma=-2, log10e_min=19.6, log10_cut=20.5, rig_cut=False)
        sim.set_charges(charges={'h': 1.})
        sim.set_sources(source_density=1e-3)
        sim.attenuate()
        sim.smear_sources(np.deg2rad(3))
        # sim.plot_arrivals()
        # sim.plot_spectrum()
        # sim.plot_distance()

        # protons propagate very far: barely protons within rmax
        mask_inside_10 = sim.crs['distances'] <= 30
        fraction_inside = np.sum(mask_inside_10) / float(sim.ncrs * sim.nsets)
        self.assertTrue(fraction_inside < 0.15)

        sim = SourceBound(self.nsets, self.ncrs)
        sim.set_energy(gamma=-2, log10e_min=19.6, log10_cut=20.5, rig_cut=False)
        sim.set_charges(charges={'he': 1.})
        sim.set_sources(source_density=1e-3)
        sim.attenuate()
        sim.smear_sources(np.deg2rad(3))
        # sim.plot_arrivals()
        # sim.plot_spectrum()
        # sim.plot_distance()
        mask_inside_10 = sim.crs['distances'] <= 30
        fraction_inside = np.sum(mask_inside_10) / float(sim.ncrs * sim.nsets)
        self.assertTrue(fraction_inside < 0.25)

        sim = SourceBound(self.nsets, self.ncrs)
        sim.set_energy(gamma=-2, log10e_min=19.6, log10_cut=20.5, rig_cut=False)
        sim.set_charges(charges={'n': 1.})
        sim.set_sources(source_density=1e-3)
        sim.attenuate()
        sim.smear_sources(np.deg2rad(3))
        # sim.plot_arrivals()
        # sim.plot_spectrum()
        # sim.plot_distance()
        mask_inside_10 = sim.crs['distances'] <= 30
        fraction_inside = np.sum(mask_inside_10) / float(sim.ncrs * sim.nsets)
        self.assertTrue(fraction_inside > 0.7)

        sim = SourceBound(self.nsets, self.ncrs)
        sim.set_energy(gamma=-2, log10e_min=19.6, log10_cut=20.5, rig_cut=False)
        sim.set_charges(charges={'si': 1.})
        sim.set_sources(source_density=1e-3)
        sim.attenuate()
        sim.smear_sources(np.deg2rad(3))
        # sim.plot_arrivals()
        # sim.plot_spectrum()
        # sim.plot_distance()
        mask_inside_10 = sim.crs['distances'] <= 30
        fraction_inside = np.sum(mask_inside_10) / float(sim.ncrs * sim.nsets)
        self.assertTrue(fraction_inside < 0.4)

        sim = SourceBound(self.nsets, self.ncrs)
        sim.set_energy(gamma=-2, log10e_min=19.6, log10_cut=20.5, rig_cut=False)
        sim.set_charges(charges={'fe': 1.})
        sim.set_sources(source_density=1e-3)
        sim.attenuate()
        sim.smear_sources(np.deg2rad(3))
        # sim.plot_arrivals()
        # sim.plot_spectrum()
        # sim.plot_distance()
        mask_inside_10 = sim.crs['distances'] <= 30
        fraction_inside = np.sum(mask_inside_10) / float(sim.ncrs * sim.nsets)
        self.assertTrue(fraction_inside < 0.2)

    @unittest.skipIf(sys.version_info < (3, 0), "Simulation libraries work only for python 3.")
    def test_03b_fluxes(self):
        densities = [1e-5, 1e-3, 1e-1]
        bound_source = [[120, 180], [30, 60], [3, 15]]

        for i, d in enumerate(densities):
            # make a separate simulation for each source density
            sim = SourceBound(self.nsets, 1000)
            sim.set_energy(log10e_min=19.6)
            sim.set_charges('first_minimum_CTG')
            sim.set_sources(source_density=d)
            sim.attenuate()
            # check if number of events from the strongest source of the representative set is within the expected range
            idx_select = sim._select_representative_set()
            ns = np.array([np.sum(sim.crs['source_labels'][idx_select] == k) for k in range(sim.universe.n_src)]).max()
            self.assertTrue((ns >= bound_source[i][0]) & (ns <= bound_source[i][1]))

        # same check as above but with all source densities simulated simultaneously
        n_each = 100
        sim = SourceBound(int(n_each * len(densities)), 1000)
        sim.set_energy(log10e_min=19.6)
        sim.set_charges('first_minimum_CTG')
        sim.set_sources(source_density=np.repeat(densities, n_each))
        sim.attenuate()
        for i in range(len(densities)):
            mask = (np.arange(sim.nsets) < (i+1)*n_each) & (np.arange(sim.nsets) >= i*n_each)
            idx_select = sim._select_representative_set(mask=mask)
            ns = np.array([np.sum(sim.crs['source_labels'][idx_select] == k) for k in range(sim.universe.n_src)]).max()
            self.assertTrue((ns >= bound_source[i][0]) & (ns <= bound_source[i][1]))

    @unittest.skipIf(sys.version_info < (3, 0), "Simulation libraries work only for python 3.")
    def test_04a_shuffle(self):
        sim = SourceBound(self.nsets, self.ncrs)
        sim.set_energy(gamma=-2, log10e_min=19.6)
        sim.set_charges(charges={'h': 1.})
        sim.set_sources(source_density=1e-3)
        sim.attenuate()
        crs = sim.get_data(shuffle=True)
        src_labels = crs['source_labels']
        self.assertTrue(np.all(src_labels[sim.signal_label] != -1))

    @unittest.skipIf(sys.version_info < (3, 0), "Simulation libraries work only for python 3.")
    def test_04b_shuffle(self):
        sim = SourceBound(self.nsets, self.ncrs)
        sim.set_energy(gamma=-2, log10e_min=19.6)
        sim.set_charges(charges={'h': 1.})
        sim.set_sources(source_density=1e-3)
        sim.attenuate()
        crs = sim.get_data(shuffle=False)
        test1 = np.unique(crs['vecs'] * crs['log10e'])
        crs = sim.get_data(shuffle=True)
        test2 = np.unique(crs['vecs'] * crs['log10e'])
        self.assertTrue(np.all(test1 == test2))

    @unittest.skipIf(sys.version_info < (3, 0), "Simulation libraries work only for python 3.")
    def test_05a_first_minimum(self):
        sim = SourceBound(self.nsets, 1000)
        sim.set_energy(log10e_min=19.6)
        sim.set_charges('first_minimum_CTG')
        sim.set_sources(source_density=1e-3)
        sim.attenuate()
        sim.smear_sources(np.deg2rad(3))
        # sim.plot_arrivals()
        # sim.plot_spectrum()
        # sim.plot_distance()

        sim = SourceBound(self.nsets, 1000)
        sim.set_energy(log10e_min=19.6)
        sim.set_charges('first_minimum_CTD')
        sim.set_sources(source_density=1e-3)
        sim.attenuate(library_path=PATH + '/simulation/crpropa3__emin_18.5__emax_21.0__IRB_Dominguez11.npz')
        sim.smear_sources(np.deg2rad(3))
        # sim.plot_arrivals()
        # sim.plot_spectrum()
        # sim.plot_distance()

    @unittest.skipIf(sys.version_info < (3, 0), "Simulation libraries work only for python 3.")
    def test_05b_second_minimum(self):
        sim = SourceBound(self.nsets, 1000)
        # sim.set_energy(gamma=-2.04, log10e_min=19.6, log10_cut=19.88, rig_cut=True)
        # sim.set_charges(charges={'n': 0.798, 'si': 0.202})
        sim.set_energy(log10e_min=19.6)
        sim.set_charges('second_minimum_CTG')
        sim.set_sources(source_density=1e-3)
        sim.attenuate()
        sim.smear_sources(np.deg2rad(3))
        # sim.plot_arrivals()
        # sim.plot_spectrum()
        # sim.plot_distance()


class TestReweight(unittest.TestCase):

    @unittest.skipIf(sys.version_info < (3, 0), "Simulation libraries work only for python 3.")
    def setUp(self):
        self.charge = {'h': 1, 'he': 2, 'n': 7, 'si': 14, 'fe': 26}
        data = np.load(PATH+'/simulation/crpropa3__emin_18.5__emax_21.0__IRB_Gilmore12.npz', allow_pickle=True)
        self.fractions = data['fractions'].item()
        self.log10e_bins = data['log10e_bins']
        self.distances = data['distances']

    @unittest.skipIf(sys.version_info < (3, 0), "Simulation libraries work only for python 3.")
    def test_01_dimensions(self):
        ne = self.log10e_bins.size - 1
        nd = self.distances.size
        for key in self.charge:
            self.assertTrue(self.fractions[key].shape == (ne, nd, 5, ne))

    @unittest.skipIf(sys.version_info < (3, 0), "Simulation libraries work only for python 3.")
    def test_02_no_energy_gain(self):
        for key in self.charge:
            for i, lge in enumerate(self.log10e_bins[:-1]):
                frac = self.fractions[key]
                self.assertTrue(np.sum(frac[i][:, :, self.log10e_bins[:-1] > lge]) == 0.)


if __name__ == '__main__':
    unittest.main()
