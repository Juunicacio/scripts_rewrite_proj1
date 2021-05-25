import pandas as pd
import os
import pyproj as pj # for reliable gps
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
    def calculateDistance(geodRef, lat1, lon1, lat2, lon2):
        v1,v2,dist = geodRef.inv(lat1,lon1,lat2,lon2) #Take the second row and the first row on the count. it shoul give 3 values, but I only need the dist.
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
        self.df = pd.DataFrame()
        self.allGpsDf = pd.DataFrame()
        self.allGpsDfCsvName = ""
        self.allGpsDf2019 = pd.DataFrame()
        self.allCleanedGpsDf = pd.DataFrame()
        self.reliableGpsDf = pd.DataFrame()
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
        for value in enumerate(lastEntry):
            #print(value[1][0])
            lastDate = value[1][0]
            date = dt.datetime.strptime(lastDate, "%Y.%m.%d")
            stringDate = date.strftime("%Y") + "_" + date.strftime("%b")
            print(f"The Last Entry in the Dataframe for {self.turtleTag} is from: ")
            print(stringDate)
            # Give the CSV a Name based on this values above
            # name = allGpsDf_tag_xxxxx_until_lastdate
            cvsName = "allGpsDf" + "_Tag_" + self.turtleTag + "_" + stringDate +".csv"
            print(f"The Name of the allGpsDf CSV for the turtleData {self.turtleTag} is: ")
            print(cvsName)
            print('--------------')
            self.allGpsDfCsvName = cvsName
    
    def saveAllGpsData(self, pathToFilePlusCsvName):
        self.allGpsDf.to_csv(pathToFilePlusCsvName, index=False)
    
    def giveAllCleanedGpsDf(self):
        # without 2019 date and without duplicate rows
        self.allCleanedGpsDf = self.allGpsDf.copy()
        print(f"Before cleaning, the AllGpsDf called: {self.allGpsDfCsvName}, contained {len(self.allCleanedGpsDf.index)} rows")
        
        ##### ---------- This Part is not needed ---------- #####
        # Remove 2019 data from 'Acquisition Time column:
        dateColumn = self.allCleanedGpsDf['Acquisition Time']
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
        self.allCleanedGpsDf.drop(self.allCleanedGpsDf[self.allCleanedGpsDf['Acquisition Time'].astype(str).str.startswith('2019')].index, inplace=True)
        self.allCleanedGpsDf.reset_index(drop=True, inplace=True) # reset index
        #print(self.allCleanedGpsDf)
        print(f"After removing 2019 data, the AllGpsDf called: {self.allGpsDfCsvName}, contained {len(self.allCleanedGpsDf.index)} rows")

        ## To save 2019 DF
        # self.allGpsDf2019 = self.allCleanedGpsDf.drop(self.allCleanedGpsDf[~self.allCleanedGpsDf['Acquisition Time'].astype(str).str.startswith('2019')].index, inplace=True)
        #self.allGpsDf2019.reset_index(drop=True, inplace=True) # reset index
        #print(self.allGpsDf2019)
        #print(self.allCleanedGpsDf)

        ### Eliminate duplicate rows
        # Select duplicate rows except first occurrence based on all columns
        ## example of Selection by Position, to see example duplicated rows ----------------------------------
        ## df.iloc[row_indexer,column_indexer]
        ##duplicateRowsTemporaryDf = self.allCleanedGpsDf.iloc[13:19,1]
        ##duplicateRowsTemporaryDf = duplicateRowsTemporaryDf.drop_duplicates(keep='first')
        ##print(duplicateRowsTemporaryDf)
        ## END of example ----------------------------------
        # Creating a TemporaryDf to save the duplicated rows
        # duplicateRowsTemporaryDf = self.allCleanedGpsDf.copy()
        # duplicateRowsTemporaryDf = duplicateRowsTemporaryDf.duplicated(
        #     [
        #         'Acquisition Time','Acquisition Start Time', 'GPS Fix Time', 'GPS Fix Attempt', 'GPS Latitude', 'GPS Longitude'
        #     ], keep='first'
        # )
        # print(f"The duplicated rows in the {self.allGpsDfCsvName} are in the duplicateRowsTemporaryDf: ")
        # print(duplicateRowsTemporaryDf)
        # print(f"with {len(duplicateRowsTemporaryDf.index)} rows")
        # print(duplicateRowsTemporaryDf.iloc[13:19,1])

        # Removing duplicated rows, to later save the new allCleanedGpsDf csv:
        print(f"Removing duplicated rows data from the {self.allGpsDfCsvName}...")
        print("Saving the allCleanedGpsDf without duplicated rows...")
        self.allCleanedGpsDf.drop_duplicates(
            [
                'Acquisition Time','Acquisition Start Time', 'GPS Fix Time', 'GPS Fix Attempt', 'GPS Latitude', 'GPS Longitude'
            ], keep='first'
        )
        self.allCleanedGpsDf.reset_index(drop=True, inplace=True) # reset index
        print("The allCleanedGpsDf is now without duplicated rows!")
        print(self.allCleanedGpsDf)
        print(f"And it contains {len(self.allCleanedGpsDf.index)} rows")
        print(self.allCleanedGpsDf.iloc[13:19,1])

        # see if I can save the removed duplicated rows
        
        

            

    # def giveReliableGpsDf(self):

    #     # BEFORE CALCULATE THIS, WE NEED TO REMOVE THE DUPLICATES ROW
    #     '''
    #     Remove GPS Errors by Angular velocity/Rotational speed 
    #     (degree per second)
    #     Geod Object for Calculations is used as objec to calculate 
    #     distances between points expressed in lat/lon (in degree)
    #     Choosing a Reference Ellipsoid - distance in degree more 
    #     accurate than a spherical method	
    #     '''
    #     self.reliableGpsDf = self.allGpsDf.copy()
    #     wgs84_geod = pj.Geod(ellps='WGS84')
    #     # Converting data to a NumPy array.
    #     latitudes = self.reliableGpsDf[['GPS Latitude']].to_numpy() 
    #     longitudes = self.reliableGpsDf[['GPS Longitude']].to_numpy()
    #     acquisitionTimes = self.reliableGpsDf[['Acquisition Time']].to_numpy()

    #     distances = []
    #     tripTimes = []
    #     speeds = []
    #     pointsToRemove = []
    #     remSpeeds = []
        
    #     distances.append(0)
    #     tripTimes.append(0)
    #     speeds.append(0)

    #     i=1
    #     while i < (len(latitudes)):
    #         foundS = False
    #         previous = i-1
    #         D = 0
    #         S = 100		
    #         while (S > 1.111) and (i < len(latitudes)):
    #             D = TurtleData.calculateDistance(wgs84_geod,latitudes[previous],longitudes[previous],latitudes[i],longitudes[i])
    #             t1 = TurtleData.convertUnixTimeFromString(acquisitionTimes[previous,0])
    #             t2 = TurtleData.convertUnixTimeFromString(acquisitionTimes[i,0])
    #             S = TurtleData.calculateSpeed(D,t1,t2)
    #             if(S > 1.111):
    #                 remSpeeds.append(S)
    #                 pointsToRemove.append(acquisitionTimes[i,0])
    #                 i+=1
    #             else:
    #                 foundS = True
    #         if(foundS):
    #             distances.append(D)
    #             tripTimes.append(t2-t1)
    #             speeds.append(S)
    #         i+=1
    #     #---------	
    #     # Saving Removed Points in another dataframe and dropping those out from this one
    #     removedPointsRow = self.reliableGpsDf[self.reliableGpsDf['Acquisition Time'].isin(pointsToRemove)]
    #     removedPointsRow.loc[:,'Speeds > 1,11111 m/s'] = remSpeeds
    #     # reseting index
    #     removedPointsRow.reset_index(drop=True, inplace=True) 
    #     removedGPSPoints = removedPointsRow.index + 1 
    #     # Creating a Column for ID Removed Track Points on the Left
    #     removedPointsRow.insert(0, 'Qty', removedGPSPoints) 
    #     # Saving the amount of removed points data
    #     qtyremovedGPSpointsSept = len(removedPointsRow.index) 
    #     print(f'QTY OF REMOVED POINTS: {qtyremovedGPSpointsSept}')
        
    #     # Count Occurrence of a value in 'GPS Fix Attempt' Column
    #     cntOccurrFixAttemptRemovedPoints = Counter(removedPointsRow['GPS Fix Attempt'])
    #     print('Qty Fix Attempt Of Removed Points:') 
    #     print(cntOccurrFixAttemptRemovedPoints)
    #     print('-----------------------')
        
    #     # EXPORTING REMOVED POINTS DATA
    #     #removedPointsRow.to_csv('Removed_Points_GPS_Data_Tag_333A_Sept.csv', index=False) # Calling DataFrame constructor on list	
        
    #     self.reliableGpsDf.drop(self.reliableGpsDf[self.reliableGpsDf['Acquisition Time'].isin(pointsToRemove)].index, inplace=True)	
        
    #     #-----------------------------------------------------------
    #     #Complete the new columns and save only reliable GPS points excluded through speed
        
    #     self.reliableGpsDf.reset_index(drop=True, inplace=True) # reset index
    #     routePoints = self.reliableGpsDf.index + 1 
    #     self.reliableGpsDf.insert(0, 'Tracked Points', routePoints) # Create a ID Column on the Left for the Tracked Points 
                
    #     self.reliableGpsDf.drop(['ID GPS Points'], axis=1, inplace=True)
        
    #     # Add the list values as New Columns of the DataFrame
    #     self.reliableGpsDf['Length (m)'] = distances
    #     self.reliableGpsDf['Length (m)'] = self.reliableGpsDf['Length (m)'].str[0] #remove the brackets of the values in the column
    #     self.reliableGpsDf['Time (s)'] = tripTimes
    #     self.reliableGpsDf['Speed m/s'] = speeds
    #     self.reliableGpsDf['Speed m/s'] = self.reliableGpsDf['Speed m/s'].str[0] #remove the brackets of the values in the column	
    #     #print(df.dtypes)
    #     self.reliableGpsDf['Time (h)'] = pd.to_timedelta(self.reliableGpsDf['Time (s)'], unit='s') # Add a Column with the Time passed from on Point to another in hours
