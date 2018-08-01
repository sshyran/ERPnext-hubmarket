# Copyright (c) 2015, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json

def update_hub_seller_activity(hub_seller, activity_details):
	activity_details = json.loads(activity_details)
	doc = frappe.get_doc({
		'doctype': 'Activity Log',
		'user': hub_seller,
		'status': activity_details.get('status', ''),
		'subject': activity_details['subject'],
		'content': activity_details.get('content', ''),
		'reference_doctype': 'Hub Seller',
		'reference_name': hub_seller
	}).insert(ignore_permissions=True)
	return doc

def update_hub_item_view_log(hub_seller, hub_item_code):
	doc = frappe.get_doc({
		'doctype': 'Hub Item View Log',
		'reference_hub_item': hub_item_code,
		'viewed_by': hub_seller
	}).insert(ignore_permissions=True)
	return doc

def update_hub_favourite_view_log(hub_seller, hub_item_code):
	doc = frappe.get_doc({
		'doctype': 'Hub Item Favourite Log',
		'reference_hub_item': hub_item_code,
		'favourited_by': hub_seller
	}).insert(ignore_permissions=True)
	return doc
