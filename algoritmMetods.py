import time
import functools

def findProbabilityField(field:list): #Метод\код вычисляет для каждой ячейки набор соседних ячеек(групп) в радиусе 1 клетка а так же вероятность нахождения мины в соседних ячейках относительно текущей

    listOfneighborCells = getListOfneighborCells(field)
    
    # for elem in listOfneighborCells:    #Цикл вывода в консоль содержимого листа соседей
    #     print(f"Ячейка: {elem[0][0]} Координаты x,y {elem[0][1]},{elem[0][2]} Содержимое соседней ячейки {elem[0][3]} Координаты x,y соседа: {elem[0][4]},{elem[0][5]} \n")
    #     time.sleep(20)

    probabilityField = summProbabilites(field,listOfneighborCells)

    probabilityField = correctProbability (probabilityField,listOfneighborCells,field)

    return probabilityField


def getListOfneighborCells (field:list):

    listOfneighborCells = []          #лист соседов                                                                             #-1,-1 -1,0   -1,1
    container = []                    #лист для заполнения листа соседов                                                        # 0,1    0     0,1
    offsetList = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]] #Все возможные смещения для соседей клетки Рисунок:    # 1,-1  1,0    1,1  координаты в формате (y,x)
    xIndex,yIndex = 0,0                 # Индексы ячейки для которой ищем соседей, используем это потому что list.index работает немного кривовато для нас
    for row in field:                   # берём каждую строчку из поля
        for cell in row:                # к каждой ячейке в строчке применяем код ниже:
            for offset in offsetList:   # Применяем к индексам ячейки смещение
                if yIndex + offset[0] >= 0 and xIndex + offset[1] >=0 and yIndex + offset[0] <= len(field) - 1 and xIndex + offset[1] <= len(row) - 1 : # первый and проверка на отрицательность смещённых индексов, что бы не получать значения с конца. Третий and для определения вышли мы за предел листа и если вышли то пропускаем такое смещение
                    container.append([cell, xIndex, yIndex, field[yIndex + offset[0]][xIndex + offset[1]], xIndex + offset[1], yIndex + offset[0]]) # Состав одного элемента listOfneighborCells: [Ячейка, Координата X, Координата Y, Содержимое соседней ячейки, Координата Х соседа, Координата У соседа]
                    listOfneighborCells.append(container)   # добавляем соседа ячейки в лист соседов                                                                                                  0         1              2                      3                        4                   5
                    container = []                          #Пересоздаём контейнер что бы не получать повторение одного массива
            xIndex += 1                       #rowIndex - счётчик символа в строке
        xIndex = 0                            #Обнуляем счётчик что бы не словить out of range
        yIndex += 1                         #columnindex - счётчик строки
    return listOfneighborCells

def summProbabilites (field:list,listOfneighborCells:list):
    probabilityField = [['*'] * len(field[0]) for i in range(len(field))] #Создаём лист который будет хранить вероятность нахождения мины в ячейках прилежащих к открытым
    xIndex,yIndex = 0,0                                                   #Используем индексы для нахождения совпадений с листом пососедей
    neighborCountClose = 0                                                #Используем для хранения числа соседей
    neighborCountOpen = 0                                                 #Используем для хранения числа открытых соседних ячеек
    records = list()                                                      #Тк после нахождения последней правильной записи перебор пойдёт дальше(но он будет continue) мы будем получать record содержащий последнюю запись в листе соседей, что бы это фиксануть нужные записи добавляем в records
    for row in probabilityField:                                          #Так как probabilityField такого же размера как и field  можно искать записи о соседстве через индексы cell                                 
        for cell in row:                                                  #Для каждой ячейки в probabilityField прогоняем цикл поиска открытых и закрытых соседних ячеек
            for record in listOfneighborCells:                            #для каждой записи в листе соседей делаем прогон по условиям и ищем записи только о тех ячейках которые прилегают к закрытым  
                
                if xIndex != record[0][1]:                                #проверка совпадения по координате x, а ниже и y, так мы находим запись в листе соседей для ячейки probabilityField
                    continue                                              #continue а не break потому что записи для другой ячейки будут прерывать цикл перебора не доходя до правильной записи

                if yIndex != record[0][2]:
                    continue

                if record[0][0] == "*":                                     #Для закрытой ячейки не ищем количество соседей, потому что не сможем узнать вероятность мины в соседних ячейках
                    continue

                if int(record[0][0]) == 0:                                  #Для ячейки рядом с которой нет мин тоже не ищем соседей 
                    probabilityField[yIndex][xIndex] = [0]                  #Вероятность встретить мину в открытой ячейке рядом с которой нет мин нулевая, не забудем отметить это.
                    continue

                if xIndex == record[0][1]:                                  #Для уверенности,для проверки открытой ячейки
                    if yIndex == record[0][2]:                          
                        probabilityField[yIndex][xIndex] = [0]              #Открытая ячейка  не взрывоопасна
                        if record[0][3] == "*":                             #Если соседняя ячейка закрыта +1 в количество соседних ячеек 
                            neighborCountClose += 1
                            records.append(record.copy())                   #Записи о соседях для подходящей ячейки заносим в records
                        if str(record[0][3]).isdigit():                     #Если соседняя ячейка открыта +1 в количетсво открытых соседних ячеек
                            neighborCountOpen += 1
                            # records.append(record.copy())                 #Запись об открытом соседе ячейки нам не нужна, и присутствует тут на всякий случай                  
            
            # if len(records) != 0 :                                        #этот цикл для вывода записей соседей для ячейки (дэбаг)
            #     for recordCopy in records:
            #         print(recordCopy, listOfneighborCells.index(recordCopy))
            #         print(f"Значение ячейки: {recordCopy[0][0]} Координата х: {recordCopy[0][1]} Координата у: {recordCopy[0][2]}, Значение соседней ячейки {recordCopy[0][3]} Координата соседней x: {recordCopy[0][4]} Координата соседней y: {recordCopy[0][5]}  Закрытых сос-х ячеек: {neighborCountClose} Открытых соседних ячеек{neighborCountOpen}")
            # else:
            #     print("Ячейка пропущена")

            if len(records) != 0:                                                                                                               #Если есть записи о ячейке то начинаем цикл записи вероятностей во все соседние ячейки   #Ячейка в probabilityField на время станет листом со всеми влияющими на нёё вероятностями     
                for recordCopy in records:
                    if type(probabilityField[recordCopy[0][5]][recordCopy[0][4]]) is not list:                                                  #Приводим ячейку к листу если она ещё не лист
                        probabilityField[recordCopy[0][5]][recordCopy[0][4]] = []
                    probabilityField[recordCopy[0][5]][recordCopy[0][4]].append(int(recordCopy[0][0])/neighborCountClose)                       #Добавляем вероятность в лист


            records  = []
            neighborCountClose = 0                   
            neighborCountOpen = 0
            xIndex += 1                                                                                                                         #Обнуляем счётчики мин  обнуляем и/или инкримируем счётчики
        xIndex = 0
        yIndex += 1

    sumOfProbabilities = 1                                                                                                                      # итоговое значение вероятности которое мы будем записывать в ячейку. Единица потому что  А=1- (1-A1)*(1-A2)*....*(1-An) из этой единицы мы будем вычитать вероятности
    subtracted = 1                                                                                                                              # то что мы будем вычитать из первой единице в формуле А=1- (1-A1)*(1-A2)*....*(1-An). Единица потому что это нейтральный по умножению элемент
    xIndex,yIndex = 0,0                                                                                                                         #Индексы по которым мы будем обращаться к ячейкам
    for row in probabilityField:            
        for cell in row:
            if type(cell) is list:
                for probability in cell:
                    subtracted = subtracted*(1-probability)                                                                                     #1-A          
                probabilityField[yIndex][xIndex] = sumOfProbabilities - subtracted                                                              #А=1- (1-A1)*(1-A2)*....*(1-An)
            sumOfProbabilities = 1
            subtracted = 1
            xIndex += 1
        xIndex = 0
        yIndex += 1
    
    return probabilityField

def correctProbability (probabilityField:list,listOfneighborCells:list,field:list):
    
    repeat = 50                                                                                                         #переменная с количеством повторений по которой мы будем проверять, нужно ли нам повторить цикл калибровки
    while repeat > 0:                                                                                                   #Цикл в котором соседние клетки будут домнажаться на: Количество мин/сумма вероятности соседних ячеек
            
        xIndex,yIndex = 0,0                                                                                             #Индексы по которым мы будем обращаться к probabilityField
        # pastProbabilityField = probabilityField.copy()                                                                #копия поля вероятности для понимания необходимости повторения корректировки
        for row in field:                                                                                           
            for cell in row:                                                                                            #для каждой ячейки в probabilityField мы будем находить соседей с помощью цикла ниже
                if cell.isdigit() and int(cell) > 0:                                                                    #Если ячейка на игровом поле закрыта или количество мин вокруг неё равно нулю то искать соседей бесмысленно
                    groupProbabilitySum = 0                                                                             #сумма вероятностей в соседних ячейках
                    for neighborRecord in listOfneighborCells:                                                          #Цикл в котором мы будем находить закрытые соседние ячейки и собирать их вероятности в groupProbabilitySum
                        if neighborRecord[0][2] == yIndex and neighborRecord[0][1] == xIndex:                           #Если запись соседства о нашей ячейке то берём её в работу
                            groupProbabilitySum += probabilityField[neighborRecord[0][5]][neighborRecord[0][4]]         #делаем += в сумму вероятностей группы 
                        

                    for neighborRecord in listOfneighborCells:                                                          #В этом цикле мы будем домножать соседние ячейки на groupProbabilitySum
                        if neighborRecord[0][2] == yIndex and neighborRecord[0][1] == xIndex:                           #Опять ищем подходящие записи о ячейке
                            probabilityField[neighborRecord[0][5]][neighborRecord[0][4]] = probabilityField[neighborRecord[0][5]][neighborRecord[0][4]]*(int(neighborRecord[0][0])/groupProbabilitySum) #Присваиваем ячейке значение равное: Значение ячейки*(Количество мин в смежной открытой для неё ячейки)
                xIndex += 1
            xIndex = 0
            yIndex += 1

        repeat -= 1

    return probabilityField