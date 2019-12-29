
import glob
import os

"""
This program is meant to find if an IMG_ has a corresponding IMG_E_ file in a directory, then delete IMG_ file, else
don't delete it. 
 
Background: iphone photo app transfers 2 (or 3) files for every picture that has been edited - 
IMG_<1234>.JPG and IMG_E<1234>.JPG. IMG.<1234>.AAE.
"""


d = os.environ['HOME']+"/Pictures/"                               # let's find the Pictures directory path

# Ask for the directory to check

while True:
    try:
        name = input('Enter Directory year/month to check: ')      #input() always returns a string
        dir = d+name
        print("We will be working with {}".format(dir))            # not checkig for syntax; Garbage in/out
        break
    except(ValueError):
        print("Enter correctly e.g. 2019/Jan ")


# first tuple in os.walk lists all subdirectories recursively;

subdirs = [x[0] for x in os.walk(dir)]
print("\tThere are {} directories in here".format(len(subdirs)-1))

for n in subdirs:
    count=countf1=countf2=countf3=0
    list=[]
    if n != dir:                                              # avoid browsing the directory, as it would have no pictures
        files = [f for f in glob.glob(n + "*/*", recursive=False)]
        for a in files:
            if a.endswith('.JPG') or a.endswith('.MOV'):
                count=count+1
                if ((a.find("IMG_E")) != -1):                 # check if the file name has IMG_E string in it
                    a1 = a.replace("IMG_E", "IMG_")           # replace the filename
                    countf1=countf1+1                         # count no of IMG_E* files found so far
                    try:
                        os.remove(a1)                         # being lazy, try removing the file even if not existing
                        countf2=countf2+1                     # count no of matching IMG_* files deleted so far
                        list.append(a1)
                    except(FileNotFoundError):
                        countf3=countf3+1

            else:
                print("<---->Sorry, we don't delete = {}".format(a))

        # printing for housekeeping stuff after every directory search 
        print("\n{}".format(n))
        print("==============================")
        print("\t{} total files were found".format(count))
        print("\t{} IMG_E* files were found".format(countf1))
        print("\t{} IMG_* files (matching) weren't found ".format(countf3))
        print("\t{} IMG_* files matched and got deleted. See file names below (if any)".format(countf2))
        print("\t\t{}".format(list))



# check total number of files between two main directories (Dec and Dec1, say)
# dir1 = dir+str(1)
# countf21=countf22=0
# for r,d,f in os.walk(dir):
#     for files in f:
#         countf21=countf21+1
# for r,d,f in os.walk(dir1):
#     for files in f:
#         countf22=countf22+1
# print(countf21, countf22)
