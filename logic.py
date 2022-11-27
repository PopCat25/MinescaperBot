from selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from siteWorker import *
from algoritmMetods import *
import time
import os
from random import *

def start(difLevel):
    try:
        url = f"https://minesweeper.online/ru/start/{difLevel}" 
        # url = "https://minesweeper.online/ru/game/1779637747"
        driver = webdriver.Chrome(executable_path="\\chromedriver.exe")
        driver.get(url = url)
        time.sleep(3)  # Ожидаем загрузки страницы
    
        h,w = 0,0           #Создание  переменных высоты и ширины поля в зависимости от выбранной сложности
        if difLevel == 1 :
            h = 9
            w = 9
        elif difLevel == 2 :
            h = 16
            w = 16
        elif difLevel == 3 :
            h = 16
            w = 30

        win, lose = 0, 0
        while True:

            mineCount = mineCountPars(driver) # Вызываем функцию из сайтворкера, что бы узнать кол-во мин 
            field = gameFieldPars(h, w, driver) # Вызываем функцию из сайтворкера для парсинга игрового поля

            os.system('CLS')    # Очищение консоли
            
            print("Игровое поле")
            print(f"Осталось мин: {mineCount}") 
            for row in field:
                print(row)
            
            probabilityField = findProbabilityField(field)  #Находим вероятность нахождения мин

            print("\n") 
            print("Поле вероятности \n") 
            for row in probabilityField:
                print(row)


            
            win, lose = checkGameConsist(driver, win, lose) #помимо ресета в случае конца игры ещё делаем +1 в счётчикам винов\лузов
            print(f"Побед:{win} Поражений: {lose}")



    except Exception as ex :
        print(ex)
    finally:
        driver.quit()