from functions import *

def main():
    # Check if some excel file has not been converted into csv yet
    check_for_excel_files()
    turtlesData = getTurtlesData()

    # see instances for Obj turtleData created and its dfs
    checkInstancesAndItsDfs(turtlesData)
    #turtlesData[0].df
    #turtlesData[1].df

    # build dfs of No gps data
    getNoGpsDataframes(turtlesData)

    # see dfs of No gps data
    displayNoGpsDf(turtlesData)
    # or
    #turtlesData[0].noGpsDf
    #turtlesData[1].noGpsDf

    # get name for each No gps DF turtleData
    createNoGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE NO GPS DATAFRAME in the Results Folder
    checkIfNoGpsDfHasBeenSaved(turtlesData)

    #
    # build dfs of all gps
    getAllGpsDataframes(turtlesData)

    # see dfs of all gps
    displayAllGpsDf(turtlesData)
    # or
    #turtlesData[0].allGpsDf
    #turtlesData[1].allGpsDf

    # get name for each ALL GPS DF turtleData
    createAllGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE ALL GPS DATAFRAME in the Results Folder
    checkIfAllGpsDfHasBeenSaved(turtlesData)

    # 
    assignTagDayDatetimeToEachInstance(turtlesData)

    # now we need to look at the all gps df and delete the duplicates rows, before calculating the errors by speed
    # deleting duplicate rows and 2019 date
    getAllCleanedGpsDataframes(turtlesData)

    # get name for each ALL CLEANED GPS DF turtleData
    createAllCleanedGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE ALL CLEANED GPS DATAFRAME in the Results Folder
    checkIfAllCleanedGpsDfHasBeenSaved(turtlesData)

    # see dfs of reliable gps (Remove GPS Errors by Angular velocity/Rotational speed)
    getReliableGpsDataframes(turtlesData)

    # get name for each RELIABLE GPS DF turtleData
    createReliableGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE RELIABLE GPS DATAFRAME in the Results Folder
    checkIfReliableGpsDfHasBeenSaved(turtlesData)

    # get name for each NO RELIABLE GPS DF turtleData
    createNoReliableGpsDfCsvNameForEachInstance(turtlesData)

    # SAVE THE NO RELIABLE GPS DATAFRAME in the Results Folder    
    checkIfNoReliableGpsDfHasBeenSaved(turtlesData)
    

    # Clean Data, filtering 'no GPS Data' from 'GPS Data'
    
    # then initiate with the depth data


if __name__ == "__main__":
    main()


