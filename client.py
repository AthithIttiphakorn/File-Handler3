
#WINDOWS ONLY!
#f#rom background import 
import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import shelve
import shutil

#Installer
def add_to_startup(target_path):
    """
    Create a shortcut to watcher.exe in the Windows Startup folder.
    This ensures the download watcher starts automatically when Windows boots.
    
    Args:
        target_path (str): Full path to the watcher.exe file
    """
    # Get Windows Startup folder path
    startup_dir = os.path.join(
        os.getenv('APPDATA'),
        r'Microsoft\Windows\Start Menu\Programs\Startup'
    )
    
    # Define path for the new shortcut
    shortcut_path = os.path.join(startup_dir, "background.exe")
    return shortcut_path

#################################################################################

if __name__ == "__main__":
    # Get the full path to watcher.exe in the current directory
    source = os.path.join(os.getcwd(), "background.exe")
    print(source)
    print(os.getcwd())
    dest = add_to_startup(source)


    print(f'Moving {source} -> {dest}')

    try:
        shutil.copy(source, dest)
        print(f"Successfully copied '{source}' to '{dest}'") #Should be shortcut not actual file - cannot use db.
    except FileNotFoundError:
        print(f"Error: Source '{source}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to copy '{source}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    

    with shelve.open('database') as db:
        if 'keywords' not in db.keys():
            print("No keywords added yet")
            db['keywords'] = {}

        keywords = db['keywords']
        print(f'Keywords = {keywords}')

        while True:
            newKey = input("Input keyword for file here: (Press X to exit) ")
            newDestination = input("Input path for file of that keyword: ")
            if newKey.lower() != "X".lower() and newKey not in keywords:
                keywords[newKey] = newDestination
            else:
                break

        db['keywords'] = keywords
        print(keywords)
