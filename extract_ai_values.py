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

sysNames = ['PSCADA', 'MPSCADA', 'TPSCADA', 'BAS', 'FAS', 'PSD2', 'PSD','PA', 'CCTV', 'PIS', 'SIG', 'ALM']
re_normal_pattern = re.compile(r'Variable\s\[(\w+-.+)\]\s@\s\((\d+/\d+/\d+/\d+/\d+)\):\s(\w+)\s:\sOLD\s(\d+[\.?|\s?]\d+)\S\sNEW\s(\d+[\.?|\s?]\d+)')
re_badlength_pattern = re.compile(r'Bad length.+AEIV.+\[(\w+\-\w+)\]\s@\s\((\d+/\d+/\d+/\d+/\d+)\)')
fileList=[]
evChanged=[]
def splitEV(evName):
	#name=deiCQ612PSDASD__110-LCBOPE, DEIV, old=0, new=0, delta=0
	#name=deiCQ612PSDASD__110-CLCECL, DEIV, old=0, new=0, delta=0
	#name=deiCQ612PSDASD__110-OPEFAL, DEIV, old=0, new=0, delta=0
	#name=aeiCQ628BASAT___ATPB-VOLAA, AEIV, old=229.0, new=228.0, delta=1.0
	#name=aeiCQ628BASAT___ATPB-VOLAB, AEIV, old=229.0, new=228.0, delta=1.0
	#name=deiCQ612PSDASD__111-FULOPSTA, DEIV, old=0, new=1, delta=1
	#name=deiCQ612PSDASD__111-FULCLSTA, DEIV, old=0, new=0, delta=0
	#re_ev_split_patt = re.compile(r'')
	pos = -1
	sys = "UNKNOWN"
	res_in_csv = evName[0:3] + "," + evName[3:8] + "," #aei,CQ612,
	for x in xrange(0,len(sysNames)):
		sys = sysNames[x]
		pos = evName.find(sys)
		if pos>0:			
			pos = pos + len(sys)	#find string last index
			break
	res_in_csv = res_in_csv + sys + "," #aei,CQ612,PSD
	res_in_csv = res_in_csv + evName[pos:pos+4] +"," #aei,CQ612,PSD,ASD_
	pos_hyphen = evName.find('-')
	len_point_name = len(evName) - pos_hyphen
	pos_label = len(evName) - len_point_name
	res_in_csv = res_in_csv + evName[pos+4+1:pos_hyphen] +"," #aei,CQ612,PSD,ASD_,110
	res_in_csv = res_in_csv + evName[pos_hyphen+1:pos_hyphen+len_point_name] #aei,CQ612,PSD,ASD_,110
	#print evName + "  -->\t\t" + res_in_csv
	return res_in_csv
def listFiles(dirPath):
	re_filename_pattern = re.compile(r'.+\.\d+')
	cnt = 0
	for root, dirs,files in os.walk(dirPath):
		for fileObj in files:
			m = re_filename_pattern.search(fileObj)
			if m:				
				print "adding file (" + str(cnt+1) + "): " + fileObj
				fileList.append(os.path.join(root,fileObj))
			else:
				print "skipping file(" + str(cnt+1) + "): " + fileObj
			cnt = cnt + 1
	print "scanning process is over. " + str(cnt) + " file(s) added."
	return fileList

def main():
	baseDir = "C:\\UnifyIO\\log"
	fileList = listFiles(baseDir)
	fileNumber = str(len(fileList))
	fileCnt = 0
	for filePath in fileList:
		print "processing file: " + filePath + " ["+ str(fileCnt+1) +" of " + fileNumber +"]..."
		cnt = 0
		prev_ev_changed = len(evChanged)		
		all_lines = open(filePath).readlines()
		#to process each file
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

		print str(len(evChanged) - prev_ev_changed) + " of " + str(len(evChanged))
		fileCnt = fileCnt + 1
	output = open(baseDir+"\\external_vars.csv",'w+')
	for x in xrange(0,len(evChanged)):
		evGet = evChanged[x]
		splitted_str = splitEV(evGet.evName)		
		output.write(evGet.evName + "," + splitted_str + "," + evGet.evAddr + "," + str(evGet.evValOLD) + "," + str(evGet.evValNEW) + "," + str(abs(evGet.evDelta)) +'\n')
		output.flush()
			#print "name=" + evGet.evName + ", " + evGet.evType + ", old=" + str(evGet.evValOLD) + ", new=" + str(evGet.evValNEW) + ", delta=" + str( abs(evGet.evDelta))
	output.close()
	return

main()
print "all done."
