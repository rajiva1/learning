#!/usr/bin/python3

import numpy as np
import random
import time
import pandas as pd
import sqlite3
import datetime

# This program is intended to help kids practice with 3 types of math exercises:
#               - addition, subtraction, multiplication
# This version is hardcoded for certain names, 20 questions per exercise type
# and using SQLITE DataBase with pandas package (since it gives us a much faster
# way to create tables using DataFrame that can be written into DB).

#This version has better error handling by using 'try and except ValueError' within math


names = ['Rishik', 'Ria', 'Rajiv', 'Richa', 'Raghav', 'Aadya','Meher']
calculation = ['nil','addition','subtraction','multiplication']
a=b=z=0
maxT=minT=60
range1=5
range2=9

#let's keep on asking for the name until it is entered exactly as expected by using 'while true' and break
#only if matching name is entered, but not do the same in case of math type being not 1 or 2 or 3.

while True:
    name = input('Welcome, Enter your name: ')                      #input() always returns a string
    if name in names:
        math = input('\n Alright {}, Press 1 for Addition, 2 for Subtraction, 3 for Multiplication: '.format(name))
        if name == names[1]:                            # Ria needs to practice for smaller numbers for time being
            print('yeeeaah')
            range1 = 1
            range2 = 5
        break
    else:
        print('\t\n Please enter the name that is in the list\n')

# The below "if" statement was not really needed, but it existed before subtraction & multiplication logic were added
# and removing it later on would have required heck a lot of formatting work...so, just left it in there while adding
# the check for subtraction (2) and multiplication (3)

if int(math)==1 or 2 or 3 :                                          #input() returned a string, so convert into int
    print('\n' )
    startGameTime = time.time()
    for x in range(20):                                              # Number of questions is 20
        x1 = random.randint(range1,range2)
        y1 = random.randint(range1,range2)
        startTime = time.time()
        print('\n')

        if int(math)==1 :                                             # if addition is chosen
            z1 = x1 + y1
            while True:
                try:
                    z = int(input('{})  {} + {} = '.format(x + 1, x1, y1)))
                    break
                except ValueError:                                    # blank or alphabets not allowed, go back
                    print('Enter a valid number')

        elif int(math)==2 :                                           # if subtraction is chosen, check if x1 is bigger than y1
            if x1 >= y1 :
                z1 = x1 - y1
                while True:
                    try:
                        z = int(input('{})  {} - {} = '.format(x + 1, x1, y1)))
                        break                                        # if a valid integer is entered, then exit
                    except (ValueError):                             # blank or alphabets not allowed, go back
                        print('Please enter a valid number')

            elif y1 > x1 :
                z1 = y1 - x1
                while True:
                    try:
                        z = int(input('{})  {} - {} = '.format(x + 1, y1, x1)))
                        break
                    except ValueError:                              # blank or alphabets not allowed, go back
                        print('Please enter a valid number')

        elif int(math)==3 :                                           # if multiplication is chosen
            z1 = x1 * y1
            while True:
                try:
                    z = int(input('{}) {} x {} = '.format(x+1,x1,y1)))
                    break
                except ValueError:
                    print('Please enter a valid number')

        endTime = time.time()
        if (z == z1):                                                 # if correct answer
            a += 1
            TimeTaken = round((endTime - startTime),2)                #limit float to 2 decimal points
            print('\t\t Correct, {} seconds '.format(TimeTaken))
            if TimeTaken < minT:
                minT = TimeTaken
            else:
                maxT = TimeTaken
        else:                                                         # if incorrect answer
            b += 1
            print('\t\t Incorrect, Correct Answer is {}'.format(z1))
    endGameTime = time.time()
    Percent = format((a/(a+b))*100, '.2f')                                              #limit float to 2 decimal points
    if Percent == format(100,'.2f'):                                                    # if all correct
        print('############################\n')
        print('\t {}, You rock :-)'.format(name))
        print('\n\t Score = {}% ({} Correct and {} Incorrect) in total {} seconds)'.format(Percent,a,b,round(endGameTime-startGameTime)))
        print('############################\n')
    elif Percent == format(0,'.2f'):                                                    # if all incorrect
        print('############################\n')
        print('{},Is that really you? All Incorrect. :-( '
              'Score = {}% in Total {} seconds'.format(name,Percent, round(endGameTime-startGameTime)))
    else:                                                                               # if at least one incorrect
        print('############################\n')
        print('{}, YOU CAN DEFINITELY DO BETTER. Just need to Practice more'.format(name))
        print('############################\n')
        print('\t Your Score = {}% ({} Correct and {} Incorrect) in total {} seconds. '
              .format(Percent, a, b, round(endGameTime-startGameTime)))
    print('\t Your fastest time was {} sec & slowest time was {} sec'.format(minT,maxT))

    # store all the info in a pandas dataframe row, which can later be written into a SQL DB
    # Note that a list requires an index to be an integer, not a string, hence, int(math) is used with calculation

    df = pd.DataFrame([[name, 1, time.strftime("%c"), calculation[int(math)], a + b, Percent, minT, maxT, round(endGameTime - startGameTime)]],
          columns=['name', 'attempt', 'datetime', 'calculation', 'totalQ', 'score', 'bestTime', 'worstTime', 'TotalTime'])
    #print(df)
    #print(df.describe())

    # open sql database and check for the Math table to be present
    # find the last attempt number for a given user name and then replace it with the current one
    # write the pandas dataframe into the table

    with sqlite3.connect('kids-test.db') as conn:
        try:                                                                            # proceed if Math table existed in DB
            a = pd.read_sql('SELECT attempt from Math WHERE name=? AND calculation=?', conn, params=[name,calculation[int(math)]])
                                                                                        #Read all attempt values for a name and math type
            max_attempt = a.max()                                                       #find the last attempt number (also a max)
            a1 = max_attempt['attempt'] + 1                                             # increase it by one for current attempt #
            if a.empty:                                                                 # first timer would have nothing in SQL table
                a1 = 1                                                                  # first timer's first attempt
            df.attempt = df.attempt.replace(1, a1)                                      # replace 1 in the dataframe with current #
        except (RuntimeError, TypeError, NameError):
            print('Learn more about error handling here - https://docs.python.org/3/tutorial/errors.html')
        except:
            print('Oops, either DB didnt have Math table, or something went wrong in logic')
                                                                                        # write the dataframe into Math table
        df.to_sql('Math', conn, if_exists='append',index=False, index_label=['name','attempt','datetime','calculation','totalQ','score','bestTime','worstTime','TotalTime'])
else:
    print('sorry, you should have chosen 1 or 2 or 3. Try again' )
