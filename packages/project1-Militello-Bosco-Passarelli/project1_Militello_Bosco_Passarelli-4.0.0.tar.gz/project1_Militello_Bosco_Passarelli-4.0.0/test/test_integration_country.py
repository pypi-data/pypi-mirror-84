import unittest, sys, os
import sqlite3
sys.path.insert(0, os.path.join(os.path.dirname(sys.path[0]),'country_package'))

class TestIntegrationCountries(unittest.TestCase):
    
    def test_integration_select(self):
        conn = sqlite3.connect('country_package/TestDB.db')  
        c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
        c.execute('''
                    SELECT Country_ID
                    FROM COUNTRY
                    WHERE Country_Name == 'Italy'
                    ''')
        name = c.fetchone()
        self.assertAlmostEqual(name[0],'ITA')
        conn.close()
    
    def test_integration_insert(self):    
        conn = sqlite3.connect('country_package/TestDB.db')  
        c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
        t = tuple(["PRV", 'Prova', 0.0])
        c.execute('''
                    INSERT INTO COUNTRY (Country_ID, Country_Name, Population_Milion)
                    VALUES (?,?,?)
                    ''', (t[0],t[1],t[2]))
        c.execute('''
                    SELECT *
                    FROM COUNTRY
                    WHERE Country_Name == 'Prova'
                    ''')
        r = c.fetchone()
        self.assertAlmostEqual(r[1:4],t)
        conn.close()
    
    def test_integration_delete(self):    
        conn = sqlite3.connect('country_package/TestDB.db')  
        c = conn.cursor() # The database will be saved in the location where your 'py' file is saved
        t = tuple(["PRV", 'Prova', 0.0])
        c.execute('''
                    INSERT INTO COUNTRY (Country_ID, Country_Name, Population_Milion)
                    VALUES (?,?,?)
                    ''', (t[0],t[1],t[2]))
        c.execute("DELETE FROM COUNTRY WHERE Country_Name == 'Prova'")
        c.execute('''
                    SELECT *
                    FROM COUNTRY
                    WHERE Country_Name == 'Prova'
                    ''')
        r = c.fetchone()
        self.assertAlmostEqual(r, None)
        conn.close()
