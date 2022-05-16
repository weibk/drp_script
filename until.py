#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :check_line.py
# @Time      :2022/5/12 10:52:40
# @Author    :weibk

import sys, paramiko


client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect(hostname="172.16.130.200", port=22, username="root", password="1234")

stdin, stdout, stderr = client.exec_command("ps aux | grep drp")
print(stdout.readlines())