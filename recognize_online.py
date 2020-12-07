#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
使用自建的接口识别来自网络的验证码
需要配置参数：
    remote_url = "https://www.xxxxxxx.com/getImg"  验证码链接地址
    rec_times = 1  识别的次数
"""
import datetime
import requests
from io import BytesIO
import time
import json
import os


def recognize_captcha(remote_url, rec_times, save_path, image_suffix):
    image_file_name = 'captcha.{}'.format(image_suffix)

    headers = {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
    }

    for index in range(rec_times):
        # 请求
        while True:
            try:
                response = requests.request("GET", remote_url, headers=headers, timeout=6)
                if response.text:
                    break
                else:
                    print("retry, response.text is empty")
            except Exception as ee:
                print(ee)

        # 识别
        s = time.time()
        url = "http://127.0.0.1:6006/b"
        files = {'image_file': (image_file_name, BytesIO(response.content), 'application')}
        r = requests.post(url=url, files=files)
        e = time.time()

        # 识别结果
        print("接口响应: {}".format(r.text))
        predict_text = json.loads(r.text)["value"]
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("【{}】 index:{} 耗时：{}ms 预测结果：{}".format(now_time, index, int((e-s)*1000), predict_text))

        # 保存文件
        img_name = "{}_{}.{}".format(predict_text, str(time.time()).replace(".", ""), image_suffix)
        path = os.path.join(save_path, img_name)
        with open(path, "wb") as f:
            f.write(response.content)
        print("============== end ==============")


def main():
    with open("conf/sample_config.json", "r") as f:
        sample_conf = json.load(f)

    # 配置相关参数
    remote_url = sample_conf["remote_url"]  # 网络验证码地址
    save_path = sample_conf["online_image_dir"]  # 下载图片保存的地址
    local_path = sample_conf["local_image_dir"]  # 保存的地址
    api_path = sample_conf["api_image_dir"]  # api的地址
    image_suffix = sample_conf["image_suffix"]  # 文件后缀
    rec_times = 10

    if not os.path.exists(save_path):
        print("【警告】找不到目录{}，即将创建".format(save_path))
        os.makedirs(save_path)
    if not os.path.exists(local_path):
        print("【警告】找不到目录{}，即将创建".format(local_path))
        os.makedirs(local_path)
    if not os.path.exists(api_path):
        print("【警告】找不到目录{}，即将创建".format(api_path))
        os.makedirs(api_path)

    recognize_captcha(remote_url, rec_times, save_path, image_suffix)

if __name__ == '__main__':
    main()
    

