import numpy as np
import cv2
import string
import math
import os
from captcha import constant

src, _ = os.path.split(os.path.abspath(__file__))
wd = os.path.dirname(src)


class Captcha:
    def __init__(self, width, high, letter=None,
                 folder=os.path.join(wd, 'samples'), debug=False):
        if letter is None:
            letter = string.ascii_uppercase + string.ascii_lowercase + string.digits
        stop_letter = {'I', 'O', 'Q', 'a'}    # 去掉I 0 Q
        self.letter = [i for i in letter if i not in stop_letter]
        self.width, self.high = width, high
        self.debug = debug
        self.folder = folder
        if not self.debug and folder:
            if not os.path.exists(self.folder):
                os.makedirs(self.folder)

        # 倾斜图片
    def _tilt_img(self, img):
        tmp_img = img.copy()
        tmp_img.fill(255)    # 填充为白色
        tile_angle = np.random.randint(
            int(100*-math.pi/7), int(100*math.pi/8)
        ) / 100
        print(tile_angle)
        high, width, _ = img.shape
        for y in range(width):
            for x in range(high):
                new_y = int(y + (x-high/2)*math.tanh(tile_angle))
                try:
                    tmp_img[x, new_y, :] = img[x, y, :]
                except IndexError:
                    pass
        img[:, :, :] = tmp_img[:, :, :]

    def _shake_img(self, img, outer_top_left, outer_bottom_right,
                   inner_top_left, inner_bottom_right):
        (x1, y1), (x2, y2) = outer_top_left, outer_bottom_right
        (i1, j1), (i2, j2) = inner_top_left, inner_bottom_right
        delta_x = np.random.randint(x1-i1, x2-i2)
        delta_y = np.random.randint(y1-j1, y2-j2)
        area = img[y1:y2, x1:x2, :]
        area_high, area_width, _ = area.shape
        tmp_area = area.copy()
        tmp_area.fill(255)

        for index_y in range(area_high):
            for index_x in range(area_width):
                new_x, new_y = index_x + delta_x, index_y + delta_y
                if new_x < area_width and new_y < area_high:
                    tmp_area[new_y, new_x, :] = area[index_y, index_x, :]

        area[:, :, :] = tmp_area[:, :, :]

    def _distort_img(self, img):
        high, width, _ = img.shape
        tmp_img = img.copy()
        tmp_img.fill(255)

        coef_vertical = np.random.randint(3, 8)
        coef_horizontal = np.random.choice([4, 5, 6]) * math.pi / width
        scale_biase = np.random.randint(0, 360) * math.pi / 180

        def new_coordinate(x, y):
            return int(x+coef_vertical*math.sin(coef_horizontal*y+scale_biase))

        for y in range(width):
            for x in range(high):
                new_x = new_coordinate(x, y)
                try:
                    tmp_img[x, y, :] = img[new_x, y, :]
                except IndexError:
                    pass

        img[:, :, :] = tmp_img[:, :, :]

    def _draw_basic(self, img, text):
        # font_face = getattr(cv2,  np.random.choice(constant.FONTS))
        font_face = getattr(cv2, constant.FONTS[2])    # 字体
        font_scale = 0.8    # 字体大小
        font_thickness = 2    # 字体粗细
        max_width = max_high = 0

        # i是一个字符
        for i in text:
            (width, high), _ = cv2.getTextSize(
                i, font_face, font_scale, font_thickness)
            # print((width, high), _)
            max_width, max_high = max(max_width, width), max(max_high, high)

        total_width = max_width * 4    # 4个字符

        # width_delta = np.random.randint(0, self.width - total_width)    # 宽度增量

        vertical_range = self.high - max_high
        images = list()
        for index, letter in enumerate(text):
            tmp_img = img.copy()
            delta_high = np.random.randint(
                int(2*vertical_range/4), int(3*vertical_range/4)
            )
            # print(delta_high, width_delta)
            # # 每个字符的偏移量 左下角是起止点
            bottom_left_coordinate = (
                # index*max_width + width_delta,
                index*self.width//4,
                self.high - delta_high
            )

            font_color = tuple(int(np.random.choice(range(0, 156)))
                               for _ in range(3))
            cv2.putText(tmp_img, letter, bottom_left_coordinate, font_face,
                        font_scale, font_color, font_thickness)
            self._tilt_img(tmp_img)    # 不倾斜字符
            images.append(tmp_img)

        high, width, _ = img.shape
        for y in range(width):
            for x in range(high):
                r, g, b = 0, 0, 0
                # 把所有图片的像素叠加在一起
                for tmp_img in images:
                    r += tmp_img[x, y, 0]
                    g += tmp_img[x, y, 1]
                    b += tmp_img[x, y, 2]
                r, g, b = r % 256, g % 256, b % 256
                img[x, y, :] = (r, g, b)

    def _draw_line(self, img):
        for _ in range(3):
            left_x = np.random.randint(0, self.width//4)
            left_y = np.random.randint(self.high)
            right_x = np.random.randint(self.width*3//4, self.width)
            right_y = np.random.randint(self.high)
            start, end = (left_x, left_y), (right_x, right_y)
            line_color = (255, 0, 51)
            # line_thickness = np.random.randint(1, 3)
            line_thickness = 1
            cv2.line(img, start, end, line_color, line_thickness)

    def _put_noise(self, img):
        for i in range(200):
            x = np.random.randint(self.width)
            y = np.random.randint(self.high)
            dot_color = tuple(int(np.random.choice(range(0, 156)))
                              for _ in range(3))
            img[y, x, :] = dot_color

    def save_img(self, text):
        img = np.zeros((self.high, self.width, 3), np.uint8)
        img.fill(255)    # np数组

        self._draw_basic(img, text)
        self._put_noise(img)
        # self._distort_img(img)
        self._draw_line(img)

        if self.debug:
            cv2.imshow(text, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            cv2.imwrite('{}/{}.jpg'.format(self.folder, text), img)

    def batch_create_img(self, number=4):
        exits = set()
        while(len(exits)) < number:
            try:
                word = ''.join(np.random.choice(self.letter, constant.LETTER_NUM))
                # print(word)    # 打印出生成的验证码内容
                if word not in exits:
                    exits.add(word)
                    self.save_img(word)
                    if not self.debug:
                        if len(exits) % 10 == 0:
                            print('{} generated.'.format(len(exits)))
            except Exception as e:
                print(e)

        if not self.debug:
            print('{} captchas saved into {}.'.format(len(exits), self.folder))


if __name__ == '__main__':
    c = Captcha(150, 40, debug=True)
    c.batch_create_img(10)
