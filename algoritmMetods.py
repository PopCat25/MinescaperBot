import time

def findNeighboringCells(field:list): #Метод\код вычисляет для каждой ячейки набор соседних ячеек(групп) в радиусе 1 клетка а так же количество открытых и неоткрытых ячеек 

    listOfneighborCells = []          #лист с результатом                                                                   #-1,-1 -1,0   -1,1
    container = []                    #лист для заполнения листа с результатами                                             # 0,1    0     0,1
    offsetList = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]] #Все возможные смещения для соседей клетки Рисунок:# 1,-1  1,0    1,1  координаты в формате (y,x)
    rowIndex,columnIndex = 0,0        # Индексы ячейки для которой ищем соседей, используем это потому что list.index работает немного кривовато для нас
    for row in field:                 # берём каждую строчку из поля
        for cell in row:                # к каждой ячейке в строчке применяем код ниже:
            for offset in offsetList:   # Применяем к индексам ячейки смещение
                if columnIndex + offset[0] >= 0 and rowIndex + offset[1] >=0 and columnIndex + offset[0] <= len(field) - 1 and rowIndex + offset[1] <= len(row) - 1 : # первый and проверка на отрицательность смещённых индексов, что бы не получать значения с конца. Третий and для определения вышли мы за предел листа и если вышли то пропускаем такое смещение
                    container.append([columnIndex + offset[0], rowIndex + offset[1], field[columnIndex + offset[0]][rowIndex + offset[1]]  ,columnIndex,rowIndex,f'Дебаг строка с содержимым ячейки: {cell}']) # записываем: (y-координата соседней ячейки,x-координата соседней ячейки), (Состояние соседней ячейки(открыто\закрыто)), (y,x индексы кому приходятся соседом)
                    print(container)
                    container.clear()   #Очищаем контейнер что бы не получать повторение одного массива
            # print(f"Символ в строке: {rowIndex} Строка: {columnIndex} Содержимое по индексу: {field[columnIndex][rowIndex]}")
            print("\n")
            # time.sleep(3)
            rowIndex += 1                       #rowIndex - счётчик символа в строке
        rowIndex = 0                            #Обнуляем счётчик что бы не словить out of range
        columnIndex +=1                         #columnindex - счётчик строки