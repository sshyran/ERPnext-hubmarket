import frappe


def get_context(context):
	companies = frappe.get_all("Hub Company", fields="country")
	region_list = []
	context.region_company_list ={}
	region_list = set([company.country for company in companies])
	for region in region_list:
		context.region_companies = frappe.db.get_all("Hub Company", filters={'country':region}, fields="name")
		context.region_company_list[region] = context.region_companies
