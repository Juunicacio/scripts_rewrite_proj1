import pandas as pd
import os

class TurtleData:
    """Commom base class for all turtle's data """

    CELL_REPORT_SUPPLIER = 'A1'
    CELL_REPORT_FORMAT = 'B2'
    CELL_HEADERS_ROW = 'B3'
    CELL_DATA_SOURCE = 'B4'
    CELL_TDC_VERSION = 'B5'

    CELL_CTN_TAG = 'B7'
    CELL_COMMENT = 'B8'
    CELL_IRIDIUM_IMEI = 'B9'

    REPORT_PERIOD_BEGINS = 'B11'
    REPORT_PERIOD_ENDS = 'B12'
    
    def __init__(self, tag):
        self.supplier = 'A1' #temporaryDf['A1']
        self.turtleTag = tag
        self.df = pd.DataFrame()
        self.header_row = []
        #self.specific_turtle_dfs_list = []
        #self.df = self.df.reindex(columns = list(self.header_row)) 
        #self.df.columns = list(self.header_row)

        #self.df = pd.DataFrame({'Empty' : []})
        #df = df.reindex(columns = header_list) 
        #mydf = mydf.reindex(mydf.columns.tolist() + ['newcol1','newcol2'], axis=1)  # version > 0.20.0
        

    def addDataFromCsv(self, folder_obj, filename):
        #def readFile(self, fileName):
        temporaryDf = pd.read_csv(os.path.join(folder_obj, filename))#, index_col=False)
        #temporaryDf = pd.read_csv(file, index_col=False)
        # Remove/Change Header
        header_row = temporaryDf.iloc[21] # Take Row 21 # Finding the Data Header
        # Cancel the Index Column Name to None
        header_row.name = ''
        # Filter/Remove the Satellite Informations in the First Lines
        temporaryDf = temporaryDf[22:]
        # Drop the Satellite Informations, to access only the data
        temporaryDf.drop(temporaryDf.index[0:21])
        # Set the new Header
        temporaryDf.columns = list(header_row)
        # Reset Index
        temporaryDf.reset_index(drop=True, inplace=True)

        #self.specific_turtle_dfs_list.append(temporaryDf)

        #self.df = temporaryDf.reindex(columns = header_row)
        self.header_row = header_row
        self.df = self.df.reindex(columns = list(self.header_row)) 
        #self.df.columns = self.header_row
        self.df = self.df.append(temporaryDf)
        #frame = pd.concat(li, axis=0, ignore_index=True)
        #for df in self.specific_turtle_dfs_list:
        #self.df.concat((df for df in specific_turtle_dfs_list), axis=0, ignore_index=True)
        
        print(f' The self.df of {filename} is now: {self.df}') 


        # start = temporaryDf (CELL_HEADER_START)
        # temporaryDf.removeTUTToprima(start)
        # self.df.aggiungi temporaryDf
        #return print(df)

    def getTag(self):
        return self.turtleTag

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