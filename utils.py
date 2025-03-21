# utils.py
import os

def save_file_to_disk(file_path, downloaded_file):
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)

def remove_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
