# This script reads data from manualy corrected .csv file (data.csv) from The World Bank,
# containing population data from all countries. 
# Then it generates an animated bar plot using matplotlib.animation which shows population sizes 
# of the chosen countries in one year (1960-current year). 
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
class PopulationPlotsGenerator:
    def __init__(self, file_name, chosen_countries, x_title, bar_colors, output_file_name, figure_color='white'):
        self.file_name = file_name
        self.chosen_countries = chosen_countries
        self.x_title = x_title
        self.bar_colors = bar_colors
        self.output_file_name = output_file_name
        self.figure_color = figure_color
        self.countries = {} # dictionary where each key is a country name and each value is a list of
        # population sizes year by year
        self.country_codes = {} # key-country name, value-country code
        self.years = []
        self.plot_data = {} # dictionary where each key is a year and each value is a list of 
        # tuples (country_name, population_size). Contains only chosen countries.
        self.max_population = 0

        self.bars_container = None
        self.bar_text_list = None
        self.year_count = None
        self.war_info = None
        self.ax = None
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
        self.ax = ax
        fig.set_facecolor(self.figure_color)
        ax.set_ylim([0,15]) # axis arbitrary fixed for this task
        ax.set_ylabel('Population size [mln]', size=12, fontweight='bold')
        ax.set_title('Population size by year', size=20, fontweight='bold')
        ax.set_xlabel(self.x_title, size=12, fontweight='bold')

        self.bars_container = ax.bar(x=country_names, height=heights, color=self.bar_colors, zorder=10)
        # create bar labels
        self.bar_text_list = [ax.text(index, height, country_codes[index], size=10,
            horizontalalignment='center', zorder=11) for index, height in enumerate(heights)]
        # add year counter
        self.year_count = ax.text(ax.get_xlim()[1]*0.955, ax.get_ylim()[1]*0.93, year_0, horizontalalignment='right', 
           verticalalignment='top', size='20', backgroundcolor='white', zorder=12, 
           bbox={'facecolor': 'white', 'pad': 5,'edgecolor': '#d4d4d4'})
        
        ax.grid(zorder=1, axis='y', color='#d4d4d4')
        # list with repeated years
        frames = [str(year) for year in range(1960, 1990)]
        for i in (1990,1991,1992,1993,1994,1995): frames.extend([str(i)]*6)
        frames.extend(str(i) for i in range(1996,2021))
        print(frames)
        # create animation
        animation = FuncAnimation(fig, func=self.animationFunction, frames=frames, interval=150, repeat=True, 
            blit=False)
        animation.save(self.output_file_name)

    def animationFunction(self, year):
        data = self.plot_data[year]
        heights = [data[i][1]/1000000 for i in range(len(data))]
        self.year_count.set_text(year)
        # update bars height
        for index, bar in enumerate(self.bars_container.get_children()):
            height = heights[index]
            bar.set_height(height)
            self.bar_text_list[index].set_y(heights[index]+self.max_population/1000000*0.01)
        # add war info
        if year == '1990' and self.war_info == None:
            self.war_info = self.ax.text(2.5,12,'BREAKUP OF YUGOSLAVIA',horizontalalignment='center', 
           verticalalignment='bottom',size='20',color='red')
            self.year_count.set_color('red')
        if year == '1996':
            self.war_info.remove()
            self.year_count.set_color('black')



if __name__=="__main__":
    PopulationPlotsGenerator(
        file_name='data.csv', 
        chosen_countries=
        ['Belarus',
        'Serbia',
        'Bulgaria',
        'Bosnia and Herzegovina',   
        'Croatia',
        'Austria'
        ], 
        x_title='European countries',
        bar_colors=['#bd1111','#eb7536','#ebc936','#199c0b', 'blue','#a504c9'],
        output_file_name='slowed_down.gif',
        figure_color= '#ded6bd'
    )
 