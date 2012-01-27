import os

def listFiles(folder):
        fileList = []
        for path, dirs, files in os.walk(folder):
                level = path.count(os.path.sep)
                if level == 0:
                        for f in files:
                                filename = os.path.join(path, f)
                                print "\t", filename
                                fileList.append(filename)
        return fileList
