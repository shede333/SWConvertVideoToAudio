
# Python批量转换 视频 为 音频MP3（即提取音频文件）

输入文件格式：**ffmpeg**支持的视频文件

输出格式格式：mp3文件

## 使用方法：

注意：使用前需要先安装 **ffmpeg** 才行（Python最终调用的是 ffmpeg 命令）

Mac上安装 **ffmpeg** 命令：

```
brew install ffmpeg
```

使用说明：

```
python convert.py -h

输出：

usage: Python批量转换 视频 为 音频MP3（即提取音频文件） [-h] [--output-dir OUTPUT_DIR]
                                      [--traverse]
                                      file_path

positional arguments:
  file_path             输入文件、目录路径，如果为目录，则遍历目录下的文件

optional arguments:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        (可选)输出目录路径，如果不传，则使用输入文件目录
  --traverse            (可选)src-path为目录是，是否遍历子目录，默认False

```

使用示例：

```
python convert.py hello.rmvb
python convert.py hello.rmvb hello.mp3
python convert.py /User/video_dir  # videos根目录下有视频文件（忽略次级目录）
python convert.py /User/video_dir /User/videos_to_mp3_dir  # 产出的mp3文件放在"/User/videos-to-mp3"目录下
python convert.py /User/video_dir /User/videos_to_mp3_dir --traverse  # videos目录下有视频文件（包含次级目录）
```



## ffmpeg命令：
  
```
ffmpeg -i source_video.avi -vn -ar 44100 -ac 2 -ab 192 -f mp3 dst_audio.mp3
```

说明： 

* 源视频：source_video.avi
* 音频位率：192kb/s
* 输出格式：mp3
* 生成的声音：dst_audio.mp3

参数说明：

* -i: 输入文件
* -vn: 取消视频（不处理视频）
* -ar: 设置音频采样率 (单位：Hz)
* -ac: 设置声道数，1就是单声道，2就是立体声，转换单声道的TVrip可以用1（节省一半容量），高品质的DVDrip就可以用2
* -ab: 设置比特率(单位：bit/s，也许老版是kb/s)前面-ac设为立体声时要以一半比特率来设置，比如192kbps的就设成96，转换 默认比特率都较小，要听到较高品质声音的话建议设到160kbps（80）以上。
* -f: 指定格式(音频或视频格式)


## 待改进的功能：

1. 转换时，使用**多进程**；


## 参考:

> <https://www.cnblogs.com/wenrisheng/p/6139845.html>  
> <https://baike.baidu.com/item/ffmpeg/2665727?fr=aladdin#7> 