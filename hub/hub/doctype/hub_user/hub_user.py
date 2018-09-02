# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import random_string
from frappe.utils.password import get_decrypted_password

class HubUser(Document):
	def validate(self):
		if not self.user:
			self.password = random_string(16)

			user = frappe.get_doc({
				'doctype': 'User',
				'email': self.user_email,
				'first_name': self.first_name,
				'last_name': self.last_name,
				'new_password': self.password
			})

			user.append_roles('System Manager', 'Hub User', 'Hub Buyer')
			user.flags.delay_emails = True
			user.insert(ignore_permissions=True)

			self.user = user.name
