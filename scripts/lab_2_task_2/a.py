# This script reads data from manualy corrected .csv file (data.csv) from The World Bank,
# containing population data from all countries. 
# It generates an animated line plot using matplotlib.animation which shows population sizes 
# of the chosen countries in one year (1960-current year). 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class PopulationPlotsGenerator:
    def __init__(self, file_name, chosen_countries, x_title, line_colors, output_file_name, figure_color='white'):
        self.file_name = file_name
        self.chosen_countries = chosen_countries
        self.x_title = x_title
        self.line_colors = line_colors
        self.output_file_name = output_file_name
        self.figure_color = figure_color
        self.countries = {} # dictionary where each key is a country name and each value is a list of
        # population sizes year by year
        self.country_codes = {} # key-country name, value-country code
        self.years = []
        self.plot_data = {} # dictionary where each key is a year and each value is a list of 
        # tuples (country_name, population_size). Contains only chosen countries.
        self.max_population = 0
    
        self.year_count = None
        self.line_text_list = None
        self.lines_list = []

        self.readCsv()
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

        # create lines
        for i in range(len(country_names)):
            self.lines_list.append(ax.plot([int(year_0)],[heights[i]], self.line_colors[i],
                marker='o', zorder=10, markersize=3)[0])

        # create line labels
        self.line_text_list = [ax.text(int(year_0)+1, height, country_codes[index], size=10,
            horizontalalignment='left', verticalalignment='center',zorder=11) for index, height in enumerate(heights)]

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
        self.year_count.set_text(year)
        # update lines
        for index, line in enumerate(self.lines_list):
            xdata = list(line.get_xdata())
            xdata.append(int(year))
            line.set_xdata(xdata)

            ydata = list(line.get_ydata())
            ydata.append(heights[index])
            line.set_ydata(ydata)

            self.line_text_list[index].set_y(heights[index])
            self.line_text_list[index].set_x(int(year)+1)

if __name__=="__main__":
    PopulationPlotsGenerator(
        file_name='data.csv', 
        chosen_countries=['China', 'India', 'United States', 'Indonesia', 'Pakistan'], 
        x_title='',
        line_colors=['#b80614', '#f5d922', '#002868', '#a504c9', '#065c29'],
        output_file_name='a_final_line.gif',
        figure_color= '#ded6bd'
    )
 