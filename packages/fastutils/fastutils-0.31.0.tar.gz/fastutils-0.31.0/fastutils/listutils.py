# -*- coding: utf-8 -*-
import typing

def int_list_to_bytes(intlist):
    from .strutils import ints2bytes
    return ints2bytes(intlist)

def pad(thelist, size, padding):
    if len(thelist) < size:
        for _ in range(size - len(thelist)):
            thelist.append(padding)
    return thelist

def chunk(thelist, size, with_padding=False, padding=None):
    data = []
    start = 0
    while True:
        if len(thelist) < size:
            if with_padding:
                pad(thelist, size, padding)
            data.append(thelist)
            break
        data.append(thelist[start:start+size])
        thelist = thelist[start+size:]
        if not thelist:
            break
    return data

def clean_none(thelist):
    """Remove None or empty element in thelist.
    """
    return [element for element in thelist if element]

ignore_none_element = clean_none


def unique(thelist):
    """Remove duplicated elements from the list.
    """
    result = []
    for element in thelist:
        if not element in result:
            result.append(element)
    return result

def replace(thelist, map, inplace=False):
    """Replace element in thelist, the map is collection of {old_value: new_value}.
    
    inplace == True, will effect the original list.
    inplace == False, will create a new list to return.
    """
    if inplace:
        for index in range(len(thelist)):
            value = thelist[index]
            if value in map:
                thelist[index] = map[value]
        return thelist
    else:
        newlist = []
        thelist = list(thelist)
        for index in range(len(thelist)):
            value = thelist[index]
            if value in map:
                newlist.append(map[value])
            else:
                newlist.append(value)
        return newlist

def append_new(thelist, value):
    """Append new value and only new value to the list.
    """
    if not value in thelist:
        thelist.append(value)
    return value

def group(thelist):
    """Count every element in thelist. e.g. ["a", "b", "c", "a", "b", "b"] => {"a": 2, "b": 3, "c": 1}.
    """
    info = {}
    for x in thelist:
        if x in info:
            info[x] += 1
        else:
            info[x] = 1
    return info


def compare(old_set, new_set):
    """Compare old_set and new_set, return set_new, set_delete, set_update.
    """
    old_set = set(old_set)
    new_set = set(new_set)

    set_new = new_set - old_set
    set_delete = old_set - new_set
    set_update = old_set.intersection(new_set)

    return set_new, set_delete, set_update

def first(*thelist, check=lambda x: x, default=None):
    """Return first non-none value. check is a callable function that returns the real value.
    """
    for value in thelist:
        if check(value) != None:
            return value
    return default


class CyclicDependencyError(ValueError):
    pass

def topological_sort(*thelists):
    mapping = {}
    for thelist in thelists:
        for element in thelist:
            if not element in mapping:
                mapping[element] = set()
        for index in range(1, len(thelist)):
            prev = thelist[index-1]
            current = thelist[index]
            mapping[current].add(prev)
    result = []
    while True:
        oks = []
        for k in list(mapping.keys()):
            v = mapping[k]
            if not len(v):
                result.append(k)
                oks.append(k)
                del mapping[k]
        if not oks:
            break
        else:
            for ok in oks:
                for k, v in mapping.items():
                    if ok in v:
                        v.remove(ok)
    if mapping:
        raise CyclicDependencyError()
    return result

def topological_test(thelist, tester):
    last_index = -1
    for element in tester:
        index = thelist.index(element)
        if index < last_index:
            return False
        last_index = index
    return True

