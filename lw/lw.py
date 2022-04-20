#!/usr/bin/python3
## -*- coding: utf-8 -*-

import os
import sys
import vw
import re
import socket
from datetime import datetime

mask = vw.mask
cfg_dir = vw.cfg_dir


freq_list_err = vw.freq_list_err
freq_list_warn = vw.freq_list_warn

count_lww = open("{}/count_lw.txt".format(cfg_dir), 'r')
count_lw = int(count_lww.read())+1
count_lww.close()
f = open("{}/count_lw.txt".format(cfg_dir),'w')
f.write(str(count_lw))
f.close()

if (os.environ.get('USER')!=vw.user):
    print(f"Required login as {vw.user}!!!")
    sys.exit()

if ("--count-used" in sys.argv):
    print(count_lw)
    sys.exit()

def help():
    print ('''
 _                        _    __        __
| |    ___   __ _  __   _(_) __\ \      / /__ _ __
| |   / _ \ / _` | \ \ / / |/ _ \ \ /\ / / _ \ '__|
| |__| (_) | (_| |  \ V /| |  __/\ V  V /  __/ |
|_____\___/ \__, |   \_/ |_|\___| \_/\_/ \___|_|
            |___/
''')
    print("\nScript to catch logs and reboot services faster\n")
    print("Usage:")
    print("lw [-c][--node][-r][--config] {component}\n")
    print("   -c {argv}")
    print("        Count lines to print (default=1000)")
    print("   --cat")
    print("        Print all log file (default=1000)")
    print("   --node or -n")
    print("        Choose node (default=0)")
    print("   --config")
    print("        Show config file for choosen component")
    print("   -r")
    print("        Restart component")
    print("   --analize")
    print("        Statistic of error's count")
    print("   --count-used")
    print("        Get number of uses")
    print("   --help or -h")
    print("        This help")
    print("\n\nThanks!")
    sys.exit()

if ('-h' in sys.argv) or ('--help' in sys.argv) or len(sys.argv) == 1:
    help()


count_lines = '1000'
if "-c" in sys.argv:
    try:
        count_lines = str(sys.argv[sys.argv.index("-c")+1])
    except IndexError:
        print("1 argument needed for key: '-c'")
        sys.exit()

if ("--analize") in sys.argv:
    count_lines = "3"

def is_local(host):
    host = str(host)
    try:
        s = str(os.environ.get('HOSTNAME').split(".")[0])
    except AttributeError:
        s = ""
    if "localhost" in host or "127.0.0.1" in host or str(os.environ.get('HOSTNAME')) in host or str(socket.gethostbyname(socket.gethostname())) in host or s in host:
        return True
    else:
        return False

def uhq(mask, node, count_lines):
    key = list(vw.components_t.keys())
    print(mask)
    if "--cat" in sys.argv or " cat%s" in mask:
        count_lines = ""
    for i in range(len(vw.components_t)):
        if ".txt" in vw.components_t[key[i]][1] or ".log" in vw.components_t[key[i]][1]:
            mask = mask.rstrip(".main.log")
        for d in vw.components_t[key[i]][2]:
            if d in sys.argv[1:]:
                try:
                    if is_local(vw.components_t[key[i]][0][node]):
                        cmd = mask[mask.find("%s")+2:]  % (count_lines, key[i], vw.components_t[key[i]][1])
                    else:
                        cmd = mask % (vw.components_t[key[i]][0][node], count_lines, key[i], vw.components_t[key[i]][1])
                    os.system(cmd)
                except IndexError:
                    print(f'Node {node} does not exist. Try to initialize it.')
                except TypeError:
                    if is_local(vw.components_t[key[i]][0][node]):
                        cmd = mask[mask.find("%s")+2:]  % (count_lines, vw.components_t[key[i]][1])
                    else:
                        cmd = mask % (vw.components_t[key[i]][0][node], count_lines, vw.components_t[key[i]][1])
                break


def archive(mask, node,year,month,day):
    key = list(vw.components_t.keys())
    for i in range(len(vw.components_t)):
        for d in vw.components_t[key[i]][2]:
            if d in sys.argv[1:]:
                try:
                    if is_local(vw.components_t[key[i]][0][node]):
                        cmd = mask[mask.find("%s")+2:]  % (key[i], vw.components_t[key[i]][1],year,month,day)
                    else:
                        cmd = mask % (vw.components_t[key[i]][0][node], key[i], vw.components_t[key[i]][1],year,month,day)
                    os.system(cmd)
                except IndexError:
                    print(f'Node {node} does not exist. Try to initialize it.')
                except TypeError:
                    if is_local(vw.components_t[key[i]][0][node]):
                        cmd = mask[mask.find("%s")+2:]  % (vw.components_t[key[i]][1],year,month,day)
                    else:
                        cmd = mask % (vw.components_t[key[i]][0][node], vw.components_t[key[i]][1],year,month,day)
                    os.system(cmd)
                break



def show_config(mask, node):
    key = list(vw.components_t.keys())
    for i in range(len(vw.components_t)):
        for d in vw.components_t[key[i]][2]:
            if d in sys.argv[1:]:
                try:
                    if is_local(vw.components_t[key[i]][0][node]):
                        cmd = mask[mask.find("%s")+2:] % (key[i])
                    else:
                        cmd = mask % (vw.components_t[key[i]][0][node], key[i])
                    os.system(cmd)
                except IndexError:
                    print(f'Node {node} does not exist. Try to initialize it.')
                break

def diff(mask, node):
    sure = False
    key = list(vw.components_t.keys())
    if "-y" in sys.argv or "-ry" in sys.argv:
        sure = True
    for i in range(len(vw.components_t)):
        for d in vw.components_t[key[i]][2]:
            if d in sys.argv[1:]:
                print("Changed:")
                os.system(f"lw --config {d} > {cfg_dir}/last_edits/{d}_{node}_new.yml")
                os.system(f"diff {cfg_dir}/last_edits/{d}_{node}.yml {cfg_dir}/last_edits/{d}_{node}_new.yml")
                if not sure:
                    if 'y' in input(f"\nReboot {key[i].upper()} from {vw.components_t[key[i]][0][node]} ? (y/N): ").lower():
                        sure = True
                    else:
                        sys.exit()
                if sure:
                    print("1")
                    restart(mask, node)
                    os.system(f"cp {cfg_dir}/last_edits/{d}_{node}_new.yml {cfg_dir}/last_edits/{d}_{node}.yml")
                    sys.exit()

def restart(mask, node):
    key = list(vw.components_t.keys())
    for i in range(len(vw.components_t)):
        for d in vw.components_t[key[i]][2]:
            if d in sys.argv:
                try:
                    if is_local(vw.components_t[key[i]][0][node]):
                        cmd = mask[mask.find("%s")+2:] % key[i]
                    else:
                        cmd = mask % (vw.components_t[key[i]][0][node], key[i])
                    print("--> Restarting \033[1;36;49m{}\033[0;37;49m from \033[1;36;49m{}\033[0;37;49m".format(key[i], vw.components_t[key[i]][0][node]))
                    os.system(cmd)
                except IndexError:
                    print(f'Node {node} does not exist. Try to initialize it.')
                break

def show_port():
    key = list(vw.components_t.keys())
    for i in range(len(vw.components_t)):
        for d in vw.components_t[key[i]][2]:
            if d in sys.argv[1:]:
                if not "--with-url" in sys.argv:
                    print(f"{vw.components_t[key[i]][3]}")
                    break
                else:
                    print(f"{vw.components_t[key[i]][0][0]}:{vw.components_t[key[i]][3]}")
                    try:
                        print(f"{vw.components_t[key[i]][0][1]}:{vw.components_t[key[i]][3]}")
                    except:
                        pass

def analize():
    percent_warns = []
    percent_errors = []
    count_warns = []
    count_errors = []
    sum_info = 0
    count_info = []
    warn_all = []
    error_all = []
    components_server = []
    log_file = []
    components = list(vw.components_t.keys())
    for dd in range(len(vw.components_t)):
        components_server.append(vw.components_t[components[dd]][0][0])
        log_file.append(vw.components_t[components[dd]][1])
    is_critical = {components[i]: False for i in range(len(components))}
    for k in range(len(components)):
        if is_local(components_server[k]):
            cmd = mask[mask.find("%s")+2:].replace("tail -n %s", "cat") % (components[k],log_file[k])
        else:
            cmd = mask.replace("tail -n %s", "cat") % (components_server[k],components[k],log_file[k])
        warn = cmd + " | grep \" WARN \" -c"
        warn = int(os.popen(warn).read())
        count_warns.append(warn)
        info = cmd + " | grep \" INFO \" -c"
        info = int(os.popen(info).read())
        count_info.append(info)
        sum_info += info
        error = cmd + " | grep \" ERROR \" -c"
        error = int(os.popen(error).read())
        count_errors.append(error)
        try:
            percent = round((warn / (info+warn))*100,2)
        except ZeroDivisionError:
            percent = 0
        percent_warns.append(percent)
        try:
            percent_err = round((error / (info + error))*100,2)
        except ZeroDivisionError:
            percent_err = 0
        percent_errors.append(percent_err)
        warn = cmd + " | grep \"  WARN \" -T"
        warn_all.append(os.popen(warn).read())
        error = cmd + " | grep \" ERROR \" -T"
        error_all.append(os.popen(error).read())
        sys.stdout.write('\r')
        sys.stdout.write('[%-40s] %d%% %20s ' % ('===='*k,(100/(len(components))*(k)),log_file[k]))
        sys.stdout.flush()
        if (k==len(components)-1):
            k+=1
            sys.stdout.write('\r')
            sys.stdout.write('[%-40s] %d%% %20s ' % ('===='*k,(100/(len(components))*(k)),log_file[k-1]))
            sys.stdout.flush()

    sum_count_err = 0
    sum_count_warns = 0
    print("\n{0:13s} {1:>5s} {2:>8s}  {3:>6s} {4:>8s} {5:>8s} {6:>8s}".format("Component", "Error", "Error%", "Warn", "Warn%", "Total", "Critical"))
    for i in range(len(components)):
        sum_count_err += count_errors[i]
        sum_count_warns += count_warns[i]
        critical = 'no'
        try:
            sum_total_by_comp = ((count_errors[i] + count_warns[i]) / (count_errors[i] + count_warns[i] + count_info[i]))*100
        except ZeroDivisionError:
            sum_total_by_comp = 0
        if (percent_errors[i]>=15):
            is_critical[components[i]] = True
            critical = '\033[0;37;41myes\033[0;37;49m'
        print("{0:13.13s} {1:5d} {2:7.2f}% {3:7d} {4:7.2f}% {5:7.2f}% {6:7s}".format(components[i],count_errors[i],percent_errors[i],count_warns[i],percent_warns[i],sum_total_by_comp,critical))
    sum_percent_err = (sum_count_err / (sum_count_err + sum_info))*100
    sum_percent_warns = (sum_count_warns / (sum_count_warns + sum_info))*100
    sum_total = ((sum_count_err + sum_count_warns) / (sum_count_err + sum_count_warns + sum_info))*100
    print("{0:13s} {1:5d} {2:7.2f}% {3:7d} {4:7.2f}% {5:7.2f}%".format("Total", sum_count_err , sum_percent_err , sum_count_warns , sum_percent_warns , sum_total))



    warn_all = sorted(warn_all)
    error_all = sorted(error_all)

    error_all = str(error_all).split(r"\n")

    error_splt = str(error_all).lower().split(" ")
    error_splt = sorted(error_splt)
    freq = list(set(error_splt))

    freq = {i : 0 for i in freq_list_err}
    i = 0

    for d in range(len(freq_list_err)):
        for k in range(len(error_splt)):
            if freq_list_err[d] in error_splt[k]:
                freq[freq_list_err[d]] += 1
    freq_err = {}
    for k in freq.keys():
        if freq[k]!=0:
            freq_err[k] = freq[k]
    print("\nFrequency by keywords(errors):\n{0}".format(freq_err))
    warn_all = str(warn_all).split(r"\n")
    freq_warn = {i : 0 for i in freq_list_warn}
    warn_splt = str(warn_all).lower().split(" ")
    warn_splt = sorted(warn_splt)
    for d in range(len(freq_list_warn)):
        for k in range(len(warn_splt)):
            if freq_list_warn[d] in warn_splt[k]:
                freq_warn[freq_list_warn[d]] += 1
    freq_warn_r = {}
    for k in freq_warn.keys():
        if freq_warn[k]!=0:
            freq_warn_r[k] = freq_warn[k]
    print("\nFrequency by keywords(warns):\n{0}".format(freq_warn_r))

try:
    if ("--node" in sys.argv) or ("-n" in sys.argv):
        try:
            node = int(sys.argv[sys.argv.index("-n")+1])
        except:
            node = int(sys.argv[sys.argv.index("--node")+1])
    else:
        node = 0
    if '-r' in sys.argv or '-ry' in sys.argv:
        mask = vw.mask_restart
        diff(mask, node)
    elif '--analize' in sys.argv:
        analize()
    elif ("--config" in sys.argv):
        show_config(vw.mask_config, node)
    elif "--cat" in sys.argv:
        mask = mask.replace("tail -n ", "cat")
        uhq(mask,node,count_lines)
    elif "-f" in sys.argv:
        year, month, day = sys.argv[sys.argv.index("-f")+1:sys.argv.index("-f")+4]
        if int(day)==datetime.now().day:
            mask = mask.replace("tail -n ", "cat")
            uhq(mask,node,count_lines)
        archive(vw.archive_mask,node, year,month,day)
        archive(vw.archive_mask_reserve,node, year,month,day)
    elif "-fd" in sys.argv:
        day = sys.argv[sys.argv.index("-fd")+1]
        if int(day)==datetime.now().day:
            mask = mask.replace("tail -n ", "cat")
            uhq(mask,node,count_lines)
        archive(vw.archive_mask,node,year=datetime.now().year,month=datetime.now().month,day=day)
        archive(vw.archive_mask_reserve,node,year=datetime.now().year,month=datetime.now().month,day=day)
    elif "--port" in sys.argv:
        show_port()
    else:
        uhq(mask, node,count_lines)
except KeyboardInterrupt:
    print("\n\nCancelled")
    sys.exit()

