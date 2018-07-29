import frappe


def get_context(context):
    context.companies = frappe.get_all("Hub Company", fields="name")
    context.products_count = {}
    for company in context.companies:
    	context.products_count[company.name] = frappe.db.count("Hub Item", filters={'company_name':company.name})
