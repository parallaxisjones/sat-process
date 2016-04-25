import unittest
from stestdata import TestData
from sprocess.sentinel2 import Sentinel2
from sprocess.errors import SatProcessError


class TestProduct(unittest.TestCase):

    def setUp(self):
        self.t = TestData('sentinel2')
        self.filenames = self.t.files[self.t.names[0]]
        self.bandnames = self.t.bands[self.t.names[0]]

    def test_product_name(self):
        scene = Sentinel2(self.filenames)
        self.assertEqual(len(scene.bandnames()), len(scene.filenames()))
        self.assertEqual(scene.bandnames()[0], 'coastal')

    def test_ndvi(self):
        scene = Sentinel2(self.filenames)
        self.assertEquals(scene.band_numbers, 8)

        scene.ndvi()
        self.assertEquals(scene.band_numbers, 9)
        self.assertTrue('ndvi' in scene.bands)

    def test_ndvi_incorrect_bands(self):
        scene = Sentinel2(self.filenames)
        self.assertEquals(scene.band_numbers, 8)

        scene2 = scene.select(['red', 'blue', 'green'])

        try:
            scene2.ndvi()
        except SatProcessError as e:
            self.assertEquals(e.message, 'nir band is not provided')

        scene2 = scene.select(['nir', 'blue', 'green'])

        try:
            scene2.ndvi()
        except SatProcessError as e:
            self.assertEquals(e.message, 'red band is not provided')

    def test_evi(self):
        scene = Sentinel2(self.filenames)
        self.assertEquals(scene.band_numbers, 8)

        scene.evi()
        self.assertEquals(scene.band_numbers, 9)
        self.assertTrue('evi' in scene.bands)

    def test_process_chaining(self):
        scene = Sentinel2(self.filenames)
        self.assertEquals(scene.band_numbers, 8)

        scene.ndvi().evi()
        self.assertEquals(scene.band_numbers, 10)
        self.assertTrue('evi' in scene.bands)
        self.assertTrue('ndvi' in scene.bands)
