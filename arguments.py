csv_folder='D:/reports/check_space'
space_less_then=20 #Gb
servers_f='servers.txt' #file where we dump servers from csv_folder
servers_buffer_f = '1.txt' #file where we dump files after checkSpace
servers_to_clean_f = 'servers_to_clean.txt' #file where we dump servers from servers_buffer_f
user = 'alpha\pakay'
password = ''
wd=r'\\v-middle-8r2-02.ca.sbrf.ru\d$\div\scripts\maintanance_space'
log_older_then=1
dump_older_then=0
stat_f="stat.txt"