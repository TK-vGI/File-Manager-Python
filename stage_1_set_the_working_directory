import os

# run the user's program in our generated folders
os.chdir('module/root_folder')

def file_manager():
    print("Input the command")

    while True:
        try:
            usr = input()
            if usr == 'quit':
                # Exits program
                break
            elif usr == 'pwd':
                # Print absolute path of the current directory
                print(os.getcwd())
            elif usr == 'cd ..':
                # Moves one directory up
                parent_dir = os.path.dirname(os.getcwd())
                os.chdir(parent_dir)
                print(os.path.basename(parent_dir))
            elif usr.startswith('cd '):
                # Move to the folder specified by the user
                path = usr[3:].strip()

                try:
                    os.chdir(path)
                    print(os.path.basename(os.getcwd()))
                except FileNotFoundError:
                    print('File or directory not found')
            else:
                print('Invalid command')
        except FileNotFoundError:
            print('File or directory not found')


if __name__ == '__main__':
    file_manager()