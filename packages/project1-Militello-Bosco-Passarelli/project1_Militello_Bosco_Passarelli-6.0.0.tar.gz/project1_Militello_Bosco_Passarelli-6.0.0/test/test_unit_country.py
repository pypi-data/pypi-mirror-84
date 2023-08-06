import unittest, sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'country_package'))
from funzioni_country import sumPopulation, maxPopulation, orderedState
import pandas as pd

class TestUnitCountries(unittest.TestCase):
    df = pd.read_csv ('test/country_test.csv')
    def test_unit_sumPopulation(self):
        #test sulla somma totale  
        self.assertAlmostEqual(sumPopulation(self.df['Population_Milion']), 1027.75)
        self.assertAlmostEqual(sumPopulation(pd.array([1,2,3,4,5])), 15)
    
   
    def test_unit_maxPopulation(self):
        self.assertAlmostEqual(maxPopulation(self.df), "USA")
    
    def test_unit_orderedState(self):
        self.assertAlmostEqual(orderedState(self.df['Country_Name']), ["Australia", "Brasil", "Egypt", "France", "Italy", "Japan", "Portugal", "Spain", "UK", "USA"])
        self.assertAlmostEqual(orderedState(["f", "a", "e", "z", "g"]), ["a", "e", "f", "g", "z"])