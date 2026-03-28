#!/usr/bin/python
import glob
import subprocess
import os
import argparse
import sys

HOME = os.getenv("HOME")

BASE_DIR = "./config"
CONFIG_DIR = f"{HOME}/.config"
base_files = []


def copy_to_git(config_dir, base_dir, files):
    print("Copying .config files to git...")
    for file in files:
        subprocess.run(["cp", f"{config_dir}{file}", f"{base_dir}{file}"])

    print("Done.")


def copy_to_config(base_dir, config_dir, files):
    print("Copying git files to .config...")
    for file in files:
        subprocess.run(["cp", f"{base_dir}{file}", f"{config_dir}{file}"])

    print("Done.")


def get_check_files(config_dir, base_dir):
    # Update files
    subprocess.run(["./get_filenames.sh"])

    to_cp = []

    with open("filenames.txt", "r") as f:
        for line in f.readlines():
            if line.startswith("./config"):
                base_files.append(line.strip()[8:])
            else:
                continue

    for file in base_files:
        out = subprocess.run(["diff", "-s", f"{config_dir}{file}", f"{base_dir}{file}"], capture_output=True)
        if 'identical' not in out.stdout.decode():
            to_cp.append(file)


    if len(to_cp) == 0:
        print("No files to copy.")
        print("Everything is up to date.")
    else:
        print("Found differences in the following files:")
        for file in to_cp:
            print(file)

    return to_cp



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--check", help="Check for differences between .config files and git files. Use with -g or -c for copying files.", action="store_true", required=True)
    parser.add_argument("-g", "--git", help="If differences exist, copy the .config files to git. Cannot be used with -c", action="store_true")
    parser.add_argument("-c", "--config", help="If differences exist, copy git files to .config files. Cannot be used with -g", action="store_true")

    args = parser.parse_args()

    if args.git and args.config:
        print("Error.")
        print("Cannot use -g and -c together.")
        sys.exit(1)

    if args.check:
        to_cp = get_check_files(config_dir=CONFIG_DIR, base_dir=BASE_DIR)

    if args.check and args.git:
        if len(to_cp) != 0:
            copy_to_git(config_dir=CONFIG_DIR, base_dir=BASE_DIR, files=to_cp)

    if args.check and args.config:
        if len(to_cp) != 0:
            copy_to_config(base_dir=BASE_DIR, config_dir=CONFIG_DIR, files=to_cp)


if __name__=="__main__":
    main()    
