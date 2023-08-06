import pandas as pd
import numpy as np

from scipy import stats

import matplotlib.pyplot as plt
import seaborn as sns
import joypy as joypy

from copy import deepcopy

try:
    from automated_pricing_flow.standard_functions import *
except:
    from standard_functions import *
    

def plot_with_vs_without_outliers(df_without, df_with, df_without_length, df_full_length, columns=None, save=True, prefix_name_fig='ibnr'):
    """
        Helps to see at which values are located the outliers
        Arguments --> df without outliers, df with outliers, the lenght of the two df
                        and the list of features (or the name for only one feature)
        Returns --> line plots with overlapped lines showing feature values with and without outliers
    """

    def plot_line(column):
        fix, ax = plt.subplots()
        ax.plot(df_with.index, column, data=df_with, color='orange', label='With outliers')
        ax.plot(df_without.index, column, data=df_without, label='Outliers removed')

        legend = ax.legend(loc='upper right', shadow=True)

        column = remove_words(column, feature=('feature', ''), bins=('bins', ''), underscore=('_', ' '))
        plt.ylabel(column)
        plt.show()

        if save == True:
            plt.savefig('charts/' + prefix_name_fig + '_' + column + '.png')

    plot_columns = [columns] if isinstance(columns, str) == True else columns

    for column in plot_columns:
        plot_line(column)
        
        

def plot_scatter_charts(df, features, target_column=None, height=5, save=True, prefix_name_fig='scatter'):
    """
        Plots a scatter plot between the target column and the features
        Arguments --> the df, the dependant variable, the features,
                    the figure size, and the indication to save or not and with which prefix
    """

    new_features = [features] if isinstance(features, str) == True else features

    if target_column is None:
        for i,j,v in features:
            sns.pairplot(df, height=6, x_vars=i, y_vars=j)
            plt.savefig('charts/' + prefix_name_fig + '_' + '.png')

    else:
        for feature in new_features:
            feature_name = remove_words(feature, feature=('feature', ''), bins=('bins', ''), underscore=('_', ' '))
            new_df = df.rename(columns={feature: feature_name})

            sns.pairplot(new_df, height=height, x_vars=feature_name, y_vars=target_column)

            if save == True:
                plt.savefig('charts/' + prefix_name_fig + '_' + feature_name + '.png')

                

def plot_text_bars_chars(df, target_column, columns=None, figsize=(14,14), save=True, prefix_name_fig='diverging_bars'):
    """
        Plots the target column variance mean values depending on the features
        Arguments --> the df, the dependant variable, the features,
                    the number of charts to display side by side, the figure size, and the indication to save or not and with which prefix
    """

    plot_columns = [columns] if isinstance(columns, str) == True else deepcopy(columns)
    target_column_name = remove_words(target_column, feature=('feature', ''), bins=('bins', ''), underscore=('_', ' '))

    for column in plot_columns:

        column_name = remove_words(column, feature=('feature', ''), bins=('bins', ''), underscore=('_', ' '))

        new_df = df.groupby(column)[target_column].mean().to_frame()
        new_df['z_score'] = stats.zscore(new_df[target_column])
        new_df = new_df.sort_values('z_score')
        new_df = new_df.reset_index()
        colors = ['red' if x < 0 else 'green' for x in new_df['z_score']]

        plt.figure(figsize=figsize)
        plt.hlines(y=new_df.index, xmin=0, xmax=new_df['z_score'], color=colors)

        for x, y, value_text in zip(new_df['z_score'], new_df.index, new_df['z_score']):
            t = plt.text(x, y, round(value_text, 2), horizontalalignment='right' if x < 0 else 'left',
                         verticalalignment='center', fontdict={'color':'red' if x < 0 else 'green', 'size':14})

        plt.yticks(new_df.index, new_df[column], fontsize=12)
        plt.title('Diverging Text Bars of {0} by {1}'.format(target_column_name, column_name), fontdict={'size':20})
        plt.grid(linestyle='--', alpha=0.5)
        plt.xlim(-2.5, 2.5)
        plt.show()

        if save == True:
            plt.savefig('charts/' + prefix_name_fig + '_' + column_name + '.png')

            

def plot_joypy_charts(df, target_column, transformer=None, columns=None, n_cols=1, figsize=(16, 10), save=True, prefix_name_fig='joypy'):
    """
        Plots in a fashion and easy way the target variable distributions depending on the features
        Arguments --> the df, the dependant variable, the target variable transformer (e.g. a log normal transformation),
                    the features, the number of charts to display side by side, the figure size, and the indication to save or not and with which prefix
    """

    new_df = deepcopy(df)
    num_columns = [columns] if isinstance(columns, str) == True else deepcopy(columns)

    if transformer is not None:
        new_df[target_column] = transformer.transform(new_df[target_column])

    plot_expression = "joypy.joyplot(df, column=target_column, by=variable, ylim='own', ax=ax[j] if n_cols > 1 else ax)"
    title="ax.set_title('Joy Plot of {0} by {1}'.format(target_column, variable), fontsize=22)"

    run_multiple_plots(new_df, plot_expression, target_column, list_variables=num_columns, n_cols=n_cols, figsize=figsize, save=save, prefix_name_fig=prefix_name_fig, title=title)

    

def plot_bar_line_charts(df, columns=None, target_columns={'barplot': None, 'lineplot': None}, agg_func={'barplot': 'sum', 'lineplot': 'mean'}, sort=False, figsize=(10,6), save=True, prefix_name_fig='bar_line'):
    """
        Combines in a same chart a bar and a line plot. Useful to compare volume vs average by feature
        Aruments --> the df, the target column we are looking at, the columns to loop through and perform mean/sum aggregation,
                    a dict indication which aggregation functio to do for lineplot and barplot
    """

    def get_right_interval(x):
        right = x
        try:
            right = '<' + str(int(x.right))
        except:
            pass
        return '<' + right

    new_df = deepcopy(df)
    dict_agg = {'sum': np.sum, 'mean': np.mean}
    plot_columns = [columns] if isinstance(columns, str) == True else deepcopy(columns)
    barplot_target_column = target_columns['barplot']
    lineplot_target_column = target_columns['lineplot']

    for column in plot_columns:

        column_name = remove_words(column, feature=('feature', ''), bins=('bins', ''), underscore=('_', ' '))

        fig, ax1 = plt.subplots(figsize=figsize)
        color = 'tab:green'
        ax1 = sns.barplot(x=column, y=barplot_target_column, data=new_df, estimator=dict_agg[agg_func['barplot']], palette='summer')
        title_column = barplot_target_column.replace('asif_', '') + (' ' + lineplot_target_column.replace('asif_', '') if lineplot_target_column != barplot_target_column else '')
        ax1.set_title(title_column + ' ' + 'by' + ' ' + column_name, fontsize=16)
        ax1.set_xlabel(column_name, fontsize=16)
        ax1.set_ylabel(barplot_target_column.replace('asif_', '') + ' ' + agg_func['barplot'], fontsize=16, color=color)
        ax1.tick_params(axis='y')

        ax2 = ax1.twinx()
        color = 'tab:red'

        if '_bins' in column:
            new_df[column] = new_df[column].map(get_right_interval)

        ax2 = sns.lineplot(x=column, y=lineplot_target_column, data=new_df, sort=sort, estimator=dict_agg[agg_func['lineplot']], err_style='bars', color=color)
        ax2.set_ylabel(lineplot_target_column.replace('asif_', '') + ' ' + agg_func['lineplot'], fontsize=16, color=color)
        ax2.tick_params(axis='y', color=color)
        plt.show()

        if save == True:
            plt.savefig('charts/' + prefix_name_fig + '_' + column_name + '.png')

            

def plot_pie_charts(df, columns=None, agg_func='count', absolute_figures=True, percentages=True, currency='€', save=True, prefix_name_fig='pie'):
    """
        Plots pie charts for the specified columns, based on a specified aggregation operation, and indicates the absolute figures + proportion if they are set to True
    """

    def func(pct, allvals):
        absolute = "({0:,d}{1})".format(int(pct/100.*np.sum(allvals)), currency if currency is not None else '') if absolute_figures == True else ''
        pct = "{:.1f}%".format(pct) if percentages == True else ''
        return pct + ' ' + absolute

    plot_columns = [columns] if isinstance(columns, str) == True else deepcopy(columns)

    n_cols = 2
    n_rows = len(plot_columns) // n_cols + len(plot_columns) % n_cols

    for i in range(n_rows):
        fig, ax = plt.subplots(nrows=1, ncols=n_cols, figsize=(12, 7), subplot_kw=dict(aspect="equal"), dpi= 80)

        for j in range(n_cols):

            if i*n_cols+j < len(plot_columns):
                variable = plot_columns[i*n_cols+j]

                df_pie = df.groupby(variable).agg(agg_func).reset_index()
                data = df_pie[df_pie.columns[1]]
                categories = df_pie[variable]

                wedges, texts, autotexts = ax[j].pie(data, autopct=lambda pct: func(pct, data), textprops=dict(color="w"),colors=plt.cm.Dark2.colors, startangle=140)

                if 'feature' in variable:
                    feature_name = remove_words(variable, feature=('feature', ''), bins=('bins', ''), underscore=('_', ' '))
                    variable = feature_name

                ax[j].legend(wedges, categories, title=variable, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
                plt.setp(autotexts, size=10, weight=700)
                ax[j].set_title(variable + " : Pie Chart")

                if save == True:
                    plt.savefig('charts/' + prefix_name_fig + '_' + variable + '.png')

            else:
                fig.delaxes(ax[j])

                

def plot_violin_charts(df, target_column, transformer=None, columns=None, n_cols=2, figsize=(8, 5), save=False, prefix_name_fig='violin'):
    """
        Plots target variable distribution depending on the features specified in arguments
        Arguments --> the df, the dependant variable, the target variable transformer (e.g. a log normal transformation),
                the features, the number of charts to display side by side, the figure size, and the indication to save or not and with which prefix
    """

    new_df = deepcopy(df)
    num_columns = None if columns is None else [columns] if isinstance(columns, str) == True else deepcopy(columns)

    if transformer is not None:
        new_df[target_column] = transformer.transform(new_df[target_column])

    if num_columns is None:
        plot_expression = "sns.violinplot(x=target_column, data=df)"
        title="ax.set_title(target_column + ' distribution')"
    else:
        plot_expression = "sns.violinplot(x=target_column, y=variable, data=df, ax=ax[j] if n_cols > 1 else ax)"
        title="ax.set_title(target_column + ' distribution by {}'.format(variable))"

    run_multiple_plots(new_df, plot_expression, target_column, list_variables=num_columns, n_cols=n_cols, figsize=figsize, save=save, prefix_name_fig=prefix_name_fig, title=title)

    

def plot_hist_charts(df, columns=None, transformer=None, n_cols=2, figsize=(8, 5), save=False, prefix_name_fig='histo'):
    """
        Plots histograms of the values of the columns specified in the arguments
        Arguments --> the df, the variables to plot, thee transformer to use (e.g. a log normal transformation),
                    the number of charts to display side by side, the figure size, and the indication to save or not and with which prefix
    """

    new_df = deepcopy(df)
    num_columns = [columns] if isinstance(columns, str) == True else deepcopy(columns)

    if transformer is not None:
        new_df[num_columns] = transformer.transform(new_df[num_columns])

    plot_expression = "sns.distplot(df[variable], ax=ax[j] if n_cols > 1 else ax)"
    run_multiple_plots(new_df, plot_expression, list_variables=num_columns, n_cols=n_cols, figsize=figsize, save=save, prefix_name_fig=prefix_name_fig)

    

def plot_count_charts(df, columns=None, n_cols=2, figsize=(8, 5), save=False, prefix_name_fig='count'):
    """
        Plots distribution for categorical columns
        Arguments --> the df, the variables to plot,
                    the number of charts to display side by side, the figure size, and the indication to save or not and with which prefix
    """

    new_df = deepcopy(df)
    num_columns = [columns] if isinstance(columns, str) == True else deepcopy(columns)
    plot_expression = "sns.countplot(x=variable, data=df, ax=ax[j] if n_cols > 1 else ax)"
    run_multiple_plots(new_df, plot_expression, list_variables=num_columns, n_cols=n_cols, figsize=figsize, save=save, prefix_name_fig=prefix_name_fig)

    

def plot_line_charts(df, target_column, transformer=None, num_features=None, cat_features=None, n_cols=2, figsize=(8, 5), save=False, prefix_name_fig='line'):
    """
        Plots either a line curve for continous features or a bar plot for categorical features for the target column depending on the features
        Arguments --> the df, the dependant variable, the target variable transformer (e.g. a log normal transformation),
                    the numerical and categorical features,
                    the number of charts to display side by side, the figure size, and the indication to save or not and with which prefix
    """

    new_df = deepcopy(df)
    num_columns = new_df.select_dtypes(include='number').columns
    new_num_features = [num_features] if isinstance(num_features, str) == True else deepcopy(num_features)
    cat_new_features = [cat_features] if isinstance(cat_features, str) == True else deepcopy(cat_features)

    if transformer is not None:
        new_df[target_column] = transformer.transform(new_df[target_column])

    lineplot_plot_expression = "sns.lineplot(x=variable, y=target_column, data=df[columns_graph], ax=ax[j] if n_cols > 1 else ax)"
    barplot_expression = "sns.barplot(x=variable, y=target_column, data=df[columns_graph], ax=ax[j] if n_cols > 1 else ax)"

    run_multiple_plots(new_df, lineplot_plot_expression, target_column, new_num_features, n_cols=n_cols, figsize=figsize, save=save, prefix_name_fig='lineplot')
    run_multiple_plots(new_df, barplot_expression, target_column, cat_new_features, n_cols=n_cols, figsize=figsize, save=save, prefix_name_fig='barplot')

    

def plot_bar_by_charts(df, target_column, columns=None, agg_func='mean', n_cols=2, figsize=(8, 5), save=False, prefix_name_fig='bar'):
    """
        Makes bar plot of the features specified by the user as list, or as name if only one feature
    """

    new_df = deepcopy(df)
    num_columns = [columns] if isinstance(columns, str) == True else deepcopy(columns)
    plot_expression = "sns.barplot(x=variable, y=target_column, data=df, estimator=agg_func_eval, ax=ax[j] if n_cols > 1 else ax)"
    run_multiple_plots(new_df, plot_expression, target_column, list_variables=num_columns, agg_func=agg_func, n_cols=n_cols, figsize=figsize, save=save, prefix_name_fig=prefix_name_fig)

    

def run_multiple_plots(df, plot_expression, target_column=None, list_variables=None, group_by=False, agg_func=None, n_cols=None, figsize=(8, 5), save=False, prefix_name_fig=None, **kwargs):
    """
        Plots multiple charts
        Arguments --> the df, the expression that will be evaluated to plot the right chart,
                    the target column (y axis), the variables (x axis), a boolean indicating if a aggregation must be done,
                    the aggregation function, the number of axes for the plot, the figure size, if it will be saved and with which prefix name
    """

    df_backup = deepcopy(df)

    if target_column is None and list_variables is None:
        return

    target_column, agg_func, prefix_name_fig = target_column if target_column is not None else '', agg_func if agg_func is not None else '', prefix_name_fig if prefix_name_fig is not None else ''
    agg_func_eval = np.sum if agg_func == 'sum' else np.mean

    if list_variables is None and isinstance(target_column, str) == True:
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=figsize)
        variable = None
        
        target_column_name = remove_words(target_column, underscore=('_', ' '))
        df = df.rename(columns={target_column: target_column_name})
        
        target_column = target_column_name
        columns_graph = [target_column]
        
        eval(plot_expression)

        if save == True:
            plt.savefig('charts/' + prefix_name_fig + '_' + agg_func + '_' + target_column + '.png')

        return

    n_rows = len(list_variables) // n_cols + len(list_variables) % n_cols

    for i in range(n_rows):
        fig, ax = plt.subplots(nrows=1, ncols=n_cols, figsize=figsize)

        for j in range(n_cols):

            if i*n_cols+j < len(list_variables):
                variable = list_variables[i*n_cols+j]
                variable_name = remove_words(variable, feature=('feature_', ''), bins=('_bins', ''), underscore=('_', ' '))

                if isinstance(df, dict) == True:
                    df = df[variable].reset_index()
                else:
                    df = df.rename(columns={variable: variable_name})
                    variable = variable_name

                if group_by == True:
                    df = df.groupby(variable)[target_column].agg(agg_func).reset_index()

                columns_graph = [variable] + ([target_column] if isinstance(target_column, str) == True else target_column)

                if 'ax=' not in plot_expression and 'ax[j]=' not in plot_expression:
                    if n_cols == 1:
                        ax = eval(plot_expression)
                    else:
                        ax[j] = eval(plot_expression)
                else:
                    eval(plot_expression)

                df = deepcopy(df_backup)

                if 'title' in kwargs.keys():
                    eval(kwargs['title'])

                if n_cols == 1 and hasattr(ax, 'set_xlabel') == True:
                    ax.set_xlabel(variable)
                elif n_cols > 1 and hasattr(ax[j], 'set_xlabel') == True:
                    ax[j].set_xlabel(variable)

                if save == True:
                    plt.savefig('charts/' + prefix_name_fig + '_' + agg_func + '_' + variable + '_' + (target_column if isinstance(target_column, str) == True else '') + '.png')

            elif n_cols > 1:
                fig.delaxes(ax[j])
                
                

def plot_unique_values(df):
    """
        Displays histogram with number of values in x-axis and number of features concerned on y-axis
    """

    if len(df) >0:
        fig, ax = plt.subplots(1, 1)

        fig.set_size_inches(16,5)

        ax.hist(df.number_of_uniques, bins=50)
        ax.set_title('Number of features with X unique values')
        ax.set_xlabel('Distinct values')
        ax.set_ylabel('Features')