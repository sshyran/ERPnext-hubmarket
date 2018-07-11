import json

import frappe

def safe_json_loads(string):
    try:
        string = json.loads(string)
    except Exception as e:
        pass

    return string

def assign_if_empty(a, b):
    return a if a else b

def get_categories_and_subcategories():
    """
    Return a list of parent categories where each parent category has a key `child_items`.
    """
    categories = frappe.get_list('Hub Category', fields=['name', 'parent_hub_category'], filters=[["name", "!=", "All Categories"]])
    parents = filter(lambda category: category['parent_hub_category'] == 'All Categories', categories)
    sub_categories = filter(lambda category: category['parent_hub_category'] != 'All Categories', categories)
    parents_dict = {parent['name']: parent for parent in parents}
    for parent in parents_dict.values():
        parent['child_items'] = []
    for sc in sub_categories:
        parent_name = sc['parent_hub_category']
        parent = parents_dict[parent_name]
        parent['child_items'].append(sc)
    return parents_dict.values()
