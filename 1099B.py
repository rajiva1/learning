import csv
import pandas as pd

# This program is useful for finding 1099-B 2 or more transactions that relate to a single trade, so they can be
# consolidated to work within the turbotax limit of 3000 transactions.
# For ex, using this .csv file with 5 rows, output would be = LRN repeats 4 times
#ENTERCOM	5000	10/29/20	10/29/20	8249.82	11000	--	-2750.18	0	--	A	S	5
#LRN	-54	10/29/20	10/29/20	1717.16	1609.2	--	107.96	0	--	A	SS	54S K TWELVE INC             XXXNAME CHANG
#LRN	-76	10/29/20	10/29/20	2416.75	2264.8	--	151.95	0	--	A	SS	76S K TWELVE INC             XXXNAME CHANG
#LRN	-82	10/29/20	10/29/20	2607.54	2443.6	--	163.94	0	--	A	SS	82S K TWELVE INC             XXXNAME CHANG
#LRN	-84	10/29/20	10/29/20	2671.14	2503.2	--	167.94	0	--	A	SS	84S K TWELVE INC             XXXNAME CHANG

# v1: This program takes .csv file as an input and outputs no of times (rows) a word e.g. AMZN that appears in the same
# column


file = '~/<dir>/test-4-rows.csv'
data = table = []
count = 0

# open .csv file and convert the data into an array
# try:
#     with open(file, encoding='utf8') as f:
#         try:
#             for row in csv.reader(f):
#                 data.append(row)
#                 df = pd.DataFrame(data[0], columns=['symbol'])     # name the first column as symbol
#         except csv.Error as e:
#             print('Error: {err}'.format(err=e))
# except IOError as e:
#     print(e)
#
# convert array into a panda dataframe
#df = pd.DataFrame(data)
#print(df)

original_df = pd.read_csv(file)
print("this file has rows:{} and columns:{}".format(len(original_df), len(original_df.columns)))

    #just need the first column, so let's drop the rest. Need +1 to columns, since it is exlusive)
original_df.drop(original_df.columns[1:(len(original_df.columns)+1)], axis=1, inplace=True)

original_df.columns = ['symbol']                       #rename the remaining column - symbol
modified_df = original_df.drop_duplicates()            #get rid of rows with matching symbol values
modified_df['repeat'] = 0                              #rename second column and initialize it with 0
#print(df1.iloc[1:10, 0:1])                            #get 9 cell values in column 0 of row 1-9

#now, use modified dataframe to pick up each symbol 1 by 1 and count the repeations of that symbol in the original df

for index1, row1 in modified_df.iterrows():
    #print(original_df.iloc[index1][0])
    for index, row in original_df.iterrows():
        #print(row1, row)
        if row[0] == row1[0]:
            row1[1] += 1
        modified_df.loc[index1, 'repeat'] = row1[1]

#    if row['symbol'] != original_df.iloc['symbol']:

#print(modified_df.sort_values(by=['repeat']))                  #print all rows after sorted by values in repeat column
print(modified_df.nlargest(30, 'repeat'))                       #print first 30 rows that are sorted by the values in repeat

#print(modified_df.loc[modified_df['symbol'] == 'LRN'])         #print the row that has a matching symbol value
