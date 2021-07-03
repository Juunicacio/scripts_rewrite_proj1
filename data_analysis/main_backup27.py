from functions import *

def main():
    # Check if some excel file has not been converted into csv yet
    check_for_excel_files()
    turtlesData = getTurtlesData()

    # see instances for Obj turtleData created and its dfs
    checkInstancesAndItsDfs(turtlesData)

    # build dfs of No gps data
    getNoGpsDataframes(turtlesData)

    # see dfs of No gps data
    displayNoGpsDf(turtlesData)

    # get name for each No gps DF turtleData
    createNoGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE NO GPS DATAFRAME in the Results Folder
    checkIfNoGpsDfHasBeenSaved(turtlesData)

    # build dfs of all gps
    getAllGpsDataframes(turtlesData)

    # see dfs of all gps
    displayAllGpsDf(turtlesData)

    # get name for each ALL GPS DF turtleData
    createAllGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE ALL GPS DATAFRAME in the Results Folder
    checkIfAllGpsDfHasBeenSaved(turtlesData)

    assignTagDayDatetimeToEachInstance(turtlesData)

    # deleting duplicate rows and 2019 date
    getAllCleanedGpsDataframes(turtlesData)

    # get name for each ALL CLEANED GPS DF turtleData
    createAllCleanedGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE ALL CLEANED GPS DATAFRAME in the Results Folder
    checkIfAllCleanedGpsDfHasBeenSaved(turtlesData)

    # Assign the CRS data
    giveCoordinateReferenceSystemCrs(turtlesData)

    # see dfs of reliable gps and no reliable gps (Remove GPS Errors by Angular velocity/Rotational speed)
    getReliableAndNoReliableGpsDataframes(turtlesData)

    # get name for each RELIABLE GPS DF turtleData
    createReliableGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE RELIABLE GPS DATAFRAME in the Results Folder
    checkIfReliableGpsDfHasBeenSaved(turtlesData)

    # get name for each NO RELIABLE GPS DF turtleData
    createNoReliableGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE NO RELIABLE GPS DATAFRAME in the Results Folder    
    checkIfNoReliableGpsDfHasBeenSaved(turtlesData)
    
    # then initiate with the depth data
    getRemainingDataDataframes(turtlesData)

    # get name for each Remaining Data DF turtleData
    createRemainingDataDfCsvNameForEachInstance(turtlesData)

    # SAVE THE REMAINING DATA DATAFRAME in the Results Folder 
    checkIfRemainingDataDfHasBeenSaved(turtlesData)

    # build dfs for Depth Data
    getDepthDataDataframes(turtlesData)

    # get name for each Depth Data DF turtleData
    createdepthDataDfCsvNameForEachInstance(turtlesData)

    # SAVE THE DEPTH DATA DATAFRAME in the Results Folder 
    checkIfdepthDataDfHasBeenSaved(turtlesData)

    #
    # get plotlyLines from reliable gps
    ### USE WITH JUPYTER NOTEBOOK
    #getLines(turtlesData) # just to see the map without projection

    # get plotlyLines from reliable gps with map projection
    ### USE WITH JUPYTER NOTEBOOK
    getProjLines(turtlesData)

    # see the CRS
    askCrs(turtlesData)

    #askArray(turtlesData) #just to see if the append arrays inside the empty object works

if __name__ == "__main__":
    main()


