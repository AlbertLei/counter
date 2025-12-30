#!/usr/bin/env python3
""" usage: counter <filename> <prefix>
- counter main.txt
- counter main.txt '2.'
- cat main.txt | counter
- cat main.txt | counter - '2.'

Note that it will remove all trailing spaces 
"""


import sys
import re
from collections import defaultdict


# Find all __#id__ patterns and extract the 'id'
def get_ids(lines):
    ids = []

    # A valid id must begin with "__#"
    pattern = r"__#([^_]+)__"
    # matches __#id__ and captures the id
    for line in lines:
        matches = re.findall(pattern, line)
        ids.extend(matches)

    return ids


# check id duplicates
def check_duplicates(ids):
    seen = set()
    duplicates = set()

    for id in ids:
        if id in seen:
            duplicates.add(id)
        else:
            seen.add(id)

    if duplicates:
        raise ValueError(f"Duplicate ids found: {', '.join(duplicates)}")
    else:
        return 0


# return the kind of id
# An id without ":" belongs to the default kind.
def get_kind(id):
    split_index = id.find(":")
    if split_index != -1:
        kind = id[:split_index]
    else:
        kind = "default"
    return kind


# Groupping ids by their kind.
def group_ids(ids):
    # When a key is not found, the default type is 'list'
    grouped_ids = defaultdict(list)
    for id in ids:
        kind = get_kind(id)
        grouped_ids[kind].append(id)

    return grouped_ids


def get_counter(id, grouped_ids):
    kind = get_kind(id)
    counter = grouped_ids[kind].index(id) + 1
    return counter


def get_lookup_table(ids, grouped_ids):
    out = dict()
    for id in ids:
        counter = get_counter(id, grouped_ids)
        id_key = f"__#{id}__"
        id_value = str(counter)
        out[id_key] = id_value
        ref_key = "@" + id
        ref_value = str(counter)
        out[ref_key] = ref_value
    return out


def get_newline(line, table, sorted_keys, prefix):
    newline = line  # initialize
    for key in sorted_keys:
        val = str(prefix) + str(table[key])
        newline = newline.replace(key, val)
    return newline


def get_lines(args):
    if len(args) == 1:  # read from stdin
        lines = sys.stdin.readlines()
    elif args[1] == "-":
        lines = sys.stdin.readlines()
    else:
        filepath = sys.argv[1]
        with open(filepath, "r") as f:
            lines = f.readlines()
    return lines


def get_prefix(args):
    if len(args) <= 2:
        return ""  # no prefix
    if len(args) == 3:
        return args[2]
    else:
        msg = "At most two arguments:\n1. first argument for file path\n2. second argument for prefix."
        raise ValueError(msg)


# below are main.py
args = sys.argv
lines = get_lines(args)
prefix = get_prefix(args)

ids = get_ids(lines)
check_duplicates(ids)
grouped_ids = group_ids(ids)
table = get_lookup_table(ids, grouped_ids)
keys = table.keys()
sorted_keys = sorted(keys, key=len, reverse=True)
for line in lines:
    line = get_newline(line, table, sorted_keys, prefix)
    print(line.rstrip())
