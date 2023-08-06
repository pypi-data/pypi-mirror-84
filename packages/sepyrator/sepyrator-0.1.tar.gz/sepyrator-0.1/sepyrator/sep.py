#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['print_sep']


def print_sep(arr: list, size: int = -1):
    if size == -1:
        if type(arr[0]) == list:
            size = len(arr[0])
    tab_size: list = []
    for i in range(size):
        local_size: int = 0
        for j in range(len(arr)):
            lg: int = len(arr[j][i])
            if local_size < lg:
                local_size = lg
        tab_size.append(local_size)
    for i in range(len(arr)):
        for j in range(size):
            sep: str = " "*(tab_size[j] - len(arr[i][j]) + 6)
            print(arr[i][j], end=sep)
        print()
