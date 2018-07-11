import frappe

from hub.paginator import Paginator


def get_context(context):
    fields = ['published', 'route', 'image', 'name', 'company_name', 'price', 'stock_qty', 'currency']
    filters = {'published': 1}
    page_number = int(frappe.local.request.args.get('page_number', 1))
    paginator = Paginator('Hub Item', page_number=page_number, fields=fields, filters=filters, order_by='name')
    context.items = paginator.get_page()
    context.paginator = paginator
    context.no_breadcrumbs = False
    context.show_search = True
    context.add_next_prev_links = True
