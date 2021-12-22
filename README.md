# 1.项目介绍
小白也能快速上手的基于PaddleHub实现一键动漫风格化

# 2.安装第三方库
```
# 参考paddlepaddle官网安装
pip install paddlepaddle-gpu==2.2.1.post112 -f https://www.paddlepaddle.org.cn/whl/windows/mkl/avx/stable.html
pip install --upgrade paddlehub -i https://mirror.baidu.com/pypi/simple
pip install opencv-python tqdm moviepy
```

# 3.项目使用
- 图片文件夹的Python脚本

```
python style_transfer_demo.py --input_path images --output_path output --model_index 0 --use_gpu True
```


- 图片文件的Python脚本

```
python style_transfer_demo.py --input_path images/test.jpg --output_path output --model_index 0 --use_gpu True
```


- 视频文件的Python脚本

```
python style_transfer_demo.py --input_path video/test.mp4 --output_path output --model_index 0 --use_gpu True
```


- 对应参数介绍：

```
--input_path： 输入文件的路径,默认为test.jpg,其中可以是图片文件夹，图片文件，也可以是视频
            图片：['bmp', 'jpg', 'jpeg', 'png', 'tif', 'tiff', 'dng', 'webp', 'mpo'] 
            视频：['mp4','mov', 'avi', 'flv', 'mpg', 'mpeg', 'm4v', 'wmv', 'mkv']

--output_path： 输出文件的路径,默认输出文件的路径为output

--model_index:动漫风格化模型的序号，默认为0，也就是'animegan_v2_hayao_99'，模型列表：['animegan_v2_hayao_99','animegan_v2_shinkai_53','animegan_v2_hayao_64','animegan_v2_shinkai_33',                  'animegan_v1_hayao_60','animegan_v2_paprika_74','animegan_v2_paprika_97','animegan_v2_paprika_98','animegan_v2_paprika_54']
        
--use_gpu:  指的是 要不要开启GPU,默认为True，默认开启GPU

```




# 4.参考链接
* [PaddleHub官网](https://www.paddlepaddle.org.cn/hub)
* [AnimeGANv2](https://github.com/TachibanaYoshino/AnimeGANv2)
* [AnimeGAN动漫化模型一键应用（含动漫化小程序体验）](https://aistudio.baidu.com/aistudio/projectdetail/1308514)
* [PaddleHub一键视频动漫化](https://aistudio.baidu.com/aistudio/projectdetail/1432755)
* [AI创造营——AnimeGAN视频动漫化一键生成](https://aistudio.baidu.com/aistudio/projectdetail/1640682)


# 5.个人介绍
> 中南大学 机电工程学院 机械工程专业 2019级 研究生 雷钢

> 百度飞桨官方帮帮团成员

> Github地址：https://github.com/leigangblog

> Gitee地址：https://gitee.com/leigangblog

> B站：https://space.bilibili.com/53420969

来AI Studio互关吧，等你哦~ https://aistudio.baidu.com/aistudio/personalcenter/thirdview/118783
欢迎大家fork喜欢评论三连，感兴趣的朋友也可互相关注一下啊~

