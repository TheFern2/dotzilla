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
common_paths_override = ''
all_paths = []
found_paths = []
ignored_paths = []

def copy_settings_file():
    if not os.path.isdir(settings_path):
        os.mkdir(settings_path)
    
    if not os.path.exists(settings_path + "settings.conf"):
        copyfile(dir_path + "/sample.settings.conf", settings_path + "settings.conf")


# common paths is a bit simpler
# since we don't have starting identifiers
def process_common_paths(paths):
    for i in range(len(paths)):
        if not paths[i].startswith(";"): # ignore comments
            if paths[i].startswith("~"):
                all_paths.append(home_path + paths[i][1:-1] + "\n")
            else:
                all_paths.append(paths[i] + "\n")

            if not paths[i].startswith("~") and not paths[i].startswith("/"):
                # this prob needs to be an exception
                print('Error! Unknown modifier at Line ' + str(i + 1) + " " + paths[i])

# could be simplified, is working for now
# user paths can have + for searching a path
# a - for ignoring a path
# and ; for comments
# comments are processed here to be able to tell user of line errors
def process_user_paths(paths):
    for i in range(len(paths)):
        if not paths[i].startswith(";"): # ignore comments
            if paths[i].startswith("+"):
                if "~" in paths[i][1]:
                    all_paths.append(home_path + paths[i][2:-1] + "\n")
                else:
                    all_paths.append(paths[i][1:-1] + "\n")
            if paths[i].startswith("-"):
                if "~" in paths[i][1]:
                    ignored_paths.append(home_path + paths[i][2:-1] + "\n")
                else:
                    ignored_paths.append(paths[i][1:-1] + "\n")
            if not paths[i].startswith("+") and not paths[i].startswith("-"):
                # this prob needs to be an exception
                print('Error! Unknown modifier at Line ' + str(i + 1) + " " + paths[i])


# will scan system with given common paths
# and user paths, but not ignored paths
def find_dotfile(all_paths):
    for path in all_paths:
        if path not in ignored_paths:
            if os.path.isfile(path.rstrip()):
                found_paths.append(path.rstrip())
                #print('Found a file! ' + path, end='')
                #print('Link status ' + str(os.path.islink(path.rstrip())))
                # os.path.realpath(path)
                # create dotfile obj and save to pickle on links folder
            if os.path.isdir(path.rstrip()):
                found_paths.append(path.rstrip())
                #print('Found a dir!' + path, end='')
            
            # folder link returns false for isdir and isfile unlike
            # linked file which still returns true for file
            if not os.path.isfile(path.rstrip()) and os.path.islink(path.rstrip()):
                #print('Link status ' + str(os.path.islink(path.rstrip())))
                # os.path.realpath(path)
                # create dotfile obj and save to pickle on links folder
                found_paths.append(path.rstrip())


# all dotfiles will be copied to a new folder inside the repo
# with the default folder name
# hostname + platform.system() + platform.release() + random 8 digit number
# computer-01-Windows-XP-45677895
# terminal-02-Linux-5.4.0-31-generic-32146548
# if machine_name is provided:
# machine_name = Ubuntu01_Work
# Ubuntu01_Work-12354568
def copy_dotfile_to_repo(repo_path, machine_name=None):
    pass


'''
This function reads all paths which will used to scan machine for configs
common paths are scanned by default, unless user choose not to and only use
user paths. Common paths can be the default common paths file provided by
dotzilla, or a user provided common paths in ~/.config/dotzilla/common_paths.txt
'''
def scan_paths(user_paths=None, override_common_paths=None,ignore_common_paths=False):
    
    if not ignore_common_paths:
        if override_common_paths:
            with open(settings_path + override_common_paths, 'r') as f:
                common_lines = f.readlines()
        else:
            with open(dir_path + "/common_paths.txt", 'r') as f:
                common_lines = f.readlines()

    if user_paths:
        with open(settings_path + user_paths, 'r') as f:
            user_lines = f.readlines()

    process_common_paths(common_lines)
    
    process_user_paths(user_lines)


# commands scan, backup, deploy, sync, path, name, settings
# on first deploy dotzilla will look for a default dotfiles folder, if not it will list the current ones
# and give user the option to rename or sync to same
def main():
        debug = False

        parser = argparse.ArgumentParser()
        parser.add_argument('--repo-path')
        parser.add_argument('--scan-only', action='store_true')
        parser.add_argument('--init', help='Initialize dotfiles' , action='store_true')
        parser.add_argument('--backup', action='store_true')
        args = parser.parse_args()

        copy_settings_file() # only done once

        config = configparser.ConfigParser()
        config.read(settings_path + "settings.conf")
        repo_path = config['DEFAULT']['repo_path']
        update_repo_script = config['DEFAULT']['update_repo_script']
        machine_name = config['DEFAULT']['machine_name']
        user_paths = config['DEFAULT']['user_paths']
        ignore_common_paths = config['DEFAULT'].getboolean('ignore_common_paths')
        common_paths_override = config['DEFAULT']['common_paths_override']

        # logging stuff
        if debug:
            print(repo_path, "repo_path")
            print(args.repo_path, "args.repo_path")
            print(update_repo_script, "update_repo_script")
            print(user_paths, "user_paths")
            print(ignore_common_paths, "ignore_common_paths\n")

        # ask user for required values
        if not repo_path and not args.repo_path:
            print("Update settings.conf or run dotzilla with --repo-path flag")
            sys.exit()
        
        
        scan_paths(user_paths, common_paths_override, ignore_common_paths)

        if debug:
            print('All paths:')
            print(len(all_paths))
            for l in all_paths:
                print(l, end='')

            print('Ignored paths:')
            print(len(ignored_paths))
            for l in ignored_paths:
                print(l, end='')

        # TODO generate dotfile objects for links
        # if is init, then pickled to repo
        find_dotfile(all_paths)

        if args.scan_only:
            for l in found_paths:
                print(l)
            os.sys.exit()

        # init dotfiles, dotfiles found will be copied
        # to repo, then symbolic links will be created to target
        # repo files will be the source
        # take into account linked files, and folders
        if args.init:
            pass

        # copy found_paths to repo_path
        if args.backup and not args.scan_only:
            pass

            
 
if __name__ == '__main__':
          main()
