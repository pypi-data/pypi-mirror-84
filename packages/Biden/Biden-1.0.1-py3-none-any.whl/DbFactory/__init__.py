# coding:utf-8
# author caturbhuja
# date   2020/8/31 2:01 下午 
# wechat chending2012

from .biden import Biden


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


__version__ = '1.0.9'
VERSION = tuple(map(int_or_str, __version__.split('.')))

__all__ = [
    'Biden'
]
