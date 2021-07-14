# living, learning & sharing 

kids-math.py 
============
This program is designed to help kids practice with basic math type - Addition, Substraction, Multiplication and Division. 

By default, the program asks 3 x 10 questions per type (e.g. Addition, Substraction) and keeps track of time taken to answer each question and overall. As soon as the program starts, it checks the previous performance and prints it along with an encouraging message. At the end, the overall performance summary before sending an email (to parents) as well.

The score/time/date etc. are stored in SQL DB with reasonable granularity.  


1099B.py
========
By default, a stock trade of 1000 shares can be filled in using upto 1000 transactions and get reported in 1099-B in the same way to IRS. Few brokerages do consolidate the transactions to a single trade, but tax filing software e.g. Turbotax, H&R etc. ignore them. 

This program finds the matching transactions that relate to a single trade by looking into 1099B .csv file.

Note that one would need to manually update the .csv file accordingly (i.e. deletee those extra rows for the matching transactions and adding 1 row with cost, sale, gain/loss, wash sale etc.). This part is yet to be automated. 
Once .csv file is ready, then use the .csv to .txf conversion per https://github.com/rajiva1/stock-gain-tax-import/tree/patch-1 and import .txf into turbotax 
