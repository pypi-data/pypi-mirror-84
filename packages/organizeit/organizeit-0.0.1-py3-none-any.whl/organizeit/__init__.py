import os
import collections
import shutil

EXT_AUDIO = ['mp3', 'wav', 'raw', 'mid', 'midi']
EXT_VIDEO = ['mp4', 'mpg', 'mpeg', 'avi', 'mov', 'flv', 'mkv', 'm4v', 'h264']
EXT_DOCUMENTS = ['doc', 'xlsx', 'pptx', 'txt', 'pdf', 'csv', 'xls', 'docx', 'html', 'odt', 'ods', 'tex']
EXT_COMPR = ['zip', 'z', '7z', 'rar', 'tar', 'pkg', 'deb', 'gz', 'rpm']
EXT_INSTL = ['dmg', 'exe', 'iso']
EXT_PICTURES = ['jpg', 'png', 'svg', 'bmp', 'psd', 'gif', 'tiff', 'tif', 'jpeg']


def createFolders(FOLDERS_NAMES, path):
    # Creating folders
    for folder in FOLDERS_NAMES:
        dir_path = os.path.join(path, folder)
        if folder not in path:
            os.mkdir(dir_path)


def insertFiles(path):
    files_in_folder = os.listdir(path)
    files_mapping = collections.defaultdict(list)
    for file in files_in_folder:
        file_ext = file.split('.')[-1]
        files_mapping[file_ext].append(file)

    for f_ext, f_name in files_mapping.items():
        if f_ext in EXT_PICTURES:
            for file in f_name:
                shutil.move(path + "\\" + file, path + "\\Images")
        elif f_ext in EXT_AUDIO:
            for file in f_name:
                shutil.move(path + "\\" + file, path + "\\Music")
        elif f_ext in EXT_VIDEO:
            for file in f_name:
                shutil.move(path + "\\" + file, path + "\\Videos")
        elif f_ext in EXT_INSTL:
            for file in f_name:
                shutil.move(path + "\\" + file, path + "\\Applications")
        elif f_ext in EXT_DOCUMENTS or f_ext in EXT_COMPR:
            for file in f_name:
                shutil.move(path + "\\" + file, path + "\\Documents")