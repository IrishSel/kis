import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage import color


# функция:сколько озёр и заливов(списано с доски было)
def lakes_and_bays(image):
    b = ~image
    lb = label(b)
    regs = regionprops(lb)

    count_lakes = 0  # озёра
    count_bays = 0  # заливы

    for reg in regs:
        on_bound = False
        for y, x in reg.coords:
            if y == 0 or x == 0 or \
                    y == image.shape[0] - 1 or \
                    x == image.shape[1] - 1:
                on_bound = True
                break
        if not on_bound:
            count_lakes += 1
        else:
            count_bays += 1
    return count_lakes, count_bays


# функция:распознование буквы с картинки
def recognize2(region):
    lakes_image, bays_image = lakes_and_bays(region.image)
    # озёра и заливы
    if lakes_image == 1:  # если озёр 1
        cy = region.image.shape[0] // 2  # y в ширину
        cx = region.image.shape[1] // 2  # x это в ширину, // это целочисленное деление
        if region.image[cy, cx] > 0:
            return "R"
        else:
            return "D"
    # если в середине пустота, то это D, а если не пустота, то R

    if lakes_image == 0:  # озёра
        if bays_image == 3:  # заливы
            return "K"
        else:
            if region.image[0, 0] == 1:  # тут по угловому пикселу
                return "L"
            else:
                return "J"
    return None


image = plt.imread("task3.png")  # считывает с картинки
binary = color.rgb2gray(image[:, :, 0:3])  # цвета в серый

binary[binary > 0] = 1  # если цвет больше 0, то он делается 1(чёрный цвет)
labeled = label(binary)  # функция нумерует все пиксели
regions = regionprops(labeled)  # соиьрает инфу о каждой букве по номерам
print("Количество объектов: " + str(len(regions)))  # размер массива и по этому выводим количество букв

ard = {None: 0}  # ard-словарь(буква и число(количество))
# цикл погоняет каждую букву и зансит в массив значение
for region in regions:
    symbol = recognize2(region)  # распознование, даётся картинка и выдаётся буква
    if symbol not in ard:
        ard[symbol] = 0
    ard[symbol] += 1
# цикл показывает количество букв. то есть если символ не найден, то ничего не прибавляем
# и если символ не в словаре, то прибавляем + 1
# то есть, если есть она буква, то он заносит в словарь
# если повторяется буква, то он не заносит повторно, а считает количество уже буквы


for i in ard:
    if (i == None):
        print("Неизвестные: " + str(ard[i]))
    else:
        print(str(i) + ": " + str(ard[i]))

plt.imshow(binary, cmap="hot")
plt.show()
