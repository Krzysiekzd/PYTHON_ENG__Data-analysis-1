# Overview  
This repository is actually a report made for "Data analysis and visualization" laboratories. It contains various animated plots, Gantt charts and scripts + data to generate them. All of them were created using Python's *matplotlib* library. In order to practise my Python skills, in the first and second lab tasks, I wrote a custom parser to read csv file instead of using *pandas* library. Some scripts may differ by only one line of code, as it was a requirement to have seperate scripts for each plot. The quality of the code was not a priority in this project. The report was converted from HTML to Markdown using an online tool and can be found below or in the *report.html* file. 
   
   
   

Lab 1
=====

Task 2
======

### Task definition:

![](lab_1_task_2.png)

### About my solution:

All scripts have similar structure - one main class, that slightly differs between them.  
Scripts create and save series of plots to a directory that must be specified by the user.  
Scripts parse data from manualy corrected CSV downloaded from The World Bank (groups filtered out, some unnecessary lines deleted).  
In tasks **b** and **c**, 4 'closest countries' are 2 with higher populations and 2 with lower populations than the selected one.  
Each run of **b** and **c** should return different results, because countries and years are randomly chosen in a runtime.  
Saved images has been converted into .gif file using _convert -delay 15 \*.png final\_output.gif_ .

a)
--

![](plots/a_lab_1.gif)

b)
--

![](plots/b_lab_1.gif)

c)
--

![](plots/c_lab_1.gif)

Lab 2
=====

Task 1
======

### Task definition:

![](lab_2_task_1.png)

### About my solution:

Scripts have similar structure to those from lab 1, but now matplotlib.animation is being used instead of saving images to files. Important thing to mention is that those scripts might sometimes return bugged plots. This is probably caused by some data-reading bug (because some countries have an incomplete population data).  
In such case, the script should be run again and it should work.

Colored
-------

a)
--

![](plots/a_final_colored.gif)

b)
--

![](plots/b_final_colored.gif)

c)
--

![](plots/c_final_colored.gif)

B&W
---

a)
--

![](plots/a_final_bw.gif)

b)
--

![](plots/b_final_bw.gif)

c)
--

![](plots/c_final_bw.gif)

Task 2
======

### Task definition:

![](lab_2_task_2.png)

### About my solution:

Again, scripts are somewhat similar to the original ones.  
In the line plot, I positioned country codes to be on the right side of the lines, instead of being above them. In my opinion this is a better solution, because country codes (almost) do not overlap. Unfortunately, I forgot to add a legend.  
Bubble plot is probably the least readable one. It lacks a legend and a proper desription (especially about countries density). Country codes overlap with bubbles and it looks messy.  
I might have not understood the task correctly. Also it takes the most time to be generated.  
One thing I should mention is that the x-axis is not labeled 'years' in any of those plots. However, I did that on purpose as it is obvious and may be deducted by reading the main titles.

a) Line plot
------------

![](plots/a_final_line.gif)

b) Bubble plot
--------------

![](plots/b_final_bubble.gif)

c) Pie chart
------------

![](plots/c_final_pie.gif)

Lab 3
=====

Task 3
======

### Task definition:

![](lab_3_task_3.png)

Breakup of Yugoslavia plot
--------------------------

![](plots/slowed_down.gif)

Task 4
======

### Task definition:

![](lab_3_task_4.png)

### About my solution:

I've translated, modified and grouped data and saved them to file 'caledar\_year\_table.csv'.  
While working with the plot, I decided that placing labels inside the bars would make it unreadable.  
One option was to create the arrow annotations, but each one of those would have to be implicilty positioned inside the script.  
It would probably be way faster to make those annotations using Paint or any other easy graphic editor.  
I could also assign unique numbers to each event, position them on the plot, and create a table on the side of the plot, but after all I think that it would require too much work.  
Thus, I did not make any labels at all. In my opinion, this plot would look way better using an interactive visualization.  

a) Colored Gantt plot
---------------------

![](plots/gannt_plot_colored.png)

a) B&W Gantt plot
-----------------

![](plots/gannt_plot_black_white.png)
