#生成验证码
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

#生成随机字母
def rndChar():
    return chr(random.randint(65,90))
print(chr(65))

#随机生成数字和字母
def getrand(num, many):     #num 位数   many 个数
    for x in range(many):  #验证码一共的位数
        s = ""
        for y in range(num):
            n = random.randint(1, 2)   # n=1 或者 n=2, n=1生成数字 n=2 生成字母
            if n == 1:
                numb = random.randint(0, 9)
                s += str(numb)
            else:
                nn = random.randint(1, 2)
                cc = random.randint(1, 26)
                if nn == 1:
                    numb = chr(64+cc)
                    s += numb
                else:
                    numb = chr(96+cc)
                    s += numb
        return s

#随机的颜色
def rndColor():
    return (random.randint(32,127),random.randint(32,127),random.randint(32,127))
def rndColor1():
    return (random.randint(64,255),random.randint(64,255),random.randint(64,255))

width = 60 * 4   # 生成四个随机字母
height = 60

image = Image.new('RGB', (width, height), (255, 255, 255))





#创建Font对象: 选择文字字体和大小
font = ImageFont.truetype("Arial.ttf", 36)
#创建Draw对象:
draw = ImageDraw.Draw(image)

#填充每个像素
for x in range(width):
    for y in range(height):
        draw.point((x,y), fill=rndColor1())


#输出文字:
for t in range(4):
    draw.text((60 * t + 10, 10), getrand(1,4), font=font, fill=rndColor())
image.show()
image.save('static/vcode/vcode.jpg', 'jpeg')



