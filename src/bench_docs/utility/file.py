import os


class File:
    def __init__(self, folders, name, ext, abspath):
        self.folders = folders
        self.name = name
        self.ext = ext
        self.abspath = abspath


def retrieve_all_files_from(root):
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            relpath = os.path.relpath(dirpath, root)
            name, ext = os.path.splitext(filename)
            file = File(relpath.split(os.sep), name, ext, os.path.join(os.path.abspath(dirpath), filename))
            files.append(file)
    return files
