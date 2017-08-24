# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, requests, json, redis, re
from datetime import datetime
from frappe.utils import get_datetime_str
from frappe.model.document import Document

class HubOutgoingMessage(Document):
	def autoname(self):
		self.name = "OUT-" + self.type + '-' + re.sub('[^A-Za-z0-9]+', '-',
			get_datetime_str(datetime.now())[:-7])

	def on_update(self):
		enqueue_message(self.receiver_site, self.method, self.arguments, self.name)

def enqueue_message(receiver_site, method, message, message_id, now=False):
	if now:
		return send_message_to_hub_client(receiver_site, method, message, message_id)
	try:
		frappe.enqueue('hub.hub.doctype.hub_outgoing_message.hub_outgoing_message.send_message_to_hub_client', now=now,
			receiver_site=receiver_site, site_method=method, message=message, message_id=message_id)
	except redis.exceptions.ConnectionError:
		send_message_to_hub_client(receiver_site, method, message, message_id)


def send_message_to_hub_client(receiver_site, site_method, message, message_id):
	response = requests.post(receiver_site + "/api/method/erpnext.hub_node.api." + "call_method",
		data = {
			"access_token": "bcm63cZ1tWQ39wMi", # At handshake
			"method": site_method,
			"message": message,
		}
	)
	response.raise_for_status()
	response_msg = response.json().get("message")
	if response_msg:
		frappe.db.set_value("Hub Outgoing Message", message_id, "status", "Successful")
	# Deleting mechanism for successful messages?, or logging
	return response_msg