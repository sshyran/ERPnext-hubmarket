# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from hub.hub.utils import autoname_increment_by_field

class HubCompany(Document):
	def autoname(self):
		# super(HubCompany, self).autoname()
		# self.name = autoname_increment_by_field(self.doctype, "company_name", self.name)
		self.name = autoname_increment_by_field(self.doctype, "company_name", self.company_name)

