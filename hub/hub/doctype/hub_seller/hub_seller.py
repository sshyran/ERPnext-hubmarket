# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class HubSeller(Document):
	def autoname(self):
		name_length = 16
		hash_length = 12
		company_name = self.company.replace(' ', '-')
		self.name = company_name[:name_length] + '-' + frappe.generate_hash(self.doctype, hash_length)
