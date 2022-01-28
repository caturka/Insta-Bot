from config import Config
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
DRIVE=Config.DRIVE
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
folder_metadata = {'title' : ".Temp","parents":  [{"id": DRIVE}], 'mimeType' : 'application/vnd.google-apps.folder'} #meta data for gfolder
gFolderCreate = drive.CreateFile(folder_metadata) #set gfolderename
gFolderCreate.Upload() #upload