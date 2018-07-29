import itertools

import frappe


def get_context(context):
    companies = frappe.get_all("Hub Company", fields="name, country", order_by="country, name")
    context.companies_grouped_by_country = itertools.groupby(companies, key=lambda x: x['country'])
