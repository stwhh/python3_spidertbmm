# -*-coding:utf-8-*-
import requests
from urllib import request, parse
import json
import re
import ssl
import os


class spider_tbmm:
    def __init__(self):
        self.url = 'https://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'

    # 先打开首页，获取基本信息【分页是post，待实现分页】
    def get_basicinfo_list(self):
        url = self.url
        req = request.Request(url)  # 构造request
        response = request.urlopen(req).read().decode('gbk', 'ignore')
        basic_info = json.loads(response)['data']['searchDOList']

        # for i in basic_info:
        #     print(i['userId'])
        return basic_info

    # 获取每个用户所有相册id
    def get_album_list(self, userid):
        album_url = 'https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20={}'.format(userid)
        req = request.Request(album_url)
        response = request.urlopen(req).read().decode('gbk')

        # print(response)
        # 特殊字符记得转义
        pattern = 'a class="mm\-first" href="//mm\.taobao\.com/self/album_photo\.htm\?user_id={0}&album_id=(.*?)&album_flag=0'.format(userid)
        albums = re.findall(pattern, response)
        # for i in albums[::2]:
        #     print(i)
        return albums[::2] # 这里返回的相册信息是重复的所以去重

    # 获取所有每个照片id，picid
    def get_album_detail_list(self, userid, albumid):
        album_detail_url = 'https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id={}&album_id={}'.format(
            userid, albumid)
        response = request.urlopen(album_detail_url).read().decode('gbk', 'ignore')

        # print(response)
        # pattern = r'href="//mm.taobao.com/self/album_photo.htm?user_id=(.*)&album_id=(.*)"'
        # print(re.findall(pattern, response))
        # for i in json.loads(response)['picList']:
        #     print(i['userId'] + '-' + i['albumId'] + '-' + i['picId'])

        detailurl = []
        for i in json.loads(response)['picList']:
            # print(i['picId'])
            detailurl.append(i['picId'])
        # print(detailurl)
        return detailurl
        # return json.loads(response)['picList']

    # 获取每张照片的真实url
    def get_alum_bigpic_url(self, userid, picid):
        picurl = 'https://mm.taobao.com/album/json/get_photo_data.htm?_input_charset=utf-8'
        data = {'album_user_id': userid,
                'pic_id': picid,
                'album_id': '',
                '_tb_token_': '3373b115eccce',
                'is_edit': 'True'
                }
        header = {'User-Agent':
                      'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25',
                  'Host': 'mm.taobao.com',
                  'X-Requested-With': 'XMLHttpRequest',
                  'Origin': 'https://mm.taobao.com',
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'  # 经过fiddler测试这个必须加,其他几个非必须
                  }

        ssl._create_default_https_context = ssl._create_unverified_context  # 取消ssl验证
        req = request.Request(picurl, parse.urlencode(data).encode('gbk'), headers=header)
        response = request.urlopen(req).read().decode('gbk', 'ignore')
        # print(response)
        # print(json.loads(response)['photo_url'][2:])

        realurl='http:' + json.loads(response)['photo_url']
        print(realurl)
        return realurl

    # 启动爬虫
    def spider_start(self):
        print('爬虫已启动')
        cla = spider_tbmm()
        for i in cla.get_basicinfo_list():
            index = 0
            # 以mm姓名为依据，创建文件夹
            rootpath = "D:\\淘宝mm\\{}\\".format(i['realName'])
            cla.mkdir(rootpath)
            # 创建基本信息
            print('发现一个mm,姓名:{},身高:{},体重:{}KG'.format(i['realName'], i['height'], i['weight']))
            mminfo = '姓名：{name}\n城市：{city}\n身高：{height}\n体重：{weight}KG'.format(name=i['realName'], city=i['city'],
                                                                               height=i['height'], weight=i['weight'])
            cla.save_mmbasic_info(rootpath + '{}简介.txt'.format(i['realName']), mminfo)
            # 找到当前mm的所有相册
            for j in cla.get_album_list(i['userId']):
                # 找到相册里面的每张图片的真实地址
                for m in cla.get_album_detail_list(i['userId'], j):
                    pic_real_url = cla.get_alum_bigpic_url(i['userId'], m)  # 获取到了图片的真实地址开始保存
                    print('找到了{}的一张照片，正在保存哦'.format(i['realName']))
                    picpath = (rootpath + '{}{}.jpg').format(i['realName'], index)
                    cla.save_img(pic_real_url, picpath)
                    index += 1

    # 创建目录
    def mkdir(self, dirpath):
        '''

        :param dirpath: 目录路径
        :return:
        '''
        path = dirpath.strip()
        if (os.path.exists(path)):
            # print('文件夹{}已存在'.format(dirpath))
            pass
        else:
            os.makedirs(path)

    # 保存个人简介
    def save_mmbasic_info(self, txtpath, mminfo):
        '''

        :param txtpath: 要保存的简介路径
        :param mminfo: mm描述信息
        :return:
        '''
        print(txtpath)
        with open(txtpath, 'w') as f:  # txtpath不支持多级目录
            f.write(mminfo)

    # 保存图片
    def save_img(self, picurl, filepath):
        p = request.urlopen(picurl)
        data = p.read()
        with open(filepath, 'wb') as f:
            f.write(data)


spider_tbmm().get_album_list(176817195)
# spider_tbmm().get_album_detail_list(176817195,10000962815)
# spider_tbmm().get_alum_bigpic_url(176817195, 10003453420)
# spider_tbmm().get_basicinfo_list()
# spider_tbmm().spider_start()
