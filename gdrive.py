#import Modules
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

#Route the modules
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

#New Function  Which Check And Overwrite files
#dir = '' #Dir For test purpose..!

def gup(dir):
    
    gFolderID='1lgl0K453dJW7zkP8qzA_bEq925xwJN3J' #gdrive Folder id to store all the user posts conatining files  Folder
    directory = dir
   
    #Getting Gdrive Details
    folder_metadata = {'title' : dir,"parents":  [{"id": gFolderID}], 'mimeType' : 'application/vnd.google-apps.folder'} #create folder for the dir in Given gFolderID with Given Tittle dir
    gListFolderstr = "\'" + gFolderID + "\'" + " in parents and trashed=false" #get list the Files in Given gUserFolderID 
    gfile_list = drive.ListFile({'q': gListFolderstr}).GetList()#list the Files using gListFolderstr
     
    #intial check Whether the user dir is already present.
    for glistfile in gfile_list: #list and store  files inglistfile to get title or id
        print("All Folder Title in Given GDrive Folder ID:",glistfile['title'])

        #intial check Whether the user dir is already present.  
        if glistfile ['title'] == folder_metadata['title']: #if the folder in gFolder Match With Folder_Metada folder (dir) title
            matchedFolderID=glistfile['id'] #get the matched folder id
            print(f'The matched Folder ID is: {matchedFolderID}')

            #compare files in matchFolderId with Local Files
            gcmpListFolderstr = "\'" +  matchedFolderID + "\'" + " in parents and trashed=false" #get list the Files in Given MatchedFolderID
            gcmpfile_list = drive.ListFile({'q': gcmpListFolderstr}).GetList()#list the Files using gListFolderstr
            
            #get list Of Files in Dir
            for gfilelist in gcmpfile_list: 
                print("The GDrive File list are:", gfilelist['title']) #list  files in Gdrive dir in gfilelist
            for localfilelist in os.listdir(directory):
                print("The Local Dir File list are:", localfilelist)
                
                #overwrite the files if Exists
                try:
                    for file1 in gcmpfile_list:
                        if file1['title'] == localfilelist:
                            file1.Delete()
                            print(f'File is Successfully deleted')                                  
                except:
                    pass
                
            #Upload the Overwritten Files
                #for localfilelist in os.listdir(directory):
                filename = os.path.join(directory, localfilelist)
                gfile = drive.CreateFile({'parents' : [{'id' : matchedFolderID}], 'title' : localfilelist})
                gfile.SetContentFile(filename)
                gfile.Upload()
                print(f'File {localfilelist} is Successfully Uploaded') 
            break
            
            #Else part To Create New Folder And Store Files...!
        else:
                #Get folder info and print to screen
                gFolderCreate = drive.CreateFile(folder_metadata)
                gFolderCreate.Upload()
                newgFolderID = gFolderCreate['id']
                print(gFolderCreate['title'] ," -->Successfully created")

                for localfilelist in os.listdir(directory):
                    filename = os.path.join(directory, localfilelist)
                    gfile = drive.CreateFile({'parents' : [{'id' : newgFolderID}], 'title' : localfilelist})
                    gfile.SetContentFile(filename)
                    gfile.Upload()
                    print(f'File {localfilelist} is Successfully Uploaded') 

                print("All Files was Successfully Uploaded")

                break

#End of New Code