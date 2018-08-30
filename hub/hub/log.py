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
	}).insert(ignore_permissions=True)


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


def get_seller_items_synced_count(hub_seller):
	# TODO: Fix dependency on past logs, this causes a very great chance of error
	logs = frappe.get_all('Hub Seller Publish Stats', fields=['*'] ,filters={ 'hub_seller': hub_seller })
	current_total_seller_item_count = get_total_items_of_seller(hub_seller)

	if len(logs) > 0:
		latest_log = logs[0]
		items_synced_count = current_total_seller_item_count - latest_log.total_items_count_after_sync
	else:
		items_synced_count = current_total_seller_item_count

	return items_synced_count


def get_total_items_of_seller(hub_seller):
	return frappe.get_all('Hub Item',
		fields=['count(name) as item_count'],
		filters={
			'hub_seller': hub_seller
		}
	)[0].item_count


def add_seller_publish_stats(hub_seller, items_synced_count=None):
	if not items_synced_count:
		items_synced_count = get_seller_items_synced_count(hub_seller)

	current_total_seller_item_count = get_total_items_of_seller(hub_seller)

	frappe.get_doc({
		'doctype': 'Hub Seller Publish Stats',
		'hub_seller': hub_seller,
		'items_synced_count': items_synced_count,
		'total_items_count_after_sync': current_total_seller_item_count
	}).insert()


def add_hub_seller_activity(hub_seller, subject=None, content=None, status=None):
	doc = frappe.get_doc({
		'doctype': 'Activity Log',
		'user': hub_seller,
		'status': status,
		'subject': subject,
		'content': json.dumps(content),
		'reference_doctype': 'Hub Seller',
		'reference_name': hub_seller
	}).insert(ignore_permissions=True)
	return doc
