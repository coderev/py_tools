import os
import re
import shutil
print "here begins the replace progress ..."
#global port_num
fileList=[]
def listFiles(dirPath):
	for root, dirs,files in os.walk(dirPath):
		for fileObj in files:
			suffix = os.path.splitext(fileObj)[1]
			if suffix=='.dat':
				#print 'the suffix is:' + suffix
				print "adding " + fileObj
				fileList.append(os.path.join(root,fileObj))
	return fileList
def replace_port():
	return "Port = " + port_num

def main():
	port_num = 1234
	target_linenum = 4 #zero bases line number

	fileDir = "C:\QSango\Bak"
	backup_dir = r'.\backup'
	if not os.path.exists(backup_dir):
		os.makedirs(backup_dir)
	fileList = listFiles(fileDir)
	for filePath in fileList:
		shutil.copy(filePath, backup_dir)
		all_lines = open(filePath).readlines()
		cnt = 0
		for line in all_lines:
			if line.find('Port')==0:
				all_lines[cnt] = line.replace('Port = 1234,', 'Port = ' + str(port_num) +',')
				print all_lines[cnt]				
				open(filePath,'wb').writelines(all_lines)
				port_num = port_num + 1
				break
			cnt = cnt + 1
	return
main()
print "replace all done."
