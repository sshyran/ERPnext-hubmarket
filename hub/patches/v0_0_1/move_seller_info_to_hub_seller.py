import frappe

def execute():
	hub_items = frappe.get_all('Hub Item', fields=['name', 'seller', 'company_name', 'country', 'seller_city'])
	frappe.reload_doc('hub', 'doctype', 'hub_seller')
	frappe.reload_doc('hub', 'doctype', 'hub_seller_activity')
	frappe.reload_doc('hub', 'doctype', 'hub_seller_message')
	frappe.reload_doc('hub', 'doctype', 'hub_item')
	for item in hub_items:

		if not item.seller:
			continue

		hub_seller = frappe.get_doc({
			'doctype': 'Hub Seller',
			'user': item.seller,
			'company': item.company_name,
			'country': item.country,
			'city': item.seller_city
		})

		hub_seller.insert(ignore_if_duplicate=True)
		frappe.db.set_value('Hub Item', item.name, 'hub_seller', hub_seller.name, update_modified=False)
