# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "hub"
app_title = "Hub"
app_publisher = "Frappe"
app_description = "Hub"
app_icon = "octicon octicon-globe"
app_color = "orange"
app_email = "hub@erpnext.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/hub/css/hub.css"
# app_include_js = "/assets/hub/js/hub.js"

# include js, css files in header of web template
web_include_css = "/assets/hub/css/hub.css"
# web_include_js = "/assets/hub/js/hub.js"

website_context = {
	# "navbar_search": 1,
	"brand_html": "<img class='navbar-icon' src='/assets/hub/img/hub-logo.png' /><span>Hub Market</span>",
	"copyright": "Hub Market",
	"footer_address": "<br>Discover products",
	"hide_login": 1,
	"favicon": "/assets/hub/img/hub-logo.png",
	"top_bar_items": [
        {"label": "Shop by categories", "right": 1, "url": "/categories/"},
		{"label": "Companies", "child_items": [
			{"label": "Company List", "url": ""}
		], "right": 1},
		{"label": "Products", "child_items": [
			{"label": "Product List", "url": "/item-listing/"}
		], "right": 1},
	]
}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "hub.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "hub.install.before_install"
# after_install = "hub.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "hub.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"hub.tasks.all"
# 	],
# 	"daily": [
# 		"hub.tasks.daily"
# 	],
# 	"hourly": [
# 		"hub.tasks.hourly"
# 	],
# 	"weekly": [
# 		"hub.tasks.weekly"
# 	]
# 	"monthly": [
# 		"hub.tasks.monthly"
# 	]
# }

scheduler_events = {
	"daily": [
		"hub.hub.doctype.hub_user.hub_user.check_last_sync_datetimes"
	],
}

# Testing
# -------

# before_tests = "hub.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
override_whitelisted_methods = {
	"frappe.core.doctype.user.user.sign_up": "hub.hub.api.sign_up"
}

