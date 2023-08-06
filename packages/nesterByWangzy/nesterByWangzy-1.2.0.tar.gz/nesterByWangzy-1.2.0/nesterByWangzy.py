"""This is the "nester.py" module and it provides one functioncalled print_lol()
    which prints lists that may not include nested lists """
import sys


def print_lol(the_list, indent=False, level=0, fh=sys.stdout):
    """This fuction takes one positional argument called "the_list",
        which is any python list ( of - possibly -nested lists).
        Each data item in the provided list in ( recursively ) printed to the screen on it's own line.
        第二个参数（名为"level")用来在遇到哦嵌套列表时插入制表符。"""
    for each_item in the_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=fh)
                print(each_item, file=fh)
