from matplotlib import colors
from matplotlib.pyplot import title
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import pylab as plt
import threading
import csv
import re


def elementExistsByClass(name):
    try:
        driver.find_element_by_class_name(name)
    except NoSuchElementException:
        print("Element not found")
        return False
    return True


def getData():

    writer = csv.writer(csvFile)
    writer.writerow(('Model', 'Price', 'Year',
                    'Mileage', 'Displacement', 'Power', 'Link'))

    while elementExistsByClass('next'):

        # Gets all posts in a page.
        posts = driver.find_elements_by_class_name('announcement-item')

        for post in posts:
            try:
                title=str(post.find_element_by_class_name('announcement-title').text)

                displacement=title.split(",")[1].strip()
                if re.match("^ ?[0-9]\.[0-9] l\.$", displacement):
                    displacement=displacement[:-3]
                else : displacement=0

                makeModel=title.split(",")[0]
                print("Title: ", makeModel)
                params = post.find_element_by_class_name('bottom-aligner')
                
                link=post.get_attribute("href")
                price=str(post.find_element_by_class_name('announcement-pricing-info').text).split("€")[0]
                metai = params.find_element_by_xpath('.//span[@title="Pagaminimo data"]').text
                galia = params.find_element_by_xpath('.//span[@title="Galia"]').text

                if len(metai) > 5:
                    # Gets date depending on its format.
                    data = datetime.strptime(metai, '%Y-%m')
                else:
                    data = datetime.strptime(metai, '%Y')

                rida = int(params.find_element_by_xpath('.//span[@title="Rida"]').text.strip('km').replace(" ", ""))

                with lock:
                    datos.append(data)
                    ridos.append(rida)

                print(price)

                writer.writerow((makeModel, price, data, rida, displacement, galia, link))
            except Exception as e:
                print(e)

        # Finds "next" button and presses it
        nextBut = driver.find_element_by_class_name('next')
        driver.execute_script('arguments[0].click()', nextBut)

        # Sleeps to not get kicked out.
        sleep(0.5)


# WebDriver setup
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://autoplius.lt/skelbimai/naudoti-automobiliai")
sleep(0.2)

csvFile = open('autoData.csv', 'w+', newline='')


lock = threading.Lock()
try:
    datos = []
    ridos = []

    # Creates a thread for getting car data and starts it
    getDataThread = threading.Thread(target=getData, args=())
    getDataThread.start()

    # Main loop, draws data.
    while True:
        plt.clf()
        with lock:
            if len(datos) == len(ridos):
                plt.scatter(datos, ridos, s=2, color="blue")

        plt.pause(0.05)


except KeyboardInterrupt:
    print("While was interrupted")

except Exception as e:
    print(e)

driver.quit()
