#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-App.
# @File         : app_run
# @Time         : 2020/11/5 4:48 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
"""
'console_scripts': [
    'app-run=iapp.app_run.run:run'
]
"""

import fire
from pathlib import Path
from iapp.utils import get_module_path


class AppRun(object):
    """doc"""

    def __init__(self, arg=0, **kwargs):
        """

        :param arg:
        """
        self.arg = arg
        print(kwargs)

    def apps_list(self):
        path = get_module_path('../apps', __file__)
        return list(Path(path).glob('*app.py'))


def run():
    fire.Fire(AppRun)

if __name__ == '__main__':
    print(AppRun().apps_list())