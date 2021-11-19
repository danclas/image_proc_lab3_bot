import cv2
import matplotlib.pyplot as plt
import numpy as np


def read_img(user_id):
    return cv2.imread('photos/photo_{}.jpg'.format(user_id))


def save_img(img, user_id):
    cv2.imwrite('photos/result_{}.jpg'.format(user_id), img)


def get_grayscale_img(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def get_blur_img(img):
    return cv2.medianBlur(img, 15)


def get_add_bright_img(img):
    increase = 30

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    v = np.where(v <= 255 - increase, v + increase, 255)
    hsv[:, :, 2] = v

    result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return result


def get_sub_bright_img(img):
    increase = 30

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2]
    v = np.where(v > increase, v - increase, 0)
    hsv[:, :, 2] = v

    result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return result


if __name__ == '__main__':

    def get_black_white_img(img):
        (thresh, im_bw) = cv2.threshold(get_grayscale_img(img), 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return im_bw

    img = cv2.imread('wallhaven-28ovmy.jpg')

    fig, axs = plt.subplots()
    axs.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    fig, axs = plt.subplots()
    axs.imshow(get_grayscale_img(img), cmap='gray')

    fig, axs = plt.subplots()
    axs.imshow(get_black_white_img(img), cmap='gray')

    fig, axs = plt.subplots()
    axs.imshow(cv2.cvtColor(get_blur_img(img), cv2.COLOR_BGR2RGB))

    fig, axs = plt.subplots()
    axs.imshow(cv2.cvtColor(get_sub_bright_img(img), cv2.COLOR_BGR2RGB))

    plt.show()

    cv2.imwrite('saveim.jpg', get_sub_bright_img(img))
