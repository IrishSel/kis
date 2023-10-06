import cv2
import numpy as np
from skimage.color import rgb2hsv
from skimage.measure import label, regionprops
import matplotlib.pyplot as plt


value_saturated = 0.
region_saturated = None

source = cv2.imread("task2.png")
for region in regionprops(label(source))[::source.shape[2]]:
    y, x, dim = region.centroid
    value = rgb2hsv(source[int(y), int(x)])[1]
    if (value > value_saturated):
        value_saturated = value
        region_saturated = region

result = np.zeros((source.shape[0], source.shape[1], source.shape[2]), np.uint8)
miny, minx, _, maxy, maxx, _ = region_saturated.bbox
result[miny : maxy, minx : maxx] = source[miny : maxy, minx : maxx]
print(value_saturated)
plt.imshow(result)
plt.show()
