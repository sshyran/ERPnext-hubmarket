# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe.utils import random_string, now, get_datetime, today, add_days, add_months

class HubUser(Document):
	def autoname(self):
		access_token = random_string(16)
		self.access_token = access_token

	def update_details(self, args):
		self.old = frappe.get_doc('Hub User', self.name)
		for key, new_value in args.iteritems():
			old_value = self.old.get(key)
			if(new_value != old_value):
				self.set(key, new_value)
				frappe.db.set_value("Hub User", self.name, key, new_value)
		return {}

	def delete_item(self, item_code):
		"""Delete item on portal"""
		item = frappe.db.get_value("Hub Item", {"item_code": item_code, "hub_user": self.name})
		if item:
			frappe.delete_doc("Hub Item", item)

	def unpublish(self):
		"""Un publish seller"""
		self.unpublish_all_items()
		self.publish = 0

	def disable(self):
		"""Disable user"""
		self.disable_all_items()
		self.enabled = 0

	def clear_items_pricing_info(self):
		pass

	def clear_items_stock_info(self):
		pass

	def unregister(self):
		"""Unregister user"""
		self.delete_all_items()
		self.delete_company()
		# TODO: delete messages
		frappe.delete_doc('Hub User', self.name, ignore_permissions=True)
		return {}

	def delete_company(self):
		company_name = frappe.get_all('Hub Company', filters={"hub_user": self.name})[0]["name"]
		frappe.db.set_value("Hub User", self.name, "company_name", None)
		frappe.db.set_value("Hub Company", company_name, "hub_user", None)
		frappe.delete_doc('Hub Company', company_name, ignore_permissions=True)


	def update_item_fields(self, args):
		items_with_fields_updates = json.loads(args["items_with_fields_updates"])
		fields_to_update = json.loads(args["fields_to_update"])
		print(fields_to_update)
		for item in items_with_fields_updates:
			item_code = frappe.db.get_value("Hub Item",
				{"hub_user": self.name, "item_code": item.get("item_code")})
			hub_item = frappe.get_doc("Hub Item", item_code)
			for field in fields_to_update:
				hub_item.set(field, item.get(field))
			hub_item.save(ignore_permissions=True)

		now_time = now()
		self.last_sync_datetime = now_time
		self.save(ignore_permissions=True)
		return {"total_items": len(items_with_fields_updates)}

	def disable_all_items(self):
		for item in frappe.get_all("Hub Item", fields=["name"], filters={ "hub_user": self.name}):
			frappe.db.set_value("Item", item.name, "disabled", 1)

	def unpublish_all_items(self):
		for item in frappe.get_all("Hub Item", fields=["name"], filters={ "hub_user": self.name}):
			frappe.db.set_value("Item", item.name, "published", 0)

	def delete_all_items(self):
		all_items = frappe.db.sql_list("select name from `tabHub Item` where hub_user=%s", self.name)
		for name in all_items:
			frappe.delete_doc("Hub Item", name, ignore_permissions=True)
		return {"total_items": len(all_items)}

def check_last_sync_datetime():
	users = frappe.db.get_all("Hub User", fields=["name", "access_token", "last_sync_datetime"], filters={"enabled": 1})
	for user in users:
		if get_datetime(user.last_sync_datetime) < add_days(today(), -7):
			user_doc = frappe.get_doc("Hub User", user.name)
			user_doc.disable()
			enqueue_disable_user_message(user.access_token)
			return
		if get_datetime(user.last_sync_datetime) < add_months(today(), -1):
			user_doc = frappe.get_doc("Hub User", user.name)
			user_doc.unregister()

def enqueue_disable_user_message(access_token):
	message = frappe.new_doc("Hub Outgoing Message")

	message.type = "CLIENT-DISABLE"
	message.method = "disable_and_suspend_hub_user"

	receiver_user = frappe.get_doc("Hub User", {"access_token": access_token})
	message.receiver_site = receiver_user.site_name

	message.save(ignore_permissions=True)
	return 1

