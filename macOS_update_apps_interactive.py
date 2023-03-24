import subprocess
import time
import threading
from queue import Queue

def format_size(size):
    """Converts a size in bytes to a human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def format_time(seconds):
    """Converts a time in seconds to a human-readable format."""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def update_app(q, app_name):
    """Updates the specified app and reports progress to the main thread."""
    start_time = time.time()
    process = subprocess.Popen(["softwareupdate", "-i", app_name], stdout=subprocess.PIPE)
    while True:
        output = process.stdout.read(1024)
        if output == b"" and process.poll() is not None:
            break
        if output:
            output_str = output.decode("utf-8")
            if "Downloaded" in output_str:
                downloaded = float(output_str.split()[1])
                total = float(output_str.split()[3])
                progress = downloaded / total * 100
                speed = downloaded / (time.time() - start_time)
                time_remaining = (total - downloaded) / speed
                q.put((app_name, progress, speed, time_remaining))
                if q.get() == "cancel":
                    process.terminate()
                    return

def main():
    while True:
        updates = subprocess.run(["softwareupdate", "-l"], capture_output=True, text=True)
        if "No new software available." in updates.stdout:
            print("No new updates available.")
            break
        for line in updates.stdout.splitlines():
            if line.startswith("*"):
                app_name = line.split("\t")[1]
                print(f"Do you want to update {app_name}? (y/n/s)")
                response = input()
                if response.lower() == "y":
                    print(f"Updating {app_name}...")
                    q = Queue()
                    thread = threading.Thread(target=update_app, args=(q, app_name))
                    thread.start()
                    while thread.is_alive():
                        try:
                            app_name, progress, speed, time_remaining = q.get(timeout=0.1)
                            print(f"Downloaded: {format_size(progress/100*total)} / {format_size(total)} "
                                  f"({progress:.1f}%)  Speed: {format_size(speed)}/s  "
                                  f"Time remaining: {format_time(time_remaining)}")
                        except:
                            pass
                        if input("Do you want to cancel this update? (y/n)").lower() == "y":
                            q.put("cancel")
                            thread.join()
                            print(f"Update for {app_name} cancelled.")
                            break
                    if not thread.is_alive():
                        print(f"{app_name} updated successfully!")
                elif response.lower() == "s":
                   
