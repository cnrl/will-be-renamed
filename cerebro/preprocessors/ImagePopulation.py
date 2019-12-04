import cv2
import glob

import numpy

from cerebro.models import Neuron
from cerebro.models import Population


class ImagePopulation(Population):

    image_type = ["jpg", "png"]
    image_list = []

    def __init__(self, size, path, filter_type, coding_scheme="intensity_to_latency", **filter_params):
        self.neuron = Neuron(
            variables="""
                tts = 0 : local
                base_time = 0 : shared
            """,
            spike="((base_time + tts) >= t) & ((base_time + tts) <= t)",
        )
        super().__init__(size, self.neuron)
        self.set_image(path)
        self.filtered_image_list = self.apply_filter(filter_type, **filter_params)
        self.coding_scheme = coding_scheme

    def load_image(self, name):
        try:
            img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
        except Exception:
            raise Exception("there is no image")

        img = cv2.resize(img, (self.size // 2, self.size // 2))

        return img

    def set_image(self, path):
        name = path.split('/')[-1]
        if '.' in name:
            self.image_list.append(self.load_image(name))
        else:
            for j in self.image_type:
                for i in glob.glob(path + "/*." + j):
                    self.image_list.append(self.load_image(i))

    def apply_filter(self, filter_type, **params):
        if filter_type == "Gabor":
            filtered_image = self.gabor_filter(**params)
        elif filter_type == "DoG":
            filtered_image = self.dog_filter(**params)
        else:
            raise Exception("wrong filter")

        return filtered_image

    def dog_filter(self, size_of_gaussian_1, size_of_gaussian_2):
        image_with_dog_list = []
        for i in self.image_list:
            dog_img_1 = cv2.GaussianBlur(i, (size_of_gaussian_1, size_of_gaussian_1), 0)
            dog_img_2 = cv2.GaussianBlur(i, (size_of_gaussian_2, size_of_gaussian_2), 0)
            image_with_dog_list.append(dog_img_1 - dog_img_2)

        return image_with_dog_list

    def gabor_filter(self, gabor_size, sigma,
                     theta_list, lambd, gamma, psi, k_type):

        image_with_gabor_list = []
        for i in self.image_list:
            for j in theta_list:
                g_kernel = cv2.getGaborKernel((gabor_size, gabor_size), sigma, j, lambd, gamma, psi, ktype=k_type)
                image_with_gabor_list.append(cv2.filter2D(i, cv2.CV_8UC3, g_kernel))
        return image_with_gabor_list

    def intensity_to_latency(self):
        if self.filtered_image_list is None:
            raise Exception('no image list exist !')
        tmp = []
        for k in range(len(self.filtered_image_list)):
            for i in range(len(self.filtered_image_list[k])):
                for j in range(len(self.filtered_image_list[k][i])):
                    # tmp.append((k, i, j, self.filtered_image_list[k][i][j]))
                    tmp.append(self.filtered_image_list[k][i][j])
                    # k is index of pictures
                    # (i,j) shows location of each point in kth photo
                    # img_list[k][i][j] shows spike

        # tmp.sort(key=lambda tup: tup[3], reverse=True)
        # # print(tmp[0][3])
        # for i in range(len(tmp)):
        #     tmp[i] = (tmp[i][0], tmp[i][1], tmp[i][2], abs(tmp[i][3] - 255))

        return numpy.asarray(tmp)
