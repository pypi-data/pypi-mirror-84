#!/usr/bin/python3
# coding:utf-8
import sys, requests, time, xlwt
import jieba
import re
from collections import Counter


def __regexChange(line):
    # 前缀的正则
    username_regex = re.compile(r"^\d+::")
    # 剔除所有数字
    decimal_regex = re.compile(r"[^a-zA-Z]\d+")
    # 剔除空格
    space_regex = re.compile(r"\s+")
    html_regex = re.compile('<[^>]*>')
    line = username_regex.sub(r"", line)
    line = decimal_regex.sub(r"", line)
    line = space_regex.sub(r"", line)
    line = html_regex.sub(r"", line)
    return line


class cutWord:
    def __init__(self):
        pass
