import cv2
import glob
from skimage.measure import block_reduce
import numpy as np


def load_image(image_name):
    img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
    return img


def pooling(img, pooling_window):
    return block_reduce(img, pooling_window, np.max)


def intesity_to_latency_encoding(img_list):
    tmp = []
    for k in range(len(img_list)):
        for i in range(len(img_list[k])):
             for j in range(len(img_list[k][i])):
                tmp.append((k, i, j, img_list[k][i][j]))

    tmp.sort(key=lambda tup: tup[3], reverse=True)
    # print(tmp[0][3])
    for i in range(len(tmp)):
        tmp[i] = (tmp[i][0], tmp[i][1], tmp[i][2], abs(tmp[i][3] - 255))

    return tmp



print("Enter folder name for reading images :")
folder_name = input()
print("Enter default size of images:")
x = int(input())
default_size = (x, x)

print("pool size")
x = int(input())
pooling_window = (x, x)
image_list = []
for i in glob.glob(folder_name + "/*.jpg"):
    image = load_image(i)
    print(image.shape)
    image = cv2.resize(image, default_size)
    print(image.shape)
    image = pooling(image, pooling_window)
    print(image.shape)
    cv2.imshow("Aa", image)
    image_list.append(image)
spike_list = intesity_to_latency_encoding(image_list)
print(spike_list)
cv2.waitKey(0)
cv2.destroyAllWindows()
