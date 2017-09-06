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
		self.name = autoname_increment_by_field(self.doctype, "item_code", self.name)

	def update_item_details(self, item_dict):
		self.old = None
		if frappe.db.exists('Hub Item', self.name):
			self.old = frappe.get_doc('Hub Item', self.name)
		for field, new_value in item_dict.iteritems():
			old_value = self.old.get(field) if self.old else None
			if(new_value != old_value):
				self.set(field, new_value)
				frappe.db.set_value("Hub Item", self.name, field, new_value)

	def validate(self):
		if not self.route:
			self.route = 'items/' + self.name

	def get_context(self, context):
		context.no_cache = True

@frappe.whitelist(allow_guest=True)
def sync_items(access_token, items):
	hub_user = hub.get_user(access_token)
	# company_id = frappe.db.get_value("Hub Company", hub_user.company_name, "name")

	# insert / update items
	for item in items:
		item_code = frappe.db.get_value("Hub Item",
			{"hub_user": hub_user, "item_code": item.get("item_code")})
		if item_code:
			hub_item = frappe.get_doc("Hub Item", item_code)
		else:
			hub_item = frappe.new_doc("Hub Item")
			hub_item.hub_user = hub_user

		for key in item:
			hub_item.set(key, item.get(key))

		hub_item.company_id = company_id

		for key in hub_user_fields:
			hub_item.set(key, hub_user.get(key))

		hub_item.published = 1
		hub_item.disabled = 0
		hub_item.save(ignore_permissions=True)

	return {"total_items": len(items)}

def get_list_context(context):
	context.allow_guest = True
	context.no_cache = True
	context.title = 'Items'
	context.no_breadcrumbs = True
	context.order_by = 'creation desc'
