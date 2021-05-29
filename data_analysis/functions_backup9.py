import pandas as pd
import os
from turtleData import TurtleData
import datetime as dt # to create csv names

# To run with Debug:
DIRNAME = os.path.dirname(__file__)
ASSETS_FOLDER = os.path.join(DIRNAME, 'assets')
##ASSETS_FOLDER_OBJ = "data_analysis\\assets"
ASSETS_FOLDER_ITENS = os.listdir(ASSETS_FOLDER)# ("data_analysis/assets")

DATACLEANINGRESULTS_FOLDER = os.path.join(DIRNAME, 'dataCleaningResults')
DATACLEANINGRESULTS_FOLDER_ITENS = os.listdir(DATACLEANINGRESULTS_FOLDER)# ("data_analysis/dataCleaningResults")

# To run with terminal OR jupyter notebook:
#ASSETS_FOLDER = "assets"
#ASSETS_FOLDER_ITENS = os.listdir(ASSETS_FOLDER)# ("assets")

#DATACLEANINGRESULTS_FOLDER = "dataCleaningResults"
#DATACLEANINGRESULTS_FOLDER_ITENS = os.listdir(DATACLEANINGRESULTS_FOLDER)# ("data_analysis/dataCleaningResults")

TAG_TURTLE_1 = '710333a'
DATE_TAG_TURTLE_1 = '2020.07.09'
TIME_TAG_TURTLE_1 = '23:00:09'

TAG_TURTLE_2 = '710348a'
DATE_TAG_TURTLE_2 = '2020.08.12'
TIME_TAG_TURTLE_2 = '02:00:11'

INITIAL_TAG_DIGITS = '7103'

# Replace spaces in filenames with underlines
def replace_space_with_underline(file_name):
    return file_name.replace(" ", "_")

# Convert excel files into csv
def converting_excel_file_into_csv_file(folder_obj, file):        
    # read excel   
    df_xlsx = pd.read_excel(os.path.join(folder_obj, file))
    # change file format
    file_in_csv = file.replace(".xlsx", ".csv")
    # transform excel to csv file with path to store the CSV file
    df_xlsx.to_csv(os.path.join(folder_obj, file_in_csv), index = False)        

# Check if some excel file has not been converted into csv yet
def check_for_excel_files():
    all_my_files = []
    n = 0
    for file in ASSETS_FOLDER_ITENS:
        # put all the file names in the same format
        file = replace_space_with_underline(file).lower()
        all_my_files.append(file)
    
    # Create a copy of list
    for file in all_my_files[:]:
        if file.endswith('.xlsx'):
            print('- Excel file = ' + file)
            file_name = file.split('.', 1)[0] # remove everything (the format) after the dot
            # remove the excel file from my all_my_files list
            all_my_files.remove(file)            
            # check if another file with the same name in the folder exists
            if any(file_name in word for word in all_my_files):            
                print(f"-- Excellent! We've already converted the excel file \'{file_name}\' into csv file")
            else:
                print(f'-- Oh No! The excel file \'{file_name}\' has been not converted. Converting it into csv file...')
                # Call function "Convert excel files into csv"
                converting_excel_file_into_csv_file(ASSETS_FOLDER, file)
                file_in_csv = file.replace(".xlsx", ".csv") 
                all_my_files.append(file_in_csv)
                print('---> ' + file_in_csv + ' has been created!')
                
    # Updated all_my_files List
    print('--- CSV files in the assets folder: ', all_my_files)

def getTurtlesData():
    split_char = '_'
    csvs = []        
    turtlesData = []
    #turtleDfs = []
    for file in ASSETS_FOLDER_ITENS:
        if file.endswith('.csv'):
            # put all the file names in the same format
            csv_string_filename = replace_space_with_underline(file).lower()
            filename_splitted = csv_string_filename.split(split_char)                        
            for word in filename_splitted:
                if word.startswith(INITIAL_TAG_DIGITS):
                    csvs.append(file)
                    currentFileCsv = ASSETS_FOLDER + '\\' + file
                    print('--------------')
                    print("Found TAG ("+ word +") in filename , check if tag is already associated with an object...")

                    #--------------------
                                
                    foundTurtleData = None
                    # check inside the list if the turtle has already been created with that tag (word)
                    for obj in turtlesData:
                        if obj.getTag() == word:
                            foundTurtleData = obj
                            break    
                    #--------------------    
                                    
                    if foundTurtleData == None:
                        print("Instance for TAG ("+ word +") NOT found! Creating a new instance...")
                        # create a TurtleData obj with the turtle tag
                        foundTurtleData = TurtleData(word)
                        turtlesData.append(foundTurtleData)
                        print("Instance for TAG ("+ word +") CREATED!")
                    else:
                        print("Instance for TAG ("+ word +") ALREADY EXISTS, skipping object creation!")
                        print('--------------')

                    # for the instances turtleData objs in the list (for each turtle tag):
                    foundTurtleData.addDataFromCsv(currentFileCsv)                    

    return turtlesData

def checkInstancesAndItsDfs(turtlesData):
    print('Created instances for Obj turtleData: ')
    for turtleData in turtlesData:        
        print(turtleData.getTag())
    print('--------------')
    print('Created Dataframes: ')
    i = 0
    for turtleData in turtlesData: 
        print(f'turtlesData[{i}].df')
        print(turtleData.turtleTag)
        print(turtleData.df)
        print('--------------')
        i+=1

def getAllGpsDataframes(turtlesData):
    for turtleData in turtlesData:
        turtleData.giveAllGpsDf()

def displayAllGpsDf(turtlesData):
    i = 0
    for turtleData in turtlesData:
        print(f'turtlesData[{i}].allGpsDf')
        print(turtleData.turtleTag)
        print(turtleData.allGpsDf)

def createAllGpsDfCsvNameForEachInstance(turtlesData):
    # create a AllGpsDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateAllGpsDfCsvName()

def checkIfAllGpsDfHasBeenSaved(turtlesData):
    filesInResultsFolder = []    
    
    for file in DATACLEANINGRESULTS_FOLDER_ITENS:
        filesInResultsFolder.append(file)    
    print(filesInResultsFolder)

    for turtleData in turtlesData:
        if not filesInResultsFolder:
            print(f"The filename {turtleData.allGpsDfCsvName} is not yet in the folder... saving csv")
            pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allGpsDfCsvName)
            turtleData.saveAllGpsDfData(pathToFilePlusCsvName)
            print(f"{turtleData.allGpsDfCsvName} has been saved in the results folder!")
            #append file in list

        elif turtleData.allGpsDfCsvName in filesInResultsFolder:
            print(f"The CSV {turtleData.allGpsDfCsvName} has already been saved in the results folder")
        else:
            print(f"The filename {turtleData.allGpsDfCsvName} is not yet in the folder... saving csv")
            pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allGpsDfCsvName)
            turtleData.saveAllGpsDfData(pathToFilePlusCsvName)

def assignTagDayDatetimeToEachInstance(turtlesData):
    notFoundTurtleTagDatetime = False
    for turtleData in turtlesData:
        if turtleData.getTag() == TAG_TURTLE_1:
            turtleData.assignTagTurtleDayDatetime(DATE_TAG_TURTLE_1, TIME_TAG_TURTLE_1)
        elif turtleData.getTag() == TAG_TURTLE_2:
            turtleData.assignTagTurtleDayDatetime(DATE_TAG_TURTLE_2, TIME_TAG_TURTLE_2)
        else:
            notFoundTurtleTagDatetime = True
            print("Attention!")
            print(f"{turtleData.turtleTag} has not a Tag Datetime yet!")
        # for obj in Class, print its tagDatetime
        print("For obj in Class, print its tagDatetime")
        print(turtleData.tagDatetime)
    if not notFoundTurtleTagDatetime:
        print("Tag Datetime for all instances assign!")
    
def getAllCleanedGpsDataframes(turtlesData):
    for turtleData in turtlesData:
        turtleData.giveAllCleanedGpsDf()

def createAllCleanedGpsDfCsvNameForEachInstance(turtlesData):
    # create a allCleanedGpsDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateAllCleanedGpsDfCsvName()

def checkIfAllCleanedGpsDfHasBeenSaved(turtlesData):
    filesInResultsFolder = []    
    
    for file in DATACLEANINGRESULTS_FOLDER_ITENS:
        filesInResultsFolder.append(file)    
    print(filesInResultsFolder)

    for turtleData in turtlesData:
        if not filesInResultsFolder:
            ## Saving AllGpsDf Data 
            #print(f"The filename {turtleData.allGpsDfCsvName} is not yet in the folder... saving csv")
            #pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allGpsDfCsvName)                       
            #turtleData.saveAllGpsData(pathToFilePlusCsvName)
            #print(f"{turtleData.allGpsDfCsvName} has been saved in the results folder!")            
            #print('--------------')
            ## Saving AllCleanedGps Data
            print(f"The filename {turtleData.allCleanedGpsDfCsvName} is not yet in the folder... saving csv")
            pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allCleanedGpsDfCsvName)
            turtleData.saveAllCleanedGpsDfData(pathToFilePlusCsvName)
            print(f"{turtleData.allCleanedGpsDfCsvName} has been saved in the results folder!")

        #elif turtleData.allGpsDfCsvName in filesInResultsFolder:
            #print(f"The CSV {turtleData.allGpsDfCsvName} has already been saved in the results folder")
        elif turtleData.allCleanedGpsDfCsvName in filesInResultsFolder:
            print(f"The CSV {turtleData.allCleanedGpsDfCsvName} has already been saved in the results folder")
        else:            
            ## Saving AllGpsDf Data
            #print(f"The filename {turtleData.allGpsDfCsvName} is not yet in the folder... saving csv")
            #pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allGpsDfCsvName)
            #turtleData.saveAllGpsData(pathToFilePlusCsvName)
            #print(f"{turtleData.allGpsDfCsvName} has been saved in the results folder!")              
            #print('--------------')
            ## Saving AllCleanedGps Data
            print(f"The filename {turtleData.allCleanedGpsDfCsvName} is not yet in the folder... saving csv")
            pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allCleanedGpsDfCsvName)
            turtleData.saveAllCleanedGpsDfData(pathToFilePlusCsvName)
            print(f"{turtleData.allCleanedGpsDfCsvName} has been saved in the results folder!")
        #print(filesInResultsFolder)
        print('--------------')

        # THIS FUNCTION ABOVE IS THE SAME FUNCTION TO SAVE THE ALL GPS DF, TRY TO DO ONLY ONE FUNCTION TO BOTH,
        # AND ALSO TRY TO MAKE THIS ONE FUNCTION TO WAIT UNTIL THE CLEANING HAS BEEN MADE TO THEN SAVE THE
        # ALL CLEANED GPS DF

def getTempReliableGpsDfWithNoTagDateDataframes(turtlesData):
    for turtleData in turtlesData:
        turtleData.giveTempReliableGpsDfWithNoTagDate()

def createTempReliableGpsDfWithNoTagDateCsvNameCsvNameForEachInstance(turtlesData):
    # create a reliableGpsDf's name for each turtleData
    for turtleData in turtlesData:
        turtleData.generateTempReliableGpsDfWithNoTagDateCsvName()

def checkIfTempReliableGpsDfWithNoTagDateHasBeenSaved(turtlesData):
    filesInResultsFolder = []    
    
    for file in DATACLEANINGRESULTS_FOLDER_ITENS:
        filesInResultsFolder.append(file)    
    print(filesInResultsFolder)

    for turtleData in turtlesData:
        if not filesInResultsFolder:
            ## Saving AllGpsDf Data 
            #print(f"The filename {turtleData.allGpsDfCsvName} is not yet in the folder... saving csv")
            #pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allGpsDfCsvName)                       
            #turtleData.saveAllGpsData(pathToFilePlusCsvName)
            #print(f"{turtleData.allGpsDfCsvName} has been saved in the results folder!")            
            #print('--------------')
            ## Saving AllCleanedGps Data
            #print(f"The filename {turtleData.allCleanedGpsDfCsvName} is not yet in the folder... saving csv")
            #pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allCleanedGpsDfCsvName)
            #turtleData.saveAllCleanedGpsData(pathToFilePlusCsvName)
            #print(f"{turtleData.allCleanedGpsDfCsvName} has been saved in the results folder!")
            ## Saving tempReliableGpsDfWithNoTagDate Data
            print(f"The filename {turtleData.tempReliableGpsDfWithNoTagDateCsvName} is not yet in the folder... saving csv")
            pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.tempReliableGpsDfWithNoTagDateCsvName)
            turtleData.saveTempReliableGpsDfWithNoTagDateData(pathToFilePlusCsvName)
            print(f"{turtleData.tempReliableGpsDfWithNoTagDateCsvName} has been saved in the results folder!")

        #elif turtleData.allGpsDfCsvName in filesInResultsFolder:
            #print(f"The CSV {turtleData.allGpsDfCsvName} has already been saved in the results folder")
        #elif turtleData.allCleanedGpsDfCsvName in filesInResultsFolder:
            #print(f"The CSV {turtleData.allCleanedGpsDfCsvName} has already been saved in the results folder")
        elif turtleData.tempReliableGpsDfWithNoTagDateCsvName in filesInResultsFolder:
            print(f"The CSV {turtleData.tempReliableGpsDfWithNoTagDateCsvName} has already been saved in the results folder")
        else:            
            ## Saving AllGpsDf Data
            #print(f"The filename {turtleData.allGpsDfCsvName} is not yet in the folder... saving csv")
            #pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allGpsDfCsvName)
            #turtleData.saveAllGpsData(pathToFilePlusCsvName)
            #print(f"{turtleData.allGpsDfCsvName} has been saved in the results folder!")              
            #print('--------------')
            ## Saving AllCleanedGps Data
            #print(f"The filename {turtleData.allCleanedGpsDfCsvName} is not yet in the folder... saving csv")
            #pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allCleanedGpsDfCsvName)
            #turtleData.saveAllCleanedGpsData(pathToFilePlusCsvName)
            #print(f"{turtleData.allCleanedGpsDfCsvName} has been saved in the results folder!")
            ## Saving ReliableGpsDf Data
            print(f"The filename {turtleData.tempReliableGpsDfWithNoTagDateCsvName} is not yet in the folder... saving csv")
            pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.tempReliableGpsDfWithNoTagDateCsvName)
            turtleData.saveTempReliableGpsDfWithNoTagDateData(pathToFilePlusCsvName)
            print(f"{turtleData.tempReliableGpsDfWithNoTagDateCsvName} has been saved in the results folder!")
        #print(filesInResultsFolder)
        print('--------------')

        # THIS FUNCTION ABOVE IS THE SAME FUNCTION TO SAVE THE ALL GPS DF AND FOR THE All CLEANED GPS, 
        # TRY TO DO ONLY ONE FUNCTION FOR ALL,
        # AND ALSO TRY TO MAKE THIS ONE FUNCTION TO WAIT UNTIL THE CLEANING HAS BEEN MADE 
        # TO THEN SAVE THE FIRST THE ALL CLEANED GPS DF AND THEN THE RELIABLE GPS DF

#def appendTurtlePropertiesToDictionary(sample_dict, key, value):
    #if key not in sample_dict:
        #sample_dict[key] = value
    #return sample_dict

def getReliableGpsDataframes(turtlesData):


            

        
        
        
        # if this file already exists in the folder do not save it



    # for turtleData in turtlesData:
    #     if turtleData.allGpsDfCsvName in DATACLEANINGRESULTS_FOLDER:
    #         print(DATACLEANINGRESULTS_FOLDER)
    #         print(f"The CSV {turtleData.allGpsDfCsvName} has already been saved in the results folder")
    #     else:
    #         print(f"The filename {turtleData.allGpsDfCsvName} is not yet in the folder... saving csv")
    #         pathToFilePlusCsvName = os.path.join(DATACLEANINGRESULTS_FOLDER, turtleData.allGpsDfCsvName)
    #         turtleData.saveAllGpsData(pathToFilePlusCsvName)
    #         print(f"{turtleData.allGpsDfCsvName} has been saved in the results folder!")
        


#def getReliableGpsDataframes(turtlesData):
    #for turtleData in turtlesData:
        #turtleData.giveReliableGpsDf()
