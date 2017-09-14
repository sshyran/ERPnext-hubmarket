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
