# This script reads data from manualy corrected .csv file (data.csv) from The World Bank,
# containing population data from all countries. 
# Then it chooses random year and random country, finds 4 closest countries by population size in
# the drawn year (2 lower and 2 higher).
# Then it generates series of plots and saves them in the indicated path. Each bar plot
# shows population sizes of the chosen countries in one year (1960-current year). 
# Those images can be easily converted into a .gif file.
import matplotlib.pyplot as plt
import random
class PopulationPlotsGenerator_RandomChoice:
    def __init__(self, file_name, output_path):
        self.file_name = file_name
        self.chosen_countries = []
        self.output_path = output_path
        self.x_title = ""
        self.countries = {} # dictionary where each key is a country name and each value is a list of
        # population sizes year by year
        self.years = []
        self.plot_data = {} # dictionary where each key is a year and each value is a list of 
        # tuples (country_name, population_size). Contains only chosen countries.
        self.max_population = 0
        self.readCsv()
        self.getRandomCountryAndYear()
        self.preparePlotData()
        self.generatePlots()

    def readCsv(self):
        with open(self.file_name) as data_file:
            rows = data_file.read().split('\n') # used read+split instead of readlines not to deal with EOL signs
            titles = [i[1:] for i in rows[0].split('",')[:-1]]
            self.years = titles[4:].copy()
            for row in rows[1:]:
                country_data = row.split('",')[:-1]
                self.countries[country_data[0][1:]] = [int(i[1:]) if i[1:] else None for i in country_data[4:]]

    def extractDataFromYear(self, year):
        # Method that returns dicitonary with data from the indicated year. Each key is a country name
        # and each value its population size. 
        year_index = self.years.index(year)
        return_list = []
        for i in self.countries:
            population_size = None
            try: population_size = self.countries[i][year_index]
            except: pass
            if population_size: return_list.append((i, population_size))
        return_list.sort(key= lambda x: x[1], reverse=True)
        return{i[0]:i[1] for i in return_list}

    def preparePlotData(self):
        # Fills self.plot_data dictionary
        for i in range(len(self.years)):
            # if data from all countries in given year can't be found, than this year is skipped
            try:
                year_data = []
                for country in self.chosen_countries:
                    population = self.countries[country][i]
                    if  population > self.max_population: self.max_population = population
                    year_data.append((country, self.countries[country][i]))
                self.plot_data[self.years[i]]=year_data
            except: pass
        
    def generatePlots(self):
        for year in self.plot_data:
            data = self.plot_data[year]
            max_y = int(self.max_population/1000000 * 1.1)

            fig, ax = plt.subplots(figsize=(10,5))
            ax.bar(x=[i[0] for i in data], height=[round(i[1]/1000000, 2) for i in data])
            plt.ylim([0,max_y])
            #figure = plt.figure(figsize=(10, 5))
            #plt.axis(ymin=0, ymax=max_y)
            #plt.bar(x=[i[0] for i in data], height=[round(i[1]/1000000, 2) for i in data])

            plt.ylabel('Population [mln]')
            plt.title(f'Population by year, current year: {year}')
            plt.xlabel(self.x_title)
            plt.savefig(f'{self.output_path}/{year}.png')
            plt.close()
    def randomYear(self):
        year_index = random.randint(0,len(self.years)-1)
        data_from_year = [(i, self.countries[i][year_index]) for i in self.countries]
        data_from_year.sort(key=lambda x:x[1], reverse=True)
        return year_index, data_from_year
        
    def getRandomCountryAndYear(self):
        year_index, data_from_year = None, None
        is_full_data_not_defined = True
        while is_full_data_not_defined:
            try:
                year_index, data_from_year = self.randomYear()
                is_full_data_not_defined = False
            except:pass
        # choose random country
        country_index = random.randint(2, len(data_from_year)-3)
        self.chosen_countries = [i[0] for i in data_from_year[country_index-2:country_index+3]]
        self.x_title = f'Randomly chosen: country - {data_from_year[country_index][0]}, year - {self.years[year_index]} '


if __name__=="__main__":
    PopulationPlotsGenerator_RandomChoice(
        file_name='data.csv', 
        output_path='task_b_images'
    )
