# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class HubChatMessage(Document):
	def validate(self):
		hub_seller = frappe.db.get_value('Hub User', self.sender, 'hub_seller')

		if hub_seller and hub_seller == self.reference_hub_seller:
			self.hub_item_belongs_to_sender = 1

