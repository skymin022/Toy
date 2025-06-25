# folder_to_txt/templatetags/tree_tags.py

from django import template
import os
from collections import defaultdict

register = template.Library()

def build_tree(paths):
    from collections import defaultdict

    def tree():
        return defaultdict(tree)

    def convert(d):
        if isinstance(d, defaultdict):
            return {k: convert(v) for k, v in d.items()}
        else:
            return d

    root = tree()
    for path in paths:
        parts = path.split('/')
        cur = root
        for part in parts:
            cur = cur[part]
    return convert(root)


@register.filter
def filetree(value):
    # value: file_tree 리스트
    return build_tree(value)
