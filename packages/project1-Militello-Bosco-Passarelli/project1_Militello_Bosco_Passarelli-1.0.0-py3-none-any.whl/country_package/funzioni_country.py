# Return the ammount of total population
def sumPopulation(population):
    sumPop = 0;
    for a in population:
        sumPop = sumPop + a
    return (sumPop)

# Return the name of the country with the highest population
def maxPopulation(df):
    maxPop = 0
    maxCountry = ""
    for i, row in df.iterrows():
        if row['Population_Milion'] > maxPop:
            maxPop = row['Population_Milion']
            maxCountry = row['Country_Name']
    return (maxCountry)

def orderedState(nomi):
    if type(nomi) not in [list]:
        nomi = nomi.tolist()
    nomi.sort()
    return nomi
