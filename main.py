import keyboard
import pyautogui
import requests
import time
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url: str) -> None:
        self.url = url
        self.passwords = []
    
    def fetch_data(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            print(f'Error fetching data {e}')
            return None

    def parse_data(self):
        html_content = self.fetch_data()
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            ol_tag = soup.find('ol', class_='customlist')

            if ol_tag:   
                dirty_pwd = ol_tag.find_all('li')
                self.passwords = [x.get_text() for x in dirty_pwd]
            else:
                print("Didn't find data")
        else:
            print('No HTML code fetched')

class Typer:
    def __init__(self, passwords, start) -> None:
        self.start = start
        self.passwords = passwords
        self.counter = 0

    def emulate_entering_password(self):
        if self.counter < len(self.passwords):
            current_password = self.passwords[self.counter]
            print(f'Entering password: {current_password}')
            
            for digit in current_password:
                pyautogui.press(digit)
            
            pyautogui.press('enter')
            self.counter += 1

            print(f'Entered {self.counter} passwords')       
        else:
            print('Entered all passwords')

    def listener(self):
        while True:
            keyboard.wait('shift+f')
            self.emulate_entering_password()
            time.sleep(0.5)

        
if __name__ == '__main__':        
    # Recieving passwords
    rust = Parser('https://rusttips.com/top-10000-rust-door-lock-codes')
    rust.parse_data()
        
    #starting script    
    typer = Typer(rust.passwords, 0)
    print('print shift+f to write one password')
    typer.listener()

