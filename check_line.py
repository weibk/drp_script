#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :check_line.py
# @Time      :2022/5/12 10:52:40
# @Author    :weibk

import sys, paramiko

data_dir = sys.argv[1]
file_lines = sys.argv[2]

client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect(hostname="172.16.130.200", port=22, username="root", password="1234")

stdin, stdout, stderr = client.exec_command(f"cd {data_dir} && wc -l *")
result = [x[:-1].strip().split(" ") for x in stdout.readlines()[:-1]]
file_list = [x[1] for x in result]

for item in result:
    lines_num = item[0]
    fname = item[1]
    if lines_num == file_lines:
        # print(f"{fname} 文件行数合格")
        pass
    else:
        fid = int(fname.split("_")[-1].split(".")[0])
        file_type = fname.split(".")[1]
        next_fid = str(fid+1).zfill(3)
        new_file = fname.split("_")[:3]
        new_file.append(next_fid)
        new_file = "_".join(new_file) + "." + file_type
        if new_file in file_list:
            print(f"{fname} 文件行数不合格, 行数为{lines_num}")
        else:
            # print(f"{fname} 文件行数合格")
            pass