import os, traceback, sys
sys.path.append(os.getcwd())
import maintanance_lib_v1 as mlib
import arguments as arg

def main():
	if sys.argv[1] == 'step1':
		pull_servers()
	if sys.argv[1] == 'step2':
		get_servers_to_clean()

def get_servers_to_clean():
	stc = mlib.Servers_To_Clean(arg.servers_buffer_f, arg.servers_to_clean_f, arg.space_less_then)
	stc.generate_list()


def pull_servers():
	#Getting the latest cs_filepath
	cwd=os.getcwd()
	log_file=cwd+'/log/generate_list.log'
	sys.stdout=open(log_file, 'w') #logging to log file in the same directory
	# servers_file_path=cwd+'/servers.txt'
	servers_file_path=arg.servers_f
	folder = arg.csv_folder
	space_less_then=arg.space_less_then
	cs_file=mlib.CS_File(folder)
	cs_file.locate_file()
	cs_filepath=cs_file.get_filepath()

	#get list of servers
	data=mlib.DataCollector(cs_filepath, space_less_then)
	data.collect_data()
	servers=data.get_data()

	#create the file with server list dump:
	srv=mlib.Servers(servers, servers_file_path)
	srv.generate_list()




if __name__=="__main__":
	main()