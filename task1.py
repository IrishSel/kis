import numpy as np
import matplotlib.pyplot as plt
from skimage import filters
from skimage.measure import label, regionprops


image = plt.imread('task1.png')  # считывает с картинки
image1 = np.mean(image, 2)

sobel = filters.sobel(image1)
sobel = np.array(sobel)
sobel[sobel > 0] = 1  #выделяет контуры на изображении и запоминает их в массив

labeled = label(sobel)   # функция нумерует все пиксели

regions = regionprops(labeled)  # собирает инфу о каждой букве по номерам/запоминет данные с картинки

images = []
areas = []
for region in regions: #подсчитывает все площади фигур
    if not np.all(region.image):
        area = 0
        beginning = False
        in_figure = False
        for i in range(region.image.shape[0]): #  пиксель 0, то не складываем
            for j in range(region.image.shape[1] - 1): # пиксель 1, то складываем и запоминаем
                if beginning:
                    if in_figure:
                        if region.image[i][j] == 0:
                            area += 1
                        else:
                            in_figure = False
                    else:
                        if region.image[i][j] == 1 and region.image[i][j + 1] == 0: #если нынешний пиксель 1, а след 0, то то фигура
                            in_figure = True
                elif region.image[i][j] == 0 and region.image[i - 1][j] == 1 and region.image[i][j - 1] == 1: # а если нынешний 0, а предыдущие два 1, то это тоже фигура
                    beginning = True
                    in_figure = True
        images.append(region.image)
        areas.append(area)

max_area = [0, 0] # поиск самой большой площади, если находит больше, то перезаписывает
for area_ind in range(len(areas)):
    if areas[area_ind] > max_area[0]:
        max_area = [areas[area_ind], area_ind]

print('Максимальная внутренняя площадь', max_area[0])
plt.figure()
plt.imshow(images[max_area[1]]) #отображает в окне фигуру с самой большой площадью

print('Все площади:', areas)

plt.figure()
plt.imshow(labeled)
plt.show()
