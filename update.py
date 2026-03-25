#!/usr/bin/python
import glob
import subprocess

BASE_DIR = "./config"
CONFIG_DIR = "/home/shrutip/.config"
base_files = []


def copy_to_git(config_dir, base_dir, files):
    for i in range(len(files)):
        subprocess.run(["cp", f"{config_dir}{files[i]}", f"{base_dir}{files[i]}"])


def copy_to_config(base_dir, config_dir, files):
    for i in range(len(files)):
        subprocess.run(["cp", f"{base_dir}{files[i]}", f"{config_dir}{files[i]}"])


def get_check_files(config_dir, base_dir):
    to_cp = []

    # Create filenames.txt with `find ./ -type f > filenames.txt`
    with open("filenames.txt", "r") as f:
        for line in f.readlines():
            if line.startswith("./config"):
                base_files.append(line.strip()[8:])
            else:
                continue

    for i in range(len(base_files)):
        out = subprocess.run(["diff", "-s", f"{config_dir}{base_files[i]}", f"{base_dir}{base_files[i]}"], capture_output=True)
        if 'identical' not in out.stdout.decode():
            to_cp.append(base_files[i])

    return to_cp


if __name__=="__main__":
    to_cp = get_check_files(config_dir=CONFIG_DIR, base_dir=BASE_DIR)
    if len(to_cp) == 0:
        print("No files to copy.")
        print("Everything is up to date.")
    else:
        copy_to_git(config_dir=CONFIG_DIR, base_dir=BASE_DIR, files=to_cp)
