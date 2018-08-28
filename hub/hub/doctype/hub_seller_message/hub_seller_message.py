# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class HubSellerMessage(Document):
	def validate(self):
		if self.sender == self.receiver:
			frappe.throw(frappe._('Sender cannot be the same as Receiver'))
