# Copyright (c) 2015, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

from __future__ import print_function, unicode_literals
import frappe, json
from frappe.utils import now, add_years, random_string

seller_fields = ["site_name", "seller_city", "seller_description"]
publishing_fields = ["publish", "publish_pricing", "publish_availability"]

response_item_fields = ["item_code", "item_name", "item_group", "description",
	"image", "stock_uom"] # creation_at_client, request_count

item_fields_to_update = ["price", "currency", "stock_qty"]

### Commands
@frappe.whitelist(allow_guest=True)
def register(email):
	"""Register on the hub."""
	try:
		if email.lower() == 'administrator':
			frappe.throw(_('Please login with another user'))
			return

		password = random_string(16)

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
				'first_name': email.split("@")[0],
				'new_password': password
			})

			user.append_roles("System Manager")
			user.flags.delay_emails = True
			user.insert(ignore_permissions=True)

		return {
			'email': email,
			'password': password
		}

	except:
		print("Hub Server Exception")
		print(frappe.get_traceback())

		return {
			'error': "Hub Server Exception",
			'traceback': frappe.get_traceback()
		}

### Queries
def get_items(access_token, args):
	"""Returns list of items by filters"""
	# args["text"]=None, args["category"]=None, args["company"]=None, args["country"]=None, args["start"]=0, args["limit"]=50
	hub_user = get_user(access_token)
	fields = response_item_fields + ['hub_user', 'country', "company_id", "company_name", "site_name", "seller_city"]
	filters = {
		"published": "1",
		"hub_user": ["!=", hub_user.name]
	}

	if hub_user.publish_pricing:
		fields += ["price", "currency", "formatted_price"]
	if hub_user.publish_availability:
		fields += ["stock_qty"]

	if args["item_codes"]:
		item_codes = args["item_codes"]
		items = []
		for d in item_codes:
			item_code = d[4:]
			f = filters
			f["item_code"] = item_code
			items.append(frappe.get_all("Hub Item", fields=fields, filters=f)[0])
		return {"items": items}

	or_filters = [
		{"item_name": ["like", "%{0}%".format(args["text"])]},
		{"description": ["like", "%{0}%".format(args["text"])]}
	]

	# if args["hub_category"]:
	# 	filters["hub_category"] = args["hub_category"]
	if args["company_name"]:
		filters["company_name"] = args["company_name"]
	if args["country"]:
		filters["country"] = args["country"]

	order_by = ''
	if args["order_by"]:
		order_by = args["order_by"]

	items = frappe.get_all("Hub Item", fields=fields, filters=filters, or_filters=or_filters,
		limit_start = args["start"], limit_page_length = args["limit"], order_by=order_by)

	return {"items": items}

def get_all_companies(access_token):
	all_company_fields = ["company_name", "hub_user", "country", "seller_city", "site_name", "seller_description"]
	companies = frappe.get_all("Hub Company", fields=all_company_fields)
	return {"companies": companies}

def get_categories(access_token):
	lft, rgt = frappe.db.get_value('Hub Category', {'name': 'All Categories'}, ['lft', 'rgt'])
	categories = frappe.db.sql('''
		select
			hub_category_name from `tabHub Category`
		where
			lft >= {lft} and
			rgt <= {rgt}
	'''.format(lft=lft, rgt=rgt), as_dict=1)
	# # TODO: Send catgory Object
	# categories = frappe.get_all("Hub Category", fields=["category_name"])
	return {"categories": categories}

def get_item_details(access_token, args):
	hub_item = frappe.get_doc("Hub Item", {"item_code": args["item_code"]})
	return {"item_details": hub_item.as_dict()}

def get_company_details(access_token, args):
	hub_company = frappe.get_doc("Hub Company", {"name": args["company_id"]})
	return {"company_details": hub_company.as_dict()}

def get_all_users(access_token):
	users = frappe.get_all("Hub User", fields=["hub_user", "country"])
	return {"users": users}

def get_user(access_token):
	return frappe.get_doc("Hub User", {"access_token": access_token})
