import pandas as pd
import os
from turtleData import TurtleData

# To run with Debug:
ASSETS_FOLDER_OBJ = "data_analysis\\assets"
ASSETS_FOLDER_ITENS = os.listdir("data_analysis/assets")
# To run with terminal:
#ASSETS_FOLDER_OBJ = "assets"
#ASSETS_FOLDER_ITENS = os.listdir("assets")

TAG_TURTLE_1 = '710333A'
TAG_TURTLE_2 = '710348A'

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
    df_xlsx.to_csv(os.path.join(folder_obj, file_in_csv), index=False)        

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
            print('- Excel file= ' + file)
            file_name = file.split('.', 1)[0] # remove everything (the format) after the dot
            # remove the excel file from my all_my_files list
            all_my_files.remove(file)            
            # check if another file with the same name in the folder exists
            if any(file_name in word for word in all_my_files):            
                print(f"-- Excellent! We've already converted the excel file \'{file_name}\' into csv file")
            else:
                print(f'-- Oh No! The excel file \'{file_name}\' has been not converted. Converting it into csv file...')
                # Call function "Convert excel files into csv"
                converting_excel_file_into_csv_file(ASSETS_FOLDER_OBJ, file)
                file_in_csv = file.replace(".xlsx", ".csv") 
                all_my_files.append(file_in_csv)
                print('---> ' + file_in_csv + ' has been created!')
                
    # Updated all_my_files List
    print('LAST: CSV files in the assets folder: ', all_my_files)

def getTurtleTagFromFilename():
    csv_turtle_files = []
    numbers = []
    n = 0
    split_char = '_'
    turtlesData = []
    for file in ASSETS_FOLDER_ITENS:
        # filename = file
        if file.endswith('.csv'):
            # put all the file names in the same format
            csv_string_filename = replace_space_with_underline(file).lower()
            filename_splitted = csv_string_filename.split(split_char)                        
            for word in filename_splitted:
                #print(word)
                if word.startswith(INITIAL_TAG_DIGITS):
                    #print(file)
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
                        print("Instance for TAG ("+ word +") NOT found! Creating a new instance.")
                        # create a TurtleData obj with the turtle tag
                        foundTurtleData = TurtleData(word)
                        turtlesData.append(foundTurtleData)
                    else:
                        print("Instance for TAG ("+ word +") already exist, skipping object creation!")

                    # for the instances turtleData objs in the list (for each turtle tag):
                    #foundTurtleData.addDataFromCsv(ASSETS_FOLDER_OBJ, file)
                    #print(ASSETS_FOLDER_OBJ)

            #csv_turtle_files.append(csv)
    for turtleData in turtlesData:
        print(turtleData.getTag())
        print(f'DataFrame is {turtleData.addDataFromCsv(ASSETS_FOLDER_OBJ, file)}')
