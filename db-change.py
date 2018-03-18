#!/usr/bin/python3

import numpy as np
import random
import datetime
import time
import pandas as pd
import sqlite3
import re

#This program converts the datetime values in a column in an existing SQL table into two separate columns date & time
#values with a different date format (old format = Fri Dec  1 20:54:49 2017; new format = 2017-12-01 20:54:49)
#This program should be needed only once (if migrating from kids-test.py v2 to v3)

#This version v1 avoids needing to use time.strftime("%x") or datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")

with sqlite3.connect('kids-test.db') as conn:
    try:
        df2 = pd.read_sql('SELECT * from Math', conn)

        #let's make sure that the datetime column exists and date column doesn't exist before proceeding
        if 'datetime' not in df2.columns and 'date' in df2.columns:
            print('Forget it, there is no datetime column to convert, since it was already done before. see below...')
            print(df2.tail(1))

        else:
            print('There are {} rows in table. see last row of original table below...'.format(len(df2.index)))
            print(df2.tail(1))
            print('===========starting conversion ============')

            #convert existing timedate column values from %c to %x format and convert the object type to string for split to work
            df2['datetime'] = pd.to_datetime(df2['datetime'])
            df2['datetime'] = df2['datetime'].astype('str')

            #Now, divide datetime column into 2 columns - date and time (dtype = string now)
            df2['date'], df2['time'] = zip(*df2['datetime'].apply(lambda x: x.split(' ', 1)))
            #df2['date'] = df2['datetime'].map(lambda x:str(x)[0:-14])


            #Let's get rid of datetime column and move date & time columns from end to after attempt column
            df2.drop('datetime', axis=1, inplace=True)
            df2 = df2[['name','attempt','date', 'time','calculation','totalQ','score','bestTime','worstTime','TotalTime']]

            #replace the SQL table content with the new dataframe
            df2.to_sql('Math', conn, if_exists='replace')

            #Let's see the last row to confirm the conversion
            print('There are {} rows in table. see last row of updated table below...'.format(len(df2.index)))
            print(df2.tail(1))

    except (RuntimeError, TypeError, NameError):
        print('Learn more about error handling here - https://docs.python.org/3/tutorial/errors.html')
    except:
        print('Oops, either DB didnt have Math table, or table did not have a column, or something went wrong in logic')

