# Copyright (c) 2015, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json


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


def update_hub_item_view_log(hub_item_code, hub_seller):
	log_type = 'ITEM-VIEW'

	hub_item_seller = frappe.db.get_value(
		'Hub Item', hub_item_code, 'hub_seller')

	is_own_item_of_seller = hub_seller == hub_item_seller

	existing_logs = frappe.db.get_all('Hub Log', filters={
		'type': log_type,
		'primary_document': hub_item_code,
		'secondary_document': hub_seller
	})

	if not is_own_item_of_seller and not len(existing_logs):
		frappe.get_doc({
			'doctype': 'Hub Log',

			'type': log_type,

			'primary_doctype': 'Hub Item',
			'primary_document': hub_item_code,
			'secondary_doctype': 'Hub Seller',
			'secondary_document': hub_seller
		}).insert(ignore_permissions=True)


def get_item_view_count(hub_item_code):
	return len(frappe.get_all('Hub Log',
		filters={
			'type': 'ITEM-VIEW',
			'primary_document': hub_item_code
		}
	))


# Cardinal sin: should use the update_hub_item_favourite_log() method below instead,
# But if we can do an ORDER BY before a GROUP BY
def mutate_hub_item_favourite_log(hub_item_code, hub_seller, favourited=1):
	log_type = 'ITEM-FAV' if favourited else 'ITEM-UNFAV'

	hub_item_seller = frappe.db.get_value(
		'Hub Item', hub_item_code, 'hub_seller')

	is_own_item_of_seller = hub_seller == hub_item_seller

	if is_own_item_of_seller:
		return

	existing_logs = frappe.db.get_all('Hub Log', filters={
		'primary_doctype': 'Hub Item',
		'primary_document': hub_item_code,
		'secondary_doctype': 'Hub Seller',
		'secondary_document': hub_seller
	})

	latest_log = existing_logs[0] if len(existing_logs) else ''

	if latest_log:
		frappe.db.set_value('Hub Log', latest_log.get('name'), 'type', log_type)
	else:
		frappe.get_doc({
			'doctype': 'Hub Log',
			'type': log_type,
			'primary_doctype': 'Hub Item',
			'primary_document': hub_item_code,
			'secondary_doctype': 'Hub Seller',
			'secondary_document': hub_seller
		}).insert(ignore_permissions=True)


def get_favourite_item_logs_seller(hub_seller):
	return frappe.get_all('Hub Log', fields=['primary_document', 'type'], filters={
			'type': 'ITEM-FAV',
			'secondary_doctype': 'Hub Seller',
			'secondary_document': hub_seller
		}
	)


def update_hub_item_favourite_log(hub_item_code, hub_seller, favourited=1):
	log_type = 'ITEM-FAV' if favourited else 'ITEM-UNFAV'

	hub_item_seller = frappe.db.get_value(
		'Hub Item', hub_item_code, 'hub_seller')

	is_own_item_of_seller = hub_seller == hub_item_seller

	existing_logs = frappe.db.get_all('Hub Log', filters={
		'type': log_type,
		'primary_doctype': 'Hub Item',
		'primary_document': hub_item_code,
		'secondary_doctype': 'Hub Seller',
		'secondary_document': hub_seller
	})

	latest_log = existing_logs[0] if len(existing_logs) else ''

	if not is_own_item_of_seller and not latest_log:
		frappe.get_doc({
			'doctype': 'Hub Log',

			'type': log_type,

			'primary_doctype': 'Hub Item',
			'primary_document': hub_item_code,
			'secondary_doctype': 'Hub Seller',
			'secondary_document': hub_seller
		}).insert(ignore_permissions=True)


def get_all_favourite_item_logs_seller(hub_seller):
	favourite_log_types = ['ITEM-FAV', 'ITEM-UNFAV']

	return frappe.get_all('Hub Log', fields=['primary_document', 'type'], filters={
			'type': ['in', favourite_log_types],
			'secondary_doctype': 'Hub Seller',
			'secondary_document': hub_seller
		},
		order_by = 'modified desc',

		# Group by Hub Item document
		group_by = 'primary_document'
	)

