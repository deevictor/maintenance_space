"""
Possible paths of WAS: d$/IBM/{websphere,AppServer_AS}/profiles/{Dmgr01,AppSrv01}

def main():

class Server():
    methods:
        detect and create object of instances.

        parse d$/IBM and if r'^websphere.*' or r'^AppServer.*':
            create instance


class Instance():
    methods:
        checks whether Node, cell or standalone
        depending on the type trigger appropriate wsadmin.bat and launch cleaner.


if __name__ == "__main__":
    main()

"""
import os, re, sys, traceback, subprocess
import arguments as arg

def main():
    servers_obj=ServerList(arg.servers_to_clean_f)
    host_names=servers_obj.get_list()
    global user, password, wd
    wd = arg.wd
    user = arg.user
    password = arg.password

    srvs=[Server(host_name) for host_name in host_names]
    # print("srvs created")
    for srv in srvs:
        srv.create_instances()
        srv.clean_server()
        

#################################################################################################
class ServerList():
    """returns the list of the servers"""
    def __init__(self, source_f):
        self.source=source_f

    def get_list(self):
        """"""
        with open(self.source) as f_obj:
            srvs=f_obj.readlines()
            srvs=[server.strip() for server in srvs]
        return srvs
################################################################################################
class Server():
    """This class represents the server with instances of WAS installed"""
    def __init__(self, host_name):
        self.host = host_name
        self.instances=[]

    def create_instances(self):
        """if instance has profile with bin/wsadmin.bat it is valid instance"""
        disk_d = "//"+self.host+"/d$"
        mask = r"^IBM$|^WebSphere.*"
        root_flag = 0
        # print(os.listdir(disk_d))  #checkpoint
        for item in os.listdir(disk_d):
            searchObj = re.search(mask, item, re.M|re.I)
            if searchObj:
                root_flag = 1
                rootdir=disk_d+"/"+searchObj.group()
                # print(rootdir)  #checkpoint

                if os.path.isdir(rootdir):
                    candidates=os.listdir(rootdir)
                    # print(candidates) #checkpoint
                    for candidate in candidates:
                        if os.path.isdir(rootdir+'/'+candidate+'/profiles'):
                            user_install_root=rootdir+'/'+candidate
                            candidate_instance=Instance(user_install_root)
                            candidate_instance.get_profiles()
                            if candidate_instance.profiles:
                                self.instances.append(candidate_instance)
                                # print(candidate_instance.uir+": "+str(candidate_instance.profiles)) #checkpoint

        if root_flag == 0:  print(self.host+" does not have IBM or WebSphere directory on disk D")

    def clean_server(self):
        for instance in self.instances:
            # pass the argument 'backup' on to the first instance in the list
            if self.instances.index(instance) == 0:
                instance.trigger_clean_script('backup')
            else:
                instance.trigger_clean_script()
            # print(instance.profiles)  #checkpoint

######################################################################################################
class Instance():
    """this class represents the instance with the location of wsadmin we will use for our job"""
    def __init__(self, user_install_root):
        self.uir=user_install_root
        self.profiles=[]
        self.host = self.uir.split('/')[2]

    def get_profiles(self):
        """
        if profiles directory exist and this directory has at least one profile with wsadmin.bat inside, then this profile is valid and
        is added to profiles list of the Instance object.
        """
        # print(self.uir) #checkpoint
        if os.path.isdir(self.uir+"/profiles"):
            profiles=os.listdir(self.uir+"/profiles")
            # print(profiles)       #checkpoint
            for profile in profiles:
                wsadmin=self.uir+"/profiles/"+profile+"/bin/wsadmin.bat"
                if os.path.isfile(wsadmin):                #check for wsadmin.bat.
                    self.profiles.append(self.uir+"/profiles/"+profile)

        else:   print(self.uir+' Instance does not have "profile" folder in '+self.uir)
        return

    def trigger_clean_script(self, arg=""):
        # print(str(self.profiles)+'\n')  #checkpoint
        for profile in self.profiles:
            local_profile = '/'.join(profile.split('/')[3:]).replace('$', ':')
            w_profile = local_profile.replace('/', '\\')
            #pass the argument only to the first profile.
            arg1 = ''
            if self.profiles.index(profile) == 0:
                arg1 = arg
            command = r'd:\wa\wis\psexec \\'+self.host+' -h -u '+user+' -p '+password+' -d cmd /c "pushd '+wd+' && call '+w_profile+r'\bin\wsadmin.bat -f clean_space_v9.py '+local_profile+' '+arg1+'"'
            # print(command)
            p=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            stdout, stderr=p.communicate()
            print(p.returncode)
            
        return

if __name__ == "__main__":
    main()



