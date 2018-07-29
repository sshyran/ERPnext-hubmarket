import frappe

def get_context(context):
	"""
	get the company related to country
	"""
	country = frappe.local.request.args.get('name')
	context.companies = frappe.get_all("Hub Company", filters={'country': country})
