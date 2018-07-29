import frappe


def get_context(context):
    context.companies = frappe.get_all("Hub Company", fields="name")
    context.products_count = {}
    for company in context.companies:
        # TODO: This makes db call for each company which isn't performant. Keep a field product count on company.
    	context.products_count[company.name] = frappe.db.count("Hub Item", filters={'company_name':company.name})
