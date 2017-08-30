import frappe

def get_context(context):
	fields = ['published', 'route', 'image', 'name', 'company', 'price', 'stock_qty', 'currency']
	filters = {'published': 1}
	context.items = frappe.get_list('Hub Item', fields=fields, filters=filters, start=0, limit=20)
	context.no_breadcrumbs = False