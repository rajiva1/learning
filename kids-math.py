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


names = ['Rname1','Rname2','Rname3','Rname4']
a=b=z=0
maxT=minT=60
range1=5
range2=20

#let's keep on asking for the name until it is entered exactly as expected by using 'while true' and break

while True:
    name = input('Welcome, Enter your name: ')
    if name in names:
        print('\n')
        math = input('Alright {}, Press 1 for Addition, 2 for Subtraction, 3 for Multiplication: '.format(name))
        if name == names[1]:            # Ria needs to practice for smaller numbers for time being
            print('yeeeaah')
            range1 = 1
            range2 = 5
        break
    else:
        print('\t\n Please enter the name that is in the list\n')

if int(math)==1 or 2 or 3 :                                                  #Remember, input() returns string, so convert into int
    startGameTime = time.time()
    for x in range(20):                                              # Number of questions is 20
        x1 = random.randint(range1,range2)
        y1 = random.randint(range1,range2)
        startTime = time.time()
        print('\n')

        if int(math)==1 :                                             # if addition is chosen
            z1 = x1 + y1
            while True:
                z = input('{})  {} + {} = '.format(x + 1, x1, y1))
                break
        elif int(math)==2 :                                           # if subtraction is chosen
            if x1 >= y1 :
                z1 = x1 - y1
                while True:
                    z = input('{})  {} - {} = '.format(x + 1, x1, y1))
                    break
            elif y1 > x1 :
                z1 = y1 - x1
                while True:
                    z = input('{})  {} - {} = '.format(x + 1, y1, x1))
                    break
        elif int(math)==3 :                                           # if multiplication is chosen
            z1 = x1 * y1
            while True:
                z = input('{}) {} x {} = '.format(x+1,x1,y1))
                break

        endTime = time.time()
        if ( int(z) == z1 ):                                                            #input() returns string, not int
            a += 1
            TimeTaken = round((endTime - startTime),2)                                  #limit float to 2 decimal points
            print('\t\t Correct, {} seconds '.format(TimeTaken))
            if TimeTaken < minT:
                minT = TimeTaken
            else:
                maxT = TimeTaken
        else:
            b += 1
            print('\t\t Incorrect, Correct Answer is {}'.format(z1))
    endGameTime = time.time()
    Percent = format((a/(a+b))*100, '.2f')                                              #limit float to 2 decimal points
    if Percent == format(100,'.2f'):
        print('############################\n')
        print('\t {}, You rock :-)'.format(name))
        print('\n\t Score = {}% ({} Correct and {} Incorrect) in total {} seconds)'.format(Percent,a,b,round(endGameTime-startGameTime)))
        print('############################\n')
    elif Percent == format(0,'.2f'):
        print('############################\n')
        print('{},Is that really you? All Incorrect. :-( '
              'Score = {}% in Total {} seconds'.format(name,Percent, round(endGameTime-startGameTime)))
    else:
        print('############################\n')
        print('{}, YOU CAN DEFINITELY DO BETTER'.format(name))
        print('\t Your Score = {}% ({} Correct and {} Incorrect) in total {} seconds. '
              .format(Percent, a, b, round(endGameTime-startGameTime)))
    print('\t Your fastest time was {} sec & slowest time was {} sec'.format(minT,maxT))
    df = pd.DataFrame([[name, 1, time.strftime("%c"), 'addition', a + b, Percent, minT, maxT, round(endGameTime - startGameTime)]],
          columns=['name', 'attempt', 'datetime', 'calculation', 'totalQ', 'score', 'bestTime', 'worstTime', 'TotalTime'])

    with sqlite3.connect('kids-test.db') as conn:
        try:
            a = pd.read_sql('SELECT attempt from Math WHERE name=?', conn, params=[name])       #Read the attempt column for a given name
            max_attempt = a.max()                                                               #find the last attempt number
            a1 = max_attempt['attempt'] + 1                                                     # increase it by one for current attempt
            if a.empty:                                                                         # first timer would have nothing in SQL table
                a1 = 1                                                                           # first timer's first attempt
            df.attempt = df.attempt.replace(1, a1)                                           # replace 1 in the dataframe with current
        except:
            print('Oops, DB didnt have the table, we just created it. lets hope this doesnt happen again')
       # df = pd.DataFrame([[name, a1, time.strftime("%c"), 'addition', a + b, Percent, minT, maxT, round(endGameTime - startGameTime)]], columns=['name', 'attempt', 'datetime', 'calculation', 'totalQ', 'score', 'bestTime', 'worstTime', 'TotalTime'])
       # print(df)
        df.to_sql('Math', conn, if_exists='append',index=False, index_label=['name','attempt','datetime','calculation','totalQ','score','bestTime','worstTime','TotalTime'])
else:
    print('sorry, you should have choosen 1 or 2 or 3. Try again' )
