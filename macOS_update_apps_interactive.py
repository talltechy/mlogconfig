import logging
import subprocess
import sys
import threading
import time
from queue import Queue

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)

def format_size(size: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

def format_time(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {seconds}s"
    else:
        return f"{seconds}s"

def update_app(q: Queue, app_name: str, start_time: float) -> None:
    size_output = subprocess.run(
        ["softwareupdate\", \"-i", app_name], capture_output=True, text=True)

    for line in size_output.stdout.splitlines():
        if "downloaded" in line.lower():
            total = float(line.split()[1])
            break

    process = subprocess.Popen(
        ["softwareupdate", "-i", app_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    while True:
        output = process.stdout.read(1024)

        if not output and process.poll() == 0:
            break

        if output:
            output_str = output.decode("utf-8")

            if "Downloaded" in output_str:
                downloaded = float(output_str.split()[1])
                progress = downloaded / total * 100
                speed = downloaded / (time.time() - start_time)
                time_remaining = (total - downloaded) / speed
                q.put((app_name, progress, speed, time_remaining))

                if q.get() == "cancel":
                    process.terminate()
                    process.wait()
                    q.task_done()
                    return

    process.stdout.close()
    process.stderr.close()
    process.wait()
    q.task_done()

def main() -> None:
    if sys.version_info < (3, 7):
        raise ValueError(
            "Python version 3.7 or higher is required to run this script.")

    while True:
        updates = subprocess.run(
            ["softwareupdate", "-l"], capture_output=True, text=True)

        if "No new software available." in updates.stdout:
            print("No new updates available.")
            break

        for line in updates.stdout.splitlines():
            if line.startswith("*"):
                app_name = line.split("\t")[1]

                response = input(
                    f"Do you want to update {app_name}? (y/n/s)\n")

                if response.lower() == "y":
                    size_output = subprocess.run(
                        ["softwareupdate", "-i", app_name], capture_output=True, text=True)

                    for line in size_output.stdout.splitlines():
                        if "downloaded" in line.lower():
                            total = float(line.split()[1])
                            break

                    print(f"Updating {app_name}...")
                    q = Queue()
                    start_time = time.time()
                    thread = threading.Thread(
                        target=update_app, args=(q, app_name, start_time))
                    thread.start()
                    while thread.is_alive():
                        try:
                            app_name, progress, speed, time_remaining = q.get(
                                timeout=0.1)

                            print(
                                f"Downloaded: {format_size(progress/100*total)} / {format_size(total)} ({progress}%)  Speed: {format_size(speed)}/s  Time remaining: {format_time(time_remaining)}")

                        except queue.Empty:
                            pass

                        cancel = input(
                            f"Do you want to cancel the update for {app_name}? (y/n)\n> ")

                        if cancel.lower() == "y":
                            q.put("cancel")
                            thread.join()
                            print(f"Update for {app_name} cancelled.")
                            break

                    q.join()

                elif response.lower() == "s":
                    break

                else:
                    continue

if __name__ == "__main__":
    main()
