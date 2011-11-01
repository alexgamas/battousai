import os

def listFiles(folder):
	fileList = []
	for path, dirs, files in os.walk(folder):
		print path
		for f in files:
			filename = os.path.join(path, f)
			fileList.append(filename)
	return fileList
