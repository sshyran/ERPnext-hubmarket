# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class HubSeller(Document):
	def autoname(self):
		self.name = get_name(self.company)

def get_name(company_name):
	name_length = 16
	hash_length = 12
	company_name = company_name.replace(' ', '-')
	return company_name[:name_length] + '-' + frappe.generate_hash('Hub Seller', hash_length)
