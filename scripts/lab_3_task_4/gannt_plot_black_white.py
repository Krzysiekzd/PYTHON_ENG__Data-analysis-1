from matplotlib import pyplot as plt
import pandas as pd
# read data
dataframe = pd.read_csv('table.csv')
dataframe.START=pd.to_datetime(dataframe.START, dayfirst=True)
dataframe.END=pd.to_datetime(dataframe.END, dayfirst=True)
dataframe['DURATION']=dataframe.END-dataframe.START
dataframe.DURATION=dataframe.DURATION.apply(lambda x: x.days+1)
p_start=dataframe.START.min()
dataframe['REL_START']=dataframe.START.apply(lambda x: (x-p_start).days)
categories = ['Individual decisions', 'Courses resignations', 'Removing allocations', 'Performing allocations', 'Language exams', 'Examination sessions','Breaks','Classes', 'Semesters']
#colors = ['#bfbfbf','#e6e49c','#57ba84','#9b71bf','#150f6b','#e8569a','#348ceb','#f0e24a','#eb4034']
# prepare plot data
gannt_plot_rows = {}
for category_index,category in enumerate(categories):
    selected_records = dataframe.loc[dataframe['CATEGORY']==category]
    gannt_plot_rows[category_index]=[(s,d) for s,d in zip(selected_records['REL_START'],selected_records['DURATION'])]
# y axis ticks
fig,ax = plt.subplots(figsize=(15,5))
ax.set_title('Academic calendar 2022/2023',size=18)
for i in gannt_plot_rows:
    ax.broken_barh(gannt_plot_rows[i], (0.5+i*3.5, 3),edgecolor='black',facecolors='white')
ax.set_ylim(0,3.5*len(categories)+0.5)
ax.set_yticks([2+3.5*i for i in range(len(categories))],labels=categories)
# x axis ticks
months = ['Oct 1st','Nov 1st','Dec 1st','Jan 1st','Feb 1st', 'Mar 1st','Apr 1st','May 1st','Jun 1st','Jul 1st','Aug 1st','Sep 1st','Oct 1st']
months_durations = [31,30,31,31,28,31,30,31,30,31,31,30,31]
ax.set_xticks([sum(months_durations[:i]) for i in range(len(months_durations))],labels=months)

plt.savefig('gannt_plot_black_white.pdf',dpi=200,format='pdf')
plt.savefig('gannt_plot_black_white.png')
plt.show()