import pandas as pd
import os
#import pyproj as pj # for reliable gps
# or from pyproj import Geod (and remove the pj when executing the functionality)
from pyproj import Geod, Proj
import numpy as np # for reliable gps
from collections import Counter # for reliable gps
import datetime as dt # for reliable gps
import sys
#import geopandas as gpd # for geometry column for reliable gps # install first GDAL, then fiona and then geopandas
import matplotlib.pyplot as plt #produces maps and diagrams

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
    
    # COLUMN ID NAME
    # Access using TurtleData. before
    #ID_RAWDATA_COLUMN_NAME = "Raw Data ID"
    ID_ALLGPSDF_COLUMN_NAME = "All GPS's Track ID"
    ID_RELIABLE_COLUMN_NAME = 'Reliable Speed ID'
    ID_NORELIABLE_COLUMN_NAME = 'Removed GPS by Speed'
    ID_NOGPSDATA_COLUMN_NAME = 'No GPS Data ID'
    ID_REMAININGDATA_COLUMN_NAME = 'Remaining Data ID'
    ID_DEPTHDATA_COLUMN_NAME = 'Depth Data ID'

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
    principal_depth_col_names = list([
        ID_NOGPSDATA_COLUMN_NAME, C1, C2, C18, C19, C20, C22, C23, C30, C31, C32, C33, C34, C35, C36, 
        C37, C38, C39, C40, C41, C42, C43, C44, C45, C46, C47, C48, C49
    ])

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
    
    @staticmethod
    def checkIfDfHasBeenSavedAndSaveDf(folderToSaveItems, folderToSave, dataframe, stringDfName):
        filesInResultsFolder = []       
        for file in folderToSaveItems:
            filesInResultsFolder.append(file)    
        print(filesInResultsFolder)
        if not filesInResultsFolder:
            print(f"The filename {stringDfName} is not yet in the folder... saving csv")
            pathToFilePlusCsvName = os.path.join(folderToSave, stringDfName)
            dataframe.to_csv(pathToFilePlusCsvName, index=False)
            print(f"{stringDfName} has been saved in the results folder!")
        elif stringDfName in filesInResultsFolder:
            print(f"The CSV {stringDfName} has already been saved in the results folder")
        else:
            print(f"The filename {stringDfName} is not yet in the folder... saving csv")
            pathToFilePlusCsvName = os.path.join(folderToSave, stringDfName)
            dataframe.to_csv(pathToFilePlusCsvName, index=False)
            print(f"{stringDfName} has been saved in the results folder!")
        print('--------------')

    def __init__(self, tag):        

        if not sys.gettrace()==None:
            # To run with Debug:
            self.DIRNAME = os.path.dirname(__file__)
            self.ASSETS_FOLDER = os.path.join(self.DIRNAME, 'assets')
            ##ASSETS_FOLDER_OBJ = "data_analysis\\assets"
            self.ASSETS_FOLDER_ITENS = os.listdir(self.ASSETS_FOLDER)# ("data_analysis/assets")

            self.DATACLEANINGRESULTS_FOLDER = os.path.join(self.DIRNAME, 'dataCleaningResults')
            self.DATACLEANINGRESULTS_FOLDER_ITENS = os.listdir(self.DATACLEANINGRESULTS_FOLDER)# ("data_analysis/dataCleaningResults")
        else:
            # To run with terminal OR jupyter notebook:
            self.ASSETS_FOLDER = "assets"
            self.ASSETS_FOLDER_ITENS = os.listdir(self.ASSETS_FOLDER)# ("assets")

            self.DATACLEANINGRESULTS_FOLDER = "dataCleaningResults"
            self.DATACLEANINGRESULTS_FOLDER_ITENS = os.listdir(self.DATACLEANINGRESULTS_FOLDER)# ("data_analysis/dataCleaningResults")

        self.turtleTag = tag
        self.tagDate = ""
        self.tagTime = ""
        self.tagDatetime = ""
        self.df = pd.DataFrame()
        #self.noGpsDf = {"dataframe": pd.DataFrame(), "stringDfName": ""}
        self.noGpsDf = pd.DataFrame()
        self.noGpsDfCsvName = ""
        self.allGpsDf = pd.DataFrame()
        self.allGpsDfCsvName = ""
        #self.allGpsDf2019 = pd.DataFrame()
        self.allCleanedGpsDf = pd.DataFrame()
        self.allCleanedGpsDfCsvName = ""
        self.noReliableGpsDf = pd.DataFrame()
        self.noReliableGpsDfCsvName = ""
        self.reliableGpsDf = pd.DataFrame()
        self.reliableGpsDfCsvName = ""
        self.remainingDataDf = pd.DataFrame()
        self.remainingDataDfCsvName = ""
        self.depthDataDf = pd.DataFrame()
        self.depthDataDfCsvName = ""
        self.crs = ""
        self.ellps = ""
        self.proj4 = ""
        # reliableGpsDF lat, lon and acquisition time into numpy array for faster calculations
        self.xlon_np = np.array([])
        self.xlat_np = np.array([])
        self.acquisitionTime_np = np.array([])

    def addDataFromCsv(self, filename):
        temporaryDf = pd.read_csv(filename, skiprows=23, names=TurtleData.col_names)        
        self.df = self.df.append(temporaryDf, ignore_index=True)
        self.df.sort_values("Acquisition Time", inplace = True)

        #### Create new column for the raw data df ID
        # rawDataId = self.df.index + 1
        # self.df.insert(0, TurtleData.ID_RAWDATA_COLUMN_NAME, rawDataId)
        # print('DF WITH NEW ID COLUMN')
        # print(self.df)
        # print(' End of Df ^')
        # print('--------------')

    def getTag(self):
        return self.turtleTag

    def getDf(self):        
        return self.df
    
    def giveNoGpsDf(self):
        # Clean Data, filtering 'no GPS Data' from 'GPS Data'
        # Filtering rows that do not contain GPS information
        temporaryNoGPSData = self.df.copy()
        temporaryNoGPSData = (temporaryNoGPSData[~temporaryNoGPSData['GPS Latitude'].notna()])
        temporaryNoGPSData.reset_index(drop=True, inplace=True) # reset index        
        print('Temporary No GPS df is temporaryNoGPSData')
        print(temporaryNoGPSData)
        self.noGpsDf = self.noGpsDf.append(temporaryNoGPSData, ignore_index=True)
        #### Create new column for the new rows ID
        newid = self.noGpsDf.index + 1
        self.noGpsDf.insert(0, TurtleData.ID_NOGPSDATA_COLUMN_NAME, newid)
        print('No GPS df WITH NEW ID COLUMN')
        print(self.noGpsDf)
        print(' End of NO GPS Df ^')
        print('--------------')
    
    def generateNoGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.noGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        # assign the Name in the Class Variable
        self.noGpsDfCsvName = TurtleData.basedNamesForCsv(lastEntry, "noGpsDf", self.turtleTag)        
    
    def saveNoGpsDfData(self):
        return TurtleData.checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.noGpsDf, self.noGpsDfCsvName)

    def giveAllGpsDf(self):
        # see all the columns in the df
        #print(self.df.columns)
        # see one column at a time        
        temporaryAllGpsDf = self.df.copy()
        print(TurtleData.gps_col_names)
        tempList = TurtleData.gps_col_names.copy()
        for c in temporaryAllGpsDf.columns:
            print(c)            
            if c not in tempList:
                temporaryAllGpsDf.drop(c, inplace=True, axis=1)
            else:
                tempList.remove(c)
        if tempList:
            print("Colummn Data missing in!")
        else:
            print("The dataframe contains all the GPS columns")

        print('-----TEMPORARY DF with NaN values ---------')
        print(temporaryAllGpsDf)        
        #### Eliminate those GPS's null (NaN) rows from the dataframe
        temporaryAllGpsDf.drop(temporaryAllGpsDf[~temporaryAllGpsDf['GPS Latitude'].notna()].index, inplace=True)
        temporaryAllGpsDf.reset_index(drop=True, inplace=True) # reset index
        print('-----SAME TEMPORARY DF without NaN values, BUT WITH DUPLICATED ROWS ---------')
        print(temporaryAllGpsDf)
        print('--------------')
        duplicateRowsTemporaryAllGpsDf = temporaryAllGpsDf
        duplicateRowsTemporaryAllGpsDf = duplicateRowsTemporaryAllGpsDf.drop_duplicates(
            [
                'Acquisition Time','Acquisition Start Time', 'GPS Fix Time', 'GPS Fix Attempt', 'GPS Latitude', 'GPS Longitude'
            ], keep='first'
        )
        print(duplicateRowsTemporaryAllGpsDf)
        print(duplicateRowsTemporaryAllGpsDf.iloc[13:19,1])
        print(f"Without duplicated rows, the dataframe has now {len(duplicateRowsTemporaryAllGpsDf.index)} rows")
        # Drop same aquisition time that is giving us error in the calculation of distances and speeds
        duplicateRowsTemporaryAllGpsDf = duplicateRowsTemporaryAllGpsDf.drop_duplicates(['Acquisition Time'], keep='first')
        print(duplicateRowsTemporaryAllGpsDf)
        print(duplicateRowsTemporaryAllGpsDf.iloc[13:19,1])
        print("The lines where we had the same acquisition time")
        print(duplicateRowsTemporaryAllGpsDf.iloc[23:29,1])
        print(f"Without duplicated acquisition times, the dataframe has now {len(duplicateRowsTemporaryAllGpsDf.index)} rows")
        print("The df without duplicated rows and Without duplicated acquisition times is the duplicateRowsTemporaryDf")
        print('--------------')
        print('-----SAME TEMPORARY DF without DUPLICATED ROWS ---------')
        print(duplicateRowsTemporaryAllGpsDf)
        self.allGpsDf = self.allGpsDf.append(duplicateRowsTemporaryAllGpsDf, ignore_index=True)
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

    def saveAllGpsDfData(self):
        return TurtleData.checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.allGpsDf, self.allGpsDfCsvName)
    
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

    def saveAllCleanedGpsDfData(self):
        return TurtleData.checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.allCleanedGpsDf, self.allCleanedGpsDfCsvName)

    def assignCoordinateReferenceSystemCrs(self, crsEpsgCode, ellpsForGeod, proj4ForProj):
        self.crs = crsEpsgCode
        self.ellps = ellpsForGeod
        self.proj4 = proj4ForProj

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
        geod = Geod(ellps=self.ellps)
        ## Converting data to a NumPy array.        
        latitudes = removingGpsErrorsTemporaryDf[['GPS Latitude']].to_numpy() 
        longitudes = removingGpsErrorsTemporaryDf[['GPS Longitude']].to_numpy()
        acquisitionTimes = removingGpsErrorsTemporaryDf[['Acquisition Time']].to_numpy()

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
                D = TurtleData.calculateDistance(geod, longitudes[previous], latitudes[previous], longitudes[i], latitudes[i])
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
        removingGpsErrorsTemporaryDf.insert(0, TurtleData.ID_RELIABLE_COLUMN_NAME, speedTrackedPoints)        
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
        wrongSpeedDf.insert(0, TurtleData.ID_NORELIABLE_COLUMN_NAME, speedTrackedPoints)        
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

    def saveReliableGpsData(self):
        return TurtleData.checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.reliableGpsDf, self.reliableGpsDfCsvName)
     
    def generateNoReliableGpsDfCsvName(self):
        # Last entry:
        lastEntry = self.noReliableGpsDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.noReliableGpsDfCsvName = TurtleData.basedNamesForCsv(lastEntry, "noReliableGpsDf", self.turtleTag, "_bySpeed")
    
    def saveNoReliableGpsData(self):
        return TurtleData.checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.noReliableGpsDf, self.noReliableGpsDfCsvName)
    
    ## Remaining Data = No GPS and No Depth data
    def giveRemainingDataDf(self):        
        temporaryDfRemainingData = self.noGpsDf.copy()
        temporaryDfRemainingData = (temporaryDfRemainingData[~temporaryDfRemainingData['Dive Count'].notna()])        
        temporaryDfRemainingData.reset_index(drop=True, inplace=True) # reset index        
        print('Temporary No GPS AND NO DEPTH df is temporaryDfRemainingData')
        print(temporaryDfRemainingData)

        ##blankcolumns removed
        temporaryDfRemainingData = temporaryDfRemainingData.dropna(axis=1, how='all') # dropping all columns where are completely empty. '=' the equal signal means to say pandas, I want to modify the copy no the view
        temporaryDfRemainingData.reset_index(drop=True, inplace=True) # reset index 
        #temporaryDfRemainingData.drop(TurtleData.ID_NOGPSDATA_COLUMN_NAME, axis=1, inplace=True) # remove entire rows or columns based on their name.
        #print("----------without new id column and blank columns-----------")
        print("----------without blank columns-----------")
        print(temporaryDfRemainingData)
        print(f"Before cleaning, the remainingDataDf called: {self.remainingDataDfCsvName}, contained {len(temporaryDfRemainingData.index)} rows")
        print('--------------')
        duplicateRowsRemainingDataTemporaryDf = temporaryDfRemainingData
        duplicateRowsRemainingDataTemporaryDf = duplicateRowsRemainingDataTemporaryDf.drop_duplicates(
            [
                'Acquisition Time','Acquisition Start Time', 'Iridium CEP Radius', 'Iridium Latitude', 'Iridium Longitude', 'Temperature', 
                'Satellite Uplink', 'Receive Time', 'Repetition Count', 'Low Voltage', 'Saltwater Failsafe', 'Schedule Set', 'Diagnostic Dive Data'
            ], keep='first'
        )
        print(duplicateRowsRemainingDataTemporaryDf)
        print(duplicateRowsRemainingDataTemporaryDf.iloc[59:69,1])
        print(f"Without duplicated rows, the dataframe has now {len(duplicateRowsRemainingDataTemporaryDf.index)} rows")
        
        #### Eliminate test date before its Turtle tag day Datetime
        print("Excluding date BEFORE TAG DAY DATETIME")
        testDateRowsRemainingDataTemporaryDf = duplicateRowsRemainingDataTemporaryDf
        #print(testDateRowsTemporaryDf[testDateRowsTemporaryDf['Acquisition Time'].astype(str).str.startswith(self.tagDatetime)])
        ## listing days before
        print(testDateRowsRemainingDataTemporaryDf[testDateRowsRemainingDataTemporaryDf['Acquisition Time'] < self.tagDatetime])
        ## dropping them
        testDateRowsRemainingDataTemporaryDf.drop(testDateRowsRemainingDataTemporaryDf[testDateRowsRemainingDataTemporaryDf['Acquisition Time'] < self.tagDatetime].index, inplace=True)
        print("TEST -------------- TEST ------- TEST")
        print(self.tagDatetime)
        print(testDateRowsRemainingDataTemporaryDf)
        testDateRowsRemainingDataTemporaryDf.reset_index(drop=True, inplace=True) #reset index
        print('--------reset index------')
        print(testDateRowsRemainingDataTemporaryDf)
        print(f"Without days before turtle tag day, the dataframe has now {len(testDateRowsRemainingDataTemporaryDf.index)} rows")
        print("The df without duplicated rows and without days before turtle tag is the testDateRowsRemainingDataTemporaryDf")
        print('--------------')
        print("ALL THE DF THAT IS GONNA BE SAVE IN remainingDataDf DATAFRAME")
        print("Saving this temporary df into the remainingDataDf...")
        self.remainingDataDf = self.remainingDataDf.append(testDateRowsRemainingDataTemporaryDf, ignore_index=True)
        print(self.remainingDataDf)
        print(self.remainingDataDf.iloc[59:69,1])
        print("The df without duplicated rows is now the self.remainingDataDf")

        #### Create new column for the new rows ID
        noDepthNoGpsId = self.remainingDataDf.index + 1
        self.remainingDataDf.insert(0, TurtleData.ID_REMAININGDATA_COLUMN_NAME, noDepthNoGpsId)
        print('No REMAINING DATA df WITH NEW ID COLUMN')
        print(self.remainingDataDf)
        print(' End of REMAINING DATA Df ^')
        print('--------------')
    
    def generateRemainingDataDfCsvName(self):
        # Last entry:
        lastEntry = self.remainingDataDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.remainingDataDfCsvName = TurtleData.basedNamesForCsv(lastEntry, "remainingDataDf", self.turtleTag)        

    def saveRemainingDataDf(self):
        return TurtleData.checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.remainingDataDf, self.remainingDataDfCsvName)
    # -------- end of Remaining Data

    def giveDepthDataDf(self): # depthDataDf
        ### DEPTH DATA
        temporaryDfDepthData = self.noGpsDf.copy()
        # List of columns that contains depth data on the original df
        # principal_depth_col_names
        columnsTempList = TurtleData.principal_depth_col_names.copy()
        for c in temporaryDfDepthData.columns:
            if c not in columnsTempList:
                # if it is not the column I'm looking for, drop it.
                temporaryDfDepthData.drop(c, inplace=True, axis=1)
            else:
                #remove the column for the list. This help me to know if the is missing some column I need in the rawdata
                columnsTempList.remove(c)            
        print(temporaryDfDepthData)
        print('-----------------------')
        # if remains some column in this list, means that this column is missing on the rawdata
        if columnsTempList:
            print("Some data is missing!")        
        ## eliminate those Depth's null (NaN) rows from the dataframe
        ## eliminate all the rows that are not Dive informations
        temporaryDfDepthData.drop(temporaryDfDepthData[~temporaryDfDepthData['Dive Count'].notna()].index, inplace=True)
        temporaryDfDepthData.reset_index(drop=True, inplace=True) #reset index
        print(temporaryDfDepthData)
        print(temporaryDfDepthData.dtypes)
        #--------------------------
        #converting number to percentage in layer columns
        #df.sport = df.sport.apply(lambda x: 'ball sport' if 'ball' in x else x)

        temporaryDfDepthData['Underwater Percentage'] = temporaryDfDepthData['Underwater Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 1 Percentage'] = temporaryDfDepthData['Layer 1 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 2 Percentage'] = temporaryDfDepthData['Layer 2 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 3 Percentage'] = temporaryDfDepthData['Layer 3 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 4 Percentage'] = temporaryDfDepthData['Layer 4 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 5 Percentage'] = temporaryDfDepthData['Layer 5 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 6 Percentage'] = temporaryDfDepthData['Layer 6 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 7 Percentage'] = temporaryDfDepthData['Layer 7 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 8 Percentage'] = temporaryDfDepthData['Layer 8 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 9 Percentage'] = temporaryDfDepthData['Layer 9 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))
        temporaryDfDepthData['Layer 10 Percentage'] = temporaryDfDepthData['Layer 10 Percentage'].apply(lambda x: str(x).replace('%', '') if '%' in str(x) else "%.3f" %float(x*100))

        print(temporaryDfDepthData)

        #Changing data type of multiple columns 
        #df['Percent'] = df['Grade'].astype(str) + '%'

        temporaryDfDepthData['Underwater Percentage'] = temporaryDfDepthData['Underwater Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 1 Percentage'] = temporaryDfDepthData['Layer 1 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 2 Percentage'] = temporaryDfDepthData['Layer 2 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 3 Percentage'] = temporaryDfDepthData['Layer 3 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 4 Percentage'] = temporaryDfDepthData['Layer 4 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 5 Percentage'] = temporaryDfDepthData['Layer 5 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 6 Percentage'] = temporaryDfDepthData['Layer 6 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 7 Percentage'] = temporaryDfDepthData['Layer 7 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 8 Percentage'] = temporaryDfDepthData['Layer 8 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 9 Percentage'] = temporaryDfDepthData['Layer 9 Percentage'].astype(str) + '%'
        temporaryDfDepthData['Layer 10 Percentage'] = temporaryDfDepthData['Layer 10 Percentage'].astype(str) + '%'

        print(temporaryDfDepthData.dtypes)
        
        #--------------------------
        print(f"Before cleaning, the depthDataDf called: {self.depthDataDfCsvName}, contained {len(temporaryDfDepthData.index)} rows")
        print('--------------')
        duplicateRowsDepthDataTemporaryDf = temporaryDfDepthData
        duplicateRowsDepthDataTemporaryDf = duplicateRowsDepthDataTemporaryDf.drop_duplicates(
            [
                'Acquisition Time','Acquisition Start Time', 'Dive Count', 'Average Dive Duration', 'Maximum Dive Depth',
                'Layer 1 Dive Count', 'Layer 2 Dive Count', 'Layer 3 Dive Count'
            ], keep='first'
        )
        print(duplicateRowsDepthDataTemporaryDf)
        print(duplicateRowsDepthDataTemporaryDf.iloc[59:69,1])
        print(f"Without duplicated rows, the dataframe has now {len(duplicateRowsDepthDataTemporaryDf.index)} rows")
        
        #### Eliminate test date before its Turtle tag day Datetime
        print("Excluding date BEFORE TAG DAY DATETIME")
        testDateRowsDepthDataTemporaryDf = duplicateRowsDepthDataTemporaryDf
        #print(testDateRowsTemporaryDf[testDateRowsTemporaryDf['Acquisition Time'].astype(str).str.startswith(self.tagDatetime)])
        ## listing days before
        print(testDateRowsDepthDataTemporaryDf[testDateRowsDepthDataTemporaryDf['Acquisition Time'] < self.tagDatetime])
        ## dropping them
        testDateRowsDepthDataTemporaryDf.drop(testDateRowsDepthDataTemporaryDf[testDateRowsDepthDataTemporaryDf['Acquisition Time'] < self.tagDatetime].index, inplace=True)
        print("TEST -------------- TEST ------- TEST")
        print(self.tagDatetime)
        print(testDateRowsDepthDataTemporaryDf)
        testDateRowsDepthDataTemporaryDf.reset_index(drop=True, inplace=True) #reset index
        print('--------reset index------')
        print(testDateRowsDepthDataTemporaryDf)
        print(f"Without days before turtle tag day, the dataframe has now {len(testDateRowsDepthDataTemporaryDf.index)} rows")
        print("The df without duplicated rows and without days before turtle tag is the testDateRowsDepthDataTemporaryDf")
        print('--------------')
        print("ALL THE DF THAT IS GONNA BE SAVE INTO the depthDataDf DATAFRAME")
        print("Saving this temporary df into the depthDataDf...")
        self.depthDataDf = self.depthDataDf.append(testDateRowsDepthDataTemporaryDf, ignore_index=True)
        print(self.depthDataDf)
        print(self.depthDataDf.iloc[59:69,1])         
        print("The df without duplicated rows and without days before turtle tag is now the self.depthDataDf")

        #### Create new column for the new rows ID
        depthId = self.depthDataDf.index + 1
        self.depthDataDf.insert(0, TurtleData.ID_DEPTHDATA_COLUMN_NAME, depthId)
        print('depthDataDf WITH NEW ID COLUMN')
        print(self.depthDataDf)
        print(self.depthDataDf.dtypes) 
        print(' End of depthDataDf ^')
        print('--------------')
    
    def generateDepthDataDfCsvName(self):
        # Last entry:
        lastEntry = self.depthDataDf['Acquisition Time'].tail(1)
        #print(lastEntry)
        # separing date from time in that column
        lastEntry = pd.Series([[y for y in x.split()] for x in lastEntry])
        #print(lastEntry)
        # assign the Name in the Class Variable
        self.depthDataDfCsvName = TurtleData.basedNamesForCsv(lastEntry, "depthDataDf", self.turtleTag)

    def saveDepthDataDf(self):
        return TurtleData.checkIfDfHasBeenSavedAndSaveDf(self.DATACLEANINGRESULTS_FOLDER_ITENS, self.DATACLEANINGRESULTS_FOLDER , self.depthDataDf, self.depthDataDfCsvName)

    # Create Points Shapefiles of GPS points and SAVE IT
    ##-------Create GeoPandas GeoDataFrame using the Pandas DataFrame dfGpsRoute, 
    # with the corresponding entries for the geometry column
    #self.reliableGpsDf
    #def createGeometryColumnForReliableGpsDf(self):
        #geoGpsDf = gpd.GeoDataFrame(self.reliableGpsDf, geometry = gpd.points_from_xy(self.reliableGpsDf['GPS Longitude'], self.reliableGpsDf['GPS Latitude']), crs="EPSG:4326")
        # not working, because I could not install geopandas inside pipenv
    
    # create a plot of the track
    def createLinesWithoutProjection(self, color):
        #This create all the points connected with lines!!
        ##It is this what I need to transform into shapefile
        i=0
        while(i < len(self.reliableGpsDf['GPS Latitude'])-1):
            x1, y1 = self.reliableGpsDf['GPS Longitude'][i], self.reliableGpsDf['GPS Latitude'][i]
            x2, y2 = self.reliableGpsDf['GPS Longitude'][i+1], self.reliableGpsDf['GPS Latitude'][i+1]
            plt.plot([x1, x2], [y1, y2], color=color, marker = 'o',markersize = 1)
            i+=1
    
    def convertCoordinatesIntoMapProjection(self, color):
        '''
        Converts from longitude,latitude to native map projection x,y coordinates
        '''
        #coordinatesColumnsArray = self.reliableGpsDf[['GPS Longitude', 'GPS Latitude']].to_numpy()
        ##Put the Longitude values inside a numpy_array
        xlon = self.reliableGpsDf['GPS Longitude'].to_numpy()        
        ##Put the Latitudes values inside a numpy_array
        ylat = self.reliableGpsDf['GPS Latitude'].to_numpy()        
        acTime = self.reliableGpsDf['Acquisition Time'].to_numpy()
        
        #------
        print(f"THE XLON ARRAY WITHOUT PUT INSIDE THE OBJECT IS: {xlon}")
        print(type(xlon))
        print("Size of the array: ", xlon.size)
        print("Length of one array element in bytes: ", xlon.itemsize)
        print("Total bytes consumed by the elements of the array: ", xlon.nbytes)
        #------
        print(f"THE ylat ARRAY WITHOUT PUT INSIDE THE OBJECT IS: {ylat}")
        print(type(ylat))
        print("Size of the array: ", ylat.size)
        print("Length of one array element in bytes: ", ylat.itemsize)
        print("Total bytes consumed by the elements of the array: ", ylat.nbytes)
        #------
        print(f"THE XLON ARRAY WITHOUT PUT INSIDE THE OBJECT IS: {acTime}")
        print(type(acTime))
        print("Size of the array: ", acTime.size)
        print("Length of one array element in bytes: ", acTime.itemsize)
        print("Total bytes consumed by the elements of the array: ", acTime.nbytes)

        # passing array to the obj
        #self.xlon_np = np.array([])
        #self.xlat_np = np.array([])
        #self.acquisitionTime_np = np.array([])
        #example:
        self.xlon_np = np.append(self.xlon_np, xlon)
        self.xlat_np= np.append(self.xlat_np, ylat)
        self.acquisitionTime_np = np.append(self.acquisitionTime_np, acTime)

        ## initialize a Proj class instance
        ## example:
        ## p = Proj('+proj=utm +zone=10 +ellps=WGS84') # use proj4 string
        ## x,y = p(-120.108, 34.36116666)
        ##wgs84 = Proj('+proj=longlat +datum=WGS84 +no_defs') # http://epsg.io/4326
        p = Proj(self.proj4)
        x, y = p(xlon, ylat)
        ## Create lines in projection
        i=0
        while(i < len(ylat)-1):
            x1, y1 = x[i], y[i]
            x2, y2 = x[i+1], y[i+1]
            plt.plot([x1, x2], [y1, y2], color=color, marker = 'o',markersize = 1)
            i+=1
        # ## Create lines in projection
        # i=0
        # while(i < len(ylat)-1):
        #     x1, y1 = p(xlon[i], ylat[i])
        #     x2, y2 = p(xlon[i+1], ylat[i+1])
        #     plt.plot([x1, x2], [y1, y2], color=color, marker = 'o',markersize = 1)
        #     i+=1
        
    def viewTheCoordinateReferenceSystemCrsAssociated(self):
        print("The CRS of this data is:", self.crs)
    
    def viewArrays(self):        
        print("The xlon numpy array is:", self.xlon_np)
        print(type(self.xlon_np))     
        print("Size of the array: ", self.xlon_np.size)
        print("Length of one array element in bytes: ", self.xlon_np.itemsize)
        print("Total bytes consumed by the elements of the array: ", self.xlon_np.nbytes)
        #------
        print("The xlat numpy array is:", self.xlat_np)
        print(type(self.xlat_np))  
        print("Size of the array: ", self.xlat_np.size)
        print("Length of one array element in bytes: ", self.xlat_np.itemsize)
        print("Total bytes consumed by the elements of the array: ", self.xlat_np.nbytes)
        #------
        print("The xlat numpy array is:", self.acquisitionTime_np)
        print(type(self.acquisitionTime_np))  
        print("Size of the array: ", self.acquisitionTime_np.size)
        print("Length of one array element in bytes: ", self.acquisitionTime_np.itemsize)
        print("Total bytes consumed by the elements of the array: ", self.acquisitionTime_np.nbytes)
    
    # to do Create_Half_Time_Depth_Point
    # gdf and df to numpy
    ### gpsDataNumpyArray = self.reliableGpsDf.to_numpy()
    ### depthDataNumpyArray = self.depthDataDf.to_numpy()
    # reliableGpsDF lat, lon and acquisition time into numpy array for faster calculations
        #self.xlon_np = np.array([])
        #self.xlat_np = np.array([])
        #self.acquisitionTime_np = np.array([])
    #def createHalfTimeDepthPoint(self):