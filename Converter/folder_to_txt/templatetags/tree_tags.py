# folder_to_txt/templatetags/tree_tags.py

from django import template
import os
from collections import defaultdict

register = template.Library()

def build_tree(paths):
    tree = lambda: defaultdict(tree)
    root = tree()
    for path in paths:
        parts = path.split(os.sep)
        cur = root
        for part in parts:
            cur = cur[part]
    return root

@register.filter
def filetree(value):
    # value: file_tree 리스트
    return build_tree(value)
