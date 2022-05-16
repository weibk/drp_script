#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :counter_util.py
# @Time      :2022/5/13 11:51:39
# @Author    :weibk

import paramiko, sys, time, os, re, json

log_dir = "/home/flowdrp/release/log/"


client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect(hostname="172.16.130.200", port=22, username="root", password="1234")

def get_new_file():
    stdin, stdout, stderr = client.exec_command(f"ls -lrt {log_dir}")
    log_files = [x[:-1].split(" ")[-1] for x in stdout.readlines()[1:]]
    return log_files[-1]

re_1 = '({ "receiver": \[.*), { "processor":.*'

while True:
    new_file = get_new_file()
    with open(f"{log_dir}{new_file}", mode="r", encoding="utf-8") as f:
        data = [x for x in f.readlines() if "3412 INFO" in x]
        receiver = 0
        err = 0
        try:
            for item in data:
                receiver_info= json.loads(re.search(re_1, item).groups()[0])
                if receiver_info["receiver"]:
                    if receiver_info["receiver"][0]["thread"][-1]["stat"]:
                        current_receiver = receiver_info["receiver"][0]["thread"][-1]["stat"]["rx_msg"]
                        err_counter = receiver_info["receiver"][0]["thread"][-1]["stat"]["error"]
                        receiver += current_receiver
                        err += err_counter
                        print(f"rx_msg: {current_receiver}")
        except:
            pass
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        print("当前receiver统计如下：")
        print(f"rx_msg: {receiver}, error: {err}")
        print(f"-------------------stop-------------------")
    time.sleep(60)
