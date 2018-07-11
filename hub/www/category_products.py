import frappe

def get_context(context):
    category_name = frappe.local.request.args['category_name']
    fields = ['published', 'route', 'image', 'name', 'company_name', 'price', 'stock_qty', 'currency']
    filters = {'published': 1, 'hub_category': category_name}
    context.items = frappe.get_list('Hub Item', fields=fields, filters=filters, start=0, limit=20)
    context.no_breadcrumbs = False
    context.show_search = True
    context.title = "%s %s" % (category_name, 'Products')
