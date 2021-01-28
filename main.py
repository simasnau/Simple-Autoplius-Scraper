from matplotlib import colors
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException
import pylab as plt
import threading

def elementExistsByClass(name):
    try: driver.find_element_by_class_name(name)
    except NoSuchElementException:
        print("Element not found")
        return False
    return True



def getData():
    try:
        while elementExistsByClass('next'):

            # Gets all posts in a page.
            posts=driver.find_elements_by_class_name('announcement-parameters')

            for post in posts:
                stats=post.find_elements_by_tag_name('span')
                metai=stats[0].text
                if len(metai)>5: data=datetime.strptime(metai, '%Y-%m')  # Gets date depending on its format.
                else: data=datetime.strptime(metai, '%Y')

                if len(stats)>3 and 'km' in stats[3].text: # Gets mileage, it may be in different indexes in stats array.
                    rida=int((stats[3].text.strip('km')).replace(" ",""))
                    datos.append(data)
                    ridos.append(rida)
                elif len(stats)>4 and 'km' in stats[4].text:
                    rida=int((stats[4].text.strip('km')).replace(" ",""))
                    datos.append(data)
                    ridos.append(rida)
                else: rida=0
                print(metai,rida)

            # Finds "next" button and presses it
            nextBut=driver.find_element_by_class_name('next')
            driver.execute_script('arguments[0].click()',nextBut)
            
            # Sleeps to not get kicked out.
            sleep(0.5)


    except Exception as e:
        print(e)

# WebDriver setup
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://autoplius.lt/skelbimai/naudoti-automobiliai")
sleep(0.2)

try:
    datos=[]
    ridos=[]

    # Creates a thread for getting car data and starts it
    getDataThread=threading.Thread(target=getData,args=())
    getDataThread.start()

    # Main loop, draws data.
    while True:
        plt.clf()
        plt.scatter(datos,ridos,s=2, color="blue")
        plt.pause(0.05)

        
except KeyboardInterrupt:
    print("While was interrupted")

except Exception as e:
    print(e)

driver.quit()
