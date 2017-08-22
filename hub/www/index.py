import frappe

def get_context(context):
	fields = ['published', 'route', 'image', 'name', 'company', 'price']
	context.items = frappe.get_all('Hub Item', fields=fields)
	context.no_breadcrumbs = False