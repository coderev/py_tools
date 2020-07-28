#!C:/Python27
#coding=utf-8
import os
import paramiko
import json
import sys, getopt

secure_port = 22
paramiko.util.log_to_file('syslogin.log')


def _runcmd(client, cmd):
    try:
        _, stdout, stderr = client.exec_command(cmd)
        print stderr.read()+stdout.read()
    except Exception as e:
        print e
    finally:
        print "--> ssh run command[" + cmd + "]"

def _putfile(client, local_path, remote_path):
    try:
        sftpAttr = client.put(local_path,remote_path,confirm=True)
        print sftpAttr.__str__()
    except Exception as e:
        print e
    finally:
        print "--> upload file["+local_path + "] to " + remote_path
            

def _getfile(client, remote_path, local_path):
    try:
        client.get(remote_path,local_path)
    except Exception as e:
        print e
    finally:
        print "--> download file["+local_path + "]"

#def updateEnv(host,user,passwd,env,svrid,version):
#    transport = paramiko.Transport((host,secure_port))
#    transport.connect(username=user,password=passwd)  
#    sftp = paramiko.SFTPClient.from_transport(transport)
#    putfile(sftp, FILE_LOCATION+"/"+env+version+".tar.gz", "/export/home/"+user+"/"+env+version+".tar.gz")    
#    transport.close()
#    ssh = paramiko.SSHClient()
#    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    ssh.connect(hostname=host,port=secure_port,username=user,password=passwd)
#    runcmd(ssh, "gunzip -c "+env+version+".tar.gz|tar xvf -")
#    runcmd(ssh, "rm current")
#    runcmd(ssh, "ln -sf "+env+version+" current")
#    runcmd(ssh, "cd ./"+env+version+"/scs/dac;ln -sf ScsDacCtrt/ScsDacCtrt_" + env[0:3] +"SRLT"+ str(svrid) + " ScsDacCtrt.cfg")
#    runcmd(ssh, "exit")
#    ssh.close()

def uploadFile(host,user,passwd,localpath,remotepath):
    transport = paramiko.Transport((host,secure_port))
    transport.connect(username=user,password=passwd)  
    sftp = paramiko.SFTPClient.from_transport(transport)
    _putfile(sftp, localpath, remotepath)    
    transport.close()


def runcmdOnRemote(host,user,passwd,command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host,port=secure_port,username=user,password=passwd)
    _runcmd(ssh,command)
    ssh.close
	
def uploadFolder(host,user,passwd,localdir,remotedir):
    transport = paramiko.Transport((host,secure_port))
    transport.connect(username=user,password=passwd)  
    sftp = paramiko.SFTPClient.from_transport(transport)
    flist = os.listdir(localdir)
    for i in range(0,len(flist)):
        npath=os.path.join(localdir, flist[i])
        rpath=remotedir+"/"+flist[i]
        if os.path.isfile(npath):
            _putfile(sftp, npath, rpath)
    transport.close()


def main(argv):
    inputfile="tasks.json"
    try:
        opts, _ = getopt.getopt(argv,"hi:o:",["input="])
    except getopt.GetoptError:
        print 'dispatcher.py -i <tasks.json>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'dispatcher.py -i <tasks.json>'
            sys.exit()
        elif opt in ("-i", "--input"):
            inputfile = arg
            print "the input is" , inputfile    
    data=json.load(open(inputfile))
    for item in data['tasks']:
        ip=item['ip']
        user=item['user']
        passwd=item['passwd']
        for one in item['task']:
            mtype=one['type']
            if mtype=='upload':
                mfile=one['file']
                mlpath=one['local']
                mrpath=one['remote']
                print "mission [upload] ", ip, user, passwd, mtype, mlpath, mrpath,mfile
                uploadFile(ip,user,passwd,mlpath+"/"+mfile,mrpath+"/"+mfile)
            elif mtype=='download':
                print "not implemented"
            elif mtype=='exec':
                mcmd=one['cmd']
                print "mission [exec] ", ip, user, passwd, mcmd
                runcmdOnRemote(ip,user,passwd,mcmd)
            else:
                print "no matching conditions"            
            
        print "all takss in tasks.json are done"


main(sys.argv[1:])
