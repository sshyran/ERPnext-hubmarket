import frappe

from hub.paginator import Paginator


def get_context(context):
    fields = ['published', 'route', 'image', 'name', 'company_name', 'price', 'stock_qty', 'currency', '`tabHub Item Review`.content', 'count(`tabHub Item Review`.content) as reviews_count']
    group_by = 'name'
    filters = {'published': 1}
    page_number = int(frappe.local.form_dict.get('page_number', 1))
    search = frappe.local.form_dict.search
    or_filters = None
    if search:
        or_filters = [
            {"name": ["like", "%{0}%".format(search)]},
            {"hub_category": ["like", "%{0}%".format(search)]},
            {"company_name": ["like", "%{0}%".format(search)]}
        ]
    paginator = Paginator('Hub Item', page_number=page_number, fields=fields, filters=filters, order_by='name', group_by=group_by, or_filters=or_filters)
    context.items = paginator.get_page()
    context.paginator = paginator
