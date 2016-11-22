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

	fileDir = "C:\SimD\exbak"
	backup_dir = r'.\backup'
	if not os.path.exists(backup_dir):
		os.makedirs(backup_dir)
	fileList = listFiles(fileDir)
	for fileObj in fileList:
		shutil.copy(fileObj, backup_dir)
		lines = open(fileObj).readlines()
		#print re.sub(r'Port = 1234','sssss', port_num)		
		#print lines, fileObj, port_num
		lines[target_linenum] = lines[target_linenum].replace('Port = 1234,','Port = ' + str(port_num) +',')
		#save changes
		print fileObj + " changed to: " + lines[target_linenum]
		open(fileObj,'wb').writelines(lines)
		port_num = port_num + 1
		#for s in lines:
		#	s.replace('Port = 1234,','Port = ' + str(port_num) +',')
		#	print fileObj + " has been done."
	return
main()
print "replace all done."
