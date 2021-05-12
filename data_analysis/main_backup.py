#import pandas as pd
#import os
from functions import *

def main():
    # Check if some excel file has not been converted into csv yet
    check_for_excel_files()
    turtlesData = getTurtlesData()

    # turtlesData[0].df
    # turtlesData[1].df

    for turtleData in turtlesData:
        #print(os.path.abspath(os.getcwd()))
        print(turtleData.getTag())
        #print(turtleData.getDf)
        print(turtleData.df)
        # sorting by Acquisition Time
        #turtleData.df.sort_values("Acquisition Time", inplace = True)
        # dropping ALL duplicte values based on two columns
        #turtleData.df.drop_duplicates(subset = ['Acquisition Time', 'Acquisition Start Time'], keep = 'last').reset_index(drop = True)
    
    turtlesData[0].df
    turtlesData[1].df


if __name__ == "__main__":
    main()


