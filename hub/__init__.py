# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe

__version__ = '0.0.1'

def get_user(access_token):
	hub_user_name = frappe.db.get_value('Hub User', {'access_token': access_token})
	if not hub_user_name:
		frappe.throw('Invalid access token', frappe.PermissionError)
	return hub_user_name
