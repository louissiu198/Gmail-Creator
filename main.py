from concurrent.futures import ThreadPoolExecutor
from DrissionPage import ChromiumPage, ChromiumOptions
from threading import Thread
from datetime import datetime
from colorama import Fore
from pystyle import Colors, Colorate
from random import randint, choice, choices
from string import ascii_letters, digits, ascii_lowercase
from shutil import rmtree
from httpx import Client
from json import load, dumps
from time import sleep, time
from uuid import uuid4
from os import system, makedirs, getcwd, path, remove

config = load(open("./input/config.json"))
proxies = open("./input/proxies.txt").read().splitlines()

class Proxy:
    def __init__(self, proxy: str):
        self.proxy = proxy

    def generate_extension(self):
        while True:
            self.random_path = '/extensions/' + ''.join(choices(ascii_letters + digits, k=30))
            self.folder_path = path.join(getcwd() + self.random_path)
            if not path.exists(self.folder_path):
                makedirs(self.folder_path)
                break
        proxy_1 = self.proxy.split("@")[0]
        proxy_2 = self.proxy.split("@")[1]

        username = proxy_1.split(":")[0]
        password = proxy_1.split(":")[1]
        host = proxy_2.split(":")[0]
        port = proxy_2.split(":")[1]

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (host, port, username, password)

        with open(f"./{self.random_path}/manifest.json", "w") as f:
            f.write(manifest_json)
        with open(f"./{self.random_path}/background.js", "w") as f:
            f.write(background_js)
        return self.random_path

    def remove_extension(self):
        rmtree(self.random_path)

class Utils:
    def __init__(self, browser: ChromiumPage):
        self.XPATH, self.CLASS, self.ID = "XPATH", "CLASS", "ID"
        self.browser = browser

    def element_text(self, choice: str, interaction_id: str, timeout: int = 10):
        key_word = ""
        if choice == self.XPATH:
            key_word = "x="
        elif choice == self.ID:
            key_word = "#="
        elif choice == self.CLASS:
            key_word = "."
        
        for _ in range(timeout):
            try:
                return self.browser(key_word + interaction_id).text
            except:
                sleep(1)

    def element_click(self, choice: str, interaction_id: str, timeout: int = 20, extra: int = 0):
        key_word = ""
        if choice == self.XPATH:
            key_word = "x="
        elif choice == self.ID:
            key_word = "#="
        elif choice == self.CLASS:
            key_word = "."

        sleep(extra)
        return self.browser(key_word + interaction_id).click(timeout = timeout, by_js = True)

    def element_input(self, choice: str, interaction_id: str, text: str, timeout: int = 20):
        sleep(0.5)
        key_word = ""
        if choice == self.XPATH:
            key_word = "x="
        elif choice == self.ID:
            key_word = "#="
        elif choice == self.CLASS:
            key_word = "."

        for _ in range(timeout):
            try:
                return self.browser(key_word + interaction_id).input(text)
            except:
                sleep(1)

class Logger:
    @staticmethod
    def SUCCESS(thread_name: str, title_text: str, result_text: str) -> None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Thread {thread_name} | (*) {title_text} | {result_text}")

    @staticmethod
    def ERROR(thread_name: str, title_text: str, result_text: str) -> None:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Thread {thread_name} | (-) {title_text} | {result_text}")

class Profile:
    def __init__(self):
        self.profile = {
            "day": randint(1, 28),
            "year": randint(1995, 2005),
            "month": randint(1, 12),
            "gender": randint(2, 3),
            "password":self.get_password(),
            "last_name":self.get_lastname(),
            "first_name":self.get_firstname(),
            "email_address":self.get_random_name(),
            "recovery_email":f"{self.get_random_name()}@outlook.com",
        }
    
    def get_firstname(self):
        lists = ["Cesco", "Andy", "Michael", "Johnson", "Cameron", "Joshua", "Hugo", "Nathan", "Vicky", "Scarlet", "Fred", "Christian", "William", "Ethan", "Hedy", "Zackary", "Jaquel", "Ksenia", "Kaylen", "Ivan", "Ava", "Emma", "Olivia", "Isabella", "Sophia", "Mia", "Charlotte", "Harper", "Amelia", "Evelyn", "Abigail", "Emily", "Elizabeth", "Avery", "Sofia", "Victoria", "Scarlett", "Ella", "Madison", "Addison", "Aubrey", "Lily", "Chloe", "Layla", "Zoey", "Nora", "Grace", "Ellie", "Hannah", "Aria", "Isabelle", "Leah", "Violet", "Audrey", "Lucy", "Stella", "Elsie", "Hazel", "Penelope", "Aurora", "Bella", "Nova", "Luna", "Ivy", "Camila", "Elena", "Kinsley", "Lydia", "Jade", "Natalie", "Maya", "Josephine", "Addyson", "Eliana", "Emilia", "Aaliyah", "Kennedy", "Madelyn", "Delilah", "Autumn", "Sarah", "Skylar", "Paisley", "Emery", "Lila", "Alice", "Leilani", "Cecilia", "Willow", "Iris", "Jacob", "William", "Michael", "Daniel", "Alexander", "Ethan", "Joshua", "Matthew", "Jayden", "Andrew", "Joseph", "David", "Benjamin", "Ryan", "Lucas", "Nathan", "Tyler", "James", "Dylan", "Logan", "Caleb", "Jackson", "Sebastian", "Alexander", "Jackson", "Owen", "Liam", "Noah", "Grayson", "Jack", "Connor", "Jayce", "Julian", "Everett", "Benjamin", "Maverick", "Ezra", "Leo", "Abraham", "Isaiah", "Gabriel", "Elijah", "Josiah", "Christian", "Hunter", "Nicholas", "Dominic", "Adrian", "Colton", "Ayden", "Brantley", "Easton", "Max", "Aaron", "Austin", "Ian", "Gavin", "Eli", "Jaxon", "Micah", "Oliver", "Levi", "Aiden", "Ezekiel", "Asher", "Samuel", "Declan", "Wyatt", "Nolan", "Ryder", "Brycen", "Hudson", "Jacob", "Theodore", "Blake", "Bryson", "Damian", "Xavier", "Carson", "Parker", "Jeremiah", "Bryson", "Emmett", "Thomas", "Jordan", "Jace", "Adam", "Miles", "Sawyer", "Jacob", "Collin", "Jonathan", "Isaiah", "Antonio", "Axel", "Silas", "Hayden", "Ezra", "Evan", "Kayden", "Jaxson", "Muhammad", "Vincent", "Weston", "Kai","Bob","Emz","Deedy","Bartholomew", "Metatron"]
        return choice(lists) + ''.join(choices(ascii_lowercase, k=3))
    
    def get_lastname(self):
        lists = ["Smith", "Johnson", "Williams", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Hernandez", "Diaz", "Reyes", "Morales", "Jimenez", "Castillo", "Gutierrez", "Flores", "Ramirez", "Romero", "Medina", "Gonzalez", "Campos", "Valdez", "Ortiz", "Vazquez", "Salazar", "Flores", "Rios", "Sandoval", "Soto", "Rojas", "Contreras", "Mercado", "Delgado", "Suarez", "Montoya", "Molina", "Meza", "Avila", "Fuentes", "Cisneros", "Cortes", "Guzman", "Ochoa", "Navarro", "Figueroa", "Hernandez", "Rivera", "Reyes", "Moreno", "Castillo", "Flores", "Diaz", "Ramos", "Campos", "Escobar", "Mendoza", "Vargas", "Jimenez", "Fernandez", "Dominguez", "Ramirez", "Torres", "Sanchez", "Serrano", "Gutierrez", "Alvarez", "Carrillo", "Guerrero", "Chavez", "Morales", "Montes", "Leon", "Valenzuela", "Robles", "Aguilar", "Soto", "Acosta", "Pacheco", "Arroyo", "Duran", "Velazquez", "Delgado", "Ortega", "Medina", "Juarez", "Santana", "Rosales", "Camacho", "Reyes", "Fuentes", "Vega", "Ayala", "Espinoza", "Zavala", "Salgado", "Galvan", "Nunez", "Cortes", "Rubio", "Rios", "Padilla", "Rocha", "Herrera", "Solis", "Salinas", "Mora", "Rangel", "Nava", "Cardenas", "Pineda", "Reyes", "Olivares", "Castaneda", "Trevino", "Villarreal", "Dominguez", "Barrera", "Lozano", "Davila", "Meléndez", "Meza", "Campos", "Reyes", "Peña", "Montaño", "Munoz", "Maldonado", "Murillo", "Palacio", "Gallegos", "Loera", "Cazares", "Beltran", "Cárdenas", "Pena", "Segura", "Andrade", "Prado", "Menendez", "Varela", "Barajas", "Trejo", "Quintero", "Figueroa", "Molina", "Salas", "Rojas", "Cervantes", "Macias", "Salcedo", "Magana", "Bermudez", "Guzman", "Gómez", "Méndez", "Duarte", "Alvarado", "Estrada", "Montes", "Rangel", "Wong", "Chan", "Chen", "Chueng", "Siu", "Ng", "Zhou", "Hao", "Liu", "Hu", "Tam", "Lam", "Lueng", "Zhao", "Lin", "Zhang", "Fung" ]
        return choice(lists) + ''.join(choices(ascii_lowercase, k=3))

    def get_password(self):
        return ''.join(choices(ascii_letters + digits, k=15))

    def get_random_name(self):
        return ''.join(choices(ascii_lowercase + digits, k=13))
    
class Verifier:
    def __init__(self):
        self.client = Client(http2 = True, verify = False)
    
    def get_numbers(self):
        while True:
            # ["IE:tesco", "LB:touch", "ZM:zamtel"]
            r = self.client.get("api").json()
            if r["success"]:
                self.number = r["number"][0]
                return self.number
    
    def get_messages(self):
        while True:
            r = self.client.get("api")
            if "is your Google verification code" in r.text:
                return r.json()["messages"][0]["message"].split("G-")[1].split(" is")[0]
            sleep(1)

class Generator:
    def __init__(self, thread_name: int):
        start_time = time()
        self.thread_name = thread_name
        try:
            self.browser_creation()
            self.account_registeration()
            Logger.SUCCESS(self.thread_name, "Account Created", f"In {time() - start_time} seconds")
        except Exception as e:
            Logger.ERROR(self.thread_name, "Error", str(e))
        self.browser.quit()
        self.proxy.remove_extension()

    def check_heading_text(self, unwanted_text: str):
        sleep(1)
        while True:
            text = self.modified.element_text(self.modified.XPATH, '//*[@id="headingText"]/span')
            if unwanted_text != text:
                return text
            sleep(1)

    def browser_creation(self):
        proxy = choice(proxies)
        Logger.SUCCESS(self.thread_name, "Proxy Loaded", proxy)
        # self.proxy = Proxy(proxy)
        # self.extension_path = self.proxy.generate_extension()

        co = ChromiumOptions().auto_port()
        # co.add_extension(getcwd() + self.extension_path)

        co_options = [
            "--disable-infobars",
            "--disable-features=VizDisplayCompositor",
            "--enable-features=MemoryOptimization",
            "--max-old-space-size=4096",
            "--disable-gpu",
            "--disable-dev-shm-usage",
            "--blink-settings=imagesEnabled=false",
            "--lang=en",
            "--window-size=900,700"
        ]
        if config["ifHeadless"]:
            co_options.append("--headless")

        # for argument in co_options:
        #     co.set_argument(argument)

        self.browser = ChromiumPage(co)
        self.profile = Profile().profile
        self.modified = Utils(self.browser)

        self.browser.get('https://www.google.com/intl/en-US/gmail/about/')
        self.browser.wait.doc_loaded()
        self.modified.element_click(self.modified.XPATH, '/html/body/header/div/div/div/a[3]', 10)

    def account_registeration(self):
        # First Page: Collect User Names
        self.modified.element_input(self.modified.XPATH, '//*[@id="lastName"]', self.profile["last_name"])
        self.modified.element_input(self.modified.XPATH, '//*[@id="firstName"]', self.profile["first_name"])
        self.modified.element_click(self.modified.XPATH, '//*[@id="collectNameNext"]/div/button')
        self.browser.wait.load_start()
        # Second Page: Basic Info Credentals
        self.modified.element_click(self.modified.XPATH, f'//*[@id="month"]/option[{self.profile["month"] + 1}]', 30)
        self.modified.element_click(self.modified.XPATH, f'//*[@id="gender"]/option[{self.profile["gender"]}]')
        self.modified.element_input(self.modified.XPATH, '//*[@id="year"]', self.profile["year"])
        self.modified.element_input(self.modified.XPATH, '//*[@id="day"]', self.profile["day"])
        self.modified.element_click(self.modified.XPATH, '//*[@id="birthdaygenderNext"]/div/button')
        self.browser.wait.load_start()
        # Third Page: Choose Email Option
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[2]/div/div[1]/div', 30)
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[1]/div[1]/div/span/div[3]/div/div[1]/div')
        self.modified.element_input(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input', self.profile["email_address"])
        self.modified.element_click(self.modified.XPATH, '//*[@id="next"]/div/button')
        self.browser.wait.load_start()
        # Forth Page: Entering Passwords
        self.modified.element_input(self.modified.XPATH, '//*[@id="passwd"]/div[1]/div/div[1]/input', self.profile["password"], 30)
        self.modified.element_input(self.modified.XPATH, '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input', self.profile["password"])
        self.modified.element_click(self.modified.XPATH, '//*[@id="createpasswordNext"]/div/button')
        self.browser.wait.load_start()

        Logger.SUCCESS(self.thread_name, "Initializing Profile", self.profile)

        headingText = self.check_heading_text("Create a strong password")
        if headingText == "Confirm you’re not a robot":
            self.phone_verification()
            self.system_recovery()
        elif headingText == "Add recovery email":
            Logger.SUCCESS(self.thread_name, "Verification Bypassed", "Phone Verification Skipped")
            self.system_recovery()
        else:
            raise Exception(f"<<IP Detected>> {headingText}")
        
        headingText = self.check_heading_text("Create a strong password")
        self.browser.wait.load_start()
        if headingText == "Choose your settings":
            self.customize_setting()
            self.privacy_terms()
        elif headingText == "Privacy and Terms":
            self.privacy_terms()
        else:
            self.privacy_terms()
        
        if config["imapEnabled"]:
            self.mail_enable_imap()
        self.finish_session()

    def phone_verification(self):
        self.verifier = Verifier()
        number = self.verifier.get_numbers()

        Logger.SUCCESS(self.thread_name, "Bought Number", number)
        self.modified.element_input(self.modified.XPATH, '//*[@id="phoneNumberId"]', number)
        # //*[@id="countryList"]/div/div[2]/ul/li[13]
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[3]/div/div[1]/div/div/button')
        print("this")
        self.browser.wait.load_start()

        code = self.verifier.get_messages()
        Logger.SUCCESS(self.thread_name, "Recieved Code", code)

        self.modified.element_input(self.modified.XPATH, '//*[@id="code"]', code)
        self.modified.element_click(self.modified.XPATH, '//*[@id="next"]/div/button')
        self.browser.wait.load_start()
        
    def system_recovery(self):
        self.modified.element_input(self.modified.XPATH, '//*[@id="recoveryEmailId"]', self.profile["recovery_email"])
        # //*[@id="yDmH0d"]/div[1]/div[1]/div[2]/div/div/div[3]/div/div[1]/div[2]/div/div/button SKIP
        self.modified.element_click(self.modified.XPATH, '//*[@id="recoveryNext"]/div/button')
        self.browser.wait.load_start()

        headingText = self.check_heading_text("Create a strong password")
        if headingText == "Add phone number":
            self.modified.element_click(self.modified.XPATH, '//*[@id="recoverySkip"]/div/button')
            self.browser.wait.load_start()

        self.modified.element_click(self.modified.XPATH, '//*[@id="next"]/div/button')
        self.browser.wait.load_start()
        
    def customize_setting(self):
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[2]/div/div/div[1]/form/span/section/div/div/div/div/div[1]/div/span/div[1]/div/div[1]/div')
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div/div/button', extra = 0.5)
        self.browser.wait.load_start()

        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[2]/div/div/button', extra = 5)
        self.browser.wait.load_start()
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div/div[2]/div/div/button', extra = 5)
        self.browser.wait.load_start()
    
    def privacy_terms(self):
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div[3]/div/div[1]/div/div/button', timeout = 20, extra = 0.5)

        try:
            self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/div[2]/div/div[2]/div[3]/div[1]', timeout = 5, extra = 0.5)
        except:
            pass
        
        is_succeed = False
        for _ in range(50):
            if self.browser.url.startswith("https://mail.google.com/"):
                is_succeed = True
                break
            sleep(1)
        
        if is_succeed == False:
            raise Exception("<<Something is wrong>>")

    
    def myaccount_google(self):
        self.browser.get("https://myaccount.google.com")
        self.browser.wait.doc_loaded()
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div/div[2]/div/c-wiz/c-wiz/div/div[3]/div/div/header/div[1]/div/button', timeout = 20, extra = 0.5)
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz/main/div/div[2]/div/div/button', timeout = 20, extra = 0.5)
        self.modified.element_click(self.modified.XPATH, f'//*[@id="yDmH0d"]/c-wiz/main/div/div[2]/c-wiz/div/div/div/section[1]/div/div[1]/div/div[{randint(1, 3)}]/button[{randint(1, 21)}]', timeout = 20, extra = 0.5)
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div[2]/div[1]/div[2]/div[2]/div/button', timeout = 20, extra = 0.5)
        self.modified.element_click(self.modified.XPATH, '//*[@id="yDmH0d"]/c-wiz[2]/div[3]/div[2]/div/div[2]/div/div[1]/div[4]/div[2]/button', timeout = 20, extra = 0.5)
        # //*[@id="yDmH0d"]/c-wiz[4]/main/div/div[1]/div[1]/h2
        sleep(10)
    
    def mail_enable_imap(self):
        if_succeed = False
        self.browser.get("https://mail.google.com/mail/u/0/#settings/fwdandpop")
        self.browser.wait.doc_loaded()
        self.modified.element_click(self.modified.XPATH, '//*[@id=":5i"]', timeout = 20, extra = 0.5)
        self.modified.element_click(self.modified.XPATH, '//*[@id=":5e"]', timeout = 20, extra = 0.5)

        for _ in range(10):
            if self.browser.url == "https://mail.google.com/mail/u/0/#inbox":
                if_succeed = True
                break
            sleep(1)
        if if_succeed == False:
            raise Exception("<<Failed To Enable IMAP>>")

    def finish_session(self):
        print(self.browser.get_cookies(all_domains = True))
        with open("accounts.txt", "a+") as f:
            f.write(dumps(self.profile) + '\n')

def main_function(thread_name: int):
    while True:
        try:
            Generator(thread_name)
        except:
            continue

with ThreadPoolExecutor(max_workers=config["threadCount"]) as executor:
    for _ in range(config["threadCount"]):
        executor.submit(main_function, _)
