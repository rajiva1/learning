#!/usr/bin/python3

import numpy as np
import random
import datetime
import time
import pandas as pd
import sqlite3
import re

# This program is intended to help kids practice with 3 types of math exercises:
#               - addition, subtraction, multiplication
# This version is hardcoded for certain names, 20 questions per exercise type
# and using SQLITE DataBase with pandas package (since it gives us a much faster
# way to create tables using DataFrame that can be written into DB).

# ------changelog -------
# version 5 introduces 2 functions for testing and checking past performance for better reusuability
# version 5 also reminds how many tests already done today by a given user and prompts to continue until user says No
# version 4 limits the multiplication to focus on table for 2 or 3
# version 3 prints encouraging messages if the performance was 100% in 4 out of 6 last attempts
# version 2 has better error handling by using 'try and except ValueError' within math
# version 1 is for 20 math questions while keeping track of time taken to answer


names = ['R1', 'R2','R3','R4']
calculation = ['nil','addition','subtraction','multiplication']



def check_last_performance(name):
    """This function connects to the sql DB and reads the pertinent data from table for further analysis.
    If it is the first test of the day, then print encouraging messages only if 2 or more 100% were obtained
    per calculation in yesterday's performance. If it is not the first test of the day, then print how many tests
     left for the day.

     TODO - This function needs check the all the rows only for the last day instead of all 10 rows.
      """

    with sqlite3.connect('kids-test.db') as conn:
        try:                                                    #do all of the below unless any failure
            df2 = pd.read_sql('SELECT attempt, date, calculation, score, TotalTime from Math WHERE name=?', conn, params=[name], index_col='attempt')

            df2 = df2.tail(10)                                   #last 10 rows should have all of last time's performance
            #print(df2.loc[data['date'].str.contains('2018-03-17')])

            Todate = time.strftime("%Y-%m-%d")
            yesterdate = (pd.to_datetime('Today') - pd.Timedelta('1 days')).strftime("%Y-%m-%d")
            #print(type(yesterdate))                            #it should be string type, but let's check

            if all(df2.date != Todate):             #For first test today, date would match none of last 20 entries' dates
                #print(df2[0:2].values)                                 # print values of first 2 rows of dataframe
                if any(df2.date == yesterdate):
                    print("Great, I remember you finishing your math yesterday. Good job.")
                else:
                    print("Oh, {} I missed you yesterday. Please dont forget me again.".format(name))

                x=y=z=0

                for index, row in df2.iterrows():                           #iterrow() returns a series, let's check row by row
                    #print(row)
                    if row['calculation'] == calculation[1]:                #note that iterrow() doesnt preserve dtypes across rows
                        if row['score'] == "100.00":                        #100.00 is no longer an integer; see comment above
                            x = x + 1
                    elif row['calculation'] == calculation[2]:
                        if row['score'] == "100.00":
                            y = y + 1
                    elif row['calculation'] == calculation[3]:
                        if row['score'] == 100.00:
                            z = z + 1
                if x >= 2 or y >=2 or z >=2:
                    print("###########################################")
                    print("{}, You rocked with 100% score last time. Very impressive. ".format(name))
                    print("###########################################")
                    print("Ready to rock again?")
                else:
                    print("###########################################")
                    print("{}, You gotta score 100% in at least 2 tests today. You ready?".format(name))
                    print("###########################################")
            else:                                                       #if it is not the first test of the day, then
                add_test_no = len(df2[(df2['date'] == Todate) & (df2['calculation'] == 'addition')])
                sub_test_no = len(df2.loc[(df2['date'] == Todate) & (df2['calculation'] == 'subtraction')])    #this also works
                mul_test_no = len(df2[(df2['date'] == Todate) & (df2['calculation'] == 'addition')])

                print("{}, Good that you want to continue. So far, You have finished,".format(name))
                print("\t {} of 3 additions,".format(add_test_no))
                print("\t {} of 3 substractions,".format(sub_test_no))
                print("\t {} of 3 multiplications,".format(mul_test_no))
                if add_test_no == 3 and sub_test_no == 3 and mul_test_no ==3:
                    print("You are done already. Have fun.")
                else:
                    print("You need to finish up quickly.")



        except (RuntimeError, TypeError, NameError):
            print('Learn more about error handling here - https://docs.python.org/3/tutorial/errors.html')
        except:
            print('Oops, DB didnt have Math table, or table didnt have a column, or something went wrong in logic')


def math_test(name):
    # Ask to select math type
    math = input('\n Alright {}, Press 1 for Addition, 2 for Subtraction, 3 for Multiplication: '.format(name))

    a = b = z = 0
    maxT = minT = 60
    range1 = 2
    range2 = 17

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
            x1 = random.randint(2, 3)                                 # let's focus on table of 2 or 3
            y1 = random.randint(0, 11)

            z1 = x1 * y1
            while True:
                try:
                    z = int(input('{}) {} x {} = '.format(x+1,x1,y1)))
                    break
                except ValueError:
                    print('Please enter a valid number')

        else:
            print('sorry, you should have chosen 1 or 2 or 3. Try again')
            exit()

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

    df = pd.DataFrame([[name, 1, time.strftime("%Y-%m-%d"), time.strftime("%X"), calculation[int(math)], a + b, Percent, minT, maxT, round(endGameTime - startGameTime)]],
          columns=['name', 'attempt', 'date', 'time', 'calculation', 'totalQ', 'score', 'bestTime', 'worstTime', 'TotalTime'])
    #print(df)
    #print(df.describe())                                                               #prints std,50% values

    # open sql database and check for the Math table to be present
    # find the last attempt number for a given user name and then replace it with the current one
    # write the pandas dataframe into the table

    with sqlite3.connect('kids-test.db') as conn:
        try:                                                                            # proceed if Math table existed in DB
            a = pd.read_sql('SELECT attempt from Math WHERE name=? AND calculation=?', conn, params=[name,calculation[int(math)]])
                                                                                        #Read all attempt values for a name and math type
            last_attempt = a.max()                                                      #find the last attempt number, which should be the max)
            a1 = last_attempt['attempt'] + 1                                            # increase it by one for current attempt #
            if a.empty:                                                                 # first timer would have nothing in SQL table
                a1 = 1                                                                  # first timer's first attempt
            df.attempt = df.attempt.replace(1, a1)                                      # replace 1 in the dataframe with current #
        except (RuntimeError, TypeError, NameError):
            print('Learn more about error handling here - https://docs.python.org/3/tutorial/errors.html')
        except:
            print('Oops, either DB didnt have Math table, or something went wrong in logic')
                                                                                        # write the dataframe into Math table
        df.to_sql('Math', conn, if_exists='append',index=False, index_label=['name','attempt','date', 'time','calculation','totalQ','score','bestTime','worstTime','TotalTime'])


#keep on asking for the name until it is entered exactly as expected by using 'while true' and break
#only if matching name is entered, but not do the same in case of math type being not 1 or 2 or 3.

while True:
    name = input('Welcome, Enter your name: ')                      #input() always returns a string

    #progress only if name is already in the list
    if name in names:

        if name == names[1]:  # If one needs to practice for smaller numbers
            # print('{}, You did great yesterday..'.format(name))
            range1 = 1
            range2 = 8

        # Let's find out about the last performance per calculation and encourage before test starts
        while True:
            check_last_performance(name)
            math_test(name)
            ans = input('\n{}, Do you want to continue (y/n): '.format(name))
            if ans != 'y':
                break

        break                                                       # to come out of if loop
    else:
        print('\t\n Please enter the name that is in the list\n')
