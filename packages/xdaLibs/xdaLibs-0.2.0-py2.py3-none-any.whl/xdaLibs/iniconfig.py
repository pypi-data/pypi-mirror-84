#!/usr/bin/env python
# -*- coding: utf-8 -*-

from configparser import SectionProxy
import os
import configparser


class IniConfig(object):
    """
    ini配置文件
    """

    def __init__(self, file_name, encoding='utf-8'):
        self.file = file_name
        self.config = configparser.ConfigParser()
        self.config.read(file_name, encoding)

    def set(self, section, option, value=''):
        """
        设置值（自动保存）
        """
        if not section in self.config:
            self.config.add_section(section)
        self.config.set(section, option, value)
        with open(self.file, 'w', encoding='utf-8') as f:
            self.config.write(f)

    def get(self, section, option, default=''):
        """
        获取值
        """
        self.checkOption(section, option)
        value = self.config.get(section, option, fallback=default)
        return value

    def listOptions(self, section):
        """
        返回指定 section 的全部 option 值的数组形式
        """
        if self.checkSection(section):
            return [self.config[section][x] for x in self.config.options(section)]

    def checkSection(self, section):
        """
        检查指定的 section 是否存在
        """
        if section in self.config:
            return True
        else:
            print('Nothing named ' + section + ' in file: ' + self.file)
            return False

    def checkOption(self, section, option):
        """
        检查指定的 section 中的 option 是否存在
        """
        if self.checkSection(section):
            if option in self.config[section]:
                return True
            else:
                print('Error: There\'s no option named ' + option +
                      ' for ' + section + ' in file: ' + self.file)
        return False
