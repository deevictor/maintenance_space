import socket, sys, os, traceback, shutil, sys, time, re
import arguments as arg
def main():	
	#turning on the logging
	print(sys.argv)
	profile = sys.argv[0]
	#check on backup_flag
	if len(sys.argv)>1:
		backup_flag = sys.argv[1]
	else:
		backup_flag = None
	host=socket.gethostname()

	orig_stdout=sys.stdout
	log_path_bit=profile.split('/')[2]+'_'+profile.split('/')[4]
	log_path=arg.wd+'/log/'+host+'_'+log_path_bit+'.log'
	f=open(log_path,'a')
	sys.stdout=f

	backups_folder='d:/backup'
	derby_file = '/'.join(profile.split('/')[:3]) + '/derby/derby.log'
	tlog_folder = profile+'/logs'

	# num_days=arg.logs_older_then
	srv=Server(backups_folder, derby_file, tlog_folder, profile)

	# #deletion of all backups in backup folder except the latest.
	if backup_flag:
		srv.clean_backups()
		#deletion of derby file
		srv.delete_derby()
	#delete temporary catalogs: temp, tranlog, wstemp:
	srv.del_temp_catalogs()
	#clear in D:\IBM\AppServer_Filial\profiles\AppSrv01\logs\server1: files; oddo, as-fsb folder content
	# if file then delete, if dir go inside and do the same (recursive)
	srv.strip_log_folder(srv.tlog_folder)
	#delete dumps with life more then dump_older_the
	srv.delete_dumps()
	print(host+'  is cleaned, SUCCESS')
	# closing the logging
	sys.stdout=orig_stdout
	f.close()

############################################

class Server:
	def __init__(self, backups_folder, derby_file, tlog_folder, profile):
		self.backups_folder=backups_folder
		self.derby_file=derby_file
		self.tlog_folder=tlog_folder
		# self.num_days=num_days
		self.host=socket.gethostname()
		self.profile = profile

	def del_folder(self, folder):
		if os.path.isdir(folder):
			try:
				shutil.rmtree(folder)
				print(folder+' is deleted')
			except OSError:
				print('unable to delete: '+folder)
				traceback.print_exc()
				pass
		else:
			print(folder+' is absent')

	def del_temp_catalogs(self):
		temp_catalogs=['temp', 'tranlog', 'wstemp']
		for temp_catalog in temp_catalogs:
			tc_path=self.profile+'/'+temp_catalog
			self.del_folder(tc_path)

	def strip_log_folder(self, log_folder):
		if log_folder:
			# print("strip_log_folder is launched")
			for the_item in os.listdir(log_folder):
				item_path=os.path.join(log_folder+"/"+the_item)
				try:
					if os.path.isfile(item_path) and self.delta_time_check(item_path, arg.log_older_then)==1:
						os.unlink(item_path)
						# print(item_path+" is deleted")
					elif os.path.isfile(item_path) and self.delta_time_check(item_path, arg.log_older_then)==0:
						# print(item_path+" is modified less then "+str(self.num_days)+"-days ago")
						pass				
					elif os.path.isdir(item_path):
						print('\n'+item_path+' is a directory, going level deeper\n')
						folder1=item_path
						self.strip_log_folder(folder1) #recursive call
					else:
						print("ERROR: doing nothing, condition is not matched")
				except OSError:
					print('unable to delete: '+item_path+'. Probably the server is running.')
					pass
			if log_folder == self.tlog_folder:
				print(self.host+' '+self.tlog_folder+' is stripped recursively')
			else:
				print(self.host+' '+log_folder+' is stripped')
		else:	print(self.host+' : '+log_folder+' does not exist')

	def delta_time_check(self, file_path, num_days):
		time_flag=0
		fileModification=os.path.getmtime(file_path)
		now=time.time()
		days_ago = now - 60*60*24*num_days
		if fileModification < days_ago:
			time_flag=1
		return time_flag

	def delete_derby(self):
		if self.derby_file:
			try:
				os.remove(self.derby_file)
				print(self.host+' '+self.derby_file+' is deleted')
			except Exception:
				traceback.print_exc()
				print(self.host+' '+self.derby_file+' is NOT deleted')
				pass
		else:	print(self.host+' derby file is NOT deleted\n'+self.derby_file+' does not exist')

	def delete_dumps(self):
		print('delete_dumps is started')
		dump_pattern = r'^[a-z]+.\d{8}.\d+..*(txt|phd)$'
		for item in os.listdir(self.profile):
			item_path = os.path.join(self.profile+'/'+item)
			searchObj = re.search(dump_pattern, item, re.M|re.I)
			try:
				if os.path.isfile(item_path) and self.delta_time_check(item_path, arg.dump_older_then) == 1 and searchObj:
					os.unlink(item_path)
					print(searchObj.group()," is deleted")
				# print(self.profile+': '+item.path)
			except OSError:
				print('unable to delete: ', item_path)
				pass



	def clean_backups(self):
		if os.path.isdir(self.backups_folder):
			list_backups=os.listdir(self.backups_folder)
			list_backups.sort()
			list_del=list_backups[0:-1]
			for item in list_del:
				try:
					folder=self.backups_folder+"/"+item
					shutil.rmtree(folder)
					print(folder+' is deleted')
				except OSError:
					traceback.print_exc()
					pass
			print(self.host+' backups are cleaned except the latest')
		else:	print("Backup folder does not exist.")

if __name__=='__main__':
	main()