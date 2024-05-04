import os
import shutil
import requests
import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://www.onlineshinanyut.am/products/amrakcman-paraganer"
driver.get(url)

while True:
    try:
        button = (driver.find_element(by=By.CLASS_NAME, value="products-load-more")
                  .find_element(by=By.TAG_NAME, value="span"))
    except:
        break
    driver.execute_script("arguments[0].scrollIntoView();", button)
    driver.execute_script("arguments[0].click();", button)
    time.sleep(2)

links = [
    div.find_element(By.TAG_NAME, "a").get_attribute("href")
    for div in driver.find_elements(By.CLASS_NAME, "product-image-wrapper")
]

counter = 1
subcategory_name = "Սեղմող գործիքներ"
img_folder = os.path.join(os.getcwd(), "img", "6)շինանյութ", "8)ամրակցման_պարագաներ")
csv_file = "csv/6)շինանյութ/8)ամրակցման_պարագաներ.csv"

with open(csv_file, "w", newline="") as csvfile:
    fieldnames = ["Product Name", "Price", "Quantity Available", "Specifications"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for link in links:
        driver.get(link)

        product_name = driver.find_element(by=By.CLASS_NAME, value="pv-name").text
        product_price = (
            driver.find_element(by=By.CLASS_NAME, value="prices-group").
            find_element(by=By.TAG_NAME, value="h4").text[:-2].replace(".", "")
        )
        quantity_available = driver.find_element(
            by=By.CLASS_NAME, value="live-basket-group").find_element(
            by=By.CLASS_NAME, value="number-input.pv-count-input").get_attribute("data-max")
        specifications = driver.find_elements(by=By.CLASS_NAME, value="pr-info-item [class^='page_speed_']")
        img_url = driver.find_element(by=By.CLASS_NAME, value="pv-general-image").get_attribute("src")
        img_extension = os.path.splitext(img_url)[1]
        img_filename = f"{counter}{img_extension}"

        img_path = os.path.join(img_folder, img_filename)
        img_response = requests.get(img_url, stream=True)
        with open(img_path, "wb") as img_file:
            shutil.copyfileobj(img_response.raw, img_file)

        specifications_dict = {}
        for sp in range(0, len(specifications) - 1, 2):
            specifications_dict[specifications[sp].text] = specifications[sp + 1].text
        specifications_str = ', '.join([f'{key} - {value}' for key, value in specifications_dict.items()])

        writer.writerow({
            "Product Name": product_name,
            "Price": product_price,
            "Quantity Available": quantity_available,
            "Specifications": specifications_str
        })

        counter += 1

driver.quit()
# All links
# Ձեռքի գործիքներ
# https://www.onlineshinanyut.am/products/%D5%81%D5%A5%D5%BC%D6%84%D5%AB-%D5%AF%D5%BF%D6%80%D5%B8%D5%B2-%D5%A3%D5%B8%D6%80%D5%AE%D5%AB%D6%84%D5%B6%D5%A5%D6%80
# https://www.onlineshinanyut.am/products/%D5%81%D5%A5%D5%BC%D6%84%D5%AB-%D5%BD%D5%A5%D5%B2%D5%B4%D5%B8%D5%B2-%D5%A3%D5%B8%D6%80%D5%AE%D5%AB%D6%84%D5%B6%D5%A5%D6%80
# https://www.onlineshinanyut.am/products/trishotkaner
# https://www.onlineshinanyut.am/products/jang-maqrogh-khozanakner
# https://www.onlineshinanyut.am/products/%D5%8A%D5%BF%D5%B8%D6%82%D5%BF%D5%A1%D5%AF%D5%A1%D5%B0%D5%A1%D5%B6%D5%B6%D5%A5%D6%80
# https://www.onlineshinanyut.am/products/%D5%8A%D5%BF%D5%B8%D6%82%D5%BF%D5%A1%D5%AF%D5%A1%D5%A2%D5%A1%D5%B6%D5%A1%D5%AC%D5%AB+%D5%AF%D5%AC%D5%B8%D6%82%D5%B9%D5%A5%D6%80
# https://www.onlineshinanyut.am/products/stepler+atrchanakner
# https://www.onlineshinanyut.am/products/chapogh-gortsiqner
# https://www.onlineshinanyut.am/products/%D5%80%D5%A1%D6%80%D5%BE%D5%A1%D5%AE%D5%B8%D5%B2-%D5%A3%D5%B8%D6%80%D5%AE%D5%AB%D6%84%D5%B6%D5%A5%D6%80
# https://www.onlineshinanyut.am/products/%D5%93%D5%A1%D5%B5%D5%BF%D5%A1%D5%A3%D5%B8%D6%80%D5%AE%D5%AB-%D5%A3%D5%B8%D6%80%D5%AE%D5%AB%D6%84%D5%B6%D5%A5%D6%80
# https://www.onlineshinanyut.am/products/hghkogh-paraganer

# Վերանորոգում
# https://www.onlineshinanyut.am/products/aerozolner
# https://www.onlineshinanyut.am/products/61-dzernocner
# https://www.onlineshinanyut.am/products/pastarner
# https://www.onlineshinanyut.am/products/nerker-ev-paraganer
# https://www.onlineshinanyut.am/products/nerkararakan-khozanakner
# https://www.onlineshinanyut.am/products/nerkararakan-glanakner+valikner
# https://www.onlineshinanyut.am/products/shpakliner

# Ավտոմոբիլային գործիքներ
# https://www.onlineshinanyut.am/products/avtomeqenayi-banaliner
# https://www.onlineshinanyut.am/products/avtomeqenayi-gortsiqneri-havaqatsuner
# https://www.onlineshinanyut.am/products/%D4%B2%D5%A1%D6%80%D5%B1%D6%80-%D5%B3%D5%B6%D5%B7%D5%B4%D5%A1%D5%B4%D5%A2-%D5%A1%D5%BE%D5%BF%D5%B8%D5%AC%D5%BE%D5%A1%D6%81%D5%B8%D6%82%D5%B4
# https://www.onlineshinanyut.am/products/avtolvacman-nyuter
# https://www.onlineshinanyut.am/products/%D5%84%D5%A5%D6%84%D5%A5%D5%B6%D5%A1%D5%B5%D5%AB-%D5%BA%D5%B8%D5%B4%D5%BA
# https://www.onlineshinanyut.am/products/meqenayi-martkoci-licqavorich
# https://www.onlineshinanyut.am/products/grunt
# https://www.onlineshinanyut.am/products/meqenayi-artaqin-khnamq
# https://www.onlineshinanyut.am/products/srahi-khnamq
# https://www.onlineshinanyut.am/products/laq
# https://www.onlineshinanyut.am/products/nerk-aerozolayin-artacologh
# https://www.onlineshinanyut.am/products/%D4%B1%D5%B4%D5%A2%D5%A1%D6%80%D5%B1%D5%AB%D5%AF+%D4%B4%D5%B8%D5%B4%D5%AF%D6%80%D5%A1%D5%BF
# https://www.onlineshinanyut.am/products/hakavazayin-tsatskuyt
# https://www.onlineshinanyut.am/products/havelumner

# Սանկերամիկա
# https://www.onlineshinanyut.am/products/khachukner-saliki
# https://www.onlineshinanyut.am/products/santekhnikayi-detalner
# https://www.onlineshinanyut.am/products/cncughner
# https://www.onlineshinanyut.am/products/pakanner-ev-kcamaser
# https://www.onlineshinanyut.am/products/fum+pakli
# https://www.onlineshinanyut.am/products/pomper
# https://www.onlineshinanyut.am/products/sankeramika
# https://www.onlineshinanyut.am/products/tsorakner
# https://www.onlineshinanyut.am/products/chkakhoghovakner
# https://www.onlineshinanyut.am/products/odapokhutyun

# Ամեն ինչ տան համար
# https://www.onlineshinanyut.am/products/kahuyqi-ankyunner
# https://www.onlineshinanyut.am/products/tntesakan-apranqner
# https://www.onlineshinanyut.am/products/koghpeqner
# https://www.onlineshinanyut.am/products/kencaghayin-paraganer
# https://www.onlineshinanyut.am/products/jang-hanogh-heghuk
# https://www.onlineshinanyut.am/products/smart-home

# Շինանյութ
# https://www.onlineshinanyut.am/products/%D5%93%D6%80%D6%83%D5%B8%D6%82%D6%80%D5%B6%D5%A5%D6%80-%D5%BD%D5%AB%D5%AC%D5%AB%D5%AF%D5%B8%D5%B6%D5%B6%D5%A5%D6%80
# https://www.onlineshinanyut.am/products/sosndzogh-nyuter-prpurner
# https://www.onlineshinanyut.am/products/posheghen
# https://www.onlineshinanyut.am/products/penoplast
# https://www.onlineshinanyut.am/products/qsanyuter+-tautner
# https://www.onlineshinanyut.am/products/lcahartichner
# https://www.onlineshinanyut.am/products/payte-reyka
# https://www.onlineshinanyut.am/products/amrakcman-paraganer
