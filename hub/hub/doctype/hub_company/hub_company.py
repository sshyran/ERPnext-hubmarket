# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.website.website_generator import WebsiteGenerator
from hub.hub.utils import autoname_increment_by_field

class HubCompany(WebsiteGenerator):
	website = frappe._dict(
		page_title_field = "company_name"
	)

	def autoname(self):
		self.name = autoname_increment_by_field(self.doctype, "company_name", self.company_name)

	def validate(self):
		if not self.route:
			self.route = 'company/' + self.name

	def get_context(self, context):
		context.no_cache = True

def get_list_context(context):
	context.allow_guest = True
	context.no_cache = True
	context.title = 'Companies'
	context.no_breadcrumbs = True
	context.order_by = 'creation desc'