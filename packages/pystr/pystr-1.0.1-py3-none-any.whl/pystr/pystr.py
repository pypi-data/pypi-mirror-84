#!/usr/bin/env python
# -*- coding: utf-8 -*-
#@作者：5478

"""
这是为了减少pyautogui.typewrite无法输入汉字的，通过复制粘贴实现输入汉字
"""



import time, pyautogui, pyperclip


def typewrite(str, interval=0.11):
    interval = interval - 0.11
    for i in str:
        pyperclip.copy(i)  # 复制i
        time.sleep(interval)  # 暂停输入的interval - 0.11秒
        pyautogui.hotkey('ctrl', 'v')  # 粘贴
