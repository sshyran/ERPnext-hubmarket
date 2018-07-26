import frappe


def get_context(context):
    context.companies = frappe.db.get_all("Hub Company", filters={}, fields="country")
    context.region_list = []

    for company in context.companies:
    	if company.country not in context.region_list:
    		context.region_list.append(company.country)