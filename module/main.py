import os
import shutil

base_path = os.getcwd()

user_path = "\\".join(base_path.split("\\")[:-2])


def sort_files(path_sort=user_path, extensions=None):
    files_name = os.listdir(path_sort)
    try:
        for i in range(0, len(files_name)):
            for j in range(0, len(extensions)):
                new_folder = f"{user_path}\\Documents\\{"".join(list(extensions[j])[1:]).upper()}s"
                if extensions[j] in files_name[i]:
                    if not os.path.isdir(new_folder):
                        os.mkdir(new_folder)
                    try:
                        shutil.move(f"{path_sort}\\{files_name[i]}", f"{new_folder}")
                    except shutil.Error:
                        raise OSError(f"\nThere was an error to move {files_name[i]}! Try look at your folder.")
    except not shutil.Error:
        raise OSError("There was an error!")
