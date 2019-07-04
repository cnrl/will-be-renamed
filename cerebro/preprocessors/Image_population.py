try:
    import cv2
except:
    raise Exception("cv2 package does not exist !")
try:
    import glob
except:
    raise Exception("glob package does not exist !")


class Image_population():
    # height = 0
    # width = 0
    # encoding type is optional
    image_type = ["jpg", "png"]
    image_list = []

    def __init__(self, folder_name, geometry):
        if len(geometry) == 2:
            self.width = geometry[0]
            self.height = geometry[1]
        else:
            raise Exception("geometry size is not correct !")
        if folder_name == "":
            raise Exception("folder name is empty")

        for j in self.image_type:
            for i in glob.glob(folder_name + "/*." + j):
                self.image_list.append(self.load_image(i, geometry))

    def load_image(self, image_name, geometry):
        try:
            img = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
        except:
            raise Exception("there is no image")

        img = cv2.resize(img, geometry)

        return img

    def filter(self, filter_type, size_of_Gaussian_1 = 5, size_of_Gaussian_2 = 3, gabor_size=11, sigma=0.8,
               theta_list=None, lambd=0.5, gamma=6, psi=0, kType= cv2.CV_32F):
        if theta_list is None:
            theta_list = [0, 45, 90, 135]
        # gabor_size = 11
        # #  Standard deviation of the gaussian envelope.
        # sigma = 0.8
        # # Orientation of the normal to the parallel stripes of a Gabor function.
        # theta_list = [0, 45, 90, 135]
        # # Wavelength of the sinusoidal factor
        # lambd = 0.5
        # # Spatial aspect ratio.
        # gamma = 6
        # # Phase offset
        # psi = 0
        # # Type of filter coefficients. It can be CV_32F or CV_64F
        # kType = cv2.CV_32F
        if filter_type == "Gabor":
            images_with_Gabor_filter = self.Gabor_filter(gabor_size, sigma,
               theta_list, lambd, gamma, psi, kType)

            return images_with_Gabor_filter
        elif filter_type == "DoG":
            images_with_DoG_filter = self.DoG_filter(size_of_Gaussian_1, size_of_Gaussian_2)

            return images_with_DoG_filter
        else:
            raise Exception("wrong filter")


    def DoG_filter(self,size_of_Gaussian_1 ,size_of_Gaussian_2):
        image_with_DoG_list = []
        for i in self.image_list:
            DoG_img_1 = cv2.GaussianBlur(i, (size_of_Gaussian_1, size_of_Gaussian_1), 0)
            DoG_img_2 = cv2.GaussianBlur(i, (size_of_Gaussian_2, size_of_Gaussian_2), 0)
            image_with_DoG_list.append(DoG_img_1 - DoG_img_2)
        return image_with_DoG_list

    def Gabor_filter(self,gabor_size, sigma,
               theta_list, lambd, gamma, psi, kType):

        image_with_Gabor_list = []
        for i in self.image_list:
            for j in theta_list:
                g_kernel = cv2.getGaborKernel((gabor_size, gabor_size), sigma, j, lambd, gamma, psi, ktype=kType)
                image_with_Gabor_list.append(cv2.filter2D(i, cv2.CV_8UC3, g_kernel))
        return image_with_Gabor_list

    def intensity_to_latensy(self, img_list=None):
        if img_list is None:
            raise Exception('no image list exist !')
        tmp = []
        for k in range(len(img_list)):
            for i in range(len(img_list[k])):
                for j in range(len(img_list[k][i])):
                    tmp.append((k, i, j, img_list[k][i][j]))
                    # k is index of pictures
                    # (i,j) shows location of each point in kth photo
                    # img_list[k][i][j] shows spike

        tmp.sort(key=lambda tup: tup[3], reverse=True)
        # print(tmp[0][3])
        for i in range(len(tmp)):
            tmp[i] = (tmp[i][0], tmp[i][1], tmp[i][2], abs(tmp[i][3] - 255))

        return tmp

