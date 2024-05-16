from core.alts import altGen
from colorama import Fore, init
import os, json
import random
from tls_client import Session
import threading
from pystyle import *
init(convert=True)

def clear():
    system = os.name
    if system == 'nt':
        os.system('cls')
    elif system == 'posix':
        os.system('clear')
    else:
        print('\n'*120)
    return

def get_proxy():
    try:
        proxies = open("proxies.txt", "r").read().splitlines()
    except FileNotFoundError:
        print(f"{Fore.LIGHTRED_EX}➜{Fore.RESET} {Fore.LIGHTBLUE_EX} Proxies file not found.{Fore.RESET}")
        input("Click enter to exit...")
        os._exit(0)
    return proxies 

def get_session():
    proxies = get_proxy()
    prox = random.choice(proxies)
    client = Session(
        client_identifier="chrome_120",
        random_tls_extension_order=True,
        h2_settings={"HEADER_TABLE_SIZE": 65536,"MAX_CONCURRENT_STREAMS": 1000,"INITIAL_WINDOW_SIZE": 6291456,"MAX_HEADER_LIST_SIZE": 262144},
        h2_settings_order=["HEADER_TABLE_SIZE","MAX_CONCURRENT_STREAMS","INITIAL_WINDOW_SIZE","MAX_HEADER_LIST_SIZE"],
        supported_signature_algorithms=["ECDSAWithP256AndSHA256","PSSWithSHA256","PKCS1WithSHA256","ECDSAWithP384AndSHA384","PSSWithSHA384","PKCS1WithSHA384","PSSWithSHA512","PKCS1WithSHA512",],
        supported_versions=["GREASE", "1.3", "1.2"],
        key_share_curves=["GREASE", "X25519"],
        cert_compression_algo="brotli",
        pseudo_header_order=[":method",":authority",":scheme",":path"],
        connection_flow=15663105,
        header_order=["accept","user-agent","accept-encoding","accept-language"]
    )

    client.proxies = {
        "http": f"http://{prox}", 
        "https": f"http://{prox}"
    }
    return client

def run_bot(service, sPath, provider):
    s = get_session()
    bot = altGen(service, sPath, s, provider)
    bot.fetch_and_automate()

def main():
    clear()
    banner = f"""
┏┓┓
┣┫┃╋┏ ┏┓┓┏
┛┗┗┗┛•┣┛┗┫
      ┛  ┛
"""
    solver_ch = input(f"{Fore.LIGHTBLACK_EX}➜ {Fore.RESET} {Fore.LIGHTWHITE_EX}Enter solver choice (capmonster/nopecha): {Fore.RESET}").lower()
    if solver_ch == "capmonster":
        if os.path.exists("./solver/capmonster/defaultSettings.json"):
            with open("./solver/capmonster/defaultSettings.json", "r") as f:
                data = json.load(f)
                if data["clientKey"].strip() == "":
                    real = input(f"{Fore.LIGHTBLACK_EX}➜ {Fore.RESET} {Fore.LIGHTWHITE_EX}Enter your CapMonster API key: {Fore.RESET}")
                    sPath = os.path.abspath("./solver/capmonster")
                    with open(f"{sPath}\\defaultSettings.json", "r") as f:
                        data = json.load(f)
                    data["clientKey"] = real
                    with open(f"{sPath}\\defaultSettings.json", "w") as f:
                        json.dump(data, f, indent=4)
                else:
                    sPath = os.path.abspath("./solver/capmonster")
            
    elif solver_ch == "nopecha":
        sPath = os.path.abspath("./solver/nopecha")
    else:
        print(f"{Fore.LIGHTRED_EX}➜{Fore.RESET} {Fore.LIGHTBLUE_EX} Invalid solver choice.{Fore.RESET}")
        return
    print(f"{Fore.LIGHTGREEN_EX}({Fore.RESET}1{Fore.LIGHTGREEN_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}bluealts.net{Fore.RESET}")
    print(f"{Fore.LIGHTGREEN_EX}({Fore.RESET}2{Fore.LIGHTGREEN_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}masteralts.com{Fore.RESET}")
    provider = input(f"{Fore.LIGHTBLACK_EX}➜ {Fore.RESET} {Fore.LIGHTWHITE_EX}Enter provider: {Fore.RESET}").lower()
    if provider not in ["1", "2"]:
        print(f"{Fore.LIGHTRED_EX}➜{Fore.RESET} {Fore.LIGHTBLUE_EX}Invalid provider.{Fore.RESET}")
        return
    provider_dict = {
        "1": "bluealts",
        "2": "masteralts"
    }
    providere = provider_dict[provider]
    clear()
    print(Center.XCenter(f"{Fore.LIGHTRED_EX}{banner}{Fore.RESET}"))
    print("\n")
    print(f"{Fore.RED}»{Fore.LIGHTYELLOW_EX} Made by nostorian {Fore.RESET}")
    print(f"{Fore.RED}»{Fore.LIGHTYELLOW_EX} feds.lol/ykreal {Fore.RESET}")
    print("\n")
    if provider == "1":
        print(f"{Fore.LIGHTGREEN_EX}»{Fore.RESET} {Fore.LIGHTWHITE_EX}Available services (bluealts): {Fore.RESET}\n")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}1{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Crunchyroll{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}2{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Hulu{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}3{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}NordVPN{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}4{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Origin{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}5{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Call of Duty{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}6{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}IPVanish{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}7{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Curiosity Stream{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}8{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Exit{Fore.RESET}")
        service = input(f"\n{Fore.LIGHTBLACK_EX}➜ {Fore.RESET} {Fore.LIGHTWHITE_EX}Enter service: {Fore.RESET}").lower()
        if service == "8":
            return
        service_dict = {
            "1": "crunchyroll",
            "2": "hulu",
            "3": "nordvpn",
            "4": "origin",
            "5": "call-of-duty",
            "6": "ipvanish",
            "7": "curiosity-stream"
        }
        try:
            service = service_dict[service]
        except KeyError:
            print(f"{Fore.LIGHTRED_EX}➜ {Fore.RESET}{Fore.LIGHTBLUE_EX} Invalid service.{Fore.RESET}")
            return
        
    elif provider == "2":
        print(f"{Fore.LIGHTGREEN_EX}»{Fore.RESET} {Fore.LIGHTWHITE_EX}Available services (masteralts): {Fore.RESET}\n")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}1{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Crunchyroll{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}2{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Hulu{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}3{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}NordVPN{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}4{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}IPVanish{Fore.RESET}")
        print(f"{Fore.LIGHTRED_EX}({Fore.RESET}5{Fore.LIGHTRED_EX}){Fore.RESET} {Fore.LIGHTWHITE_EX}Exit{Fore.RESET}")
        service = input(f"\n{Fore.LIGHTBLACK_EX}➜ {Fore.RESET} {Fore.LIGHTWHITE_EX}Enter service: {Fore.RESET}").lower()
        if service == "5":
            return
        service_dict = {
            "1": "crunchyroll",
            "2": "hulu",
            "3": "nordvpn",
            "4": "ipvanish"
        }
        try:
            service = service_dict[service]
        except KeyError:
            print(f"{Fore.LIGHTRED_EX}➜ {Fore.RESET}{Fore.LIGHTBLUE_EX} Invalid service.{Fore.RESET}")
            return
    else:
        print(f"{Fore.LIGHTRED_EX}➜{Fore.RESET} {Fore.LIGHTBLUE_EX} Invalid provider.{Fore.RESET}")
        return
    num_threads = int(input(f"{Fore.LIGHTBLACK_EX}➜ {Fore.RESET} {Fore.LIGHTWHITE_EX}Enter amount of alts to generate: {Fore.RESET}"))
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=run_bot, args=(service, sPath, providere))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
    input("Click enter to exit...")