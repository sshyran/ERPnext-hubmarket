# Copyright (c) 2015, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import json
from frappe import _
from frappe.utils import random_string
from six import string_types

from .curation import (
	get_item_fields,
	post_process_item_details,
	post_process_items,
	get_items_by_country,
	get_items_with_images,
	get_random_items_from_each_hub_seller,
	get_items_from_all_categories,
	get_items_from_hub_seller,
	get_items_from_codes
)

from .log import (
	update_hub_seller_activity,
	update_hub_item_view_log,
	get_item_view_count,
	mutate_hub_item_favourite_log,
	get_favourite_logs_seller,
	get_favourite_item_logs_seller
)


@frappe.whitelist(allow_guest=True)
def register(profile):
	"""Register on the hub."""
	try:
		profile = frappe._dict(json.loads(profile))

		password = random_string(16)
		email = profile.company_email
		company_name = profile.company

		if frappe.db.exists('User', email):
			user = frappe.get_doc('User', email)
			user.enabled = 1
			user.new_password = password
			user.save(ignore_permissions=True)
		else:
			# register
			user = frappe.get_doc({
				'doctype': 'User',
				'email': email,
				'first_name': company_name,
				'new_password': password
			})

			user.append_roles("System Manager")
			user.flags.delay_emails = True
			user.insert(ignore_permissions=True)

			seller_data = profile.update({
				'enabled': 1,
				'doctype': 'Hub Seller',
				'user': email,
				'hub_seller_activity': [{'type': 'Created'}]
			})
			seller = frappe.get_doc(seller_data)
			seller.insert(ignore_permissions=True)

		return {
			'email': email,
			'password': password
		}

	except Exception as e:
		print("Hub Server Exception")
		print(frappe.get_traceback())

		frappe.throw(frappe.get_traceback())

		# return {
		# 	'error': "Hub Server Exception",
		# 	'traceback': frappe.get_traceback()
		# }


@frappe.whitelist()
def update_profile(hub_seller, updated_profile):
	'''
	Update Seller Profile
	'''

	updated_profile = json.loads(updated_profile)

	profile = frappe.get_doc("Hub Seller", hub_seller)
	if updated_profile.get('company_description') != profile.company_description:
		profile.company_description = updated_profile.get('company_description')

	profile.save()

	return profile.as_dict()

@frappe.whitelist(allow_guest=True)
def get_data_for_homepage(country=None):
	'''
	Get curated item list for the homepage.
	'''
	fields = get_item_fields()
	items = []

	items_by_country = []
	if country:
		items_by_country += get_items_by_country(country)

	items_with_images = get_items_with_images()

	return dict(
		items_by_country=items_by_country,
		items_with_images=items_with_images or [],
		random_items=get_random_items_from_each_hub_seller() or [],
		category_items=get_items_from_all_categories() or []
	)


@frappe.whitelist(allow_guest=True)
def get_items(keyword='', hub_seller=None, filters={}):
	'''
	Get items by matching it with the keywords field
	'''
	fields = get_item_fields()

	if isinstance(filters, string_types):
		filters = json.loads(filters)

	if keyword:
		filters['keywords'] = ['like', '%' + keyword + '%']

	if hub_seller:
		filters["hub_seller"] = hub_seller

	items = frappe.get_all('Hub Item', fields=fields, filters=filters)

	items = post_process_item_details(items)

	return items


@frappe.whitelist()
def add_hub_seller_activity(hub_seller, activity_details):
	return update_hub_seller_activity(hub_seller, activity_details)


@frappe.whitelist(allow_guest=True)
def get_hub_seller_page_info(hub_seller='', company=''):
	if not hub_seller and company:
		hub_seller = frappe.db.get_all(
			"Hub Seller", filters={'company': company})[0].name
	else:
		frappe.throw('No Seller or Company Name received.')

	return {
		'profile': get_hub_seller_profile(hub_seller),
		'items': get_items_from_hub_seller(hub_seller)
	}


@frappe.whitelist()
def get_hub_seller_profile(hub_seller=''):
	profile = frappe.get_doc("Hub Seller", hub_seller).as_dict()

	if profile.hub_seller_activity:
		for log in profile.hub_seller_activity:
			log.pretty_date = frappe.utils.pretty_date(log.get('creation'))

	return profile


@frappe.whitelist(allow_guest=True)
def get_item_details(hub_item_code):
	fields = get_item_fields()
	items = frappe.get_all('Hub Item', fields=fields, filters={'name': hub_item_code})

	if not items:
		return None

	items = post_process_item_details(items)
	item = items[0]

	# frappe.session.user is the hub_seller if not Guest
	hub_seller = frappe.session.user if frappe.session.user != 'Guest' else None

	if hub_seller:
		logs = get_favourite_item_logs_seller(hub_item_code, hub_seller)
		if len(logs):
			item['favourited'] = 1

	item['view_count'] = get_item_view_count(hub_item_code)

	if hub_seller:
		update_hub_item_view_log(hub_item_code, hub_seller)

	return item


@frappe.whitelist(allow_guest=True)
def get_item_reviews(hub_item_code):
	reviews = frappe.db.get_all('Hub Item Review', fields=['*'],
	filters={
		'parenttype': 'Hub Item',
		'parentfield': 'reviews',
		'parent': hub_item_code
	}, order_by='modified desc')

	return reviews or []


@frappe.whitelist()
def add_item_to_seller_favourites(hub_item_code, hub_seller):
	# Cardinal sin
	return mutate_hub_item_favourite_log(hub_item_code, hub_seller, 1)


@frappe.whitelist()
def remove_item_from_seller_favourites(hub_item_code, hub_seller):
	# Cardinal sin
	return mutate_hub_item_favourite_log(hub_item_code, hub_seller, 0)


@frappe.whitelist()
def add_item_review(hub_item_code, review):
	'''Adds a review record for Hub Item and limits to 1 per user'''
	new_review = json.loads(review)

	item_doc = frappe.get_doc('Hub Item', hub_item_code)
	existing_reviews = item_doc.get('reviews')

	# dont allow more than 1 review
	for review in existing_reviews:
		if review.get('user') == new_review.get('user'):
			return dict(error='Cannot add more than 1 review for the user {0}'.format(new_review.get('user')))

	item_doc.append('reviews', new_review)
	item_doc.save()

	return item_doc.get('reviews')[-1]


@frappe.whitelist(allow_guest=True)
def get_categories(parent='All Categories'):
	# get categories info with parent category and stuff
	categories = frappe.get_all('Hub Category',
								filters={'parent_hub_category': parent},
								fields=['name'],
								order_by='name asc')

	return categories


@frappe.whitelist()
def get_favourite_items_of_seller(hub_seller):
	item_logs = get_favourite_logs_seller(hub_seller)
	favourite_item_codes = [d.primary_document for d in item_logs]
	return get_items_from_codes(favourite_item_codes)


@frappe.whitelist()
def get_sellers_with_interactions(for_seller):
	'''Return all sellers `for_seller` has sent a message to or received a message from'''

	res = frappe.db.sql('''
		SELECT sender, receiver
		FROM `tabHub Seller Message`
		WHERE sender = %s OR receiver = %s
	''', [for_seller, for_seller])

	sellers = []
	for row in res:
		sellers += row

	sellers = [seller for seller in sellers if seller != for_seller]

	sellers_with_details = frappe.db.get_all('Hub Seller',
											 fields=['name as email', 'company'],
											 filters={'name': ['in', sellers]})

	return sellers_with_details


@frappe.whitelist()
def get_messages(against_seller, against_item):
	'''Return all messages sent between `for_seller` and `against_seller`'''

	for_seller = frappe.session.user

	messages = frappe.db.sql('''
		SELECT name, sender, receiver, content, creation
		FROM `tabHub Seller Message`
		WHERE
			((sender = %(for_seller)s AND receiver = %(against_seller)s) OR
			(sender = %(against_seller)s AND receiver = %(for_seller)s)) AND
			reference_hub_item = %(hub_item_code)s
		ORDER BY creation asc
	''', {'for_seller': for_seller, 'against_seller': against_seller, 'hub_item_code': against_item}, as_dict=True)

	return messages

@frappe.whitelist()
def get_buying_items_for_messages(hub_seller=None):
	if not hub_seller:
		hub_seller = frappe.session.user

	validate_session_user(hub_seller)

	items = frappe.db.get_all('Hub Seller Message',
		fields='reference_hub_item',
		filters={
			'sender': hub_seller,
			'reference_hub_seller': ('!=', hub_seller)
		},
		group_by='reference_hub_item'
	)

	item_names = [item.reference_hub_item for item in items]

	return get_items(filters={
		'hub_item_code': ['in', item_names]
	})

@frappe.whitelist()
def get_selling_items_for_messages(hub_seller=None):
	if not hub_seller:
		hub_seller = frappe.session.user

	validate_session_user(hub_seller)

	items = frappe.db.get_all('Hub Seller Message',
		fields='reference_hub_item',
		filters={
			'receiver': hub_seller,
			'reference_hub_seller': hub_seller
		},
		group_by='reference_hub_item'
	)

	item_names = [item.reference_hub_item for item in items]

	return get_items(filters={
		'hub_item_code': ['in', item_names]
	})


@frappe.whitelist()
def send_message(from_seller, to_seller, message, hub_item):
	validate_session_user(from_seller)

	msg = frappe.get_doc({
		'doctype': 'Hub Seller Message',
		'sender': from_seller,
		'receiver': to_seller,
		'content': message,
		'reference_hub_item': hub_item
	}).insert(ignore_permissions=True)

	return msg

def validate_session_user(user):
	if frappe.session.user != user:
		frappe.throw(_('Not Permitted'), frappe.PermissionError)
