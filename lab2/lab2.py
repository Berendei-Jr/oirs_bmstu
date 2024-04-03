# Фигура = (вариант mod 4) + 1 = 2 mod 4 + 1 = 3 (пятиугольник)
# Цвет =  (день рождения mod 3) + 1 = 27 mod 3 + 1 = 1 (жёлтый)

import cv2
import numpy as np

def show_image(name, img):
        cv2.imshow(name, img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
        img = cv2.imread('generated_image.png')
        show_image('initial image', img)

        yellow_lower = np.array([0, 250, 220])
        yellow_higher = np.array([0, 255, 255])
        mask = cv2.inRange(img, yellow_lower, yellow_higher)
        show_image('mask', mask)

        selection = cv2.bitwise_and(img, img, mask=mask)
        show_image('selection', selection)

        gray = cv2.cvtColor(selection, cv2.COLOR_BGR2GRAY)
        show_image('gray', gray)

        canny = cv2.Canny(gray, 10, 250)
        show_image('canny', canny)

        contours = cv2.findContours(canny.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
        for cont in contours:
                #вычисление периметра и определение количества углов
                sm = cv2.arcLength(cont, True)
                apd = cv2.approxPolyDP(cont, 0.02*sm, True)

                # выделение контуров
                if len(apd) == 5:
                        cv2.drawContours(img, [cont], -1, (255, 255, 255), 10)

        show_image('final', img)

