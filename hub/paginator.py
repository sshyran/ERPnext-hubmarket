from math import ceil

import frappe


class Paginator(object):
    def __init__(self, doctype, per_page=20, page_number=1, fields=['*'], filters={}, **kwargs):
        self.doctype = doctype
        self.per_page = per_page
        self.page_number = page_number
        self.fields = fields
        self.filters = filters
        # To accomodate kwargs for get_list.
        self.kwargs = kwargs

    def get_page(self):
        bottom = (self.page_number - 1) * self.per_page
        page_items = frappe.get_list(self.doctype, fields=self.fields, filters=self.filters, start=bottom, limit=self.per_page, **self.kwargs)
        return page_items

    @property
    def has_next_page(self):
        return self.page_number < self.num_pages

    @property
    def has_prev_page(self):
        return self.page_number > 1

    @property
    def num_pages(self):
        count = self.count
        return int(ceil(float(count)/self.per_page))

    @property
    def count(self):
        if hasattr(self, 'cnt'):
            return self.cnt
        self.cnt = frappe.db.count(self.doctype, filters=self.filters)
        return self.cnt
