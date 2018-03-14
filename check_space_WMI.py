import os, wmi, win32com
import arguments as arg
import maintanance_lib_v1 as mlib
import uni_clean_launcher_v2 as uni
from operator import itemgetter

def main():
    #generating the statistics from servers.txt
    stat_file_path=arg.stat_f
    headings = ('Host', 'Disk', 'Size(Gb)', 'Free(Gb)', 'Free(%)')
    underline = ('----', '----', '--------', '--------', '-------')
    toplines = [headings, underline]
    #getting the statistic for hosts
    stats=[]
    servers_obj=uni.ServerList(arg.servers_f)
    host_names=servers_obj.get_list()
    for host in host_names:
        c = wmi.WMI(host)
        for d in c.Win32_LogicalDisk():
            if d.Caption == 'D:':
                FreeSpacePercents = int(int(d.FreeSpace)/int(d.Size)*100)
                Size = convert_to_Gb(d.Size)
                FreeSpace = convert_to_Gb(d.FreeSpace)
                stat_line = (host, d.Caption, Size, FreeSpace, FreeSpacePercents)
                stats.append(stat_line)
    #sorting by FreeSpacePercents using operator.itemgetter
    stats_sorted = sorted(stats, key=itemgetter(4), reverse=True)
    #appending stats to toplines:
    lines = toplines+stats_sorted
    print(lines)
    # printing to file:
    with open(stat_file_path, 'w') as file_object:
        #formatting lines into blocks for columns
        for line in lines:
            print_line='{0:<20} {1:<5} {2:>10} {3:>10} {4:>10}'.format(*line)
            print(print_line)
            file_object.write(print_line+'\n')
    print('\nDONE!\n')




def convert_to_Gb(b):
    gb=round(int(b)/(1024**3), 1)
    return gb

###############################################################################
if __name__ == '__main__':
    main()