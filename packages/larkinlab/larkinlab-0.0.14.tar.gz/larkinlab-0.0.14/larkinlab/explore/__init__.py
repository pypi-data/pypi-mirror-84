# Part of the 'explore' subpackage of 'larkinlab'
# functions for Exploratory Analysis
#
# v0.0.14
#
#twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
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
    # create function to explore a dataframe's shape and size quickly
    
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


##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################



##################################################################################################################