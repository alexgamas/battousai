import os

def listFiles(folder):
    fileList = []
    print "\nScan for files under the folder: {f} ... \n".format(f = folder)
    for path, dirs, files in os.walk(folder):
        print path
        for f in files:
            filename = os.path.join(path, f)
            print "\t+ (...)" + filename[-60:]
            fileList.append(filename)
    fileList.sort()
    return fileList
