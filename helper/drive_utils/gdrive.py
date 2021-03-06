#import Modules
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from os import path
from config import Config


#Route the modules
gauth = GoogleAuth()
drive = GoogleDrive(gauth)
DRIVE=Config.DRIVE



#gdrive upload function
def gup(dir,gid):

    #check if the credentials file exists
    if path.exists("credentials.json"):
    
        #Main gfolder id where store all the ig profile archive 
        gFolderID= DRIVE#Gdrive Folder id to store all the user posts conatining files  Folder
        directory = dir #Route the main dir to function directory variables
        
        #Getting Gdrive Details
        gListFolderstr = "\'" + gFolderID + "\'" + " in parents and trashed=false" #Get list the Files in Given gUserFolderID 
        gfile_list = drive.ListFile({'q': gListFolderstr}).GetList() #List the Files using gListFolderstr
        

        #Get All the folder inside the given main gfolder  
        try:
            for glistfile in gfile_list: #List and store  files in glistfile to get title or id
                print("All Folder Title in Given GDrive Folder ID:",glistfile['title'])
                if glistfile['title'] == dir: #Intial check Whether the user dir is already present.
                    folderid = glistfile ['id'] #Store already presented user gfolder id
                    foldername = glistfile ['title'] #Store already presented user gfolder title
                    break 
                else:
                    folderid = None
                    foldername = None
        except:
            pass

        #set folder variables
        matchedFolderID = folderid #Store already presented user gfolder id to the matchedFolderID
        matchedFoldername = foldername #Store already presented user gfolder title to matchedFoldername
        
        #upload section
        if matchedFoldername == dir: #validate Again
            print(f'The matched Folder is: {matchedFoldername} : {matchedFolderID}')
            
            
            #compare files in matchFolderId with Local Files
            gcmpListFolderstr = "\'" +  matchedFolderID + "\'" + " in parents and trashed=false" #get list the Files in Given MatchedFolderID
            gcmpfile_list = drive.ListFile({'q': gcmpListFolderstr}).GetList()#list the Files using gListFolderstr
            
            #get list Of Files in both Dir
            for gfilelist in gcmpfile_list: 
                print("The Matched Drive File list are:", gfilelist['title']) #list files in Gdrive dir in gfilelist
            for localfilelist in os.listdir(directory): #list files in Local dir 
                print("The Matched Local Dir File list are:", localfilelist)
                
                #overwrite the files if Exists by deletin existing file
                try:
                    for file1 in gcmpfile_list:
                        if file1['title'] == localfilelist:
                            tfile = file1['title']
                            file1.Delete()
                            print(f'File {tfile} is Successfully deleted')                                  
                except:
                    pass
                
            #Upload the Deleted Files
                filename = os.path.join(directory, localfilelist) #filename allocation
                gfile = drive.CreateFile({'parents' : [{'id' : matchedFolderID}], 'title' : localfilelist}) #where the files will be uploaded
                gfile.SetContentFile(filename) #set gfilename 
                gfile.Upload() #upload
                print(f'File {localfilelist} is Successfully Uploaded') 
            gid = (f'https://drive.google.com/drive/u/1/folders/{matchedFolderID}')
            return gid
        #Else part To Create New GFolde for the Dir And Upload the Files...!
        else:
            #Create folder for the title dir 
            folder_metadata = {'title' : dir,"parents":  [{"id": gFolderID}], 'mimeType' : 'application/vnd.google-apps.folder'} #meta data for gfolder
            gFolderCreate = drive.CreateFile(folder_metadata) #set gfolderename
            gFolderCreate.Upload() #upload
            
            #Get new folder id
            newgFolderID = gFolderCreate['id']
            print(gFolderCreate['title'] ," -->Successfully created")

            #Upload all the new files to the newly created gfolder
            for localfilelist in os.listdir(directory):
                filename = os.path.join(directory, localfilelist) #filename allocation
                gfile = drive.CreateFile({'parents' : [{'id' : newgFolderID}], 'title' : localfilelist}) #where the files will be uploaded
                gfile.SetContentFile(filename) #set gfilename
                gfile.Upload() #upload
                print(f'File {localfilelist} is Successfully Uploaded') 
            print("All Files was Successfully Uploaded")
            gid = (f'https://drive.google.com/drive/u/1/folders/{newgFolderID}')
            return gid
    else:
        print("No creditals.json file found")

#dir = '' #Dir For debug purpose..!
#gid =  #gfolderid for test purose
