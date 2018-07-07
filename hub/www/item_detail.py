import frappe

def get_context(context):
	context.pk = frappe.local.request.args['pk']
