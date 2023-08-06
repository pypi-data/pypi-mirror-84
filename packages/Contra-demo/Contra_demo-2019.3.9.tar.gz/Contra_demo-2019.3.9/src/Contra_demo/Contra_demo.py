import numpy as np
import cv2 as cv
def Contra_harmonicMeanAlogrithm(image, q):
    '''

    :param image: 噪声图
    :param q: q 值
    :return: 去噪后的图
    '''
    new_image = np.zeros(image.shape)
    image = cv.copyMakeBorder(image, 1, 1, 1, 1, cv.BORDER_DEFAULT)#填充图，充分处理噪声图每一个像素
    for i in range(1, image.shape[0] - 1):
        for j in range(1, image.shape[1] - 1):
            new_image[i - 1, j - 1] = Contra_harmonicMeanOperator(image[i - 1:i + 2, j - 1:j + 2], q)#定义窗口大小
    new_image = (new_image - np.min(image)) * (255 / np.max(image))#归一化
    return new_image.astype(np.uint8)
