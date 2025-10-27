import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .storage import vector_store_upsert


class LogHandler(FileSystemEventHandler):
    def __init__(self, directory: Path):
        self.directory = directory

    def on_created(self, event):
        if event.is_directory:
            return
        path = Path(event.src_path)
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        vector_store_upsert(path.name, text)


def start_watch(directory: Path):
    handler = LogHandler(directory)
    observer = Observer()
    observer.schedule(handler, str(directory), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
