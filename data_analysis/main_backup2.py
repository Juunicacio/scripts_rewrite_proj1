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

    # SAVE THE ALL GPS DFS
    checkIfAllGpsDfHasBeenSaved(turtlesData)

    # see dfs of reliable gps (Remove GPS Errors by Angular velocity/Rotational speed)
    #getReliableGpsDataframes(turtlesData)

    # Clean Data, filtering 'no GPS Data' from 'GPS Data'


if __name__ == "__main__":
    main()


