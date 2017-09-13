import os
import re
import shutil
print "scanning process ..."

class varEntity(object):
	"""docstring for varEntity"""
	#def __init__(self, arg):
	#	super(varEntity, self).__init__()
	#	self.arg = arg
	evName = ""
	evAddr = ""
	evType = "AEIV"
	evValOLD = 0
	evValNEW = 0
	evDelta = 0
	evAbsDelta = 0


re_normal_pattern = re.compile(r'Variable\s\[(\w+-.+)\]\s@\s\((\d+/\d+/\d+/\d+/\d+)\):\s(\w+)\s:\sOLD\s(\d+[\.?|\s?]\d+)\S\sNEW\s(\d+[\.?|\s?]\d+)')
re_badlength_pattern = re.compile(r'Bad length.+AEIV.+\[(\w+\-\w+)\]\s@\s\((\d+/\d+/\d+/\d+/\d+)\)')
fileList=[]
evChanged=[]

def listFiles(dirPath):
	cnt = 0
	for root, dirs,files in os.walk(dirPath):
		for fileObj in files:
			print "adding file (" + str(cnt+1) + "): " + fileObj
			fileList.append(os.path.join(root,fileObj))
			cnt = cnt + 1
	print "scanning process is over. " + str(cnt) + " file(s) added."
	return fileList

def main():
	baseDir = "C:\\UnifyIO\\log\\log_OCCR2_20170909110000"
	fileList = listFiles(baseDir)
	fileNumber = str(len(fileList))
	fileCnt = 0
	for filePath in fileList:
		print "processing file: " + filePath + " ["+ str(fileCnt+1) +" of " + fileNumber +"]..."
		cnt = 0
		prev_ev_changed = len(evChanged)		
		all_lines = open(filePath).readlines()
		
		for line in all_lines:
			m = re_normal_pattern.search(line)
			if m:
				evGet = varEntity()
				evGet.evName = m.group(1) 
				evGet.evAddr = m.group(2)
				evGet.evType = m.group(3)
				if m.group(4)[1] == ' ':								
					evGet.evValOLD = int(m.group(4)[0:1])
				else:
					evGet.evValOLD = float(m.group(4))
				if m.group(5)[1] == ' ':
					evGet.evValNEW = int(m.group(5)[0:1])				
				else:
					evGet.evValNEW = float(m.group(5))
				evGet.evDelta = evGet.evValNEW - evGet.evValOLD
				evChanged.append(evGet)
			cnt = cnt + 1

		print "ev changed: " + str(len(evChanged) - prev_ev_changed) + " items, and total got: " + str(len(evChanged)) +" items."
		fileCnt = fileCnt + 1
	for x in xrange(0,len(evChanged)):
		evGet = evChanged[x]
		print "name=" + evGet.evName + ", " + evGet.evType + ", old=" + str(evGet.evValOLD) + ", new=" + str(evGet.evValNEW) + ", delta=" + str( abs(evGet.evDelta))	
	return

main()
print "all done."
