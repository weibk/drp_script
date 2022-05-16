#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :check_size.py
# @Time      :2022/5/12 9:47:36
# @Author    :weibk

import paramiko, sys, re

data_dir = sys.argv[1]
file_size = sys.argv[2]

client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect(hostname="172.16.130.200", port=22, username="root", password="1234")

stdin, stdout, stderr = client.exec_command(f"cd {data_dir} && du -h *")
result = [x[:-1].split("\t") for x in stdout.readlines()]
file_list = [x[1] for x in result]

for item in result:
    size = re.search("\d*", item[0]).group()
    fname = item[1]
    if size == file_size:
        # print(f"{fname} 文件大小合格")
        pass
    else:
        fid = int(fname.split("_")[-1].split(".")[0])
        file_type = fname.split(".")[1]
        next_fid = str(fid+1).zfill(3)
        new_file = fname.split("_")[:3]
        new_file.append(next_fid)
        new_file = "_".join(new_file) + "." + file_type
        if new_file in file_list:
            print(f"{fname} 文件大小不合格, 大小为{size}")
        else:
            # print(f"{fname} 文件大小合格")
            pass