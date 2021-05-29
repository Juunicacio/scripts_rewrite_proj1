from functions import *

def main():
    # Check if some excel file has not been converted into csv yet
    check_for_excel_files()
    turtlesData = getTurtlesData()

    # see instances for Obj turtleData created and its dfs
    checkInstancesAndItsDfs(turtlesData)
    #turtlesData[0].df
    #turtlesData[1].df

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

    # see dfs of the Temp reliable gps with no tag date (Remove GPS Errors by Angular velocity/Rotational speed)
    getTempReliableGpsDfWithNoTagDateDataframes(turtlesData)

    # get name for each TEMP RELIABLE GPS DF WITH NO TAG DATE turtleData
    createTempReliableGpsDfWithNoTagDateCsvNameCsvNameForEachInstance(turtlesData)

    # SAVE THE TEMP RELIABLE GPS DATAFRAME WITH NO TAG DATE in the Results Folder
    checkIfTempReliableGpsDfWithNoTagDateHasBeenSaved(turtlesData)    

    # Clean Data, filtering 'no GPS Data' from 'GPS Data'


if __name__ == "__main__":
    main()


