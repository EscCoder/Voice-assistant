from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from ss import *    


api_address = "https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey="+ key
json_data = requests.get(api_address).json()

class info():
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
       
    
    def get_info(self, query):
        self.query = query
        self.driver.get("https://wikipedia.com")
        
        search = self.driver.find_element(By.XPATH, '//*[@id="searchInput"]')
        search.click()
        search.send_keys(query)
        enter = self.driver.find_element(By.XPATH, '//*[@id="search-form"]/fieldset/button')
        enter.click()

class music():  
    def __init__(self):
        self.options = Options()
        self.options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.options)
       
    
    def play(self, query):
        self.query = query
        self.driver.get(url="https://www.youtube.com/results?search_query=" + query)
        
        wait = WebDriverWait(self.driver, 10)  # Wait for up to 10 seconds
        video = wait.until(EC.element_to_be_clickable((By.XPATH, '//ytd-video-renderer[1]//a[@class="yt-simple-endpoint style-scope ytd-video-renderer"]')))
        video.click()

def  news():
    ar = []
    for i in range(5):
        ar.append("Number "+ str(i+1)+", " + json_data["articles"][i]["title"] + ".")
    return ar
