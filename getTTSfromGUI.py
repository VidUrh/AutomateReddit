from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


import parameters

mobile_emulation = {
    "deviceMetrics": {"width": 360, "height": 640, "pixelRatio": 3.0},
    "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile Safari/535.19"
}


option = Options()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")

option.add_argument("--window-size=1000,600")
option.add_experimental_option(
    "prefs", {"profile.default_content_setting_values.notifications": 1}
)


driver = webdriver.Chrome(
    executable_path="./chromedriver.exe",
    options=option
)

url = "https://speechify.com/voiceover/?landing_url=https%3A%2F%2Fspeechify.com%2Ftext-to-speech-online"
driver.get(url)


def getFile(text):
    textarea = driver.find_element(
        "/html/body/div[1]/div[2]/main/div[1]/div/div/div/div[2]/div/div[1]/div[2]/div/div")
    textarea.send_keys(Keys.TAB)
    textarea.clear()
    textarea.send_keys(text)
    return
    dropdown = Select(driver.find_element(
        "xpath", "/html/body/div[4]/div[2]/form/select"))
    dropdown.select_by_value('Matthew')

    download = driver.find_element(
        "xpath", "/html/body/div[4]/div[2]/form/input[2]")
    download.click()


if __name__ == "__main__":
    getFile("")
