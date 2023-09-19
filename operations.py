from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

class Operations:
    def setup(self):
        options = Options()
        options.add_argument("--remote-debugging-port=9222")  # Use an arbitrary port number    
        options.add_experimental_option("detach", True)  # Keep the browser window open after exiting the script
        self.driver = webdriver.Chrome(options = options)
        self.driver.get('http://localhost:4200/')
        self.actions = ActionChains(self.driver)
        sleep(1)
        self.driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()


    def click_element(self, xpath):
        #this is assuming that the element is on the screen
        el = self.driver.find_element(By.XPATH, xpath)
        el.location_once_scrolled_into_view
        sleep(0.1)
        try:
            el.click()
        except:
            sleep(0.1)
            el.click()


    def input_text(self, xpath, text):
        #this is assuming that the elemenet is on the screen
        el = self.driver.find_element(By.XPATH, xpath)
        el.location_once_scrolled_into_view
        self.actions.move_to_element(el)

        sleep(0.1)
        el.send_keys(text)


    def down_arrow(self, count):
        for i in range(count):
            self.actions.send_keys(Keys.ARROW_DOWN).perform()

    def enter(self):
        self.actions.send_keys(Keys.ENTER).perform()

    def select_from_dropdown(self, option, els):
        num = 0
        for iter, dropdown_el in enumerate(els):
            if iter != 0 and dropdown_el.text == option:
                num = iter
                break
        self.down_arrow(num)
        self.enter()