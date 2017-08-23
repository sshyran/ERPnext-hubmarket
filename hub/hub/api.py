# Copyright (c) 2015, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

import frappe, json, requests, os
from frappe.utils import now

user_config_fields = ["enabled"]
user_profile_fields = ["hub_user_name", "email", "country"]
seller_fields = ["company", "seller_website", "seller_city", "seller_description"]
publishing_fields = ["publish", "publish_pricing", "publish_availability"]

### Commands
@frappe.whitelist(allow_guest=True)
def register(args_data):
	"""Register on the hub."""
	args = json.loads(args_data)
	if frappe.get_all("Hub User", filters = {"email": args["email"]}):
		return

	hub_user = frappe.new_doc("Hub User")
	for key in user_profile_fields + user_config_fields + ["seller_website", "seller_city", "seller_description"]:
		hub_user.set(key, args[key])
	hub_user.insert(ignore_permissions=True)

	hub_company = frappe.new_doc("Hub Company")
	for key in ["hub_user_name", "country"] + seller_fields:
		hub_company.set(key, args[key])
	hub_company.insert(ignore_permissions=True)

	# set created company link for user
	hub_user.set("company", args["company"])
	hub_user.save(ignore_permissions=True)

	response = hub_user.as_dict()
	# response["hub_public_key_pem"] = hub_public_key_pem
	return response

@frappe.whitelist(allow_guest=True)
def call_method(access_token, method, message):
	try:
		args = json.loads(message)
		if args:
			return globals()[method](access_token, args)
		else:
			return globals()[method](access_token)
	except:
		print(frappe.get_traceback())

# Hub User API
def unregister(access_token):
	hub_user = get_user(access_token)
	hub_user.delete_all_items_of_user()
	# delete user company
	company_name = frappe.get_all('Hub Company', filters={"hub_user_name": hub_user.name})[0]["name"]
	frappe.delete_doc('Hub Company', company_name, ignore_permissions=True)

	# TODO: Delete all of user's transactions

	# Delete user
	frappe.delete_doc('Hub User', hub_user.name, ignore_permissions=True)

def update_user_details(access_token, args):
	hub_user = get_user(access_token)
	return hub_user.update_user_details(args)

def update_items(access_token, args):
	hub_user = get_user(access_token)
	return hub_user.update_items(args)

def add_item_fields(access_token, args):
	hub_user = get_user(access_token)
	return hub_user.add_item_fields(args)

def remove_item_fields(access_token, args):
	hub_user = get_user(access_token)
	return hub_user.remove_item_fields(args)

def unpublish_all_items_of_user(access_token):
	hub_user = get_user(access_token)
	return hub_user.unpublish_all_items_of_user()

def delete_all_items_of_user(access_token):
	hub_user = get_user(access_token)
	return hub_user.delete_all_items_of_user()

# Hub Item API
def update_item(access_token, args):
	hub_user = get_user(access_token)
	item_code = args["item_code"]
	item_dict = json.loads(args["item_dict"])
	item = frappe.get_doc("Hub Item", {"hub_user_name": hub_user.name, "item_code":item_code})
	return item.update_item_details(item_dict)

def insert_item(access_token, args):
	hub_user = get_user(access_token)
	item = frappe.new_doc("Hub Item")
	item_dict = json.loads(args["item_dict"])
	item.update_item_details(item_dict)
	for key in user_profile_fields + ["seller_website", "seller_city"]:
		item.set(key, hub_user.get(key))
	item.published = 1
	item.save(ignore_permissions=True)

def delete_item(access_token, args):
	hub_user = get_user(access_token)
	item_code = args["item_code"]
	item = frappe.get_doc("Hub Item", {"hub_user_name": hub_user.name, "item_code":item_code})
	frappe.delete_doc('Hub Item', item.name, ignore_permissions=True)


### Queries
def get_items(access_token, args):
	"""Returns list of items by filters"""
	# args["text"]=None, args["category"]=None, args["company"]=None, args["country"]=None, args["start"]=0, args["limit"]=50
	get_user(access_token)
	or_filters = [
		{"item_name": ["like", "%{0}%".format(args["text"])]},
		{"description": ["like", "%{0}%".format(args["text"])]}
	]
	filters = {
		"published": "1"
	}
	if args["category"]:
		filters["item_group"] = args["category"]
	if args["company"]:
		filters["company"] = args["company"]
	if args["country"]:
		filters["country"] = args["country"]
	return frappe.get_all("Hub Item", fields=["item_code", "item_name", "item_group", "description", "image",
		"hub_user_name", "email", "country", "seller_city", "company", "seller_website", "standard_rate"],
			filters=filters, or_filters=or_filters, limit_start = args["start"], limit_page_length = args["limit"])

def get_all_companies(access_token):
	all_company_fields = ["company", "hub_user_name", "country", "seller_city", "seller_website", "seller_description"]
	return frappe.get_all("Hub Company", fields=all_company_fields)

def get_user(access_token):
	return frappe.get_doc("Hub User", {"access_token": access_token})

def get_all_users(access_token):
	return frappe.get_all("Hub User", fields=["hub_user_name", "country"])

def get_categories(access_token):
	return frappe.get_all("Hub Category", fields=["category_name"])

def get_user_details(access_token, user_name):
	return frappe.get_doc("Hub User", {"hub_user_name": user_name})

