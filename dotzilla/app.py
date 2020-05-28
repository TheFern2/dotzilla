import os, sys
import argparse
import configparser
from pathlib import Path
from shutil import copyfile
home_path = str(Path.home())
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
settings_path = home_path + "/.config/dotzilla/"
has_settings = False
repo_path = ''
machine_name = ''
update_repo_script = ''
user_paths = ''
ignore_common_paths = False
all_paths = []

def copy_settings_file():
    if not os.path.isdir(settings_path):
        os.mkdir(settings_path)
    
    if not os.path.exists(settings_path + "settings.conf"):
        copyfile(dir_path + "/sample.settings.conf", settings_path + "settings.conf")


def scan_paths(user_paths=None, ignore_common_paths=False):
    if not ignore_common_paths:
        with open(dir_path + "/common_paths.txt", 'r') as f:
            common_lines = f.readlines()

    if user_paths:
        with open(settings_path + user_paths, 'r') as f:
            user_lines = f.readlines()

    # ignore comments
    for line in common_lines:
        if not line.startswith(";"):
            all_paths.append(line)

    for line in user_lines:
        if not line.startswith(";"):
            all_paths.append(line)

def print_log():
    print(repo_path, "repo_path")
    print(args.repo_path, "args.repo_path")

# commands scan, backup, deploy, sync, path, name, settings
# on first deploy dotzilla will look for a default dotfiles folder, if not it will list the current ones
# and give user the option to rename or sync to same
def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('--repo-path')
        parser.add_argument('--scan', action='store_true')
        args = parser.parse_args()

        copy_settings_file() # only done once

        config = configparser.ConfigParser()
        config.read(settings_path + "settings.conf")
        repo_path = config['DEFAULT']['repo_path']
        update_repo_script = config['DEFAULT']['update_repo_script']
        machine_name = config['DEFAULT']['machine_name']
        user_paths = config['DEFAULT']['user_paths']
        ignore_common_paths = config['DEFAULT'].getboolean('ignore_common_paths')

        # logging stuff
        if True:
            print(repo_path, "repo_path")
            print(args.repo_path, "args.repo_path")
            print(update_repo_script, "update_repo_script")
            print(user_paths, "user_paths")
            print(ignore_common_paths, "ignore_common_paths\n")

        scan_paths("paths.txt")
        print(len(all_paths))
        for l in all_paths:
            print(l, end='')

        # ask user for required values
        if not repo_path and not args.repo_path:
            print("Update settings.conf or run dotzilla with --repo-path flag")
            sys.exit()
            
 
if __name__ == '__main__':
          main()
