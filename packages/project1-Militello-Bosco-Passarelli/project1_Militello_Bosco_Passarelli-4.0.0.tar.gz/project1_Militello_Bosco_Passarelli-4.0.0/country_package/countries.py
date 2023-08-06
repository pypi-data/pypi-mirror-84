import sqlite3
import pandas as pd
import country_package.funzioni_country as fc
import os
path = os.path.dirname(os.path.realpath(__file__))
conn = sqlite3.connect('TestDB.db')  

c = conn.cursor() # The database will be saved in the location where your 'py' file is saved

c.execute('''CREATE TABLE IF NOT EXISTS COUNTRY
             ([generated_id] INTEGER PRIMARY KEY,[Country_ID] text, [Country_Name] text, [Population_Milion] float)''')

#per rendere permanente il cambiamento
conn.commit()
read_country = pd.read_csv (path + "\\country.csv")
read_country.to_sql('COUNTRY', conn, if_exists='replace', index = True) # Replace the values from the csv file into the table 'COUNTRY'

c.execute('''
SELECT DISTINCT *
FROM COUNTRY
          ''')

df = pd.read_sql_query("SELECT * FROM COUNTRY", conn)

print(c.fetchall())
conn.close()

somma = fc.sumPopulation(df["Population_Milion"])
name_max = fc.maxPopulation(df)
name_sort = fc.orderedState(df["Country_Name"])