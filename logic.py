from selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from siteWorker import *
from algoritmMetods import *
from random import *
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options   #Ипорт для того что бы была возможность настроить webdriver и сохранить это в профиль
import time
import os


def start(difLevel):
    try:
        url = f"https://minesweeper.online/ru/start/{difLevel}" 
        # url = "https://minesweeper.online/ru/game/1781484250"

        options = Options()                                                                         #Создаём переменую опции что бы сохранить профиль в котором будет указано включение блокировщика рекламы
        options.add_argument("user-data-dir=C:\\profile")                                           #Указываем путь где хранить профиль браузера. 

        driver = webdriver.Chrome(executable_path="\\chromedriver.exe",options=options)             #Тк теперь мы сохраняем опции при первом запуске надо установить блокировку рекламы, и теперь всплывающие окна не будут ломать парсер
        driver.implicitly_wait(30)                                                                  # Ожидаем загрузки страницы если не дождались то timeout
        driver.get(url = url)
    
        h,w = 0,0                                                                                   #Создание  переменных высоты и ширины поля в зависимости от выбранной сложности
        if difLevel == 1 or difLevel % 10 == 1 :
            h = 9
            w = 9
        elif difLevel == 2 or difLevel % 10 == 2 :
            h = 16
            w = 16
        elif difLevel == 3 or difLevel % 10 == 3 :
            h = 16
            w = 30

        win, lose = 0, 0

        while True:
            worktime = time.time()                                                                  #Переменная для измерения времени работы парсера
            mineCount = mineCountPars(driver)                                                       # Вызываем функцию из сайтворкера, что бы узнать кол-во мин 
            field,xMarkIndexY,xMarkIndexX = gameFieldPars(h, w, driver)                             # Вызываем функцию из сайтворкера для парсинга игрового поля, это кортеж потому что мы ещё передаём координаты крестика для режима игры без угадывания, если крестика нет возвращается field, None,None
            parserTime = time.time()-worktime

            if xMarkIndexY == None and xMarkIndexY == None:                                         #Если крестика нет то вычисляем поле вероятности, это что бы не переписывать algoritmMetods         Проверка на наличие крестика на поле, если есть то тыкаем в него, иначе совершаем обычный ход
                worktime = time.time()                                                              #Переменная для измерения времени работы алгоритма вычисления вероятностей
                probabilityField = findProbabilityField(field)                                      #Находим вероятность нахождения мин
                probabilityTime = time.time()-worktime
                makeTurn(probabilityField,driver)
            else:
                element = driver.find_element(By.XPATH, f"//*[@id=\"cell_{xMarkIndexX}_{xMarkIndexY}\"]")
                element.click()


            win, lose = checkGameConsist(driver, win, lose)                                         #помимо ресета в случае конца игры ещё делаем +1 в счётчикам винов\лузов
            print(f"Побед: {win} Поражений: {lose}")
            os.system('CLS')                                                                        # Очищение консоли
            printGame(parserTime,probabilityTime,field,mineCount,probabilityField)                  #Метод для одновременного вывода информации в консоль что бы консоль не моргала               


    except Exception as ex :
        print(ex)
    # finally:
    #     #driver.quit()                #Пока что не закрываем окно браузераы



def printGame(parserTime:int,probabilityTime:int,field:list[list[int]],mineCount:int,probabilityField:list):        #Метод кривой но позволяет консоли не моргать
    print(f"Игровое поле     Время парсинга: {parserTime}")
    print(f"Осталось мин: {mineCount}") 
    for row in field:
        print(row)

    print("\n") 
    print(f"Поле вероятности   Время вычислений: {probabilityTime} \n") 
    for row in probabilityField:
        print(row)