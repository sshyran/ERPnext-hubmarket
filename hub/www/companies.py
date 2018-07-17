import frappe


def get_context(context):
    context.companies = frappe.db.get_values("Hub Company", filters={}, as_dict=True)
