
===================================================================
-----------------------  larkinlab 0.0.12  ------------------------
===================================================================


This library contains the functions I have created or come accross that I find myself using often. 

I will be adding functions as I create and find them, so be sure to update to the latest version.
Check the CHANGELOG for release info.


========  In The Future  ========

- long description for pypi
- a new plot_ex(df, type='') function for larkinlab.explore, to return various graphs for quick analysis
plans to incluse scatterplot, regplot, bubble plot, bar chart, pie chart, histogram and more. Will work
by returning plots for each column in dataframe.
- a set of colex (column explore) functions to do some of the stuff over columns rather than the entire dataframe.
- a set of functions to perform basic machine learning algorithms over dataframes and return evaluation metrics
also with a colex function to come later.

========================================================================================
-------------------------  Code Descriptions  ------------------------------
========================================================================================


-----  to install/update  ------

pip3 install larkinlab
pip3 install --upgrade larkinlab

--------  to import  -----------

import larkinlab as ll

---------  Subpackages  --------

larkinlab.explore
larkinlab.machinelearning

--------------------------------

=========================  ll.explore  =============================

This subpackage is build for exploring data. Contains functions that help you get an understanding of the data at hand quickly.

to import: 
from larkinlab import explore as llex

Dependencies:
pandas, numpy, matplotlib.pyplot, seaborn

-------------------------------------
llex.dframe_ex(df)

The dframe_ex function takes a dataframe and returns a few things
- The number of rows, columns, and total data points
- The names of the columns, limited to the first 60 if more than 60 exist
- Displays up to the first 5 rows of the dataframe via the df.head method
        
Params:
df - pandas DataFrame

-------------------------------------    
llex.vcount_ex(df)

The vcount_ex function returns the value counts and normalized value counts 
for all of columns in the dataframe passed through it.
        
Params:
df - pandas DataFrame

-------------------------------------
llex.missing_ex(df)
        
The missing_ex function prints the number of missing values in each column of
the dataframe passed through it.

Params:
df - pandas DataFrame

-------------------------------------
llex.scat_ex(df)
        
The scat_ex function returns a scatterplot representing the value counts and 
thier respective occurances for each column in the dataframe passed through it. 

Params:
df - pandas DataFrame

-------------------------------------
llex.corr_ex(df, min_corr, min_count, fig_size, colors)
        
The corr_ex function returns either a pearson correlation values chart and a heatmap of said
correlation values, or only the heatmap, for all of the columns in the dataframe passed through it. 

Param Defaults:
df : pandas DataFrame
min_corr = (0.2) : minimum correlation value to appear on heatmap
min_count = 1 : minimum number of observations required per pair of columns to have a valid result(pandas.df.corr(min_periods) argument)
fig_size = (8, 10) : heatmap size, 2 numbers
colors = ('Reds') : color of the heatmap. Heatmap from seaborn, so uses thier color codes

-------------------------------------


-------------------------------------


-------------------------------------



=========================  ll.machinelearning  =============================

This package contains streamlined machine learning models and evaluation tools

to import:
from larkinlab import machinelearning as llml

Dependencies: 
pandas, numpy, matplotlib.pyplot 


-------------------------------------


-------------------------------------


-------------------------------------


-------------------------------------



=========================================================================================================================
-------------------------------------------------------------------------------------------------------------------------
=========================================================================================================================


Created By: Conor Larkin

email: conor.larkin16@gmail.com
GitHub: github.com/clarkin16
LinkedIn: linkedin.com/in/clarkin16

Thanks for checking this out!
