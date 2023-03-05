import os
import shutil
import threading
import logging
import argparse

file_handler = logging.StreamHandler()
file_handler.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler("sync.log", mode="w"), file_handler]
)

SYNCHRONIZATION_INTERVAL = 60
sync_log_location = r"/home/ruben/Desktop/Python Learning/Veeam_Task/sync.log"
source_folder = r"/home/ruben/Desktop/source"
replica_folder = r"/home/ruben/Desktop/replica"
replica_folder_temp = r"/home/ruben/Desktop/replica/temporary_folder"
logging.info("created temporary_folder in replica folder ")


def synchronize():

    for item in os.listdir(replica_folder):
        path = os.path.join(replica_folder, item)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)
    logging.info("deleted old files in replica folder")

    shutil.copytree(source_folder, replica_folder_temp)
    logging.info("copied files from source folder to replicate folder")

    for file in os.listdir(replica_folder_temp):
        shutil.move(os.path.join(replica_folder_temp, file), replica_folder)
    logging.info("moved files from temporary_folder to replica folder")

    os.rmdir(replica_folder_temp)
    logging.info("deleted temporary_folder")


def period_of_sync():
    synchronize()
    print("sync")
    threading.Timer(SYNCHRONIZATION_INTERVAL, period_of_sync).start()


parser = argparse.ArgumentParser(description="Choose folder path, sync interval or log file")
parser.add_argument(
    "--data",
    type=str,
    help="choose between: folder_paths, sync_interval, log_file_path"
)
args = parser.parse_args()

if args.data == "folder_paths":
    print(f"Path source_folder : {source_folder}")
    print(f"Path replica_folder : {replica_folder}")
elif args.data == "sync_interval":
    print(f"Synchronization Interval : {SYNCHRONIZATION_INTERVAL}")
elif args.data == "log_file_path":
    print(f"Path : {sync_log_location}")


period_of_sync()
