#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @FileName  :watch_counter.py
# @Time      :2022/5/12 13:37:46
# @Author    :weibk

import paramiko, sys, time, os, re, ast

log_dir = "/home/flowdrp/release/log/"


client = paramiko.SSHClient()
client.load_system_host_keys()
client.connect(hostname="172.16.130.200", port=22, username="root", password="1234")

def get_new_file():
    stdin, stdout, stderr = client.exec_command(f"ls -lrt {log_dir}")
    log_files = [x[:-1].split(" ")[-1] for x in stdout.readlines()[1:]]
    return log_files[-1]

new_file = get_new_file()

curren_position = ""
while True:
    f = open(f"{log_dir}{new_file}", mode="r", encoding="utf-8")
    data = f.readlines()
    data = [e[:-1] for e in data if "3405 INFO" in e]
    curren_position = f.tell()
    log_line = data[-1]
    # print(log_line)
    log_data = ast.literal_eval(re.search("\[\s{\s\"receiver\".*\]", log_line).group())
    if not log_data[0]["receiver"]:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        print("当前没有任务在运行")
        time.sleep(60)
    else:
        break
if log_data[0]["receiver"][0]["thread"][-1]["stat"]:
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    receiver_info = log_data[0]["receiver"][0]["thread"][-1]["stat"]
    formatter_info = log_data[2]["formatter"][0]["thread"][-1]["stat"]["xdr_type_list"][0]
    sender_info = log_data[3]["sender"][0]["thread"][-1]["stat"]
    print(f"receiver\trx_msg: {receiver_info['rx_msg']}")
    print(f"formatter\ttx_msg: {formatter_info['tx_msg']}, xdr_type: {formatter_info['xdr_type ']}")
    print(f"sender\ttx_msg: {sender_info['tx_msg']}, tx_file: {sender_info['tx_file']}")
else:
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
    print("话单处理完毕")
while True:
    time.sleep(70)
    f1 = open(f"{log_dir}{new_file}", mode="r", encoding="utf-8")
    f1.seek(curren_position, 0)
    data = f1.readlines()
    data = [e[:-1] for e in data if "3405 INFO" in e]
    curren_position = f.tell()
    log_line = data[-1]
    # print(log_line)
    log_data = ast.literal_eval(re.search("\[\s{\s\"receiver\".*\]", log_line).group())
    if log_data[0]["receiver"][0]["thread"][-1]["stat"]:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        receiver_info = log_data[0]["receiver"][0]["thread"][-1]["stat"]
        formatter_info = log_data[2]["formatter"][0]["thread"][-1]["stat"]["xdr_type_list"][0]
        sender_info = log_data[3]["sender"][0]["thread"][-1]["stat"]
        print(f"receiver\trx_msg: {receiver_info['rx_msg']}")
        print(f"formatter\ttx_msg: {formatter_info['tx_msg']}, xdr_type: {formatter_info['xdr_type ']}")
        print(f"sender\ttx_msg: {sender_info['tx_msg']}, tx_file: {sender_info['tx_file']}")
    else:
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        print(f"话单处理完毕")
