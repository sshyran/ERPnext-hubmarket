# Copyright (c) 2015, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

class Curation(object):
	fields = ['name', 'item_name', 'image', 'creation', 'hub_seller']


	def __init__(self, hub_seller=None, country=None):
		self.hub_seller = hub_seller
		self.country = country


	def get_data_for_homepage(self):
		items_by_country = self.get_items_by_country()
		items_with_images = self.get_items_with_images()
		random_items = self.get_random_items_from_each_hub_seller()
		category_items = self.get_items_from_all_categories()

		return dict(
			items_by_country=items_by_country,
			items_with_images=items_with_images,
			random_items=random_items,
			category_items=category_items
		)


	def get_items_with_images(self):
		return self.get_items(filters={
			'image': ['like', 'http%']
		}, limit=8)


	def get_items_by_country(self):
		if not self.country: return []

		return self.get_items(filters={
			'country': ['like', '%' + self.country + '%']
		}, limit=8)


	def get_items_from_all_categories(self):
		items_from_categories = {}
		for category in [d.name for d in frappe.get_all('Hub Category', fields='name')]:
			if frappe.db.count('Hub Item', filters={ 'hub_category': category }) > 20:
				items_from_categories[category] = self.get_items_by_category(category)
		return items_from_categories


	def get_random_items_from_each_hub_seller(self):
		res = frappe.db.sql('''
			SELECT * FROM (
				SELECT
					h.name AS hub_seller_name, h.name, i.name AS hub_item_name, i.item_name
				FROM `tabHub Seller` h
				INNER JOIN `tabHub Item` i ON h.name = i.hub_seller
				ORDER BY RAND()
			) AS shuffled_items
			GROUP BY hub_seller_name;
		''', as_dict=True)

		hub_item_names = [r.hub_item_name for r in res]

		return self.get_items(filters={ 'name': ['in', hub_item_names] })


	def get_items_by_category(self, category):
		return self.get_items(
			filters={ 'hub_category': category },
			limit = 4
		)


	def get_items(self, filters=None, limit=None):
		base_filters = {
			'published': 1
		}

		if filters:
			base_filters.update(filters)

		items = frappe.get_all('Hub Item', fields=self.fields, filters=filters, limit=limit)

		return self.post_process_item_details(items)


	def post_process_item_details(self, items):
		items = self.get_item_details_and_company_name(items)
		items = self.fix_image_urls(items)
		items = self.get_item_view_count(items)

		return items

	def fix_image_urls(self, items):
		url = frappe.utils.get_url()

		for item in items:
			# convert relative path to absolute path
			if item.image and item.image.startswith('/files/'):
				item.image = url + item.image

		return items

	def get_item_details_and_company_name(self, items):
		for item in items:
			res = frappe.db.get_all('Hub Item Review', fields=['AVG(rating) as average_rating, count(rating) as no_of_ratings'], filters={
				'parenttype': 'Hub Item',
				'parentfield': 'reviews',
				'parent': item.name
			})[0]

			item.average_rating = res['average_rating']
			item.no_of_ratings = res['no_of_ratings']

			if item.hub_seller:
				company, country, city = frappe.db.get_value('Hub Seller', item.hub_seller, ['company', 'country', 'city'])

				item.company = company
				item.country = country
				item.city = city

		return items

	def get_item_view_count(self, items):
		hub_item_names = [d.name for d in items]

		result = frappe.get_all('Hub Log',
			fields=['count(name) as view_count', 'reference_hub_item'],
			filters={
				'type': 'Hub Item View',
				'reference_hub_item': ['in', hub_item_names]
			},
			group_by='reference_hub_item'
		)

		view_count_map = {}
		for r in result:
			view_count_map[r.reference_hub_item] = r.view_count

		for item in items:
			item.view_count = view_count_map.get(item.name, 0)

		return items
