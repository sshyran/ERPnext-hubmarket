# Copyright (c) 2015, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def get_items_by_country(country):
	fields = get_item_fields()

	items = frappe.get_all('Hub Item', fields=fields,
		filters={
			'country': ['like', '%' + country + '%']
		}, limit=8)

	return post_process_item_details(items)

def get_random_items_from_each_hub_seller():
	res = frappe.db.sql('''
		SELECT * FROM (
			SELECT
				h.name AS hub_seller_name, h.name, i.name AS hub_item_code, i.item_name
			FROM `tabHub Seller` h
			INNER JOIN `tabHub Item` i ON h.name = i.hub_seller
			ORDER BY RAND()
		) AS shuffled_items
		GROUP BY hub_seller_name;
	''', as_dict=True)

	hub_item_codes = [r.hub_item_code for r in res]

	fields = get_item_fields()
	items = frappe.get_all('Hub Item', fields=fields, filters={ 'name': ['in', hub_item_codes] })

	return post_process_item_details(items)

def get_items_from_all_categories():
	items_from_categories = {}

	for category in [d.name for d in frappe.get_all('Hub Category', fields="name")]:
		if frappe.db.count('Hub Item', filters={ 'hub_category': category }) > 20:
			items_from_categories[category] = get_items_from_category(category)

	return dict(items_from_categories)

def get_items_from_category(category):
	items = frappe.get_all(
		'Hub Item',
		fields=get_item_fields(),
		filters={ 'image': ['not like', '%private%'], 'hub_category': category },
		limit_page_length = 4
	)
	return post_process_item_details(items)

def get_items_from_hub_seller(hub_seller):
	items = frappe.get_all(
		'Hub Item',
		fields = get_item_fields(),
		filters = { 'image': ['not like', '%private%'], 'hub_seller': hub_seller },
		limit_page_length = 8
	)
	return post_process_item_details(items)

def get_items_with_images():
	fields = get_item_fields()

	items = frappe.get_all('Hub Item', fields=fields,
		filters={
			'image': ['like', 'http%']
		}, limit=8)

	return post_process_item_details(items)

def post_process_item_details(items):
	items = get_item_details_and_company_name(items)

	url = frappe.utils.get_url()
	for item in items:
		# convert relative path to absolute path
		if item.image and item.image.startswith('/files/'):
			item.image = url + item.image

	return items

def get_items_from_codes(item_codes):
	items = frappe.get_all('Hub Item', fields=get_item_fields(), filters={
			'hub_item_code': ['in', item_codes],
		},
		order_by = 'modified desc'
	)

	return post_process_item_details(items)

def get_item_fields():
	return ['name', 'hub_item_code', 'item_name', 'image', 'creation', 'hub_seller']

def get_item_details_and_company_name(items):
	for item in items:
		res = frappe.db.get_all('Hub Item Review', fields=['AVG(rating) as average_rating, count(rating) as no_of_ratings'], filters={
			'parenttype': 'Hub Item',
			'parentfield': 'reviews',
			'parent': item.name
		})[0]

		item.average_rating = res['average_rating']
		item.no_of_ratings = res['no_of_ratings']

		company, country, city = frappe.db.get_value('Hub Seller', item.hub_seller, ['company', 'country', 'city'])

		item.company = company
		item.country = country
		item.city = city

	return items
