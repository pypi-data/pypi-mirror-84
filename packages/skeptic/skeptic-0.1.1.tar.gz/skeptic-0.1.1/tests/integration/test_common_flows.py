from pathlib import PurePath
from skeptic.interface.correlation import correlate
from skeptic.interface.utilities import csv_to_X_Y
import unittest


class TestCommonFlow(unittest.TestCase):
    def setUp(self):
        self.data_dir = PurePath(
            PurePath(__file__).parent,
            '..',
            'data')

    def test_hdi_correlation(self):
        '''
            Using a csv file with various metrics about a country and it's "Human Development Index" (hdi), find the correlation between those metrics and the hdi.
        '''
        X, Y = csv_to_X_Y(PurePath(self.data_dir,'hdi.csv'), 'Development Index')
        correlation = correlate(X, Y)
        print(f'Got a correlation of: {correlation}')
        self.assertTrue(correlation > 0.97)
