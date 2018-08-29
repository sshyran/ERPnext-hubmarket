# Copyright (c) 2015, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json


def add_log(log_type, hub_item_name=None, hub_seller=None, data=None):
	return frappe.get_doc({
		'doctype': 'Hub Log',
		'type': log_type,
		'reference_hub_item': hub_item_name,
		'reference_hub_seller': hub_seller,
		'data': json.dumps(data)
	}).insert()


def add_saved_item(hub_item_name, hub_seller):
	try:
		frappe.get_doc({
			'doctype': 'Hub Saved Item',
			'hub_seller': hub_seller,
			'hub_item': hub_item_name
		}).insert()
	except frappe.DuplicateEntryError:
		pass


def remove_saved_item(hub_item_name, hub_seller):
	name = frappe.db.get_value('Hub Saved Item', {
		'hub_item': hub_item_name,
		'hub_seller': hub_seller
	})

	if name:
		frappe.delete_doc('Hub Saved Item', name)


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
