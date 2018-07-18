#!/usr/bin/env python2.7
# _*_ coding:UTF-8 _*_
"""
__author__ = 'wangshaowei'
"""

import argparse
import os

import subprocess
from datetime import datetime


def ffmpeg(src_path, dst_path):
    """
    调用ffmpeg命令，执行转换过程
    :param src_path: 输入视频文件路径
    :param dst_path: 输出文件路径
    :return: bool值，转换结果成功or失败
    """
    command = "ffmpeg -i '{}' -vn -ar 44100 -ac 2 -ab 192 -f mp3 '{}'".format(src_path, dst_path)
    try:
        subprocess.check_call(command, shell=True)
        is_success = True
    except subprocess.CalledProcessError as e:
        print "error code: {}! shell command: {}".format(e.returncode, e.cmd)
        is_success = False
    return is_success


def convert_dir(dir_path, output_dir, is_traverse=False):
    """
    批量转换视频文件
    :param dir_path: 输入目录路径（内含视频文件）
    :param output_dir: 输出目录
    :param is_traverse: 是否遍历子目录，默认False
    :return: 元组：转换成功数目，失败数目
    """
    success_num = 0  # 转换成功的文件数
    fail_num = 0  # 转换失败的文件数
    file_list = []
    dir_list = []
    for file_name in os.listdir(dir_path):
        if file_name.startswith("."):
            continue
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            file_list.append(file_path)
        elif os.path.isdir(file_path):
            dir_list.append(file_path)
        else:
            print "暂时不支持该路径：{}".format(file_path)

    for file_path in sorted(file_list):
        print "file_path:", file_path
        result = convert_file(file_path, output_dir)
        if result:
            success_num += 1
        else:
            fail_num += 1

    for dir_path in sorted(dir_list):
        print "dir_path:", dir_path
        file_name = os.path.basename(dir_path)
        result = convert_dir(dir_path, os.path.join(output_dir, file_name), is_traverse)
        success_num += result[0]
        fail_num += result[1]

    return success_num, fail_num


def convert_file(file_path, output_dir):
    """
    转换单个视频文件
    :param file_path: 输入视频文件路径
    :param output_dir: 输出文件目录路径
    :return: bool值，转换结果成功or失败
    """
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    video_file_name = os.path.basename(file_path)
    name_body = video_file_name.rsplit(".", 1)[0]
    audio_name = name_body + ".mp3"
    dst_path = os.path.join(output_dir, audio_name)
    return ffmpeg(file_path, dst_path)


def parse_arg():
    """解析命令行的输入的参数"""
    parser = argparse.ArgumentParser(u"Python批量转换 视频 为 音频MP3（即提取音频文件）")
    parser.add_argument(u"file_path", help=u"输入文件、目录路径，如果为目录，则遍历目录下的文件")
    parser.add_argument(u"--output-dir", help=u"(可选)输出目录路径，如果不传，则使用输入文件目录")
    parser.add_argument(u"--traverse", action=u'store_true',
                        help=u"(可选)src-path为目录是，是否遍历子目录，默认False")

    return parser.parse_args()


def main():
    """主入口"""
    try:
        # 检测ffmpeg是否已安装
        result = subprocess.check_output("ffmpeg -version", shell=True)
        print "ffmpeg:\n", result
    except subprocess.CalledProcessError:
        print "ffmpeg未安装，请先安装:ffmpeg"
        return

    # 解析输入参数
    command_param = parse_arg()
    file_path = command_param.file_path
    output_dir = command_param.output_dir

    start_time = datetime.now()
    success_num = 0  # 转换成功的文件数
    fail_num = 0  # 转换失败的文件数
    if os.path.isfile(file_path):  # 文件
        if not output_dir:
            output_dir = os.path.dirname(file_path)  # 与输入文件同级目录
        result = convert_file(file_path, output_dir)
        if result:
            success_num += 1
        else:
            fail_num += 1
    elif os.path.isdir(file_path):  # 目录
        if not output_dir:
            output_dir = file_path  # 使用输入目录
        success_num, fail_num = convert_dir(file_path, output_dir,
                                            is_traverse=command_param.traverse)
    else:
        assert False, u"file_path 不存在：'{}'".format(file)

    end_time = datetime.now()
    cost_seconds = (end_time - start_time).seconds
    print u"转换的成功文件数：{}个".format(success_num)
    print u"转换的失败文件数：{}个".format(fail_num)
    print u"总耗时:{}秒".format(cost_seconds)


if __name__ == '__main__':
    main()
