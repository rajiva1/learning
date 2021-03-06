#!/usr/bin/python3

import numpy as np
import random
import time
from datetime import datetime, timedelta
from pytz import timezone
import pandas as pd
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

"""
This program is intended to help kids/adults practice with 4 types of math exercises:
               - addition, subtraction, multiplication and division
And store kids/adults scores for assessment. It also sends an email when the activity is completed and prints
messages like the below to keep the student aware of the progress:

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
XYZ, So far, You have finished::
	 1 of 3 additions with 100% score in 1 of them,
	 0 of 3 subtractions with 100% score in 0 of them,
	 0 of 3 multiplications with 100% score in 0 of them,
	 0 of 3 divisions with 100% score in 0 of them,
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You are doing great. Now, quickly finish 3 or more of each with 100% score.


This version is hardcoded for certain student names, 10 questions per test per exercise type, and
using SQLITE DataBase with pandas package (since it gives us a much faster way to create tables
using DataFrame that can be written into DataBase). 

However, if you intend to use it, then update the names, num_of_questions and mail settings. Look for "Note".

"""

# ------changelog -------
# v13 increased math levels for certain users (3 digits add/substraction)
# v12 Fixed email issue, also calculating total time from start to finish and put it in email subject itself
# v11 includes sending a mail/text message once 3 of each math type completed with score details in email body
# v10 properly includes the division (though v9 had added it unofficially and incorrectly)
# v9 adjusts the date & time to Eastern timezone even if server time is set to another timezone
# v8 enhances check_last_performance function to show score per attempt, if 100%
# v7 fixes the second bug that occurred due to a copy paste error for counting multiplication tests
# v6 fixes the very first bug that occurred due to functions that got introduced in v5
# v5 introduces 2 functions for testing and checking past performance for better reusuability
# v5 also reminds how many tests already done today by a given user and prompts to continue until user says No
# v4 limits the multiplication to focus on table for 2 or 3
# v3 prints encouraging messages if the performance was 100% in 4 out of 6 last attempts
# v2 has better error handling by using 'try and except ValueError' within math
# v1 is for 20 math questions while keeping track of time taken to answer

print("\t.....Welcome to Version 13.....\n")

""" Note: If you downloaded this from github, then Enter the list of names you would like  """
names = ['X1', 'X2', 'X3']
calculation = ['nil','addition','subtraction','multiplication', 'division']
num_of_questions = 10

def send_emails(name, body, totalQ, duration_min):
    """This function sends an email once the exercises are completed
    Flag is set to 1 only if $name had scored 100% in 2 or more them
    body would have math score breakdown per math calculation type
    """
    fromaddr = "xyz1@xyz.com"
    list = "xyz1@xyz.com", "xyz2@xyz.com"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    #msg['To'] = toaddr
    msg['Subject'] = "{} finished math; {} questions in {} minutes".format(name, totalQ, duration_min)
    #body = "{} finished math".format(name)
    msg.attach(MIMEText(body, 'plain'))
    text = msg.as_string()

    """ Note:If you downloaded this program from git, then change xyz to valid server, username and password """
    server = smtplib.SMTP('mail.xyz.com', 587)
    server.starttls()
    server.login('login','password')
    for toaddr in (list):                                           #need to send email one by one due to a smtplib issue
        server.sendmail(fromaddr, toaddr, text)
    server.quit()


def check_last_performance(name):
    """This function connects to the sql DB and reads the pertinent data from table for further analysis.
    If it is the first test of the day, then print encouraging messages only if 2 or more 100% were obtained
    per calculation in yesterday's performance. If it is not the first test of the day, then print how many tests
     left for the day.

     TODO - This function should check all the rows only for the last day instead of last 20 rows.
     TODO - This should be a function that returns useful info (instead of a procedure, which returns nothing)
      """
    x1 = x2 = x3 = y1 = y2 = y3 = z1 = z2 = z3 = zz1 = zz2 = zz3 = 0

    with sqlite3.connect('kids-test.db') as conn:
        """do all of the below (under try clause) unless any failure"""

        try:

            df2 = pd.read_sql('SELECT attempt, date, calculation, score, TotalTime from Math WHERE name=?', conn, params=[name], index_col='attempt')

            df2 = df2.tail(20)                                   #last 20 rows should have all of last time's performance
            #print(df2.loc[data['date'].str.contains('2018-03-17')])    # check if there is any row for a particular date

            # if the server date/time is not in Eastern timezone (value 18000), then convert it
            if time.timezone != 18000:
                now_utc = datetime.now(timezone('UTC'))
                now_ET = now_utc.astimezone(timezone('US/Eastern'))
                yesterday_utc = datetime.now(timezone('UTC')) - timedelta(days=1)
                yesterday_ET = yesterday_utc.astimezone(timezone('US/Eastern'))
                Todate = now_ET.strftime("%Y-%m-%d")
                yesterdate = yesterday_ET.strftime("%Y-%m-%d")
            else:
                Todate = time.strftime("%Y-%m-%d")
                yesterdate = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

            #print(type(yesterdate))                                #it should be string type, but let's check

            for index, row in df2.iterrows():                       # iterrow() returns a series, let's check row by row
                if row['calculation'] == calculation[1]:            # note that iterrow() doesnt preserve dtypes across rows
                    if row['score'] == "100.00":                    # 100.00 is no longer an integer; see comment above
                        if row['date'] == Todate:
                            x1 = x1 + 1
                        elif row['date'] == yesterdate:
                            x2 = x2 + 1
                        else:
                            x3 = x3 + 1
                elif row['calculation'] == calculation[2]:
                    if row['score'] == "100.00":
                        if row['date'] == Todate:
                            y1 = y1 + 1
                        elif row['date'] == yesterdate:
                            y2 = y2 + 1
                        else:
                            y3 = y3 + 1
                elif row['calculation'] == calculation[3]:
                    if row['score'] == "100.00":
                        if row['date'] == Todate:
                            z1 = z1 + 1
                        elif row['date'] == yesterdate:
                            z2 = z2 + 1
                        else:
                            z3 = z3 + 1
                elif row['calculation'] == calculation[4]:
                    if row['score'] == "100.00":
                        if row['date'] == Todate:
                            zz1 = zz1 + 1
                        elif row['date'] == yesterdate:
                            zz2 = zz2 + 1
                        else:
                            zz3 = zz3 + 1
                else:
                    print("OUT")

            if all(df2.date != Todate):             #For first test today, Today's date would match none of last 20 entries' dates
                #print(df2[0:2].values)                                 # print values of first 2 rows of dataframe
                if any(df2.date == yesterdate):
                    print("\n {}, I remember you finishing all of your math yesterday. Welcome back.".format(name))
                    if x2 >= 2 and y2 >= 2 or z2 >= 2 or zz2 >= 2:
                        print("##########################################################")
                        print("And You rocked with 100% score yesterday. Very impressive, {}.".format(name))
                        print("############################################################")
                        print("Ready to rock again?")
                        return(1,0,0,0)
                    else:
                        print("###########################################")
                        print("{}, You were close to rocking with 100% score yesterday. You gotta rock today. You ready?".format(name))
                        print("###########################################")
                        return(0,0,0,0)


                else:
                    print("Oh, {} I missed you yesterday. Please dont forget me again.".format(name))
                    print("###########################################################")
                    return(0,0,0,0)

            else:                                                       #if it is not the first test of the day, then find test taken so far
                #count number of rows that match test type e.g. addition and that match today's date, match on date first to minimize

                add_test_no = len(df2[(df2['date'] == Todate) & (df2['calculation'] == 'addition')])
                sub_test_no = len(df2.loc[(df2['date'] == Todate) & (df2['calculation'] == 'subtraction')])    #this also works
                mul_test_no = len(df2[(df2['date'] == Todate) & (df2['calculation'] == 'multiplication')])
                div_test_no = len(df2[(df2['date'] == Todate) & (df2['calculation'] == 'division')])

                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("{}, So far, You have finished::".format(name))
                print("\t {} of 3 additions with 100% score in {} of them,".format(add_test_no, x1))
                print("\t {} of 3 subtractions with 100% score in {} of them,".format(sub_test_no, y1))
                print("\t {} of 3 multiplications with 100% score in {} of them,".format(mul_test_no, z1))
                print("\t {} of 3 divisions with 100% score in {} of them,".format(div_test_no, zz1))
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

                if name == names[1]:
                    if add_test_no >= 3 and sub_test_no >= 3 and mul_test_no >= 3:
                        print("{}, You are done with 3 of each. Did you rock in at least 3 of them?".format(name))
                        print("\tIf yes, then quit and do something else and be Happy :-).")
                        print("\tIf No, then you may please continue to finish and remember to rock :-).")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        TotalQ = (add_test_no + sub_test_no + mul_test_no) * 10
                        email_body = "\n{} additions with 100% score in {} of them," \
                               "\n{} subtractions with 100% score in {} of them," \
                               "\n{} multiplications with 100% score in {} of them,".format(add_test_no, x1, sub_test_no, y1,mul_test_no, z1)
                        return (1,1,email_body, TotalQ)
                else:
                    if add_test_no >= 3 and sub_test_no >= 3 and mul_test_no >= 3 and div_test_no >= 3:
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        print("{}, You are done with 3 of each. Did you get 100% in at least 3 of them?".format(name))
                        print("\tIf yes, then quit and do something else and be Happy :-).")
                        print("\tIf No, then you may please continue to finish and remember to rock :-).")
                        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                        TotalQ = (add_test_no + sub_test_no + mul_test_no + div_test_no) * 10
                        email_body = "\n{} additions with 100% score in {} of them," \
                               "\n{} subtractions with 100% score in {} of them," \
                               "\n{} multiplications with 100% score in {} of them" \
                               "\n{} divisions with 100% score in {} of them,".format(add_test_no, x1, sub_test_no, y1, mul_test_no, z1, div_test_no, zz1)

                        return(1,1,email_body, TotalQ)

                print("You are doing great. Now, quickly finish 3 or more of each with 100% score.")
                return(0,0,0,0)


        except (RuntimeError, TypeError, NameError):
            print('Something gone wrong with last_check_performance')
            print('Learn more about error handling here - https://docs.python.org/3/tutorial/errors.html')
        except:
            print('Oops, DB didnt have Math table, or table didnt have a column, or something went wrong in logic')



def math_test(name, flag):
    """
    This function lets the student pick a specific calculation type, and then takes two random numbers from two separate
    ranges (hardcoded) and presents them to the student to answer. Also, hardcoded is the number of questions.
    It then compares the answer
    """
    a = b = z = 0
    maxT = minT = 60

    if name == names[1]:   #If one needs to practice for smaller numbers, then change the range in this if clause
        range1 = 1
        range2 = 20
        range3 = 3         #this is for multiplication and division
        print('{}, you may skip division for now'.format(names[1]))
    else:
        range1 = 5
        range2 = 100
        range3 = 12        #this is for multiplication and division
        if flag == 1:
            #print("Flag is {}, You just got upgraded".format(flag))
            range1 = range1 + 1
            range2 = range2 + 1

    # Ask to select math type, and ask to enter a number if non-integer is entered
    while True:
        try:
            math = int(input('\n Alright {}, Press 1 for Addition, 2 for Subtraction, 3 for Multiplication, 4 for Division: '.format(name)))
            if math is 1 or math is 2 or math is 3 or math is 4:
                break
            else:
                print('Please enter a valid number between 1 and 4 :-) ')
        except (ValueError):
            print('Please enter a valid number ')


    startGameTime = time.time()
    for x in range(num_of_questions):
        x1 = random.randint(range1,range2)
        y1 = random.randint(range1,range2)
        startTime = time.time()

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

        elif int(math) == 3:                                           # if multiplication is chosen
            x1 = random.randint(2, range3)                             # let's focus on table of upto 10
            y1 = random.randint(0, 11)
            z1 = x1 * y1
            while True:
                try:
                    z = int(input('{}) {} x {} = '.format(x+1,x1,y1)))
                    break
                except ValueError:
                    print('Please enter a valid number')

        elif int(math) == 4:                                           # In division, bigger number is divided by smaller number
            x1 = random.randint(2, range3)                                 # let's focus on table of upto range3 number
            z1 = random.randint(0, 11)
            y1 = x1 * z1
            while True:
                try:
                    z = int(input('{}) {} % {} = '.format(x+1,y1,x1)))
                    break
                except ValueError:
                    print('Please enter a valid number')

        else:
            print('Please enter a valid number between 1 and 4')
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

    # if the local time not in Eastern timezone (value 18000), then convert it
    if time.timezone != 18000:
        now_utc = datetime.now(timezone('UTC'))
        now_ET = now_utc.astimezone(timezone('US/Eastern'))
        ET_date = now_ET.strftime("%Y-%m-%d")
        ET_time = now_ET.strftime("%X")
    else:
        ET_date = time.strftime("%Y-%m-%d")
        ET_time = time.strftime("%X")

    """ store all the info in a pandas dataframe row, which can later be written into a SQL DB
     Note that a list requires an index to be an integer, not a string, hence, int(math) is used with calculation
    """

    df = pd.DataFrame([[name, 1, ET_date, ET_time, calculation[int(math)], a + b, Percent, minT, maxT, round(endGameTime - startGameTime)]],
          columns=['name', 'attempt', 'date', 'time', 'calculation', 'totalQ', 'score', 'bestTime', 'worstTime', 'TotalTime'])

    #print(df)
    #print(df.describe())                                                               #prints std,50% values

    """
    Now, let's save the dataframe in a table, but let's first check for that table to be present in DB
    find the last attempt number for a given user name and then replace it with the current one
    write the pandas dataframe into the table
    """

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


        """ All checked. Let's write the dataframe into Math table """
        df.to_sql('Math', conn, if_exists='append',index=False, index_label=['name','attempt','date', 'time','calculation','totalQ','score','bestTime','worstTime','TotalTime'])


"""keep on asking for the name until it is entered exactly as expected by using 'while true' and break
only if matching name is entered, but not do the same in case of math type being not 1 or 2 or 3 or 4
"""

while True:
    name = input('Welcome, Enter your name: ')                      #input() always returns a string

    """progress only if name is already in the list, otherwise keep asking"""
    if name in names:
        flag = done = email_body = 0
        TimeStart = time.time()
        print("----------------------------------------------------------------")
        print("\n {}, Your Time now Started, Keep going as fast as you can..{}".format(name,TimeStart))
        print("----------------------------------------------------------------")

        """ keep testing until student wants to quit by not typing 'y'. """
        while True:
            # Let's find out about the last performance per calculation and encourage before test starts
            flag, done, email_body, totalQ = check_last_performance(name)
            #print('done value is {}'.format(done))
            if done == 1:
                ans = input('\n{}, Do you want to Quit (y/n): '.format(name))
                if ans == 'y':
                    """notify by sending an email/txt, since completed """
                    TimeEnd = time.time()
                    duration_min = (round((TimeEnd - TimeStart) / 60))
                    duration = "\tTotal time spent is {} minutes\n". format(duration_min)
                    email_body = email_body + duration
                    print(duration)
                    print("Your report will be sent via Email. Wait for few seconds...")
                    send_emails(name, email_body, totalQ, duration_min)
                    print("Great. Close this window. See you tomorrow. Have fun.")
                    exit()

            math_test(name, flag)

    else:
        print('\t\n Please enter the name that is in the list\n')
