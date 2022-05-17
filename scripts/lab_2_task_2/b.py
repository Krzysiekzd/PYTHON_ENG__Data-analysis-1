# This script reads data from manualy corrected .csv file (data.csv) from The World Bank,
# containing population data from all countries. 
# It also reads country size data from country_sizes.csv.
# Then it chooses random year and random country and finds 4 closest countries by population size in
# the drawn year (2 lower and 2 higher).
# Then it generates an animated bubble plot using matplotlib.animation which shows population sizes
# of the chosen countries (1960-current year) and also their population densities. 
from turtle import color
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random
class PopulationPlotsGenerator_RandomChoice:
    def __init__(self, population_file_name, country_sizes_file_name,bubble_colors, output_file_name, figure_color='white'):
        self.file_name = population_file_name
        self.country_sizes_file_name = country_sizes_file_name
        self.chosen_countries = []
        self.x_title = ""
        self.bubble_colors = bubble_colors
        self.output_file_name = output_file_name
        self.figure_color = figure_color
        self.countries = {} # dictionary where each key is a country name and each value is a list of
        # population sizes year by year
        self.country_codes = {} # key-country name, value-country code
        self.years = []
        self.plot_data = {} # dictionary where each key is a year and each value is a list of 
        # tuples (country_name, population_size). Contains only chosen countries.
        self.country_sizes = {} # key-country name, value-country size in sq.km
        self.max_population = 0

        self.bubble_text_list = None
        self.year_count = None
        self.bubbles_list = []
        self.ax = None

        self.min_country_density = 10000000000
        self.max_country_density = 0

        self.readCsv()
        self.readCountrySizeCSV()
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
                self.country_codes[country_data[0][1:]] = country_data[1][1:]

    def readCountrySizeCSV(self):
        with open(self.country_sizes_file_name) as file:
            lines = file.read().split('\n')[:-1]
            for i in lines: self.country_sizes[i.split(';')[0]]=float(i.split(';')[1])

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
                    if population == None: pass
                    elif  population > self.max_population: self.max_population = population
                    year_data.append((country, self.countries[country][i]))
                self.plot_data[self.years[i]]=year_data
            except: pass
        # Find min and max density
        country_sizes = {i:self.country_sizes[i] for i in self.chosen_countries}
        for i in self.chosen_countries:
            country_min = min(self.countries[i])            
            if  country_min/country_sizes[i] < self.min_country_density: self.min_country_density = country_min/country_sizes[i]
            country_max = max(self.countries[i])
            if  country_max/country_sizes[i] > self.max_country_density: self.max_country_density = country_max/country_sizes[i]

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


    def generatePlots(self):
        year_0 = self.years[0]
        data = self.plot_data[year_0]
        max_y = int(self.max_population/1000000 * 1.1)
        country_names = [i[0] for i in data]
        country_codes = [self.country_codes[i] for i in country_names]
        heights = [i[1]/1000000 for i in data]

        fig, ax = plt.subplots(figsize=(13,5))
        fig.set_facecolor(self.figure_color)

        ax.set_xlim([int(year_0)-1,int(self.years[-1])+4])
        ax.set_ylim([0,max_y])
        ax.set_ylabel('Population size [mln]', size=12, fontweight='bold')
        ax.set_title('Population size by year', size=20, fontweight='bold')
        ax.set_xlabel(self.x_title, size=12, fontweight='bold')
        self.ax = ax

        # create bubbles
        for i in range(len(country_names)):
            density = data[i][1]/self.country_sizes[country_names[i]]
            self.bubbles_list.append(ax.scatter([int(year_0)],[heights[i]], color=self.bubble_colors[i],zorder=10, 
                s=(density-self.min_country_density)/(self.max_country_density-self.min_country_density)*4600+400,
                alpha=0.5
            ))
        # create bubble labels
        self.bubble_text_list = [ax.text(int(year_0), height, country_codes[index], size=10,
            horizontalalignment='center', verticalalignment='center',zorder=11, alpha=0.5,
            color='#0a0a0a'
            ) for index, height in enumerate(heights)]

        # add year counter
        self.year_count = ax.text(ax.get_xlim()[0]+3, max_y*0.93, year_0, horizontalalignment='left', 
           verticalalignment='top', size='20', backgroundcolor='white', zorder=12, 
           bbox={'facecolor': 'white', 'pad': 5,'edgecolor': '#d4d4d4'})
        
        ax.grid(zorder=1, axis='y', color='#d4d4d4')

        # create animation
        animation = FuncAnimation(fig, func=self.animationFunction, frames=self.years[1:], interval=150, repeat=True, 
            blit=False)
        animation.save(self.output_file_name)

    def animationFunction(self, year):
        data = self.plot_data[year]
        heights = [data[i][1]/1000000 for i in range(len(data))]
        densities = [data[index][1]/self.country_sizes[i] for index, i in enumerate(self.chosen_countries)]
        densities = [(i-self.min_country_density)/(self.max_country_density-self.min_country_density)*4600+400
            for i in densities]
        self.year_count.set_text(year)

        # remove bubbles
        if int(year)%7!=0:
            for i in self.bubbles_list: i.remove()
        self.bubbles_list = []

        # add bubbles
        for index, _ in enumerate(self.chosen_countries):
            
            self.bubbles_list.append(self.ax.scatter([int(year)],[heights[index]], color=self.bubble_colors[index],
                zorder=10, s=densities[index],alpha=0.5 
                ))

            self.bubble_text_list[index].set_y(heights[index])
            self.bubble_text_list[index].set_x(int(year))

if __name__=="__main__":
    PopulationPlotsGenerator_RandomChoice(
        population_file_name='data.csv', 
        country_sizes_file_name='country_sizes.csv',
        output_file_name='b_final_bubble.gif',
        bubble_colors=[ '#6cb34b', '#3e9ed6', '#db071c', '#a639e6','#d9cf1c',],
        figure_color='white'
    )
