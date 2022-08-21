#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     : 2018年11月14日
# @Author   : muyangren907
# @说明      :将JSON文件解析至IDM
import json
import os
from datetime import datetime
from subprocess import call

idmPath = r'C:\Program Files (x86)\Internet Download Manager\IDMan.exe'


def isChinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False

def isNumber(uchar):
    """判断一个unicode是否是数字"""
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False

def isAlphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False

def strFormat(content):
    contentStr = ''
    for i in content:
        if isChinese(i) or isNumber(i) or isAlphabet(i):
            contentStr = contentStr + i
    if contentStr != '':
        return contentStr
    else:
        return 'NULL'

def timestamp2strtime(timestamp):
    """将 13 位整数的毫秒时间戳转化成本地普通时间 (字符串格式)
    :param timestamp: 13 位整数的毫秒时间戳 (1456402864242)
    :return: 返回字符串格式 {str}'2016-02-25 20:21:04.242000'
    """
    local_str_time = datetime.fromtimestamp(timestamp / 1000.0).strftime('%Y_%m_%d')
    return local_str_time


def Json2List(Dir):  # 读取Json文件，返回作品list
    feeds = []
    fileList = os.listdir(Dir)  # 获取文件列表
    # print(fileList)

    for FileName in fileList:
        if os.path.splitext(FileName)[1] == '.json':
            with open(FileName, 'r', encoding='utf8') as fileObjr:
                jsonData = json.load(fileObjr)  # 返回列表数据，也支持字典
                feeds.extend(jsonData['feeds'])
    return feeds


if __name__ == '__main__':

    feeds = Json2List('./') #处理当前文件夹下的json文件
    feed0 = feeds[0]
    if 'kwaiId' in feed0:
        user_id = feed0['kwaiId']
    else:
        user_id = feed0['userId']
    user_name = feed0['userName']
    Path = 'D:\Project\PycharmProjects\Kwai\%s' % user_id

    for feed in feeds:
        type = feed['type']  # 直播或作品判断
        caption = strFormat(feed['caption'])[:20]  # 标题
        if type == 2:  # 直播信息
            print('正在直播\t%s' % caption)
            playUrls = feed['playInfo']['playUrls']
            for playUrl in playUrls:
                cdn = playUrl['cdn']
                url = playUrl['url']
                print('%s\n%s' % (cdn, url))
            continue

        timestamp = timestamp2strtime(feed['timestamp'])
        photoId = feed['share_info'].split('photoId=')[1]
        downUrl = []
        downTitle = []

        if 'main_mv_urls' in feed:  # 视频
            main_mv_urls = feed['main_mv_urls']
            downUrl.append(main_mv_urls[0]['url'])
            downPath = Path
            downTitle.append('[%s]%s[%s].mp4' % (timestamp, caption, photoId))

        elif 'atlas' in feed['ext_params']:  # 图集
            atlas = feed['ext_params']['atlas']
            cdnlist = atlas['cdn']  # 多个cdn
            cdn = cdnlist[0]  # 选择第1个cdn
            list = atlas['list']
            for image in list:
                downUrl.append('http://%s%s' % (cdn, image))
            downPath = '%s\[%s][%s]' % (Path, timestamp, photoId)
            for index in range(len(downUrl)):
                downTitle.append('%s%d.webp' % (caption, index))
        else:  # 图片
            downPath = Path
            downTitle.append('[%s]%s[%s].jpg' % (timestamp, caption, photoId))

        for index in range(len(downUrl)):  # 加入下载
            if not os.path.exists('%s\%s' % (downPath, downTitle[index])):
                print('正在加入 %s' % (downTitle[index]))
                call([idmPath, '/d', downUrl[index], '/p', downPath, '/f', downTitle[index], '/n', '/a'])
