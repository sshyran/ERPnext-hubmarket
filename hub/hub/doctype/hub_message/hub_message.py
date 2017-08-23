# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, requests, json
from frappe.model.document import Document

class HubMessage(Document):
	def on_update(self):
		self.send_message()

	def send_message(self):
		response = requests.post(self.receiver_site + "/api/method/erpnext.hub_node.api." + "call_method",
			data = {
				"access_token": "bcm63cZ1tWQ39wMi", # At handshake
				"method": self.method,
				"message": self.arguments,
			}
		)
		response.raise_for_status()
		if response.json().get("message") == "Success":
			self.status = "Successful"
