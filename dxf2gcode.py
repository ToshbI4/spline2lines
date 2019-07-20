"""
dxf2gcode.py
Author: bedlamzd of MT.lab

Чтение .dxf файла, слайсер этого dxf, перевод в трёхмерное пространство на рельеф объектов,
генерация gcode в соответствующий файл
"""
import ezdxf as ez


# TODO: написать логи

Z_max = 30
Z_up = Z_max + 3  # later should be cloud Z max + few mm сейчас это глобальный максимум печати принтера по Z
extrusionCoefficient = 0.41  # коэффицент экструзии, поворот/мм(?)


# when path is a set of elements


def dxfReader(dxf, modelspace, elementsHeap=None):  # at first input is modelspace
    """
    Рекуррентная функция
    Собирает данные об элементах в dxf с заходом во все внутренние блоки. При этом описывая их
    собственным классом Element для удобства

    :param dxf: исходное векторное изображение
    :param modelspace: пространство элементов изображения, либо пространство блока с элементами
    :param elementsHeap: массив в который собираются все элементы
    :return elements_heap: массив со всеми элементами из dxf
    """
    # TODO: чтение по отдельным слоям (i.e. отдельным контурам)
    if elementsHeap is None:
        elementsHeap = []

    for element in modelspace:
        # если элемент это блок, то пройтись через вложенные в него элементы
        if element.dxftype() == 'INSERT':
            block = dxf.blocks[element.dxf.name]
            dxfReader(dxf, block, elementsHeap)
        # если элемент не блок и при этом переопределяем, то записать его переопределение в массив
        elif elementRedef(element):
            elementsHeap.append(elementRedef(element))
        # если переопределение вернуло пустой элемент (ещё не описанный), то написать об этом
        else:
            print('undefined element')
    return elementsHeap


def elementRedef(element):
    """
    Функция для переопределения полученного элемента в соответствующий подкласс класса Element

    :param element: элемент из dxf
    :return: переопределение этого элемента
    """
    if element.dxftype() == 'POLYLINE':
        return element
    elif element.dxftype() == 'SPLINE':
        return element
    elif element.dxftype() == 'LINE':
        return element
    elif element.dxftype() == 'CIRCLE':
        return element
    elif element.dxftype() == 'ARC':
        return element
    elif element.dxftype() == 'ELLIPSE':
        pass
    elif element.dxftype() == 'LWPOLYLINE':
        pass
    elif element.dxftype() == 'POINT':
        pass
    # else:
    #     return Element(element)

