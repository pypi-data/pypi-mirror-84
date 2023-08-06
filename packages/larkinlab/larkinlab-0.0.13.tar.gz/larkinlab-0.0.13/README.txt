
===================================================================
-----------------------  larkinlab 0.0.13  ------------------------
===================================================================


This library contains the functions I have created or come accross that I find myself using often. 

I will be adding functions as I create and find them, so be sure to update to the latest version.

Check the CHANGELOG for release info.


========  In The Future  ========

- long description for pypi
- a new plot_ex(df, type='') function for larkinlab.explore, to return various graphs for quick analysis. Plans to incluse scatterplot, regplot, bubble plot, bar chart, pie chart, histogram and more. Will work by returning plots for each column in dataframe.
- a set of colex (column explore) functions to do some of the stuff over columns rather than the entire dataframe.
- a set of functions to perform basic machine learning algorithms over dataframes and return evaluation metrics
also with a colex function to come later.

========================================================================================
-------------------------  Code Descriptions  ------------------------------------------
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

This is built for exploring data. Contains functions that help you get an understanding of the data at hand quickly.

to import: 
from larkinlab import explore as llex

Dependencies:
pandas, numpy, matplotlib.pyplot, seaborn

-------------------------------------
functions
-------------------------------------

* llex.dframe_ex(df, head_val) *

The dframe_ex function takes a dataframe and returns a few things
- The number of rows, columns, and total data points
- The names of the columns, limited to the first 60 if more than 60 exist
- Displays up to the first n rows of the dataframe via the df.head method, set by head parameter.

// Parameter Default Values \\
df  ::  pandas DataFrame
head_val =5  ::  Sets the number of rown to display in the dataframe preview. Works via the pandas .head method. Set to 'all' for all rows

------------------------------------- 

* llex.vcount_ex(df, print_count) *

The vcount_ex function returns the value counts and normalized value counts for all of columns in the dataframe passed through it.
        
// Parameter Default Values \\
df  ::  pandas DataFrame
print_count =5  ::  sets the number of value counts to print for each column. Set to 'all' for all of them, for example - (df, print_count='all') 

-------------------------------------

* llex.missing_ex(df) *
        
The missing_ex function prints the number of missing values in each column of the dataframe passed through it.

// Parameter Default Values //
df  ::  pandas DataFrame

-------------------------------------

* llex.scat_ex(df) *
        
The scat_ex function returns a scatterplot representing the value counts and thier respective occurances for each column in the dataframe passed through it. 

// Parameter Default Values //
df  ::  pandas DataFrame

-------------------------------------

* llex.corr_ex(df, min_corr, min_count, fig_size, colors) *
        
The corr_ex function returns either a pearson correlation values chart and a heatmap of said correlation values, or only the heatmap, for all of the columns in the dataframe passed through it. 

// Parameter Default Values //
df  ::  pandas DataFrame
min_corr =0.2  ::  minimum correlation value to appear on heatmap
min_count =1  ::  minimum number of observations required per pair of columns to have a valid result(pandas.df.corr(min_periods) argument)
fig_size =(8, 10)  ::  heatmap size, 2 numbers
colors ='Reds'  ::  color of the heatmap. Heatmap from seaborn, so uses thier color codes

-------------------------------------
*  *

-------------------------------------
*  *

-------------------------------------



=========================  ll.machinelearning  =============================

This package contains streamlined machine learning models and evaluation tools

to import:
from larkinlab import machinelearning as llml

Dependencies: 
pandas, numpy, matplotlib.pyplot 

-------------------------------------
functions
-------------------------------------
*  *

-------------------------------------
*  *

-------------------------------------
*  *

-------------------------------------



=========================================================================================================================
-------------------------------------------------------------------------------------------------------------------------
=========================================================================================================================


Created By: Conor Larkin

email: conor.larkin16@gmail.com
GitHub: github.com/clarkin16
LinkedIn: linkedin.com/in/clarkin16

Thanks for checking this out!
