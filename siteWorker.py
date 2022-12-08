from selenium import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from siteWorker import *
from bs4 import BeautifulSoup
import sys 
import random
import time

def mineCountPars (driver:webdriver.Chrome): #Парсер количества мин
    
    mineCount = 0
    for i in (1, 10, 100):
        for j in filter (str.isdigit ,driver.find_element(By.XPATH, f"//*[@id=\"top_area_mines_{i}\"]").get_attribute("class")):
            mineCount += i * int(j)
    return mineCount

def gameFieldPars (h:int, w:int, driver:webdriver.Chrome): #Парсер игрового поля
    
    html = driver.page_source                                                       # Из селениума получаем отрендереную html страницу что бы парсить её супом а не искать через find_element в selenium
    soup = BeautifulSoup(html,"lxml")                                               # Передавая в конструктор супа, наш html мы получаем дерево элементов с помощью парсера lxml
    elements = soup.find_all("div","cell")                                          # с помощью find_all находим все элементы div с CSS классом cell

    ind = 0                                                                         # индекс для перебора элементов в elements
    xMarkIndexY = None
    xMarkIndexX = None
    field = [[0] * w for i in range(h)] # Создание поля шириной w и высотой h
    for j in range (h): 
        for i in range (w):
            # element = driver.find_element(By.XPATH, f"//*[@id=\"cell_{i}_{j}\"]") #Старый парсинг через селениум
            # elementClassLine = element.get_attribute("class").split()  
            elementClassLine = elements[ind]["class"]                               #bs4.element.ResultSet содержит внутри элементы типа Tag у которого с помощью ["class"] можно получить строку CSS классов
            ind += 1
            field[j][i] = cellPars(elementClassLine)
            if field[j][i] == "x":
                xMarkIndexY = j
                xMarkIndexX = i

    return field, xMarkIndexY, xMarkIndexX

def checkGameConsist (driver:webdriver.Chrome, win:int, lose:int):     # проверка конца игры, в случае луза ресет и возврат + 1 к лузам, при победе ресет и возврат +1 к победам

    reset = driver.find_element(By.XPATH, "//*[@id=\"top_area_face\"]") #Храним кнопку ресета игры
    if reset.get_attribute("class") == "top-area-face zoomable hd_top-area-face-lose":  #Условие проигрыша
        time.sleep(2)                                                                   #Небольшая пауза что бы немного погрустить
        reset.click()
        return win + 0, lose + 1

    elif reset.get_attribute("class") == "top-area-face zoomable hd_top-area-face-win": #Условие победы
        time.sleep(2)                                                                   #Небольшая пауза что бы насладиться победой
        reset.click()
        return win + 1, lose + 0
        
    return win + 0, lose + 0


def cellPars (elementClassLine:list[str]):

    if elementClassLine[2] == "hd_closed" and len(elementClassLine) == 3 : # Если ячейка закрыта
        return "*"

    elif elementClassLine[2] == "hd_closed" and elementClassLine[3] == "hd_flag": # Если ячейка закрыта, и на ней флаг
        return "*"      #пока поставил '*' что бы не ломалась программа при победе

    elif elementClassLine[2] == "hd_closed" and elementClassLine[3] == "start": #Если ячейка закрыта и на ней крестик, это для режима без угадывания
        return "x"

    elif elementClassLine[2] == "hd_opened": # Получение количества мин рядом с ячейкой
        return str(elementClassLine[3]).split("e")[1] # класс представляет из себя строку "cell size24 hd_opened hd_type1" можно расплитить по пробелу а потом элемент с 3 индексом  по "e" тогда в 1 индексе будет число мин

    return "*"

def makeTurn (probabilityField:list,driver:webdriver.Chrome):
    
    leastExplosiveCells = []                                                                                #Список клеток с наименьшей вероятность взрыва. Пример одного элемента: [minProbability,xIndex,yIndex]

    minProbability =  sys.maxsize                                                                           # эталон для сравнивания
    xIndex,yIndex = 0,0                                                                                     #Индексы для поиска ячейки

    for row in probabilityField:                                                                            #В листе вероятностей ищем наименьшее значение
        for cell in row:
            if type(cell) is not str and cell > 0 and cell < minProbability:                                # условие для поиска наименьшего значения вероятности тк пустые ячейки нас не интересуют вероятность должна быть больше нуля но меньше эталона
                minProbability = cell
    
    for row in probabilityField:
        for cell in row:
            if cell == minProbability:
                leastExplosiveCells.append([minProbability,xIndex,yIndex])
            xIndex += 1
        xIndex = 0
        yIndex += 1

    if minProbability == sys.maxsize:                                                           #Ход на случай если все клетки закрыты
        randomY = random.randint(1, len(probabilityField) - 1)                                  #Индексы не угловые что бы было не 3 или 5 соседей а 8   
        randomX = random.randint(1, len(probabilityField[0]) - 1)
        element = driver.find_element(By.XPATH, f"//*[@id=\"cell_{randomX}_{randomY}\"]")                             
        element.click()
        return

    randomLeastExplosiveCells = random.choice(leastExplosiveCells)

    element = driver.find_element(By.XPATH, f"//*[@id=\"cell_{randomLeastExplosiveCells[1]}_{randomLeastExplosiveCells[2]}\"]")
    element.click()

    # print(leastExplosiveCells)
