# maintenance_space
workflow:
1). "python generate_list_v0.py step1"	-	to pull ALL the servers from the report according to the free space in DiskD(arg.space_less_then is used) and damp it to servers.txt
2) "check_space_WMI.ps1 > 1.txt"	-	to make the servers_buffer_f(1.txt) and get the real free space.
3). "python generate_list_v0.py step2"	-	pulls the content of servers_buffer_f(1.txt) and damps the servers to arg.servers_to_clean_f(servers_to_clean.txt).
4). "python uni_clean_launcher.py" - to clean the servers from servers_to_clean.txt file(logs, backups, derby)
