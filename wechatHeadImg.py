# coding:utf-8
import itchat
import os
import re
import math
import random
import PIL.Image as Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# 获取头像
def headImg():
    itchat.login()
    friends = itchat.get_friends(update=True)
    # 遍历好友数据
    for count, f in enumerate(friends):
        # 根据userName获取头像
        img = itchat.get_head_img(userName=f["UserName"])
        # 根据备注保存头像文件
        imgFile = open("img/" + f["RemarkName"] + ".jpg", "wb")
        imgFile.write(img)
        imgFile.close()


# 头像拼接图
def createImg():
    x = 0
    y = 0
    imgs = os.listdir("img")
    # 随机打乱头像
    # random.shuffle(imgs)
    # 创建图片，用于拼接小图
    newImg = Image.new('RGBA', (640, 640))
    # math.sqrt()开平方根计算小图宽高，
    width = int(math.sqrt(640 * 640 / len(imgs)))
    # 每行图片数
    numLine = int(640 / width)

    for i in imgs:
        try:
            img = Image.open("img/" + i)
        # 缩小图片
            img = img.resize((width, width), Image.ANTIALIAS)
        # 拼接图片，一行排满，换行拼接
            newImg.paste(img, (x * width, y * width))
            x += 1
            if x >= numLine:
                x = 0
                y += 1
        except IOError:
            print("img/ %s can not open"%(i))
    newImg.save("weChatFriend.png")


# 获取签名
def getSignature():
    itchat.login()
    friends = itchat.get_friends(update=True)
    file = open('sign.txt', 'a', encoding='utf-8')
    for f in friends:
        signature = f["Signature"].strip().replace("emoji", "").replace("span", "").replace("class", "")
        rec = re.compile("1f\d+\w*|[<>/=]")
        signature = rec.sub("", signature)
        file.write(signature + "\n")


# 生成词云图
def create_word_cloud(filename):
    # 读取文件内容
    text = open("{}.txt".format(filename), encoding='utf-8').read()

    # 注释部分采用结巴分词
    # wordlist = jieba.cut(text, cut_all=True)
    # wl = " ".join(wordlist)

    # 设置词云
    wc = WordCloud(
        # 设置背景颜色
        background_color="white",
        # 设置最大显示的词云数
        max_words=2000,
        # 这种字体都在电脑字体中，window在C:\Windows\Fonts\下，mac下可选/System/Library/Fonts/PingFang.ttc 字体
        font_path='C:\\Windows\\Fonts\\simfang.ttf',
        height=500,
        width=500,
        # 设置字体最大值
        max_font_size=60,
        # 设置有多少种随机生成状态，即有多少种配色方案
        random_state=30,
    )

    myword = wc.generate(text)  # 生成词云 如果用结巴分词的话，使用wl 取代 text， 生成词云图
    # 展示词云图
    plt.imshow(myword)
    plt.axis("off")
    plt.show()
    wc.to_file('signature.png')  # 把词云保存下

# 微信好友头像拼接
headImg()
createImg()

# 个性签名统计
# getSignature()
# create_word_cloud("sign")