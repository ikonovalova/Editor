#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import util
import cgi
import json
from PyQt5 import QtWidgets


def try_except(function):
    """
    https://www.blog.pythonlibrary.org/2016/06/09/python-how-to-create-an-exception-logging-decorator/
    """
    import functools

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print("Exception in " + function.__name__ + ": " + repr(e))
            raise
    return wrapper

@try_except
def perform(clones: 'module', candidates: 'list[clones.VariativeElement]', lgr: 'logging.Logger', **kwargs):
    """
    Function to construct extra reports
    :param clones: clones module VariativeElement
    :param candidates: list of clones.VariativeElement instances
    :param lgr: logger to log =)
    :param kwargs: different parameters
    :return: nothing
    """
    lgr.info("==== Extra report ====")

    path =  clones.InputFile.instances()[0].fileName
    save_filename = path + '.json'

    start_point = ''
    end_point = ''

    data = {}
    data["Benchmarks"] = []

    with open(save_filename, 'w', encoding = 'utf-8') as fp:
        count_dupl = 0 # Number of clone in the file
        for g in candidates:
            number_clones = 0 # Number of clone in a group

            new_data = {}
            count_elem = len(data["Benchmarks"]) + 1
            new_data["name"] = str(count_elem)

            new_data["annotation"] = str(count_elem)

            new_data["group_ids"] = []

            while number_clones < len(g.clone_groups[0].instances):

                start = g.clone_groups[0].instances[number_clones][1]
                end = g.clone_groups[0].instances[number_clones][2]
                number_clones = number_clones + 1

                new_we = {}
                new_we["name2"] = str(count_dupl)
                count_dupl = count_dupl + 1
                new_we["id_dupl"] = count_dupl
                new_we["position"] = []

                add_pos = new_we["position"]
                add_pos.insert(0, start)
                add_pos.insert(1, end)

                new_data["group_ids"].append(new_we)

            data["Benchmarks"].append(new_data)
        json.dump(data, fp)

    pass