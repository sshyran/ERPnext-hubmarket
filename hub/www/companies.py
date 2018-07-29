import frappe


def get_context(context):
    context.companies = frappe.db.get_values("Hub Company", filters={}, as_dict=True)
    products = {}
    context.products_count = {}
    for company in context.companies:
    	products[company.name] = frappe.db.get_all("Hub Item", filters={'company_name':company.name}, fields="name")
    for key,values in products.items():
    	context.products_count[key] = len(values)
