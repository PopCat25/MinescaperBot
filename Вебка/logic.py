from selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from cellParser import *
import time
import os

def start(difLevel):
    try:
        url = f"https://minesweeper.online/ru/start/{difLevel}"
        driver = webdriver.Chrome(executable_path="\\chromedriver.exe")
        driver.get(url=url)
        time.sleep(3)  # Ожидаем загрузки страницы
    
        h,w = 0,0
        if difLevel == 1 :
            h = 9
            w = 9
        elif difLevel == 2 :
            h = 16
            w = 16
        elif difLevel == 3 :
            h = 16
            w = 30

        field = [[0] * w for i in range(h)]

        reset = driver.find_element(By.XPATH, "//*[@id=\"top_area_face\"]")
        continued = True

        while continued:
            
            mineCount = 0
            for i in (1,10,100):
                for j in filter (str.isdigit ,driver.find_element(By.XPATH, f"//*[@id=\"top_area_mines_{i}\"]").get_attribute("class")):
                    mineCount += i * int(j)

            for j in range (h): 
                for i in range (w):
                    element = driver.find_element(By.XPATH, f"//*[@id=\"cell_{i}_{j}\"]")
                    elementClassLine = element.get_attribute("class").split()                    
                    field[j][i] = cellParser(elementClassLine)
                #     print(elementClassLine,i,j)
                # print("Строчка кончилась")
            
            os.system('CLS')
            print(f"Осталось мин: {mineCount}")
            for row in field:
                print(row)


            


            if reset.get_attribute("class") == "top-area-face zoomable hd_top-area-face-lose":
                # print(reset.get_attribute("class"))
                reset.click()
                # continued = False
            elif reset.get_attribute("class") == "top-area-face zoomable hd_top-area-face-win":
                # print(reset.get_attribute("class"))
                continued = False
            # print(reset.get_attribute("class"))


    except Exception as ex :
        print(ex)
    finally:
        driver.close()
        driver.quit()
        return