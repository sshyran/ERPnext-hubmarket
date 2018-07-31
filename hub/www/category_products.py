import frappe

from hub.paginator import Paginator

def get_context(context):
    category_name = frappe.local.request.args['category_name']
    category = frappe.get_value('Hub Category', category_name, fieldname="*")
    if not category:
        raise frappe.DoesNotExistError()
    fields = ['image', 'name', 'company_name', 'price', 'stock_qty', 'currency', '`tabHub Item Review`.content', 'count(`tabHub Item Review`.content) as reviews_count']
    group_by = 'name'
    filters = {'published': 1, 'hub_category': category.name}
    page_number = int(frappe.local.request.args.get('page_number', 1))
    paginator = Paginator('Hub Item', page_number=page_number, fields=fields, filters=filters, order_by='name', group_by=group_by)

    context.items = paginator.get_page()
    context.paginator = paginator
    context.category_name = category_name
    context.no_breadcrumbs = False
    context.parents = [{"name": "All categories", "route": "/item-listing/"}, {"name": category.parent_hub_category}]
    context.show_search = True
    context.title = "%s" % (category_name,)
    context.list_heading = "Buy these amazing %s" % (category_name,)
