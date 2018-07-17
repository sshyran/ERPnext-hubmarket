import frappe

from hub.paginator import Paginator

def get_context(context):
    company_name = frappe.local.request.args.get('name')
    context.company = frappe.get_value("Hub Company", company_name, fieldname="*")
    if not context.company:
        raise frappe.DoesNotExistError()
    filters = {'published': 1, 'company_name': company_name}
    context.num_items = frappe.db.count('Hub Item', filters=filters)
