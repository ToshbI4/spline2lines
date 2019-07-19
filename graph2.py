from math import *
from tkinter import *
import ezdxf
import dxf2gcode as dx
from time import time

start = time()
root = Tk()#Создаем окно
canv = Canvas(root, width=1600,height=800)#Создаем полотно для рисования
canv.pack()
canv.create_line(0,0,400,0,fill='blue',arrow=LAST)#Рисуем оси со стрелочками направления
canv.create_line(0,0,0,400,fill='blue',arrow=LAST)


# Загружаем файл, из которого будем доставать сплайны
# dwg = ezdxf.readfile("C:\\Users\Anton\Desktop\MT.LAB\paseka\printer\ezspline3.dxf")
dwg = ezdxf.readfile("C:\\Users\Anton\Desktop\MT.LAB\paseka\printer\snow_wo_hatch&edge.dxf")

# iterate over all entities in model space
msp = dwg.modelspace()

# Загружаем все элементы из файла(сплайны, полилинии и тд)
elements = dx.dxfReader(dwg, msp)

def part(p):

#Функция, которая принимает на вход номер сплайна из общего списка элементов.
#По данным контрольных точек сплайна функция находит все точки, которые лежат на сплайне с заданным шагом t по формуле для кривой Безье.

    count = elements[p].control_point_count() #Количество контрольных точек сплайна

    #spline = msp.query('SPLINE')[0]#Берем первый сплайн
    #count = len(spline.get_control_points()) #Количество управляющих точек сплайна

    points = [point for point in elements[p].control_points] # Заполняем массив контрольных точек сплайна
    x1, y1 = 0, 0
    x2, y2 = 0, 0
    u = 6 #Коэффициент, определяющий размеры выводимого изображения. Больше коэффициент - больше изображение
    xs = []#Массивы, содержащие ControlPoints сплайна (управляющие точки)
    ys = []
    a = 0
    for i in range(0, count):
        xs.append(points[i][0])
        ys.append(points[i][1])

    #Безье по n точкам
    #Рисуем множество точек для кривой Безье, изменяя параметр t

    for t in range(0, 1000, 1):
        t = t/1000
        a = t**(count-1)
        if t == 0:
            (x, y) = 0,0
        else:
            k = count - 1
            while k >= - 1:
                x = x + xs[k] * a
                y = y + ys[k] * a
                a = a * k * (1 - t) / ((count - 1 - k + 1) * t)
                k-=1
        #canv.create_oval(u * x - u * 100 + 200, u * y + u * 100 + 400, u * x - u * 100 + 200+1, u * y + u * 100 + 400+1)


        #Разбиваем сплайн на отрезки не больше заданной длины
        if (sqrt((x-x1)**2+(y-y1)**2)<= 1) :
            (x2,y2) = (x,y)
        else:
            canv.create_line(u*x1-u*100+200,u*y1+u*100+400,u*x2-u*100+200,u*y2+u*100+400)
            x1, y1 = x, y
        print (x,y)
        x,y = 0,0
    print(time()-start)
for i in range (6,12):
    part(i)
for i in range (24,42):
    part(i)
root.mainloop()