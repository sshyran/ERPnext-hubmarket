import frappe

def get_context(context):
	"""
	get the company related to country
	"""
	region = frappe.local.request.args.get('name')
	context.companies = frappe.db.get_values("Hub Company", filters={'country':region}, as_dict=True)
