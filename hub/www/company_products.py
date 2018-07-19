import frappe

from hub.paginator import Paginator

def get_context(context):
    company_name = frappe.local.request.args.get('company_name')
    context.company = frappe.get_value("Hub Company", company_name, fieldname=["name", "company_logo"], as_dict=True)
    if not context.company:
        raise frappe.DoesNotExistError()
    fields = ['published', 'route', 'image', 'name', 'company_name', 'price', 'stock_qty', 'currency']
    filters = {'published': 1, 'company_name': company_name}
    page_number = int(frappe.local.request.args.get('page_number', 1))
    paginator = Paginator('Hub Item', page_number=page_number, fields=fields, filters=filters, order_by='name')
    context.items = paginator.get_page()
    context.paginator = paginator
    context.company_name = company_name
    context.no_breadcrumbs = False
    context.show_search = True
    context.title = "%s %s" % (company_name, 'Products')
