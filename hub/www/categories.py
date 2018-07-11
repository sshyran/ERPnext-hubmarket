import frappe
from hub.util import get_categories_and_subcategories


def get_context(context):
    context.cats = get_categories_and_subcategories()
    context.no_breadcrumbs = False
