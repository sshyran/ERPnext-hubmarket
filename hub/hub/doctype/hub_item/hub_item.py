# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json, hub
from frappe.website.website_generator import WebsiteGenerator
from hub.hub.utils import autoname_increment_by_field

class HubItem(WebsiteGenerator):
	website = frappe._dict(
		page_title_field = "item_name"
	)

	def autoname(self):
		super(HubItem, self).autoname()
		self.hub_item_code = self.name
		self.name = autoname_increment_by_field(self.doctype, 'hub_item_code', self.name)

	def validate(self):
		site_name = frappe.db.get_value('Hub Company', self.company_name, 'site_name')
		if self.image.startswith('/') and site_name not in self.image:
			self.image = '//' + site_name + self.image

		if not self.route:
			self.route = 'items/' + self.name

	def get_context(self, context):
		context.no_cache = True

def get_list_context(context):
	context.allow_guest = True
	context.no_cache = True
	context.title = 'Items'
	context.no_breadcrumbs = True
	context.order_by = 'creation desc'
