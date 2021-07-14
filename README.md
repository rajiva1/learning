# living, learning & sharing 

kids-math.py 
============
This program is designed to help kids practice with basic math type - Addition, Substraction, Multiplication and Division. 

By default, the program asks 3 x 10 questions per type (e.g. Addition, Substraction) and keeps track of time taken to answer each question and overall. As soon as the program starts, it checks the previous performance and prints it along with an encouraging message. At the end, the overall performance summary before sending an email (to parents) as well.

The score/time/date etc. are stored in SQL DB with reasonable granularity.  


Pictures-file-cleanup.py 
========================
Background: Image Capture tool on macbook (https://support.apple.com/guide/image-capture/transfer-images-imgcp1003/mac) transfers 3 files for every picture that has been edited in the iPhone photo app, though one may need only the modified pic to avoid seeing 2 pics and save on storage - 
  IMG_<1234>.JPG (original pic)
  IMG_E<1234>.JPG (modified pic), and
  IMG.<1234>.AAE (has the metadata about the changes)

This program is meant to find if an IMG_ has a corresponding IMG_E* file in a directory of macbook, then delete IMG_ file, else don't delete it. 

It would be nice for 'Image Capture' tool to allow transferring only IMG_E* files, or i would need to write the program using the Shortcut app on iPhone itself. 


1099B.py
========
Background: By default, a stock trade of 1000 shares can be filled in using upto 1000 transactions and get reported in 1099-B in the same way to IRS. Few brokerages do consolidate the transactions to a single trade, but tax filing software e.g. Turbotax, H&R etc. ignore them. 

This program finds the matching transactions that relate to a single trade by looking into 1099B .csv file.

Note that one would need to manually update the .csv file accordingly (i.e. deletee those extra rows for the matching transactions and adding 1 row with cost, sale, gain/loss, wash sale etc.). This part is yet to be automated. 
Once .csv file is ready, then use the .csv to .txf conversion per https://github.com/rajiva1/stock-gain-tax-import/tree/patch-1 and import .txf into turbotax. PITB, sigh...
