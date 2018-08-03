# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils.nestedset import NestedSet
from frappe.model.document import Document

class HubCategory(NestedSet):
	# nsm_parent_field = 'parent_hub_category'

	# def autoname(self):
	# 	self.name = self.hub_category_name
	# 	print("================", self.name, self.nsm_parent_field)

	# def on_update(self):
	# 	NestedSet.on_update(self)

	pass
