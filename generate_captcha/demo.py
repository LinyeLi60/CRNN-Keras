from PIL import Image, ImageFont, ImageDraw, ImageFilter
import random
import string
import os
import numpy as np
import cv2
import uuid


def draw_line(src):
    img = np.asarray(src)
    h, w, _ = img.shape

    for _ in range(3):
        left_x = np.random.randint(0, w)
        left_y = np.random.randint(h)
        right_x = np.random.randint(0, w)
        right_y = np.random.randint(h)
        start, end = (left_x, left_y), (right_x, right_y)
        line_color = (51, 0, 255)
        line_thickness = 1
        cv2.line(img, start, end, line_color, line_thickness)

    return Image.fromarray(img)


# 返回随机字母
def charRandom():
    letter = string.ascii_uppercase + string.ascii_lowercase + string.digits
    # stop_letter = {'I', 'O', 'Q'}  # 去掉I O Q
    stop_letter = {}  # 去掉I O Q
    letter = [i for i in letter if i not in stop_letter]
    return random.choice(letter)

# 随机颜色
def colorRandom1():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))


# 随机产生颜色2
def colorRandom2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))


width = 70
height = 30

# 创建font对象
ttf_files = [os.path.join("fonts", file) for file in os.listdir("fonts")]
# print(ttf_files)
fonts = [ImageFont.truetype(ttf_file, 26) for ttf_file in ttf_files]
for i in range(3000000):

    image = Image.new('RGB', (width, height), (255, 255, 255))
    # image.save('code.jpg', 'jpeg')



    # 创建draw对象
    draw = ImageDraw.Draw(image)


    text = ""
    # 输出文字
    for t in range(4):
        char = charRandom()
        text += char
        draw.text((width/4 * t, random.randrange(0, 1)), char, font=random.choice(fonts), fill=colorRandom2())

    
    image = draw_line(image)

    # 模糊
    # image = image.filter(ImageFilter.BLUR)
    try:
        image.save(os.path.join("samples", '%s_%s.jpg' % (text, uuid.uuid4().hex)), 'jpeg')
    except Exception as e:
        print(e)
    if i % 10 == 0:
        print("generate %d images" % i)
