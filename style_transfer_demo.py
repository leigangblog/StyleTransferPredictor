#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:lei
@file:style_transfer_demo.py
@time:2021/12/21
@邮箱：leigang431@163.com
"""
import argparse
import cv2
import os
import paddlehub as hub
from tqdm import tqdm
import numpy as np
from moviepy.editor import VideoFileClip
import time
import warnings

warnings.filterwarnings('ignore')
# 设置GPU环境变量
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


# 定义 动漫风格化迁移类
class StyleTransferPredictor(object):
    def __init__(self,
                 output_path='output',
                 model_index=0,
                 use_gpu=True):
        self.model_list = ['animegan_v2_hayao_99', 'animegan_v2_shinkai_53', 'animegan_v2_hayao_64',
                           'animegan_v2_shinkai_33',
                           'animegan_v1_hayao_60', 'animegan_v2_paprika_74', 'animegan_v2_paprika_97',
                           'animegan_v2_paprika_98'
            , 'animegan_v2_paprika_54']
        self.length = len(self.model_list)
        self.output_path = output_path
        self.model_name = self.model_list[model_index % self.length]
        self.model = hub.Module(name=self.model_name, use_gpu=use_gpu)
        # 文件后缀检查
        self.IMG_FORMATS = ['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo']  # 接受的图片后缀
        self.VID_FORMATS = ['mov', 'avi', 'flv', 'mp4', 'mpg', 'mpeg', 'm4v', 'wmv', 'mkv']  # 接受的视频后缀

    # 检查文件夹
    def check_folder(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        return

    # 处理每一帧图片
    def process_frame(self, frame):
        result = self.model.style_transfer(images=[frame])
        frame = result[0].astype(np.uint8)
        return frame

    #  图片文件夹 动漫风格化
    def generate_image_path(self, input_path):
        for file in os.listdir(input_path):
            image_path = os.path.join(input_path, file)
            file_suffix = file.split('.')[-1].lower()
            if file_suffix in self.IMG_FORMATS:
                self.generate_image(image_path)

    #  单张图片 动漫风格化
    def generate_image(self, input_path):
        file_head = input_path.split("/")[-1]
        file_head = "out_" + file_head.split("\\")[-1]
        image = cv2.imread(input_path)
        frame = self.process_frame(image)
        frame = cv2.resize(frame, (int(image.shape[1]), int(image.shape[0])))
        # 保存结果
        self.check_folder(self.output_path)
        time_str = time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime(time.time()))
        save_path = os.path.join(self.output_path, time_str + self.model_name + "_" + file_head)
        cv2.imwrite(save_path, frame)
        # 结果提示
        print("照片已保存：", save_path)
    # 视频 动漫风格化
    def generate_video(self, input_path):
        # 提示
        print("视频开始处理", input_path)
        # 得到文件头
        file_head = "out_" + input_path.split("/")[-1]
        file_name = file_head.split('.')[0]
        # 读取视频
        cap = cv2.VideoCapture(input_path)
        # 获取视频总帧数
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        # 提示
        print("视频总帧数为", frame_count)
        # 得到视频的宽和高
        frame_size = (cap.get(cv2.CAP_PROP_FRAME_WIDTH), cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        # 定义codec 编码方式以及 创建 VideoWriter 对象
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # 得到帧率
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        # 检查输出文件夹
        self.check_folder(self.output_path)
        # 定义 时间字符串
        time_str = time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime(time.time()))
        # 定义无音频的输出路径
        output_path = os.path.join(self.output_path,
                                   "no_audio_" + time_str + self.model_name + "_" + file_name + ".mp4")
        # 定义最后音频的输出路径
        save_path = os.path.join(self.output_path, time_str + self.model_name + "_" + file_name + ".mp4")
        # 保存视频
        out = cv2.VideoWriter(output_path, fourcc, fps, (int(frame_size[0]), int(frame_size[1])))
        # 定义总进度条的数量
        total = frame_count - 1
        with tqdm(total=total) as pbar:
            # 设置进度条描述
            pbar.set_description(f"Making: {save_path}")
            try:
                while (cap.isOpened()):
                    success, frame = cap.read()
                    if not success:
                        break
                    try:
                        # 处理每帧图像
                        frame = self.process_frame(frame)
                        # 缩放到指定大小
                        frame = cv2.resize(frame, (int(frame_size[0]), int(frame_size[1])))
                    except:
                        print("error")
                        pass
                    if success:
                        out.write(frame)
                        pbar.update(1)
            except:
                print("中途中断")
                pass
        # 释放保存视频文件
        out.release()
        # 关闭摄像头
        cap.release()
        # 关闭图像窗口
        cv2.destroyAllWindows()
        # ***************音视频融合***************
        # ***************提取原视频的音频部分***************
        try:
            video_clip = VideoFileClip(input_path)
            audio = video_clip.audio
            # 提取无音频的视频片段
            final_clip = VideoFileClip(output_path)
            # ***************设置音频***************
            # 原视频有音频时
            if audio is not None:
                final_video = final_clip.set_audio(audio)
                # 最终结果
                final_video.write_videofile(
                    save_path,
                    fps=fps,
                    codec='libx264',
                    preset='slower',
                    # ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow, placebo.
                    audio_codec="libmp3lame",
                    threads=4)
                # 结果提示
                print("视频已保存：", save_path)
            else:
                # 原视频没有音频时 结果提示
                print("视频已保存：", output_path)
        except:
            print("视频已保存：", output_path)


    def run(self, input_path):
        if not os.path.exists(input_path):
            print("请检查文件是否存在")
            return
        if os.path.isdir(input_path):
            # 判断为文件夹
            self.generate_image_path(input_path)
        elif os.path.isfile(input_path):
            # 判断为文件
            image_mode = False
            video_mode = False
            file_suffix = input_path.split('.')[-1].lower()
            # 判断是否为图片文件
            if file_suffix in self.IMG_FORMATS:
                image_mode = True
            # 判断是否为视频文件
            if file_suffix in self.VID_FORMATS:
                video_mode = True
            if image_mode and not video_mode:
                self.generate_image(input_path)
            elif not image_mode and video_mode:
                self.generate_video(input_path)
            else:
                print("请检查文件格式!")
        else:
            print("请检查input_path设置!")


def main():
    desc = "PaddleHub implementation of AnimeGANv2"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("--input_path", type=str, default='test.jpg', help="path to source image or video")
    parser.add_argument("--output_path", type=str, default='output', help="path to output image dir")
    parser.add_argument("--model_index", type=int, default=0, help="select style_transfer model [0-8]")
    parser.add_argument("--use_gpu", type=bool, default=True, help="use_gpu")
    args = parser.parse_args()
    # 创建 动漫风格迁移类
    predictor = StyleTransferPredictor(args.output_path, args.model_index, args.use_gpu)
    # 动漫风格迁移处理
    predictor.run(args.input_path)


if __name__ == "__main__":
    main()
