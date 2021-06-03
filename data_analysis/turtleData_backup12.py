import pandas as pd
import os
#import pyproj as pj # for reliable gps
# or from pyproj import Geod (and remove the pj when executing the functionality)
from pyproj import Geod
import numpy as np # for reliable gps
from collections import Counter # for reliable gps
import datetime as dt # for reliable gps

class TurtleData:
    """Commom base class for all turtle's data """
    
    C1 = 'Acquisition Time'
    C2 ='Acquisition Start Time'
    C3 ='Iridium CEP Radius'
    C4 ='Iridium Latitude'
    C5 ='Iridium Longitude'
    C6 ='GPS Fix Time'
    C7 ='GPS Fix Attempt'
    C8 ='GPS Latitude'
    C9 ='GPS Longitude'
    C10 ='GPS UTM Zone'
    C11 ='GPS UTM Northing'
    C12 ='GPS UTM Easting'
    C13 ='GPS Altitude'
    C14 ='GPS Horizontal Error'
    C15 ='GPS Horizontal Dilution'
    C16 ='GPS Satellite Bitmap'
    C17 ='GPS Satellite Count'
    C18 ='Underwater Percentage'
    C19 ='Dive Count'
    C20 ='Average Dive Duration'
    C21 ='Dive Duration Standard Deviation'
    C22 ='Maximum Dive Duration'
    C23 ='Maximum Dive Depth'
    C24 ='Duration Limit 1 Dive Count'
    C25 ='Duration Limit 2 Dive Count'
    C26 ='Duration Limit 3 Dive Count'
    C27 ='Duration Limit 4 Dive Count'
    C28 ='Duration Limit 5 Dive Count'
    C29 ='Duration Limit 6 Dive Count'
    C30 ='Layer 1 Percentage'
    C31 ='Layer 2 Percentage'
    C32 ='Layer 3 Percentage'
    C33 ='Layer 4 Percentage'
    C34 ='Layer 5 Percentage'
    C35 ='Layer 6 Percentage'
    C36 ='Layer 7 Percentage'
    C37 ='Layer 8 Percentage'
    C38 ='Layer 9 Percentage'
    C39 ='Layer 10 Percentage'
    C40 ='Layer 1 Dive Count'
    C41 ='Layer 2 Dive Count'
    C42 ='Layer 3 Dive Count'
    C43 ='Layer 4 Dive Count'
    C44 ='Layer 5 Dive Count'
    C45 ='Layer 6 Dive Count'
    C46 ='Layer 7 Dive Count'
    C47 ='Layer 8 Dive Count'
    C48 ='Layer 9 Dive Count'
    C49 ='Layer 10 Dive Count'
    C50 ='Temperature'
    C51 ='Satellite Uplink'
    C52 ='Receive Time'
    C53 ='Repetition Count'
    C54 ='Low Voltage'
    C55 ='Mortality'
    C56 ='Saltwater Failsafe'
    C57 ='Iridium Command'
    C58 ='Schedule Set'
    C59 ='Diagnostic Dive Data'
    C60 ='Predeployment Data'
    C61 ='Error'
    col_names = list([
        C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, 
        C11, C12, C13, C14, C15, C16, C17, C18, C19, C20, 
        C21, C22, C23, C24, C25, C26, C27, C28, C29, C30, 
        C31, C32, C33, C34, C35, C36, C37, C38, C39, C40, 
        C41, C42, C43, C44, C45, C46, C47, C48, C49, C50, 
        C51, C52, C53, C54, C55, C56, C57, C58, C59, C60, 
        C61
    ])
    gps_col_names = list([
        C1, C2, C6, C7, C8, C9
    ])
    ID_ALLGPSDF_COLUMN_NAME = "All GPS's Track ID"

    @staticmethod
    def basedNamesForCsv(lastEntryRowDF, selfDfNameString, selfTurtleTag, selfSpecificFileName=""):
        for value in enumerate(lastEntryRowDF):
            #print(value[1][0])
            lastDate = value[1][0]
            date = dt.datetime.strptime(lastDate, "%Y.%m.%d")
            stringDate = date.strftime("%Y") + "_" + date.strftime("%b")
            print(f"The Last Entry in the Dataframe for {selfTurtleTag} is from: ")
            print(stringDate)
            # Give the CSV a Name based on this values above
            # name = allGpsDf_tag_xxxxx_until_lastdate
            cvsName = selfDfNameString + selfSpecificFileName + "_Tag_" + selfTurtleTag + "_" + stringDate +".csv"
            print(f"The Name for the {selfDfNameString} CSV for the turtleData {selfTurtleTag} is: ")
            print(cvsName)
            print('--------------')
            return cvsName 

    @staticmethod
    def calculateDistance(geodRef, lon1, lat1, lon2, lat2):
        # # compute forward and back azimuths, plus distance
        az12,az21,dist = geodRef.inv(lon1, lat1, lon2, lat2) #Take the second row and the first row on the count. it shoul give 3 values, but I only need the dist.
        # f"{az12:.3f} {az21:.3f} {dist:.3f}"        
        return dist #Put the dist inside the distances variable once empty.
    
    @staticmethod
    def convertUnixTimeFromString(timeString):
        return dt.datetime.strptime(timeString, '%Y.%m.%d %H:%M:%S').timestamp() #[i] is the position in an array
    
    @staticmethod
    def calculateSpeed(d, t1, t2):
        speed = d / (t2 - t1)
        return speed

    def __init__(self, tag):
        self.turtleTag = tag
        self.tagDate = ""
        self.tagTime = ""
        self.tagDatetime = ""
        self.df = pd.DataFrame()
        self.allGpsDf = pd.DataFrame()
        self.allGpsDfCsvName = ""
        #self.allGpsDf2019 = pd.DataFrame()
        self.allCleanedGpsDf = pd.DataFrame()
        self.allCleanedGpsDfCsvName = ""
        self.reliableGpsDf = pd.DataFrame()
        self.reliableGpsDfCsvName = ""
        self.noReliableGpsDf = pd.DataFrame()
        self.noReliableGpsDfCsvName = ""
    #def addElement(self, row, header):
        #self.__dict__= dict(zip(header, row))

    def addDataFromCsv(self, filename):
        temporaryDf = pd.read_csv(filename, skiprows=23, names=TurtleData.col_names)
        
        #print(f' ITS CURRENT DF IS: {self.df}') 
        #print('--------------')
        #print(f' ITS TEMPORARY DF IS {temporaryDf}') 
        
        self.df = self.df.append(temporaryDf, ignore_index=True)
        self.df.sort_values("Acquisition Time", inplace = True)

    def getTag(self):
        return self.turtleTag

    def getDf(self):        
        return self.df
    
    def giveAllGpsDf(self):
        # see all the columns in the df
        #print(self.df.columns)
        # see one column at a time        
        self.allGpsDf = self.df.copy()
        print(TurtleData.gps_col_names)
        tempList = TurtleData.gps_col_names.copy()
        for c in self.allGpsDf.columns:
            print(c)            
            if c not in tempList:
                self.allGpsDf.drop(c, inplace=True, axis=1)
            else:
                tempList.remove(c)        

        if tempList:
            print("Colummn Data missing in!")
        else:
            print("The dataframe contains all the GPS columns")
        
        print('-----DF with NaN values ---------')
        print(self.allGpsDf)       
        
        #### Eliminate those GPS's null (NaN) rows from the dataframe
        self.allGpsDf.drop(self.allGpsDf[~self.allGpsDf['GPS Latitude'].notna()].index, inplace=True)
        self.allGpsDf.reset_index(drop=True, inplace=True) # reset index

        print('-----SAME DF without NaN values ---------')
        print(self.allGpsDf)

        ####Create a column for id GPS points to the left
        trackId = self.allGpsDf.index + 1
        self.allGpsDf.insert(0, TurtleData.ID_ALLGPSDF_COLUMN_NAME, trackId)
        
        print(self.allGpsDf)        
        print(' End of all GPS Df ^')
        print('--------------')    
    
    def generateAllGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.allGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.allGpsDfCsvName = TurtleData.basedNamesForCsv(lastEntry, "allGpsDf", self.turtleTag)        
    
    def saveAllGpsDfData(self, pathToFilePlusCsvName):
        self.allGpsDf.to_csv(pathToFilePlusCsvName, index=False)
    
    def assignTagTurtleDayDatetime(self, TagDate, TagTime):
        '''
        the Date and Time of the turtle's Tag Day
        '''
        self.tagDate = TagDate
        self.tagTime = TagTime
        self.tagDatetime = self.tagDate + " " + self.tagTime
    
    def giveAllCleanedGpsDf(self):
        # without 2019 date and without duplicate rows
        precedentYearRowsTemporaryDf = self.allGpsDf.copy()
        print(f"Before cleaning, the AllGpsDf called: {self.allGpsDfCsvName}, contained {len(precedentYearRowsTemporaryDf.index)} rows")
        
        ##### ---------- This Part is not needed ---------- #####
        # Remove 2019 data from 'Acquisition Time column:
        dateColumn = precedentYearRowsTemporaryDf['Acquisition Time']
        #print(dateColumn)
        # separing date from time in that column
        dateColumn = pd.Series([[y for y in x.split()] for x in dateColumn])
        #print(dateColumn)
        all2019DateData = []
        allOtherDateData = []        
        for value in enumerate(dateColumn):
            #print(value[1][0])
            # assign the date rows to the variable dateData
            dateData = value[1][0]
            # removing 2019 from the list
            if dateData.startswith('2019'):
                #print(f"dateData that starts with 2019 = {dateData}")
                # append the 2019 data to the list
                all2019DateData.append(dateData)
            else:
                #print(f"dateData that do not starts with 2019 = {dateData}")
                # append any other data to this list
                allOtherDateData.append(dateData)
        #print(f" 2019 list = {all2019DateData}")
        #print(f" 2020/2021 list = {allOtherDateData}")
        ##### ---------- END OF the Part not needed ---------- #####

        #### Eliminate those 2019 data rows from the dataframe
        ### example: df = df[~df['c'].astype(str).str.startswith('1')]
        print(f"Removing 2019 data from the {self.allGpsDfCsvName}")
        precedentYearRowsTemporaryDf.drop(precedentYearRowsTemporaryDf[precedentYearRowsTemporaryDf['Acquisition Time'].astype(str).str.startswith('2019')].index, inplace=True)
        precedentYearRowsTemporaryDf.reset_index(drop=True, inplace=True) # reset index
        #print(precedentYearRowsTemporaryDf)
        print(f"After removing 2019 data, the AllGpsDf called: {self.allGpsDfCsvName}, contained {len(precedentYearRowsTemporaryDf.index)} rows")
        
        ### Eliminate duplicate rows
        # Select duplicate rows except first occurrence based on all columns
        ## example of Selection by Position, to see example duplicated rows ----------------------------------
        ## df.iloc[row_indexer,column_indexer]
        print('--------------')
        duplicateRowsTemporaryDf = precedentYearRowsTemporaryDf
        duplicateRowsTemporaryDf = duplicateRowsTemporaryDf.drop_duplicates(
            [
                'Acquisition Time','Acquisition Start Time', 'GPS Fix Time', 'GPS Fix Attempt', 'GPS Latitude', 'GPS Longitude'
            ], keep='first'
        )
        print(duplicateRowsTemporaryDf)
        print(duplicateRowsTemporaryDf.iloc[13:19,1])
        print(f"Without duplicated rows, the dataframe has now {len(duplicateRowsTemporaryDf.index)} rows")
        # Drop same aquisition time that is giving us error in the calculation of distances and speeds
        duplicateRowsTemporaryDf = duplicateRowsTemporaryDf.drop_duplicates(['Acquisition Time'], keep='first')
        print(duplicateRowsTemporaryDf)
        print(duplicateRowsTemporaryDf.iloc[13:19,1])
        print("The lines where we had the same acquisition time")
        print(duplicateRowsTemporaryDf.iloc[23:29,1])
        print(f"Without duplicated acquisition times, the dataframe has now {len(duplicateRowsTemporaryDf.index)} rows")
        print("The df without duplicated rows and Without duplicated acquisition times is the duplicateRowsTemporaryDf")
        print('--------------')

        #### Eliminate test date before its Turtle tag day Datetime
        print("Excluding date BEFORE TAG DAY DATETIME")
        testDateRowsTemporaryDf = duplicateRowsTemporaryDf
        #print(testDateRowsTemporaryDf[testDateRowsTemporaryDf['Acquisition Time'].astype(str).str.startswith(self.tagDatetime)])
        ## listing days before
        print(testDateRowsTemporaryDf[testDateRowsTemporaryDf['Acquisition Time'] < self.tagDatetime])
        ## dropping them
        testDateRowsTemporaryDf.drop(testDateRowsTemporaryDf[testDateRowsTemporaryDf['Acquisition Time'] < self.tagDatetime].index, inplace=True)
        print("TEST -------------- TEST ------- TEST")
        print(self.tagDatetime)
        print(testDateRowsTemporaryDf)

        print(f"Without days before turtle tag day, the dataframe has now {len(testDateRowsTemporaryDf.index)} rows")
        print("The df without duplicated rows, without duplicated acquisition times and without days before turtle tag is the testDateRowsTemporaryDf")
        print('--------------')

        print("ALL THE DF THAT IS GONNA BE SAVE IN ALL CLEANED GPS DATAFRAME")
        print("Saving this temporary df into the allCleanedGpsDf...")
        self.allCleanedGpsDf = self.allCleanedGpsDf.append(testDateRowsTemporaryDf, ignore_index=True)
        print(self.allCleanedGpsDf)
        print(self.allCleanedGpsDf.iloc[13:19,1])
        print("The df without duplicated rows is now the self.allCleanedGpsDf")
        print('------- END -------')

    def generateAllCleanedGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.allCleanedGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.allCleanedGpsDfCsvName = TurtleData.basedNamesForCsv(lastEntry, "allCleanedGpsDf", self.turtleTag)
    
    def saveAllCleanedGpsDfData(self, pathToFilePlusCsvName):
        self.allCleanedGpsDf.to_csv(pathToFilePlusCsvName, index=False)

    def giveReliableGpsDfAndNoReliableGps(self):
        '''
        Remove GPS Errors by Angular velocity/Rotational speed 
        (degree per second)
        Geod Object for Calculations is used as objec to calculate 
        distances between points expressed in lat/lon (in degree)
        Choosing a Reference Ellipsoid - distance in degree more 
        accurate than a spherical method
        '''
        removingGpsErrorsTemporaryDf = self.allCleanedGpsDf.copy()
        #print(gpsErrorsTemporaryDf)
        wgs84_geod = Geod(ellps='WGS84')
        ## Converting data to a NumPy array.        
        latitudes = removingGpsErrorsTemporaryDf[['GPS Latitude']].to_numpy() 
        longitudes = removingGpsErrorsTemporaryDf[['GPS Longitude']].to_numpy()
        acquisitionTimes = removingGpsErrorsTemporaryDf[['Acquisition Time']].to_numpy()
        
        #latitudes = removingGpsErrorsTemporaryDf['GPS Latitude'].reset_index().values
        #longitudes = removingGpsErrorsTemporaryDf['GPS Longitude'].reset_index().values
        ##acquisitionTimes = removingGpsErrorsTemporaryDf[['Acquisition Time']].reset_index().values
        #acquisitionTimes = removingGpsErrorsTemporaryDf[['Acquisition Time']].to_numpy()        
        
        #print(latitudes.dtype)
        #print(longitudes.dtype)
        #print(acquisitionTimes.dtype)
        
        #print(latitudes)
        #print(longitudes)
        #print(acquisitionTimes)

        distances = []
        tripTimes = []
        speeds = []
        remSpeeds = []
        pointsToRemove = []        
        
        distances.append(0)
        tripTimes.append(0)
        speeds.append(0)

        i=1
        while i < (len(latitudes)):
            foundS = False
            previous = i-1
            D = 0
            S = 100
            while (S > 1.111) and (i < len(latitudes)):
                D = TurtleData.calculateDistance(wgs84_geod, longitudes[previous], latitudes[previous], longitudes[i], latitudes[i])
                t1 = TurtleData.convertUnixTimeFromString(acquisitionTimes[previous,0])
                t2 = TurtleData.convertUnixTimeFromString(acquisitionTimes[i,0])
                S = TurtleData.calculateSpeed(D,t1,t2)
                #print(f" D = {D}")
                #print('dist: %.3f' % D)
                #print(f" S = {S}")
                #print('S: %.3f' % S)
                if(S > 1.111):
                    remSpeeds.append(S)
                    #print(f"remSpeeds List: {remSpeeds}")                    
                    pointsToRemove.append(acquisitionTimes[i,0])
                    #print(pointsToRemove)                    
                    i+=1
                else:
                    foundS = True
            if(foundS):
                distances.append(D)
                tripTimes.append(t2-t1)
                speeds.append(S)
            i+=1
        print(self.turtleTag)
        print("Length of pointsToRemove List: ")
        print(len(pointsToRemove))
        print(f"remSpeeds List: {remSpeeds}")
        #---------
        print('--------------')        
        print(pointsToRemove)

        ### Cond = Points with speed > than 4km/h to be removed from the df (removingGpsErrorsTemporaryDf)
        ### Cond 2 = Points with speed > than 4km/h to be keep in the df (keepingGpsErrorsTemporaryDf)

        ### TO CREATE A DF WITHOUT SPEED ERRORS = Cond *        
        cond = removingGpsErrorsTemporaryDf['Acquisition Time'].isin(pointsToRemove)
        print('BEFORE DROP - removingGpsErrorsTemporaryDf')
        print(len(removingGpsErrorsTemporaryDf))
        removingGpsErrorsTemporaryDf.drop(removingGpsErrorsTemporaryDf[cond].index, inplace = True)
        print('AFTER DROP - removingGpsErrorsTemporaryDf')
        print(len(removingGpsErrorsTemporaryDf))        
        
        ### TO CREATE A DF JUST WITH THE SPEED ERRORS = Cond 2 *
        keepingGpsErrorsTemporaryDf = self.allCleanedGpsDf.copy()
        ##for index, rows in Time_df.head().iterrows():
         ##if(rows["Total Time"] < 6.00 ):
             ##Time_df.loc[index,"Code"] = 1
        print('BEFORE KEEPING GPS POINTS WITH SPEED > 4KM/H in the keepingGpsErrorsTemporaryDf')
        print(len(keepingGpsErrorsTemporaryDf))
        wrongSpeedPoints = []
        for indexes, rows in keepingGpsErrorsTemporaryDf.iterrows():
            if(rows['Acquisition Time'] in pointsToRemove):
                wrongSpeedPoints.append(rows)
        print(wrongSpeedPoints)
        print(len(wrongSpeedPoints))

        wrongSpeedDf = pd.DataFrame(wrongSpeedPoints)
        wrongSpeedDf.reset_index(drop=True, inplace=True)
        print("TEST AS DATAFRAME wrongSpeedPoints")
        print(wrongSpeedDf)
        print(len(wrongSpeedDf))   

        # ---------------------------------------------------
        ### CREATING NEW COLUMNS FOR BOTH DATAFRAMES AND SAVE THEM INTO A SELF DF
        ### 1 - self.reliableGpsDf
         
        removingGpsErrorsTemporaryDf['Distance (m)'] = distances        
        removingGpsErrorsTemporaryDf['Time (s)'] = tripTimes
        removingGpsErrorsTemporaryDf['Speed m/s'] = speeds
        removingGpsErrorsTemporaryDf['Time (h)'] = pd.to_timedelta(removingGpsErrorsTemporaryDf['Time (s)'], unit='s') # Add a Column with the Time passed from on Point to another in hours
        print('BEFORE CHANGES - FROM INT TO FLOAT')
        print(type(removingGpsErrorsTemporaryDf.loc[0, 'Distance (m)']))
        
        # # # Removing Square brackets From values in the 'Distance (m)' and 'Speed m/s' Columns
        # # #remove brackets of the values in Columns        
        removingGpsErrorsTemporaryDf = removingGpsErrorsTemporaryDf.astype({"Distance (m)":'float', "Speed m/s":'float'}) 
        # # #removingGpsErrorsTemporaryDf['Distance (m)'] = removingGpsErrorsTemporaryDf['Distance (m)'].str[0] #remove the brackets of the values in the column
        # # #removingGpsErrorsTemporaryDf['Speed m/s'] = removingGpsErrorsTemporaryDf['Speed m/s'].str[0] #remove the brackets of the values in the column	        
        print('AFTER CHANGES - FROM INT TO FLOAT')
        print(type(removingGpsErrorsTemporaryDf.loc[0, 'Distance (m)']))
        
        print("removingGpsErrorsTemporaryDf With new columns")
        print(removingGpsErrorsTemporaryDf)
        print(removingGpsErrorsTemporaryDf.dtypes)        
        print('--------------')
        
        # # # Create a ID Column on the Left for the Reliable Tracked Points 
        speedTrackedPoints = removingGpsErrorsTemporaryDf.index + 1
        removingGpsErrorsTemporaryDf.insert(0, 'Reliable Speed ID', speedTrackedPoints)
        
        print("removingGpsErrorsTemporaryDf With ID column")
        print(removingGpsErrorsTemporaryDf)
        print(removingGpsErrorsTemporaryDf.dtypes)        
        print('--------------')
        
        self.reliableGpsDf = self.reliableGpsDf.append(removingGpsErrorsTemporaryDf, ignore_index=True)
        
        print("Assign the Reliable GPS DF into self")
        print(self.reliableGpsDf)
        print(self.reliableGpsDf.dtypes)        
        print('--------------')

        # ---------------------------------------------------
        ### 2 - self.noReliableGpsDf
        
        wrongSpeedDf['Speeds > 1,11111 m/s'] = remSpeeds
        print('BEFORE CHANGES - FROM INT TO FLOAT')
        print(type(wrongSpeedDf.loc[0, "Speeds > 1,11111 m/s"]))
        
        # # # Removing Square brackets From values in the 'Speeds > 1,11111 m/s' Columns
        # # #remove brackets of the values in Columns        
        wrongSpeedDf = wrongSpeedDf.astype({"Speeds > 1,11111 m/s":'float'}) 
        # # #wrongSpeedDf['Speeds > 1,11111 m/s'] = wrongSpeedDf['Speeds > 1,11111 m/s'].str[0] #remove the brackets of the values in the column	        
        print('AFTER CHANGES - FROM INT TO FLOAT')
        print(type(wrongSpeedDf.loc[0, "Speeds > 1,11111 m/s"]))
        
        print("wrongSpeedDf With new columns")
        print(wrongSpeedDf)
        print(wrongSpeedDf.dtypes)        
        print('--------------')
        
        # # # Create a ID Column on the Left for the NO Reliable Tracked Points 
        speedTrackedPoints = wrongSpeedDf.index + 1
        wrongSpeedDf.insert(0, 'Removed GPS by Speed', speedTrackedPoints)
        
        print("wrongSpeedDf With ID column")
        print(wrongSpeedDf)
        print(wrongSpeedDf.dtypes)        
        print('--------------')
        
        self.noReliableGpsDf = self.noReliableGpsDf.append(wrongSpeedDf, ignore_index=True)
        
        print("Assign the NO Reliable GPS DF into self")
        print(self.noReliableGpsDf)
        print(self.noReliableGpsDf.dtypes)        
        print('--------------')
    
    def generateReliableGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.reliableGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.reliableGpsDfCsvName = TurtleData.basedNamesForCsv(lastEntry, "reliableGpsDf", self.turtleTag, "_bySpeed")
    
    def saveReliableGpsData(self, pathToFilePlusCsvName):
        self.reliableGpsDf.to_csv(pathToFilePlusCsvName, index=False)

        # -------- until this bit above works, next, works with saving the reliable df

    def generateNoReliableGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.noReliableGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.noReliableGpsDfCsvName = TurtleData.basedNamesForCsv(lastEntry, "noReliableGpsDf", self.turtleTag, "_bySpeed")
    
    def saveNoReliableGpsData(self, pathToFilePlusCsvName):
        self.noReliableGpsDf.to_csv(pathToFilePlusCsvName, index=False)
        
        


        # Saving Removed Points in another dataframe (removedPointsRowDf) and dropping those out from the gpsErrorsTemporaryDf
        #self.allGpsDf.drop(self.allGpsDf[~self.allGpsDf['GPS Latitude'].notna()].index, inplace=True)
        #self.allGpsDf.reset_index(drop=True, inplace=True) # reset index
        removedPointsRowDf = gpsErrorsTemporaryDf[gpsErrorsTemporaryDf['Acquisition Time'].isin(pointsToRemove)]
        removedPointsRowDf.loc[:,'Speeds > 1,11111 m/s'] = remSpeeds
        # reseting index
        removedPointsRowDf.reset_index(drop=True, inplace=True) 
        removedGPSPoints = removedPointsRowDf.index + 1 
        # Creating a Column for ID Removed Track Points on the Left
        removedPointsRowDf.insert(0, 'Removed GPS by Speed', removedGPSPoints) 
        # Saving the amount of removed points data
        qtyremovedGPSpointsSept = len(removedPointsRowDf.index) 
        print(f'QTY OF REMOVED POINTS: {qtyremovedGPSpointsSept}')        
        # # Count Occurrence of a value in 'GPS Fix Attempt' Column
        # cntOccurrFixAttemptRemovedPoints = Counter(removedPointsRowDf['GPS Fix Attempt'])
        # print('Qty Fix Attempt Of Removed Points:') 
        # print(cntOccurrFixAttemptRemovedPoints)
        # print('-----------------------')        
        # # EXPORTING REMOVED POINTS DATA
        # #removedPointsRowDf.to_csv('Removed_Points_GPS_Data_Tag_333A_Sept.csv', index=False) # Calling DataFrame constructor on list

        # # LATER ON, SAVE REMOVED DATA:
        # #-2019 DATA REMOVED FROM ALLGPSDF
        # #-DUPLICATED DATA REMOVED FROM ALLGPSDF
        # #-REMOVED GPS TRACK POINTS FROM THE ALLCLEANEDGPSDF
        # #-----------------------------------------------------------
        
        #gpsErrorsTemporaryDf.drop(gpsErrorsTemporaryDf[gpsErrorsTemporaryDf['Acquisition Time'].isin(pointsToRemove)].index, inplace=True)


        
    #     #-----------------------------------------------------------
    #     #Complete the new columns and save only reliable GPS points excluded through speed
        
    #     gpsErrorsTemporaryDf.reset_index(drop=True, inplace=True) # reset index
    #     routePoints = gpsErrorsTemporaryDf.index + 1 
    #     gpsErrorsTemporaryDf.insert(0, 'Tracked Points', routePoints) # Create a ID Column on the Left for the Tracked Points 
                
    #     gpsErrorsTemporaryDf.drop(['ID GPS Points'], axis=1, inplace=True)
        
    #     # Add the list values as New Columns of the DataFrame
    #     gpsErrorsTemporaryDf['Length (m)'] = distances
    #     gpsErrorsTemporaryDf['Length (m)'] = gpsErrorsTemporaryDf['Length (m)'].str[0] #remove the brackets of the values in the column
    #     gpsErrorsTemporaryDf['Time (s)'] = tripTimes
    #     gpsErrorsTemporaryDf['Speed m/s'] = speeds
    #     gpsErrorsTemporaryDf['Speed m/s'] = gpsErrorsTemporaryDf['Speed m/s'].str[0] #remove the brackets of the values in the column	
    #     #print(df.dtypes)
    #     gpsErrorsTemporaryDf['Time (h)'] = pd.to_timedelta(gpsErrorsTemporaryDf['Time (s)'], unit='s') # Add a Column with the Time passed from on Point to another in hours



#self.reliableGpsDf