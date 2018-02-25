from __future__ import absolute_import

import frappe

__version__ = '0.0.1'

def get_user(access_token):
	hub_user_name = frappe.db.get_value('Hub User', {'access_token': access_token})
	if not hub_user_name:
		frappe.throw('Invalid access token', frappe.PermissionError)
	return hub_user_name

import logging

from hub.util import safe_json_loads, assign_if_empty

log = logging.getLogger(__name__)

@frappe.whitelist(allow_guest = True)
def search(query, types = None, fields = None):
	from hub.engine import search
	
	types   = assign_if_empty(safe_json_loads(types),  [ ])
	fields  = assign_if_empty(safe_json_loads(fields), [ ])

	results = search(query, types = types, fields = fields)

	return results
