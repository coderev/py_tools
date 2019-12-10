#!C:/Python27
#coding=utf-8
#Revised by Melody 15 Jan,2019
import paramiko
import os
def runcmd(client, cmd):
    try:
        stdin, stdout, stderr = client.exec_command(cmd)
        #print stderr.read()+stdout.read()
    except Exception as e:
        print e
    finally:
        print "--> ssh run command["+cmd + "]"

def putfile(client, local_path, remote_path):
    try:
        sftpAttr = client.put(local_path,remote_path,confirm=True)
        #print sftpAttr.__str__()
    except Exception as e:
        print e
    finally:
        print "--> upload file["+local_path + "] to " + remote_path
            

def getfile(client, remote_path, local_path):
    try:
        client.get(remote_path,local_path)
        #print stderr.read()+stdout.read()
    except Exception as e:
        print e
    finally:
        print "--> download file["+local_path + "]"

def updateEnv(host,user,passwd,env,svrid,version):
    transport = paramiko.Transport((host,secure_port))
    transport.connect(username=user,password=passwd)  
    sftp = paramiko.SFTPClient.from_transport(transport)
    putfile(sftp, FILE_LOCATION+"/"+env+version+".tar.gz", "/export/home/"+user+"/"+env+version+".tar.gz")    
    transport.close()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host,port=secure_port,username=user,password=passwd)
    runcmd(ssh, "gunzip -c "+env+version+".tar.gz|tar xvf -")
    runcmd(ssh, "rm current")
    runcmd(ssh, "ln -sf "+env+version+" current")
    runcmd(ssh, "cd ./"+env+version+"/scs/dac;ln -sf ScsDacCtrt/ScsDacCtrt_" + env[0:3] +"SRLT"+ str(svrid) + " ScsDacCtrt.cfg")
    runcmd(ssh, "exit")
    ssh.close()

def uploadFile(host,user,passwd,localpath,remotepath):
    transport = paramiko.Transport((host,secure_port))
    transport.connect(username=user,password=passwd)  
    sftp = paramiko.SFTPClient.from_transport(transport)
    putfile(sftp, localpath, remotepath)    
    transport.close()


def runcmdOnRemote(host,name,pas,command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host,port=secure_port,username=name,password=pas)
    runcmd(ssh,command)
    ssh.close
	
def multiUploadFolder(host,user,passwd,localdir,remotedir):
    transport = paramiko.Transport((host,secure_port))
    transport.connect(username=user,password=passwd)  
    sftp = paramiko.SFTPClient.from_transport(transport)
    list = os.listdir(localdir)
    for i in range(0,len(list)):
        npath=os.path.join(localdir, list[i])
        rpath=remotedir+"/"+list[i]
        if os.path.isfile(npath):
            putfile(sftp, npath, rpath)
    transport.close()
	

# define the file location & software version
FILE_LOCATION="20191210"
SOFTWARE_VERSION="_A3_190530"

secure_port = 22
paramiko.util.log_to_file('syslogin.log')

#updateEnv("soldv40","nbl2","nbl2iscs","OCC",1,SOFTWARE_VERSION) 
#updateEnv("soldv40","nbl3","nbl3iscs","OCCB",1,SOFTWARE_VERSION) 
#updateEnv("soldv40","nbl4","nbl4iscs","OCCC",1,SOFTWARE_VERSION) 
#updateEnv("soldv41","nbl2","nbl2iscs","OCC",2,SOFTWARE_VERSION) 
#updateEnv("soldv41","nbl3","nbl3iscs","OCCB",2,SOFTWARE_VERSION) 
#updateEnv("soldv41","nbl4","nbl4iscs","OCCC",2,SOFTWARE_VERSION) 

#update ScsEnvList

uploadFile("soldv40","nbl2","nbl2iscs",FILE_LOCATION+"/ScsEnvList","/export/home/nbl2/current/scs/ScsEnvList")
uploadFile("soldv40","nbl3","nbl3iscs",FILE_LOCATION+"/ScsEnvList","/export/home/nbl3/current/scs/ScsEnvList")
uploadFile("soldv40","nbl4","nbl4iscs",FILE_LOCATION+"/ScsEnvList","/export/home/nbl4/current/scs/ScsEnvList")


uploadFile("soldv41","nbl2","nbl2iscs",FILE_LOCATION+"/ScsEnvList","/export/home/nbl2/current/scs/ScsEnvList")
uploadFile("soldv41","nbl3","nbl3iscs",FILE_LOCATION+"/ScsEnvList","/export/home/nbl3/current/scs/ScsEnvList")
uploadFile("soldv41","nbl4","nbl4iscs",FILE_LOCATION+"/ScsEnvList","/export/home/nbl4/current/scs/ScsEnvList")

#update OCC ScsDacCtrl.cfg in soldv40 solv41
uploadFile("soldv40","nbl2","nbl2iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT1","/export/home/nbl2/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT1")
uploadFile("soldv40","nbl2","nbl2iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT2","/export/home/nbl2/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT2")
uploadFile("soldv40","nbl3","nbl3iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT1","/export/home/nbl3/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT1")
uploadFile("soldv40","nbl3","nbl3iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT2","/export/home/nbl3/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT2")
uploadFile("soldv40","nbl4","nbl4iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT1","/export/home/nbl4/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT1")
uploadFile("soldv40","nbl4","nbl4iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT2","/export/home/nbl4/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT2")

uploadFile("soldv41","nbl2","nbl2iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT1","/export/home/nbl2/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT1")
uploadFile("soldv41","nbl2","nbl2iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT2","/export/home/nbl2/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT2")
uploadFile("soldv41","nbl3","nbl3iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT1","/export/home/nbl3/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT1")
uploadFile("soldv41","nbl3","nbl3iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT2","/export/home/nbl3/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT2")
uploadFile("soldv41","nbl4","nbl4iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT1","/export/home/nbl4/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT1")
uploadFile("soldv41","nbl4","nbl4iscs",FILE_LOCATION+"/ScsDacCtrt_OCCSRLT2","/export/home/nbl4/current/scs/dac/ScsDacCtrt/ScsDacCtrt_OCCSRLT2")

multiUploadFolder("soldv40","nbl2","nbl2iscs",FILE_LOCATION + "/trans","/export/home/nbl2/current/scs/dac/")
multiUploadFolder("soldv40","nbl3","nbl3iscs",FILE_LOCATION + "/trans","/export/home/nbl3/current/scs/dac/")
multiUploadFolder("soldv40","nbl4","nbl4iscs",FILE_LOCATION + "/trans","/export/home/nbl4/current/scs/dac/")

multiUploadFolder("soldv41","nbl2","nbl2iscs",FILE_LOCATION + "/trans","/export/home/nbl2/current/scs/dac/")
multiUploadFolder("soldv41","nbl3","nbl3iscs",FILE_LOCATION + "/trans","/export/home/nbl3/current/scs/dac/")
multiUploadFolder("soldv41","nbl4","nbl4iscs",FILE_LOCATION + "/trans","/export/home/nbl4/current/scs/dac/")