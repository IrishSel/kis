import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage import color
from skimage.filters import threshold_otsu
from skimage.exposure import adjust_sigmoid

image = plt.imread("task4.jpg")
bw = color.rgb2gray(image)
bw = adjust_sigmoid(bw, cutoff=5, gain=4) #делаем контрастной чтобы было лучше видно


binary = bw.copy()#берётся копия картинки
#на чб делится
binary[bw <= threshold_otsu(bw)] = 0
binary[binary > 0] = 1#если цвет больше 0, то он делается 1(чёрный)

#нумерутеся
labeled = label(binary)

#запоминет данные с картинки
regions = regionprops(labeled)

#Поиск объекта с наибольшей площадью.
#У нас получилось кроме шарика ещё 2 объекта - это блики от света,
#так как они яркие. Мы ищем визуально самый большой объект и считаем его шариком.
rtmp = None#регион с макисмальной площадью
maxarea = 0

for reg in regions:
    if reg.area > maxarea:
        rtmp = reg
        maxarea = reg.area#наибольшая площадь(запоминает)

#поиск ширины в пикселях(это скобочки) и * на ном разрешение (формула)
realWidth = (rtmp.bbox[2]-rtmp.bbox[0]) * 1.05714#сколько мм в 1 пикселе

print(realWidth)

plt.subplot(121)
plt.imshow(image)
plt.subplot(122)
plt.imshow(labeled)
plt.show()