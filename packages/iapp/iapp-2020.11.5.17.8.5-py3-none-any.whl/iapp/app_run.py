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
import os
import fire
from pathlib import Path
from iapp.utils import get_module_path


class AppRun(object):
    """doc"""

    def __init__(self, **kwargs):
        """

        :param arg:
        """
        self._apps_path = Path(get_module_path('../apps', __file__))

    def apps_list(self):
        return list(self._apps_path.glob('*app.py'))

    def app_run(self, app_name):
        app_file = list(self._apps_path.glob(f'*{app_name}*'))
        return os.system(f"python {app_file}")


def cli():
    fire.Fire(AppRun)


if __name__ == '__main__':
    print(AppRun().apps_list())
