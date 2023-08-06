# -*- coding: utf-8 -*-
"""

@author: eliott.kalfon

"""

import pandas as pd
import numpy as np

class GroupImputer():
    '''
    Class to be used as group null imputer - work in progress.
    The objective is to take a dataframe or array as input, and returning the
    same object, with null values imputed based on within group average/median
    (or custom function, to be applied to the array)
    '''
    def __init__(self, strategy = 'mean'):
        self.col_imputation_values = {}
        self.group_imputation_values = {}
        self.strategy = strategy
        self.groupby_column = None
        self.group_values = None
        self.imputed_columns = None
        self._impcol_isstring = None
        # Getting the imputation function based on user input
        if isinstance(self.strategy, str):
            if self.strategy.lower() == 'mean':
                self.imputation_function = lambda df: df.mean()
            elif self.strategy.lower() == 'median':
                self.imputation_function = lambda df: df.median()
            elif self.strategy.lower() == 'min':
                self.imputation_function = lambda df: df.min()
            elif self.strategy.lower() == 'max':
                self.imputation_function = lambda df: df.max()
            else:
                raise ValueError('Please enter a valid imputation strategy ("mean", "median", "min", "max")')   
        # Checks if imputation strategy is a function
        # The custom function must take a dataframe as argument and return either a series (for multiple columns) or a scalar (for single columns)
        elif callable(self.strategy):
            self.imputation_function = self.strategy
        else:
            raise ValueError('Please enter either a string ("mean", "median", "min", "max") or a custom function as an imputation strategy')
        
    def fit(self, data, groupby_column, imputed_columns):
        # Updating the groupy and imputed column attributes
        self.groupby_column = groupby_column
        self.imputed_columns = imputed_columns
        #Checking if the imputed columns input is a list
        self._impcol_isstring = isinstance(self.imputed_columns, str)
        # Getting the unique group values
        self.group_values = data[groupby_column].unique()
        # Creating a list of selected columns, composed of imputed and groupby columns
        if self._impcol_isstring:
            selected_columns = [self.imputed_columns] + [self.groupby_column]
        else:
            selected_columns = self.imputed_columns + [self.groupby_column]
        # Getting a dictionary of means by column/group
        self.group_imputation_values = self.imputation_function(df[selected_columns].groupby(by=self.groupby_column)).to_dict()
        # Getting a dictionary of means by column (used for imputation when a group is filled with NAs)
        if self._impcol_isstring:
            self.col_imputation_values = {self.imputed_columns:self.imputation_function(df[self.imputed_columns])}
        else:    
            self.col_imputation_values = self.imputation_function(df[self.imputed_columns]).to_dict()
        
    def impute_column(self, column_name, data):
        # Iteration over groups
        for group in self.group_values:
            # Imputation value selection
            # If the group mean is null, then use the column mean
            if self.group_imputation_values[column_name][group] == self.group_imputation_values[column_name][group]:
                imputation_value = self.group_imputation_values[column_name][group]
            else:
                imputation_value = self.col_imputation_values[column_name]
            # Filtering the data with pandas loc operator
            data.loc[
                # Filtering to a single group
                (data[self.groupby_column]==group) & 
                # Filtering to null values
                (data[column_name]!=data[column_name]),
                # Selecting the column
                column_name
            # Imputing the selection with the imputation value
            ] = imputation_value
        return data
    
    def transform(self, data):
        if self._impcol_isstring:
            data = self.impute_column(column_name = self.imputed_columns, data = data)
        else:
            # Iteration over columns to impute
            for imputed_column in self.imputed_columns:
                data = self.impute_column(column_name = imputed_column, data = data)
        return data
    
    def fit_transform(self,data,groupby_column,imputed_columns):
        self.fit(data,groupby_column,imputed_columns)
        self.transform(data)

