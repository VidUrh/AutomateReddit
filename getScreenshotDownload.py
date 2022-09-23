from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import parameters
from PIL import Image

mobile_emulation = {
    "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile Safari/535.19" 
}


option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

option.add_argument("--window-size=675,1080")
# Pass the argument 1 to allow and 2 to block
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

#option.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(
    executable_path="./chromedriver.exe",
    options=option
)

url = "https://www.reddit.com/r/Showerthoughts/"
driver.get(url)
acceptAll = driver.find_element("xpath","/html/body/div[1]/div/div[2]/div[3]/div[1]/section/div/section/section/form[2]/button")

acceptAll.click()

def getElementScreenshot(text,index):
    text = text.split('\'')[0]
    element = driver.find_element("xpath","//*[contains(text(), '"+text+"')]")
    element = element.find_element("xpath",'../../../../../../..')
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()
    element.screenshot(parameters.IMAGES_FOLDER+index+'.png')

def closeWindow():
    driver.quit()
