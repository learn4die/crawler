#!/usr/bin/python3
# -*- coding:utf-8 -*-
import re
import os
import urllib.request
import chardet #编码识别模块
from selenium import webdriver #使用selenium自动化测试框架运行js脚本以获取动态资源地址
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless') # 16年之后，chrome给出的解决办法，抢了PhantomJS饭碗
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')  # root用户不加这条会无法运行


# 从给出的包含商品url及商品关键词的列表获取商品图片并保存到指定的路径下
def getpic(url):
    # 获取商品url列表
    remod_url = '//item\.jd\.com/[0-9]+\.html';
    remod_itme = '[\u4e00-\u9fa5]+.*酒.*'; 
    # 提取商品url
    itmeurl_list = re.findall(remod_url,url);
    # 获取商品名列表
    itmename_list = re.findall(remod_itme,url);
    print("商品网址原始数据：",url);
    print("itmeurl_list:",len(itmeurl_list),itmeurl_list);
    print("itmename_list:",len(itmename_list),itmename_list);		
   #循环获取每个商品的图片列表
    i = 0;
    for itmeurl in itmeurl_list:
        itmeurl= 'https:' + itmeurl;
        print('part5',itmeurl);
       # 读取商品页面html码
        retryCount = 10;
        while(retryCount > 0):
            try:
                browser.get(itmeurl);
            except:
                retryCount = retryCount - 1;
                print("获取网页源码失败",itmeurl);
            else:
                break;
        html = browser.page_source; 
       # encode_type = chardet.detect(html);
       # 解码
       # html = html.decode(encode_type['encoding'],'ignore');
       # print("encode:",encode_type);
        remod_pic = '(<img data-lazyload.*?jpg)|(background-image:url.*?jpg\))';
       # 获取商品页图片网址列表
        pic_list = re.findall(remod_pic,html);
        pic_list = list(set(pic_list));# 去掉重复数据
        print('part4',pic_list);
        pic_path = '../pictures/' + re.sub("[?*<>/]","",itmename_list[i]) + '/';
        print("图片保存地址：",pic_path);
        if not os.path.isdir(pic_path):
            os.makedirs(pic_path);
        x = 1;
        
       # 获取该商品页面所有图片并保存到对应路径
        for pic_url in pic_list:
            print("图片获取中：",pic_url);
            try:
                res_url = 'http:'+ re.findall('//img\w+\.360buyimg\.com/*[\w-]+/*\w+/\w+/\w+/\w+/\w+/\w+/\w+\/*\w*.jpg',str(pic_url))[0];
            except:
                print("资源地址获取失败",res_url);
            retryCount = 10;
            while(retryCount > 0 ):
                try:
                   urllib.request.urlretrieve(res_url,pic_path + str(x) + '.jpg')
                except:
                    print('网址异常:',itmename_list[i],res_url);
                    retryCount = retryCount - 1;
                    print("剩余重试次数：",retryCount);
                else:
                    print('图片保存成功:',itmename_list[i],res_url);
                    break;
            x = x + 1;
        i = i + 1;
#根据输入的网址获取商品名称及商品列表 关键字为 白酒
def geturl_list(url):
   # 按照utf-8编码格式获取网页源码
    retryCount = 10;
    while(retryCount > 0):
        try:
            browser.get(url);
        except:
            retryCount = retryCount - 1;
            print("获取网页源码失败",url);
        else:
            html = browser.page_source;
            #匹配模式
            remod = '<a target="_blank" title="" href=".*\n.*\n.*?酒.*</em>';
            #获取包含商品名称和商品url的列表关键词为 白酒
            url_list = re.findall(remod,html);
            return url_list;
    return None;
url_list = [];
browser = webdriver.Chrome(chrome_options=chrome_options);
for i in range(1,763):
    url_main = 'http://list.jd.com/list.html?cat=12259,12260,9435&page='+str(i);
    print("part1",url_main);
    url_list = geturl_list(url_main);
    print("part2",url_list);
    for url in url_list:
        getpic(url);
