import pandas as pd
import os

class TurtleData:
    """Commom base class for all turtle's data """

    # CELL_REPORT_SUPPLIER = 'A1'
    # CELL_REPORT_FORMAT = 'B2'
    # CELL_HEADERS_ROW = 'B3'
    # CELL_DATA_SOURCE = 'B4'
    # CELL_TDC_VERSION = 'B5'

    # CELL_CTN_TAG = 'B7'
    # CELL_COMMENT = 'B8'
    # CELL_IRIDIUM_IMEI = 'B9'

    # REPORT_PERIOD_BEGINS = 'B11'
    # REPORT_PERIOD_ENDS = 'B12'
    
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
    
    def __init__(self, tag):
        #self.supplier = 'A1' #temporaryDf['A1']
        #self.__dict__= {}
        self.turtleTag = tag
        self.df = pd.DataFrame()
        #self.header_row = []
        #self.specific_turtle_dfs_list = []
        #self.df = self.df.reindex(columns = list(self.header_row)) 
        #self.df.columns = list(self.header_row)

        #self.df = pd.DataFrame({'Empty' : []})
        #df = df.reindex(columns = header_list) 
        #mydf = mydf.reindex(mydf.columns.tolist() + ['newcol1','newcol2'], axis=1)  # version > 0.20.0
    
    #def __repr__(self):
        #return self.turtleTag
    def addElement(self, row, header):
        self.__dict__= dict(zip(header, row))

    def addDataFromCsv(self, filename):
        #print(os.path.abspath(os.getcwd()))
        #def readFile(self, fileName):
        #temporaryDf = pd.read_csv(filename, names=TurtleData.col_names) # error_bad_lines=False)# , index_col=False, sep='delimiter', header=None)
        #temporaryDf = pd.read_csv(filename, skiprows=23, header=None)
        temporaryDf = pd.read_csv(filename, skiprows=23, names=TurtleData.col_names)
        #temporaryDf = pd.read_csv(file, index_col=False)
        
        # Remove/Change Header
        #header_row = temporaryDf.iloc[21] # Take Row 21 # Finding the Data Header
        
        # Cancel the Index Column Name to None
        #header_row.name = ''
        
        # Filter/Remove the Satellite Informations in the First Lines
        #temporaryDf = temporaryDf[22:]
        
        # Drop the Satellite Informations, to access only the data
        #temporaryDf.drop(temporaryDf.index[0:21])
        # Set the new Header
        #temporaryDf.columns = list(header_row)
        
        # Reset Index
        #temporaryDf.reset_index(drop=True, inplace=True)

        #self.df.reset_index(drop=True, inplace=True)
        #self.specific_turtle_dfs_list.append(temporaryDf)

        #self.df = temporaryDf.reindex(columns = header_row)
        #self.header_row = header_row
        #self.df = self.df.reindex(columns = list(self.header_row)) 
        #self.df.columns = self.header_row
        
        print(f' CURRENT DF IS {self.df}') 
        print(f' TEMPORARY DF IS {temporaryDf}') 
        
        self.df = self.df.append(temporaryDf, ignore_index=True)
        self.df.sort_values("Acquisition Time", inplace = True)

        #print(f' CURRENT DF IS {self.df}') 
        # sorting by Acquisition Time
        #self.df.loc[67:,:]
        #print(f' VIEW OF DUPLICATES {self.df.loc[67:,:]}')
        #self.df.sort_values("Acquisition Time", inplace = True)
        #print(f' VIEW OF DUPLICATES {self.df.loc[67:,:]}')
        #print(f' CURRENT DF IS {self.df}') 

        # dropping ALL duplicte values based on two columns
        #self.df = self.df.drop_duplicates(subset = ['Acquisition Time', 'Acquisition Start Time'], keep = 'last')#.reset_index(drop = True, inplace=True)
        #self.df.reset_index(drop = True, inplace=True)
        #print(f' CURRENT DF IS {self.df}') 

        #frame = pd.concat(li, axis=0, ignore_index=True)
        #for df in self.specific_turtle_dfs_list:
        #self.df.concat((df for df in specific_turtle_dfs_list), axis=0, ignore_index=True)
        
        #print(f' The self.df of {filename} is now: {self.df}') 


        # start = temporaryDf (CELL_HEADER_START)
        # temporaryDf.removeTUTToprima(start)
        # self.df.aggiungi temporaryDf
        #return print(df)

    def getTag(self):
        return self.turtleTag

    def getDf(self):
        #self.df.set_option("display.max_rows", None, "display.max_columns", None)
        return self.df
#     def getTurtleGpsData():



# turtlecsv1 = TurtleCsv("nomefile")
# turtlecsv2 = TurtleCsv("710blblba")
# . 
# .
# .

# turtlecsv1.turtleTag()


# turtledata1 = TurtleData(710333A)
# turtledata2 = TurtleData(710348A)

# turtledata1.addData(710333A_93 Condensed.csv)