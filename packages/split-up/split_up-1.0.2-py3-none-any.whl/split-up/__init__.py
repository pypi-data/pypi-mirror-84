import os
import shutil

def split_custom(source_folder, destination_folder, *p, copy = False):
    # Enter path to create new folder
    split_folder = destination_folder
    
    
    # Enter path with files to split
    file_folder = source_folder
      
    
    # Enter the ratio for the splits
    if sum(p) != 100:
    	print("The ratios provided do not add upto hundred, please check again!")
    
    # Split the files    
    ## Total number of files in the folder
    path, dirs, files = next(os.walk(file_folder))
    file_count = len(files)
    
    ## Creat split folders
    for i in range(len(p)):     
        new_folder = split_folder + "/Split_" + str(i + 1)
        if os.path.exists(new_folder) == False:
            os.mkdir(new_folder)
        
        try:
            iteration = int((p[i]/100) * file_count)
            j = 0
        
            for file in os.listdir(file_folder):
                if (j < iteration):         
                    if copy == True:
                        move_file = split_folder + "/" + file
                        shutil.copy(move_file, new_folder)
                    else:
                        move_file = split_folder + "/" + file
                        shutil.move(move_file, new_folder)                                               
                    j += 1
                               
        except:              
            pass

        
split_folder = "C:/Users/arvin/OneDrive/Desktop/Split/Train"
# split(split_folder, split_folder,60,20,20)
split_custom(split_folder, split_folder, 80, 20)