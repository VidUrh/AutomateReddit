from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

import parameters
from PIL import Image

mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile Safari/535.19"
}


option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

option.add_argument("--window-size=1920,1080")
# Pass the argument 1 to allow and 2 to block
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)

# option.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(
    executable_path="./chromedriver.exe",
    options=option
)

url = parameters.REDDIT_URL
driver.get(url)
acceptAll = driver.find_element(
    "xpath", "/html/body/div[1]/div/div[2]/div[3]/div[1]/section/div/section[2]/section[1]/form/button")

acceptAll.click()


def getElementScreenshot(text, index):
    text = text.split('\'')[0]
    element = driver.find_element("xpath", "//*[contains(text(), '"+text+"')]")
    # element.click()
    driver.execute_script("arguments[0].click();", element)
    time.sleep(0.2)
    bodyElement = driver.find_element(
        "xpath", "/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div[4]")
    element.screenshot(parameters.IMAGES_FOLDER+str(index)+'test.png')
    driver.execute_script("arguments[0].style.display = 'none';", bodyElement)
    screenshottedElement = driver.find_element(
        "xpath", "/html/body/div[1]/div/div[2]/div[3]/div/div/div/div[2]/div[1]/div[2]/div[1]")
    screenshottedElement.screenshot(parameters.IMAGES_FOLDER+index+'.png')


def closeWindow():
    driver.quit()


if __name__ == "__main__":
    getElementScreenshot(
        "I cared for my husband through illness, weight issues and law school and he's leaving me for someone else", 0)
