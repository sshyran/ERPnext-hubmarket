import frappe

def get_context(context):
    name = frappe.local.request.args['name']
    items = frappe.get_all('Hub Item', fields=['*'], filters={'name': name})
    if len(items) == 0:
        raise frappe.DoesNotExistError()
    context.item = items[0]
    context.title = context.item.name
