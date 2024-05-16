import user_agent
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from tls_client import Session
import threading
from colorama import Fore, init
import logging, os

init(convert=True)
logging.basicConfig(
    format='[%(asctime)s] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)
log_lock = threading.Lock()
file_lock = threading.Lock()

class altGen:
    def __init__(self, service, solver_path, session: Session, provider):
        self.provider = provider
        self.path_to_extension = solver_path
        self.service = service
        self.provider = provider
        self.session = session

    def fetch_service(self):
        if self.provider == "bluealts":
            fetch_shortearn = self.session.post(f"https://bluealts.net/{self.service}/", headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "accept-language": "en-US,en;q=0.7",
                "cache-control": "max-age=0",
                "content-type": "application/x-www-form-urlencoded",
                "priority": "u=0, i",
                "sec-ch-ua": "\"Chromium\";v=\"124\", \"Brave\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\"",
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "sec-gpc": "1",
                "upgrade-insecure-requests": "1",
                "Referer": "https://bluealts.net/",
                "Referrer-Policy": "strict-origin-when-cross-origin", 
            }, data={"gen": ""})

            soup = BeautifulSoup(fetch_shortearn.text, "html.parser")
            div = soup.find("div", {"class": "col-lg-7 pt-5 pt-lg-0 order-2 order-lg-1 d-flex align-items-center"})
            url = div.find("a")["href"].strip()

            return url
        elif self.provider == "masteralts":
            fetch_masteralts = self.session.post(f"https://masteralts.com/{self.service}/", headers={
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8",
                "accept-language": "en-US,en;q=0.9",
                "cache-control": "max-age=0",
                "content-type": "application/x-www-form-urlencoded",
                "priority": "u=0, i",
                "sec-ch-ua": '"Chromium";v="124", "Brave";v="124", "Not-A.Brand";v="99"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "same-origin",
                "sec-fetch-user": "?1",
                "sec-gpc": "1",
                "upgrade-insecure-requests": "1",
                "Referer": "https://masteralts.com/",
                "Referrer-Policy": "strict-origin-when-cross-origin"
            }, data={"gen": ""})

            soup = BeautifulSoup(fetch_masteralts.text, "html.parser")
            div = soup.find("div", {"class": "col-one-half middle"})
            url = div.find("a")["href"].strip()
            return url
        else:
            logging.error(f"{Fore.LIGHTRED_EX}wtf is this provider?{Fore.RESET}")
            os._exit(0)
    
    def get_account(self, url):
        code = url.split("/")[-1]
        r = self.session.get(f"http://bin.shortbin.eu:8080/documents/{code}", headers={
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9",
            "Host": "bin.shortbin.eu:8080",
            "Sec-Gpc": "1",
            "User-Agent": user_agent.generate_user_agent(),
            "X-Requested-With": "XMLHttpRequest"
        })
        content = r.json()
        email, password = content["data"].split(":")[0], content["data"].split(":")[1]
        with file_lock:
            with open(f"{self.service}_accounts.txt", "a") as f:
                f.write(f"{email}:{password}\n")      
        logging.info(f"{Fore.LIGHTGREEN_EX}Saved Account{Fore.RESET} ➜\t{Fore.LIGHTYELLOW_EX} {email}:{password} {Fore.RESET}")

        
    
    def fetch_and_automate(self):
        url = self.fetch_service()
        if url:
            result = self.automate_service(url)
            if result:
                with log_lock:
                    logging.info(f"{Fore.LIGHTGREEN_EX}Fetched URL{Fore.RESET} ➜\t{Fore.LIGHTYELLOW_EX} {result} {Fore.RESET}")
                self.get_account(result) 
        else:
            pass

    def automate_service(self, url):
        self.attempts = 0
        max_attempts = 3
        while self.attempts < max_attempts:
            try:
                with sync_playwright() as play_wright:
                    context = play_wright.chromium.launch_persistent_context(
                        "",
                        headless=False,
                        args=[
                    "--headless=new",
                    f"--disable-extensions-except={self.path_to_extension}",
                    f"--load-extension={self.path_to_extension}",
                    ],
                    )
                    page = context.new_page()
                    page.goto(url, timeout=120000)
                    page.wait_for_load_state("load")
                    if page.content() == "<html><head></head><body>Disable your adblock!</body></html>":
                        with log_lock:
                            logging.info(f"{Fore.LIGHTRED_EX}Adblock detected{Fore.RESET} : {Fore.LIGHTYELLOW_EX} Retrying {Fore.RESET}")
                        page.close()
                        continue
                    with log_lock:
                        logging.info(f"{Fore.LIGHTGREEN_EX}Solving Captcha{Fore.RESET} ➜\t{Fore.LIGHTYELLOW_EX} {page.url} {Fore.RESET}")
                    page.wait_for_timeout(30000)
                    page.locator("id=invisibleCaptchaShortlink").click()
                    page.wait_for_load_state("load")
                    page.wait_for_timeout(20000)
                    with log_lock:
                        logging.info(f"{Fore.LIGHTGREEN_EX}Fetching URL{Fore.RESET} ➜\t{Fore.LIGHTYELLOW_EX} {page.url} {Fore.RESET}")
                    a = page.locator("text=Get Link")
                    url = a.get_attribute("href")
                    return url
            except PlaywrightTimeoutError:
                with log_lock:
                    logging.info(f"{Fore.LIGHTRED_EX}Couldn't solve captcha{Fore.RESET} : {Fore.LIGHTYELLOW_EX} Attempt {self.attempts+1} {Fore.RESET}")
            finally:
                self.attempts += 1
        with log_lock:
            logging.info(f"{Fore.LIGHTRED_EX}Failed to fetch URL{Fore.RESET} : {Fore.LIGHTYELLOW_EX}{page.url} {Fore.RESET}")
        return None