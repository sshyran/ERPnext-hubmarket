from __future__ import print_function, unicode_literals
import frappe, json
from frappe import _
from frappe.utils import now, add_years, random_string
from frappe.website.utils import is_signup_enabled

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

def get_company_details(access_token, args):
	hub_company = frappe.get_doc("Hub Company", {"name": args["company_id"]})
	return {"company_details": hub_company.as_dict()}

def get_all_users(access_token):
	users = frappe.get_all("Hub User", fields=["hub_user", "country"])
	return {"users": users}

def get_user(access_token):
	return frappe.get_doc("Hub User", {"access_token": access_token})


seller_fields = ["site_name", "seller_city", "seller_description"]
publishing_fields = ["publish", "publish_pricing", "publish_availability"]

response_item_fields = ["item_code", "item_name", "item_group", "description",
	"image", "stock_uom"] # creation_at_client, request_count

item_fields_to_update = ["price", "currency", "stock_qty"]

@frappe.whitelist(allow_guest=True)
def pre_reg(site_name, protocol, route):

	redirect_url = protocol + site_name + route
	doc = frappe.get_doc({
		'doctype': 'OAuth Client',
		'app_name': site_name,
		'scopes': 'all openid',
		'default_redirect_uri': redirect_url,
		'redirect_uris': redirect_url,
		'response_type': 'Token',
		'grant_type': 'Implicit',
		'skip_authorization': 1
	})

	doc.insert(ignore_permissions=True)

	return {
		"client_id": doc.client_id,
		"redirect_uri": redirect_url
	}

### Commands
@frappe.whitelist(allow_guest=True)
def sign_up(email, full_name, redirect_to):
	# Check is signup enabled
	if not is_signup_enabled():
		frappe.throw(_('Sign Up is disabled'), title='Not Allowed')

	# Check if registered (exists)
	user = frappe.db.get("User", {"email": email})
	if user:
		if user.disabled:
			return 0, _("Registered but disabled")
		else:
			return 0, _("Already Registered")
	else:
		if frappe.db.sql("""select count(*) from tabUser where
			HOUR(TIMEDIFF(CURRENT_TIMESTAMP, TIMESTAMP(modified)))=1""")[0][0] > 300:

			frappe.respond_as_web_page(_('Temperorily Disabled'),
				_('Too many users signed up recently, so the registration is disabled. Please try back in an hour'),
				http_status_code=429)

		from frappe.utils import random_string
		user = frappe.get_doc({
			"doctype":"User",
			"email": email,
			"first_name": full_name,
			"enabled": 1,
			"new_password": random_string(10),
			"user_type": "Website User"
		})
		user.flags.ignore_permissions = True
		user.insert()

		# set default signup role as per Portal Settings
		default_role = frappe.db.get_value("Portal Settings", None, "default_role")
		if default_role:
			user.add_roles(default_role)

		if redirect_to:
			frappe.cache().hset('redirect_after_login', user.name, redirect_to)

		# TODO: Create a Hub Profile

		user.send_welcome_mail_to_user()
		return 1, _("Please check your email for verification")
