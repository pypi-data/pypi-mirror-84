#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pip install PyExecJS
# 用python执行JavaScript
import execjs


def getcompile(filePath):
    f = open(filePath, 'r')
    line = f.readline()
    jsstr = ''
    while line:
        jsstr = jsstr + line
        line = f.readline()
    return execjs.compile(jsstr)


def runFunction(filePath, funName, *args):
    ctx = getcompile(filePath)
    arges_len = len(args)
    if arges_len == 1:
        return ctx.call(funName, args[0])
    elif arges_len == 2:
        return ctx.call(funName, args[0], args[1])
    elif arges_len == 3:
        return ctx.call(funName, args[0], args[1], args[2])
    else:
        return None
