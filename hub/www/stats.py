from __future__ import unicode_literals
import frappe
from frappe import _
import json
from frappe.desk.doctype.dashboard_chart.dashboard_chart import get

def get_context(context):
	context.visitors = frappe.get_list("Hub Log", filters={'type': 'Hub Item View'}, fields=['count(name) as count'], ignore_permissions=True)[0]
	context.products = frappe.get_list("Hub Item", filters={'published': 1}, fields=['count(name) as count'], ignore_permissions=True)[0]
	context.users = frappe.get_list("User", fields=['count(name) as count'], ignore_permissions=True)[0]
	context.communications = frappe.get_list("Hub Chat Message", fields=['count(name) as count'], ignore_permissions=True)[0]
	context.chart_title='Visitors'

@frappe.whitelist(allow_guest=True)
def get_dashboard_data(chart=None, no_cache = None, from_date=None, to_date=None, refresh = None):
	chart  = json.loads(chart)
	validate_document_type(chart.get('document_type'))
	data = get(chart = chart, no_cache = no_cache, from_date=from_date, to_date=to_date)
	return data

def validate_document_type(ref_doc):
	if ref_doc not in ["Hub Chat Message", "Hub Item", "Hub Log"]:
		frappe.respond_as_web_page(_("Invalid Input"),
			_("Unauthorized webpage access"),
			indicator_color='red', http_status_code=401)