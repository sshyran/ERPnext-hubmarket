import frappe

def get_context(context):
    company_name = frappe.local.request.args['company_name']
    fields = ['published', 'route', 'image', 'name', 'company_name', 'price', 'stock_qty', 'currency']
    filters = {'published': 1, 'company_name': company_name}
    context.items = frappe.get_list('Hub Item', fields=fields, filters=filters, start=0, limit=20)
    context.no_breadcrumbs = False
    context.show_search = True
    context.title = "%s %s" % (company_name, 'Products')
