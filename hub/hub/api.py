# Copyright (c) 2015, Web Notes Technologies Pvt. Ltd. and Contributors and contributors
# For license information, please see license.txt

import frappe, json, requests, os
from frappe.utils import now, add_years

user_config_fields = ["enabled"]
user_profile_fields = ["hub_user_name", "hub_user_email", "country"]
seller_fields = ["company", "site_name", "seller_city", "seller_description"]
publishing_fields = ["publish", "publish_pricing", "publish_availability"]

base_fields_for_items = ["item_code", "item_name", "item_group", "description",
	"image", "stock_uom"]

item_fields_to_update = ["price", "currency", "stock_qty"]

### Commands
@frappe.whitelist(allow_guest=True)
def register(args_data):
	"""Register on the hub."""
	args = json.loads(args_data)
	if frappe.get_all("Hub User", filters = {"hub_user_email": args["hub_user_email"]}):
		# Renabling user
		return

	# weagsdvkebarndf

	hub_user = frappe.new_doc("Hub User")
	for key in user_profile_fields + user_config_fields + ["site_name", "seller_city", "seller_description"]:
		hub_user.set(key, args[key])
	hub_user.insert(ignore_permissions=True)

	hub_company = frappe.new_doc("Hub Company")
	for key in ["hub_user_name", "country"] + seller_fields:
		hub_company.set(key, args[key])
	hub_company.insert(ignore_permissions=True)

	# set created company link for user
	hub_user.set("company", args["company"])
	hub_user.enabled = 1
	hub_user.last_sync_datetime = add_years(now(), -10)
	hub_user.save(ignore_permissions=True)

	response = hub_user.as_dict()
	return response

@frappe.whitelist(allow_guest=True)
def call_method(access_token, method, message, debug = False):
	if not debug:
		args = json.loads(message)
		if args:
			result = globals()[method](access_token, args) or {}
		else:
			result = globals()[method](access_token) or {}
		now_time = now()
		response = {"last_sync_datetime": now_time}
		response.update(result)
		return frappe._dict(response)
	else:
		try:
			args = json.loads(message)
			if args:
				result = globals()[method](access_token, args) or {}
			else:
				result = globals()[method](access_token) or {}
			now_time = now()
			response = {"last_sync_datetime": now_time}
			response.update(result)
			return frappe._dict(response)
		except:
			print("Server Exception")
			print(frappe.get_traceback())

# Hub User API
def update_user_details(access_token, args):
	hub_user = get_user(access_token)
	return hub_user.update_details(args)

def update_items(access_token, args):
	hub_user = get_user(access_token)
	return hub_user.update_items(args)

def update_item_fields(access_token, args):
	hub_user = get_user(access_token)
	return hub_user.update_item_fields(args)

def unpublish_all_items_of_user(access_token):
	hub_user = get_user(access_token)
	return hub_user.unpublish_all_items()

def delete_all_items_of_user(access_token):
	hub_user = get_user(access_token)
	return hub_user.delete_all_items()

def unregister_user(access_token):
	hub_user = get_user(access_token)
	return hub_user.unregister()

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
	for key in user_profile_fields + ["site_name", "seller_city"]:
		item.set(key, hub_user.get(key))
	item.published = 1
	item.save(ignore_permissions=True)

def delete_item(access_token, args):
	hub_user = get_user(access_token)
	item_code = args["item_code"]
	item = frappe.get_doc("Hub Item", {"hub_user_name": hub_user.name, "item_code":item_code})
	frappe.delete_doc('Hub Item', item.name, ignore_permissions=True)

# Hub Message
def enqueue_message(access_token, args):
	message = frappe.new_doc("Hub Outgoing Message")

	message.type = args["message_type"]
	message.method = args["method"]
	message.arguments = args["arguments"]

	receiver_user = frappe.get_doc("Hub User", {"hub_user_email": args["receiver_email"]})
	message.receiver_site = receiver_user.site_name
	message.now = args["method"] or 0

	message.save(ignore_permissions=True)
	return 1

def get_message_status(access_token, args):
	msg_doc = frappe.get_doc("Hub Outgoing Message", {"name": args["message_id"]})
	return msg_doc.status

### Queries
def get_items(access_token, args):
	"""Returns list of items by filters"""
	# args["text"]=None, args["category"]=None, args["company"]=None, args["country"]=None, args["start"]=0, args["limit"]=50
	hub_user = get_user(access_token)
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

	fields = base_fields_for_items + user_profile_fields + ["company", "site_name", "seller_city"]

	if hub_user.publish_pricing:
		fields += ["price", "currency", "formatted_price"]
	if hub_user.publish_availability:
		fields += ["stock_qty"]
	items = frappe.get_all("Hub Item", fields=fields, filters=filters, or_filters=or_filters,
		limit_start = args["start"], limit_page_length = args["limit"])
	return {"items": items}

def get_all_companies(access_token):
	all_company_fields = ["company", "hub_user_name", "country", "seller_city", "site_name", "seller_description"]
	companies = frappe.get_all("Hub Company", fields=all_company_fields)
	return {"companies": companies}

def get_categories(access_token):
	categories = frappe.get_all("Hub Category", fields=["category_name"])
	return {"categories": categories}

def get_all_users(access_token):
	users = frappe.get_all("Hub User", fields=["hub_user_name", "country"])
	return {"users": users}

def get_user(access_token):
	return frappe.get_doc("Hub User", {"access_token": access_token})

def get_user_details(access_token, user_name):
	return frappe.get_doc("Hub User", {"hub_user_name": user_name})

