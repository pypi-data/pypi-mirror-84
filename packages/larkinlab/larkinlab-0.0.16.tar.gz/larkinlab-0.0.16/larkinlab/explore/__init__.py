# Part of the 'explore' subpackage of 'larkinlab'
# functions for Exploratory Analysis
#
# v0.0.16
#
##################################################################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

##################################################################################################################

def dframe_ex(df, 
               head_val=5,
               max_col=50
               ):

    # display shape and size
    print("Rows: ", df.shape[0])
    print("Columns: ", df.shape[1])
    print("Data Points: ", df.size, "\n")
    
    if max_col == 'all':
        print(df.columns)
    else:
        print("First ", max_col, " columns: ", df.columns[:max_col])

    # display first n rows of df (head_val param)    
    if head_val == 'all':
        return df.head(len(df))
    else:
        return df.head(head_val)

dframe_ex_desc = ('''
The dframe_ex function takes a dataframe and returns a few things
- The number of rows, columns, and total data points
- The names of the columns, up to the number set by max_col
- Displays up to the first n rows of the dataframe via the df.head method, set by head parameter.
''')

dframe_ex_params = ('''
> df  ::  pandas DataFrame
> head_val =5  ::  Sets the number of rown to display in the dataframe preview. Works via the pandas .head method. Set to 'all' for all rows
''')

##################################################################################################################

def vcount_ex(df,
              print_count=5
              ):
    # a function to print the value counts and their corresponding percentages of all columns in a given dataframe.
    
    #creates bold font
    class font:
        bold = '\033[1m'
        end = '\033[0m'
    
    #creates temporary list of all columns in dataframe to iterate through
    dfcol_temp_list = []
    for column in df.columns:
        x = column
        dfcol_temp_list.append(df[x])
    
    #iterate through column list getting their value counts and normalized value counts, and print them out
    n = 0
    for col in dfcol_temp_list:
        temp_comp_val_count_var = pd.concat([col.value_counts(), col.value_counts(normalize=True).mul(100)], axis=1, keys=('counts', "percentage"))
        y = df.columns[n]    
        print(font.bold + y + font.end)
        #print_count param all option
        if print_count == 'all':
            print(temp_comp_val_count_var.head(len(temp_comp_val_count_var)), "\n\n")
        else:
            print(temp_comp_val_count_var.head(print_count), "\n\n")
        n = n + 1

vcount_ex_desc = ('''
The vcount_ex function returns the value counts and normalized value counts for all of columns in the dataframe passed through it.
''')

vcount_ex_params = ('''
> df  ::  pandas DataFrame
> print_count =5  ::  sets the number of value counts to print for each column. Set to 'all' for all of them, for example - (df, print_count='all')
''')

##################################################################################################################

def missing_ex(df):
    # a function that prints how many values each column in a dataframe is missing a value in

    missing_rows_dict = {}
    missing_rows_dict_keys = df.columns

    for col in df:

        temp_frame = df[col]
        missing_rows = (df.shape[0]) - (temp_frame.value_counts().sum())

        for v in missing_rows_dict_keys:
            v = col
            missing_rows_dict[v] = [missing_rows]

        print("Missing Rows in", col, ": ", missing_rows)

missing_ex_desc = ('''
The missing_ex function prints the number of missing values in each column of the dataframe passed through it.
''')

missing_ex_params = ('''
> df  ::  pandas DataFrame
''')

##################################################################################################################

def scat_ex(df):
    # a function to return scatter plots of the value counts of all columns in a dataframe, for quick visual analysis of value counts
    for col in df.columns:
        
        #create temp dataframe to plot
        x = col
        scat_plot = df[x].value_counts()        
        scat_plot_df = pd.DataFrame(scat_plot)
        scat_plot_df = scat_plot_df.reset_index()
        scat_plot_df.columns = [x, 'val counts']
        
        #plot it
        plt.figure()
        plt.xlabel(x)
        plt.ylabel('val counts')
        plt.scatter(scat_plot_df.index.values, scat_plot_df['val counts'])

scat_ex_desc = ('''
The scat_ex function returns a scatterplot representing the value counts and thier respective occurances for each column in the dataframe passed through it.
''')

scat_ex_params = ('''
> df  ::  pandas DataFrame
''')

##################################################################################################################

def corr_ex(df, 
             min_corr=0.2, 
             fig_size=(8,10), 
             colors='Reds', 
             map_only=False, 
             min_count=1
            ):
    # a function to return a heatmap of the pearson correlation values
    
    #heat map
    corr_temp = df.corr(min_periods=min_count)
    kot = corr_temp[corr_temp>=min_corr]
    
    #map-only param
    if map_only == False :
        plt.figure(figsize=fig_size)
        sns.heatmap(kot, cmap=colors)
        return corr_temp
    elif map_only == True:
        plt.figure(figsize=fig_size)
        sns.heatmap(kot, cmap=colors)
    else:
        print("ERROR")

corr_ex_desc = ('''
The corr_ex function returns either a pearson correlation values chart and a heatmap of said correlation values, or only the heatmap, for all of the columns in the dataframe passed through it.
''')

corr_ex_params = ('''
> df  ::  pandas DataFrame
> min_corr =0.2  ::  minimum correlation value to appear on heatmap
> min_count =1  ::  minimum number of observations required per pair of columns to have a valid result(pandas.df.corr(min_periods) argument)
> fig_size =(8, 10)  ::  heatmap size, 2 numbers
> colors ='Reds'  ::  color of the heatmap. Heatmap from seaborn, so uses thier color codes
''')

##################################################################################################################

def func_list(desc=False):
    #check functions quickly
    
    if desc == True:
        print("larkinlab.explore contains these functions: ")
        print('================================================', "\n")
        for k, v in explore_info_dict.items():
            print("* ", k, " *", "\n")
            print("Description: ", v[0])
            print("Params/Args: ", v[1])
            print('---------------------------------------------')
            
    elif desc == False:
        print("larkinlab.explore contains these functions: ")
        print('================================================', "\n")
        for k in explore_info_dict:
            print("> ", k)

func_list_desc = ('''
A function to list all of the functions in the subpackage, with a description of them an optional argument
''')

func_list_params = ('''
> desc =False  ::  short for description, a True value will list function along with description and perameters
''') 

##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################

#list of all functions

explore_info_dict = {'dframe_ex(df, head_val=5, max_col=50)' : (dframe_ex_desc, dframe_ex_params),
                      'vcount_ex(df, print_count=5)' : (vcount_ex_desc, vcount_ex_params),
                      'missing_ex(df)' : (missing_ex_desc, missing_ex_params),
                      'corr_ex(df, min_corr=0.2, min_count=1, fig_size=(8,10), colors="Reds")' : (corr_ex_desc, corr_ex_params),
                      'func_list(desc=False)' : (func_list_desc, func_list_params),
                      }

##################################################################################################################