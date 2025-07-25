import os
import shutil

# run the user's program in our generated folders
os.chdir('module/root_folder')


def format_size(size):
    if size < 1024:
        return f"{size}B"
    elif size < 1024 ** 2:
        return f"{round(size / 1024)}KB"
    elif size < 1024 ** 3:
        return f"{round(size / 1024 ** 2)}MB"
    else:
        return f"{round(size / 1024 ** 3)}GB"

def get_replace_confirmation(filename):
    while True:
        response = input(f"{filename} already exists in this directory. Replace? (y/n): ").strip().lower()
        if response == 'y':
            return True
        elif response == 'n':
            return False
        # print("Please enter 'y' or 'n'")

def file_manager():
    print("Input the command")

    while True:
        try:
            usr = input()
            match usr.split():
                case ['quit']:
                    # Exits program
                    break

                case ['pwd']:
                    # Print absolute path of the current directory
                    print(os.getcwd())

                case ['cd ..']:
                    # Moves one directory up
                    parent_dir = os.path.dirname(os.getcwd())
                    os.chdir(parent_dir)
                    print(os.path.basename(parent_dir))

                case ['cd', path]:
                    # Move to the folder specified by the user
                    if os.path.isdir(path):
                        os.chdir(path)
                        print(os.path.basename(os.getcwd()))
                    else:
                        print("Error: Directory does not exist")

                case ['ls'] | ['ls', '-l'] | ['ls', '-lh']:
                    # "ls" List files and subdirectories
                    # "ls -l" List files with sizes in bytes
                    # "ls -lh" List files with human-readable sizes
                    items = os.listdir()
                    directories = [item for item in items if os.path.isdir(item)]
                    files = [item for item in items if os.path.isfile(item)]

                    if not directories and not files:
                        break

                    for directory in directories:
                        print(directory)

                    for file in files:
                        size = os.stat(file).st_size
                        if usr == 'ls -lh':
                            size_str = format_size(size)
                            print(f"{file} {size_str}")
                        elif usr == 'ls -l':
                            size_str = f"{size}B"
                            print(f"{file} {size_str}")
                        else:
                            print(file)  # Print file names only

                case ['rm', *path_usr]:
                    # Deletes folder or file
                    path = " ".join(path_usr).strip() # Join parts in case of spaces

                    if path == "":  # Check if path is missing in command
                        print("Specify the file or directory")
                        return

                    if path.startswith('.'):
                        extension = path.lower()
                        files_to_delete = [f for f in os.listdir() if
                                           os.path.isfile(f) and f.lower().endswith(extension)]
                        if not files_to_delete:
                            print(f"File extension {extension} not found in this directory")
                            return
                        # print("Files to delete:", ", ".join(files_to_delete))
                        # confirm = input(
                        #     f"Are you sure you want to delete all {extension} files? [y/n]: ").strip().lower()
                        # if confirm != 'y':
                        #     print("Deletion cancelled")
                        #     return
                        for file in files_to_delete:
                            os.remove(file)
                        continue

                    if not os.path.exists(path):  # Check if the file or directory exists
                        print("No such file or directory")
                        return

                    # confirm = input(f"Are you sure you want to delete '{path}'? [y/n]: ").strip().lower()
                    # if confirm != 'y':
                    #     print("Deletion cancelled")
                    #     return

                    try:
                        if os.path.isfile(path):
                            os.remove(path)  # Remove file
                            # print(f"File '{os.path.basename(path)}' deleted successfully")
                        elif os.path.isdir(path):
                            shutil.rmtree(path)  # Remove directory and its contents
                            # print(f"Directory '{os.path.basename(path)}' deleted successfully")
                    except shutil.Error as e:
                        print(f"Error: {e}")
                    except Exception as e:
                        print(f"Error deleting item: {e}")

                case ['mv', *path_usr]:
                    # Rename or move a file
                    source = path_usr[0] if len(path_usr) > 0 else None
                    destination = path_usr[1] if len(path_usr ) > 1 else None

                    if len(path_usr) != 2 or not source or not destination:  # Ensure both names are specified
                        print("Specify the current name of the file or directory and the new location and/or name")
                        return

                    if source.startswith('.'):
                        extension = source.lower()
                        files_to_move = [f for f in os.listdir() if os.path.isfile(f) and f.lower().endswith(extension)]
                        if not files_to_move:
                            print(f"File extension {extension} not found in this directory")
                            return
                        # if not os.path.isdir(destination):
                        #     print("Destination must be a directory for extension-based moves")
                        #     return
                        for file in files_to_move:
                            dest_path = os.path.join(destination, file)
                            if os.path.exists(dest_path):
                                if get_replace_confirmation(file):
                                    os.remove(dest_path)
                                else:
                                    continue
                            shutil.move(file, dest_path)
                        return

                    if not os.path.exists(source):  # Check if the old file/folder exists
                        print("No such file or directory")
                        return

                    dest_path = os.path.join(destination, os.path.basename(source)) if os.path.isdir(
                        destination) else destination

                    if os.path.exists(dest_path):  # Check if the new name already exists
                        print("The file or directory already exists")
                        return

                    try:
                        shutil.move(source, dest_path)  # Move or rename the file or folder
                        # print(f"Moved '{source}' to '{dest_path}' successfully")
                    except Exception as e:
                        print(f"Error moving item: {e}")

                case ['mkdir', *path_usr]:
                    # Create folder with absolute or relative path
                    path = "".join(path_usr).strip()

                    if path == "":  # Check if path is missing in command
                        print("Specify the name of the directory to be made")
                        return

                    if os.path.exists(path):  # Check if the directory already exists
                        print("The directory already exists")
                    else:
                        try:
                            os.makedirs(path)  # Create the directory
                            # print(f"Directory '{os.path.basename(path)}' created successfully")
                        except Exception as e:
                            print(f"Error creating directory: {e}")

                case ['cp', *path_usr]:
                    # Copy a file
                    source = path_usr[0] if len(path_usr) > 0 else None
                    destination = path_usr[1] if len(path_usr) > 1 else None

                    if len(path_usr) == 0:
                        print("Specify the file")
                        return
                    if len(path_usr) != 2 or not source or not destination:  # Ensure both names are specified
                        # print("Specify the file")
                        print("Specify the current name of the file or directory and the new location and/or name")
                        return

                    if source.startswith('.'):
                        extension = source.lower()
                        files_to_copy = [f for f in os.listdir() if os.path.isfile(f) and f.lower().endswith(extension)]
                        if not files_to_copy:
                            print(f"File extension {extension} not found in this directory")
                            return
                        # if not os.path.exists(destination):
                        #     os.makedirs(destination)
                        for file in files_to_copy:
                            dest_path = os.path.join(destination, file)
                            if os.path.exists(dest_path):
                                if get_replace_confirmation(file):
                                    os.remove(dest_path)
                                else:
                                    continue
                            shutil.copy2(file, dest_path)
                        continue

                    if not os.path.exists(source):  # Check if the old file/folder exists
                        print("No such file or directory")
                        return

                    if os.path.isdir(source):
                        print("Cannot copy directories, only files")
                        return

                    dest_path = os.path.join(destination, os.path.basename(source)) if os.path.isdir(
                        destination) else destination

                    if os.path.exists(dest_path):
                        print(f"{os.path.basename(dest_path)} already exists in this directory")
                        return

                    try:
                        shutil.copy2(source, dest_path)  # Preserve metadata while copying
                        # print(f"Copied '{source}' to '{dest_path}' successfully")
                    except Exception as e:
                        print(f"Error copying item: {e}")

                case _:
                    print('Invalid command')

        except FileNotFoundError:
            print('File or directory not found')


if __name__ == '__main__':
    file_manager()
