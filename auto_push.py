
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class AutoPush(FileSystemEventHandler):
    def on_modified(self, event):
        if ".git" in event.src_path or "auto_push" in event.src_path:
            return
        if event.src_path.endswith(".py"):
            push(event.src_path)

    def on_created(self, event):
        if ".git" in event.src_path or "auto_push" in event.src_path:
            return
        push(event.src_path)

def push(path):
    print(f"Detected: {path}")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"auto: {path}"])
    subprocess.run(["git", "push"])

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(AutoPush(), path=".", recursive=True)
    observer.start()
    print("Watching... Ctrl+C to stop")
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()