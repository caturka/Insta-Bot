import shutil
from pathlib import Path

#function to remove sub dir
def rmv(subdir):
      dir = Path(subdir).is_dir()
      if dir == True:
            shutil.rmtree(subdir)
            print("sub folder successfully removed")
      else:
            print("Path doesn't exists....Skiped!")
            pass
