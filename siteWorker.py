from selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from siteWorker import *

def mineCountPars (driver:webdriver.Chrome): #Парсер количества мин
    
    mineCount = 0
    for i in (1, 10, 100):
        for j in filter (str.isdigit ,driver.find_element(By.XPATH, f"//*[@id=\"top_area_mines_{i}\"]").get_attribute("class")):
            mineCount += i * int(j)
    return mineCount

def gameFieldPars (h:int, w:int, driver:webdriver.Chrome): #Парсер игрового поля
    
    field = [[0] * w for i in range(h)] # Создание поля шириной w и высотой h
    for j in range (h): 
        for i in range (w):
            element = driver.find_element(By.XPATH, f"//*[@id=\"cell_{i}_{j}\"]")
            elementClassLine = element.get_attribute("class").split()                    
            field[j][i] = cellPars(elementClassLine)
    return field

def checkGameConsist (driver:webdriver.Chrome, win:int, lose:int):     # проверка конца игры, в случае луза ресет и возврат + 1 к лузам, при победе ресет и возврат +1 к победам

    reset = driver.find_element(By.XPATH, "//*[@id=\"top_area_face\"]") #Храним кнопку ресета игры
    if reset.get_attribute("class") == "top-area-face zoomable hd_top-area-face-lose":  #Условие проигрыша
        reset.click()
        return win + 0, lose + 1

    elif reset.get_attribute("class") == "top-area-face zoomable hd_top-area-face-win": #Условие победы
        reset.click()
        return win + 1, lose + 0
        
    return win + 0, lose + 0


def cellPars (elementClassLine:list[str]):

    if elementClassLine[2] == "hd_closed" and len(elementClassLine) == 3 : # Если ячейка закрыта
        return "*"

    elif elementClassLine[2] == "hd_closed" and elementClassLine[3] == "hd_flag": # Если ячейка закрыта, и на ней флаг
        return "F"

    elif elementClassLine[2] == "hd_closed" and elementClassLine[3] == "start": #Если ячейка закрыта и на ней крестик, это для режима без угадывания
        return "x"

    elif elementClassLine[2] == "hd_opened": # Получение количества мин рядом с ячейкой
        return str(elementClassLine[3]).split("e")[1] # класс представляет из себя строку "cell size24 hd_opened hd_type1" можно расплитить по пробелу а потом элемент с 3 индексом  по "e" тогда в 1 индексе будет число мин