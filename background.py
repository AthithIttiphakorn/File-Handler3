#WINDOWS ONLY!

import os
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import shelve
import shutil

def moveFile( source, dest ):
    print(f'Moving {source} -> {dest}')

    try:
        shutil.move(source, dest)
        print(f"Successfully moved '{source}' to '{dest}'")
    except FileNotFoundError:
        print(f"Error: Source '{source}' not found.")
    except PermissionError:
        print(f"Error: Permission denied to move '{source}'.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    

class DownloadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            newFile = event.src_path
            print(f"✅ New file downloaded: {newFile}")
            time.sleep(0.5)
            
            with shelve.open("database") as db:
                if "keywords" not in db:
                    db["keywords"] = []
                for i in db['keywords']:
                    if i in str(newFile):
                        destinationPath = db["keywords"][i]
                        moveFile( newFile, destinationPath )


watchFolder = Path.home() / "Downloads"
observer = Observer()
observer.schedule(DownloadHandler(), watchFolder, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print("Stopped")
observer.join()
