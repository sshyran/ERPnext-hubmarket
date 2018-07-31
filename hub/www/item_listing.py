import frappe

from hub.paginator import Paginator


def get_context(context):
    fields = ['published', 'route', 'image', 'name', 'company_name', 'price', 'stock_qty', 'currency', '`tabHub Item Review`.content', 'count(`tabHub Item Review`.content) as reviews_count']
    group_by = 'name'
    filters = {'published': 1}
    page_number = int(frappe.local.request.args.get('page_number', 1))
    paginator = Paginator('Hub Item', page_number=page_number, fields=fields, filters=filters, order_by='name', group_by=group_by)
    context.items = paginator.get_page()
    context.paginator = paginator
    context.no_breadcrumbs = False
    context.show_search = True
    context.add_next_prev_links = True
