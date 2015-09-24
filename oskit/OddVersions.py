#!/usr/bin/env python
# -*- coding: utf-8 -*-
# title       :
# description :
# author      :'Aaron'
# mtine       :'2015/9/24'
# version     :
# usage       :
# notes       :

# Built-in modules
import os
import json
import getpass
import time
import logging

# Third-party modules

# Studio modules

# Local modules
from get_md5 import get_md5
from copy_file import copy_file
from remove_file import remove_file


logging.basicConfig(filename=os.path.join(os.environ["TMP"], 'OddVersion_log.txt'),
                    level=logging.WARN, filemode='a', format='%(asctime)s - %(levelname)s: %(message)s')


class HiveAsset(object):
    """
        每一个资产都会包含一个文件和这个文件的历史版本文件夹。
        每一个资产文件都有一个对应的json文件，里面记录了版本号（新的为None），上传者，上传信息，上传时间，文件md5值等信息。json文件和资产文件同时放在一个文件夹下。
    """

    def __init__(self, path):
        # 将给定的位置识别为目标位置
        self.path = path
        self.dir, self.full_name = os.path.split(path)
        self.name, self.ext = os.path.splitext(self.full_name)
        self.hist_dir = r"{base_dir}/{file_name}_versions".format(
            base_dir=self.dir, file_name=self.name)

    def add_to_version(self):
        # 将文件放入版本库中
        src_file_dict = self.get_version_info()
        src_file_hash = src_file_dict["file_MD5"]
        version_list = self.list_versions()
        for version in version_list:
            version_dict = self.get_version_info(version)
            version_hash = version_dict["file_MD5"]
            if src_file_hash == version_hash:
                logging.debug("this file already exists in the folder...")
                return
        # get version num
        new_version = self.get_last_version()+1
        # update json file
        if self.set_version_info(set_dict={"version": new_version}):
            file_tar_path = self.__get_version_file_path(new_version)
            json_src_path = self.__get_file_json_path(None)
            json_tar_path = self.__get_file_json_path(new_version)
            # move file into history folder
            copy_file(self.path, file_tar_path)
            copy_file(json_src_path, json_tar_path)
            logging.debug("copy {file_path} and {josn_path} into {hist_path}".format(
                file_path=self.path, josn_path=json_src_path, hist_path=self.hist_dir))

    def drop_in(self, file_path, message="no description..."):
        # 新增文件，将当前放入版本库，并将新文件设为当前

        if self.__has_current_file():
            if not self.__has_json_file():
                self.__make_json_file(self.path)
            if not self.__has_history():
                # create self.hist_dir
                os.makedirs(self.hist_dir)
            # move self.path to self.hist_dir
            self.add_to_version()
            # clear current path
            self._clear_current()
        # make json file
        self.__make_json_file(file_path=file_path, message=message)
        # copy file to path
        copy_file(file_path, self.path)

    def set_current(self, version):
        # 设置当前文件，将当前放入版本库，并将被设置文件设为当前
        # move self.path to self.hist_dir
        self.add_to_version()
        # clear current path
        self._clear_current()
        # copy file to current
        file_src_path = self.__get_version_file_path(version)
        json_src_path = self.__get_file_json_path(version)
        json_tar_path = self.__get_file_json_path(None)
        copy_file(file_src_path, self.path)
        copy_file(json_src_path, json_tar_path)
        # set version to None
        self.set_version_info(set_dict={"version": None})
        logging.info(
            "set version {version} to current ".format(version=version))

    def delete_version(self, version):
        # 删除一个版本
        file_path = self.__get_version_file_path(version)
        json_path = self.__get_file_json_path(version)
        remove_file(file_path)
        remove_file(json_path)

    def verify_files(self, version=None):
        # 检查文件MD5值是否有误
        file_path = self.__get_file_json_path(version)
        file_hash = get_md5(file_path)
        version_dict = self.get_version_info(version)
        json_hash = version_dict["file_MD5"]
        if file_hash == json_hash:
            logging.info("{file_path} checked. Result Match.")
            return True
        else:
            logging.warning("{file_path} MD5 not Match.")
            return False

    def list_versions(self):
        # 列举所有版本
        version_list = []
        if os.path.isdir(self.hist_dir):
            hist_file_list = os.listdir(self.hist_dir)
            for hist_file in hist_file_list:
                if ".hive_data" in hist_file:
                    hist_file_path = os.path.join(self.hist_dir, hist_file)
                    info_dict = self.__dict_from_json_file(hist_file_path)
                    version_list.append(info_dict["version"])
        return version_list

    def get_last_version(self):
        # 获取最后版本号
        version_list = self.list_versions()
        if version_list:
            return sorted(version_list)[-1]
        return 0

    def get_version_info(self, version=None):
        # 获取版本信息
        json_path = self.__get_file_json_path(version)
        # read info dict from json
        info_dict = self.__dict_from_json_file(json_path)
        return info_dict

    def set_version_info(self, set_dict, version=None):
        # 更新版本信息
        info_dict = self.get_version_info(version)
        for key in set_dict:
            if key in info_dict:
                info_dict[key] = set_dict[key]
                logging.debug("update attribute {key}, now value is {value}".format(
                    key=key, value=info_dict[key]))
            else:
                logging.warning("no attribute named {key}".format(key=key))
        json_file_path = self.__get_file_json_path(version)
        # update to json file
        return self.__dict_to_json_file(info_dict, json_file_path)

    def _clear_current(self):
        # 清理当前文件
        os.remove(self.path)
        os.remove(self.__get_file_json_path())

    def __get_version_file_path(self, version):
        # 获取版本文件位置
        if version:
            file_dir = self.hist_dir
            file_path = r"{file_dir}/{file_name}_v{version:0>3}{ext}".format(
                file_dir=file_dir, file_name=self.name, version=version, ext=self.ext)
        else:
            js_dir = self.dir
            file_path = r"{file_dir}/{file_name}{ext}".format(
                js_dir=js_dir, file_name=self.name)
        return file_path

    def __get_file_json_path(self, version=None):
        # 获取此版本的json文件地址
        if version:
            js_dir = self.hist_dir
            json_path = r"{js_dir}/{file_name}_v{version:0>3}.hive_data".format(
                js_dir=js_dir, file_name=self.name, version=version)
        else:
            js_dir = self.dir
            json_path = r"{js_dir}/{file_name}.hive_data".format(
                js_dir=js_dir, file_name=self.name)
        return json_path

    def __has_history(self):
        # 判断是否已存在历史文件夹
        if os.path.isdir(self.hist_dir):
            return True
        return False

    def __has_current_file(self):
        # 判断是否已存在当前文件
        if os.path.isfile(self.path):
            return True
        return False

    def __has_json_file(self):
        json_file = self.__get_file_json_path()
        if os.path.isfile(json_file):
            return True
        return False

    def __make_json_file(self, file_path, version=None, message="no description..."):
        # 创建json文件

        json_file_path = self.__get_file_json_path(version)
        # check file exists
        if os.path.isfile(json_file_path):
            logging.warning("{json_file_path} exists, do nothing...".format(
                json_file_path=json_file_path))
            return False
        # get user
        user = getpass.getuser()
        # get current time
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        # get file MD5
        hash_code = get_md5(file_path)
        # init info dict
        info_dict = {}
        info_dict["file_name"] = self.full_name
        info_dict["message"] = message
        info_dict["uploader"] = user
        info_dict["upload_time"] = current_time
        info_dict["file_MD5"] = hash_code
        info_dict["version"] = version
        # write info into json file
        return self.__dict_to_json_file(info_dict, json_file_path)

    def __dict_from_json_file(self, json_file_path):
        # read json file
        json_file = open(json_file_path, "r")
        info_json = json.load(json_file)
        json_file.close()
        # convert json to dict
        info_dict = json.loads(info_json)
        return info_dict

    def __dict_to_json_file(self, info_dict, json_file_path):
        # convert dict to json
        info_json = json.dumps(info_dict, encoding="gbk")
        # make file
        json_file = open(json_file_path, "w")
        json.dump(info_json, json_file)
        json_file.close()
        logging.info("{json_file_path} wrote successful...".format(
            json_file_path=json_file_path))
        return True
