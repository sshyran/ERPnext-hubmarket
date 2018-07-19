# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class HubItemReview(Document):

    def before_naming(self):
        if self.user:
            user = frappe.get_doc('User', self.user)
            self.username = user.full_name or user.username or None
