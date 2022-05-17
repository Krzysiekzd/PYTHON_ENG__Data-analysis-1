# This script reads data from manualy corrected .csv file (data.csv) from The World Bank,
# containing population data from all countries. 
# Then it chooses random year, finds 4 countries closest to Poland by population size in
# the drawn year (2 lower and 2 higher).
# Then it generates an animated pie chart using matplotlib.animation which shows population sizes
# of the chosen countries in one year (1960-current year). 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.patches as mpatches

import random
class PopulationPlotsGenerator_RandomChoice_PolandCentered:
    def __init__(self, file_name,pie_colors, output_file_name, figure_color='white'):
        self.file_name = file_name
        self.chosen_countries = []
        self.subtitle = ""
        self.pie_colors = pie_colors
        self.output_file_name = output_file_name
        self.figure_color = figure_color
        self.countries = {} # dictionary where each key is a country name and each value is a list of
        # population sizes year by year
        self.country_codes = {} # key-country name, value-country code
        self.years = []
        self.plot_data = {} # dictionary where each key is a year and each value is a list of 
        # tuples (country_name, population_size). Contains only chosen countries.
        self.max_population = 0
        
        self.readCsv()
        self.getRandomYear()
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
        
    def randomYear(self):
        year_index = random.randint(0,len(self.years)-1)
        data_from_year = [(i, self.countries[i][year_index]) for i in self.countries]
        data_from_year.sort(key=lambda x:x[1], reverse=True)
        return year_index, data_from_year

    def getRandomYear(self):
        # choose random year index
        year_index, data_from_year = None, None
        is_full_data_not_defined = True
        while is_full_data_not_defined:
            try:
                year_index, data_from_year = self.randomYear()
                is_full_data_not_defined = False
            except:pass
        # find index of Poland
        index_of_poland = -1
        for index, i in enumerate(data_from_year):
            if i[0]=='Poland': index_of_poland = index
        self.chosen_countries = [i[0] for i in data_from_year[index_of_poland-2:index_of_poland+3]]
        self.subtitle = f'Countries closest to Poland in year {self.years[year_index]}'

    def generatePlots(self):
        year_0 = self.years[0]
        data = self.plot_data[year_0]
        country_names = [i[0] for i in data]
        country_codes = [self.country_codes[i] for i in country_names]
        sizes = [i[1]/1000000 for i in data]

        fig, ax = plt.subplots(figsize=(8,8))
        fig.set_facecolor(self.figure_color)
        self.ax = ax
        
        ax.text(0,1.3,'Total population of 5 five countries', size=16, fontweight='bold',
            horizontalalignment='center', verticalalignment='center')
        ax.text(0,1.2,self.subtitle, size=10, fontstyle='italic',
            horizontalalignment='center', verticalalignment='center')
        ax.text(0, -1.2, f'Combined populations size: {round(sum(sizes),2)} MLN', size=12, fontweight='bold',
            horizontalalignment='center', verticalalignment='center')
        
        self.handles = [mpatches.Patch(color=self.pie_colors[i], label=self.chosen_countries[i])
            for i in range(len(self.chosen_countries))]
        
        ax.legend(handles=self.handles, bbox_to_anchor=(0.15,0.15))

        # create pie chart
        ax.pie(sizes, colors=self.pie_colors, 
            labels=[f'{i}, {round(sizes[index],2)} MLN, {round(sizes[index]/sum(sizes)*100,2)}%' 
                for index,i in enumerate(country_codes)], radius=0.8)
        
        # add year counter
        ax.text(1,1,year_0, size='20', backgroundcolor='white', zorder=12, 
           bbox={'facecolor': 'white', 'pad': 5,'edgecolor': '#d4d4d4'})

        # create animation
        animation = FuncAnimation(fig, func=self.animationFunction, frames=self.years[1:], interval=150, repeat=True, 
            blit=False)
        animation.save(self.output_file_name)

    def animationFunction(self, year):
        print(year)
        data = self.plot_data[year]
        sizes = [i[1]/1000000 for i in data]
        country_names = [i[0] for i in data]
        country_codes = [self.country_codes[i] for i in country_names]
        ax = self.ax
        ax.clear()
        
        # new chart
        ax.text(0,1.3,'Total population of 5 five countries', size=16, fontweight='bold',
            horizontalalignment='center', verticalalignment='center')
        ax.text(0,1.2,self.subtitle, size=10, fontstyle='italic',
            horizontalalignment='center', verticalalignment='center')
        ax.text(0, -1.2, f'Combined populations size: {round(sum(sizes),2)} MLN', size=12, fontweight='bold',
            horizontalalignment='center', verticalalignment='center')
        ax.pie(sizes, colors=self.pie_colors, 
            labels=[f'{i}, {round(sizes[index],2)} MLN, {round(sizes[index]/sum(sizes)*100,2)}%' 
                for index,i in enumerate(country_codes)], radius=0.8)
        ax.text(1,1,year, size='20', backgroundcolor='white', zorder=12, 
           bbox={'facecolor': 'white', 'pad': 5,'edgecolor': '#d4d4d4'})
        ax.legend(handles=self.handles, bbox_to_anchor=(0.15,0.15))


        

if __name__=="__main__":
    PopulationPlotsGenerator_RandomChoice_PolandCentered(
        file_name='data.csv', 
        output_file_name='c_final_pie.gif',
        pie_colors=[ '#6cb34b', '#3e9ed6', '#db071c', '#a639e6','#d9cf1c',],
        figure_color='#e6e1e6'
    )
