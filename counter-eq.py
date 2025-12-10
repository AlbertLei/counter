#!/usr/bin/env python3
import re
import sys


def get_lines(file):
    with open(file, "r") as f:
        lines = f.readlines()
    return lines


def get_eq_ids(lines):
    # Find all \label{id} patterns and extract the 'id'
    # A valid id must begin with "eq:"
    label_ids = []
    pattern = r"\\label\{eq:([^}]+)\}"
    # matches \label{eq:...} and captures inside the braces
    for line in lines:
        matches = re.findall(pattern, line)
        label_ids.extend(matches)

    return label_ids


def check_duplicates(strings_list):
    seen = set()
    duplicates = set()

    for item in strings_list:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    if duplicates:
        raise ValueError(f"Duplicate equation ids found: {', '.join(duplicates)}")
    else:
        return 0


def replace_eq_ids(lines, eq_ids):
    """Replace label{id} with tag{prefix+counter}."""
    result = []
    for line in lines:
        new_line = line
        for index, value in enumerate(eq_ids):
            key = f"\\label{{eq:{value}}}"
            val = str(index + 1)
            value = f"\\tag{{{val}}}"
            new_line = new_line.replace(key, value)
        result.append(new_line)
    return result


def get_eq_table(eq_ids, prefix):
    out = dict()
    for counter, id in enumerate(eq_ids):
        counter = counter + 1
        id_key = f"\\label{{eq:{id}}}"
        id_value = f"\\tag{{{counter}}}"
        out[id_key] = id_value
        ref_key = f"@eq:{id}"
        ref_value = f"({prefix}{counter})"
        out[ref_key] = ref_value
    return out


def print_replace_eq(lines, eq_ids, prefix):
    table = get_eq_table(eq_ids, prefix)
    keys = table.keys()
    # Descending order (longest first)
    keys = sorted(keys, key=len, reverse=True)

    for line in lines:
        new_line = line
        for key in keys:
            val = table[key]
            new_line = new_line.replace(key, val)
        print(new_line, end="")
    return 0


# below are main.py
args = sys.argv

if len(args) == 1:  # read from stdin
    lines = sys.stdin.read()
    prefix = ""
elif len(args) == 2:  # read from file
    file = sys.argv[1]
    lines = get_lines(file)
    prefix = ""
elif len(args) == 3:  # read from file and prefix
    file = sys.argv[1]
    lines = get_lines(file)
    prefix = sys.argv[2]
else:
    msg = """At most two arguments:
    1. first argument for file path
    2. second argument for prefix 
    """
    raise ValueError(msg)


# file = "./pandoc-counter/eq.md"
# lines = get_lines(file)
eq_ids = get_eq_ids(lines)
check_duplicates(eq_ids)
print_replace_eq(lines, eq_ids, prefix)
