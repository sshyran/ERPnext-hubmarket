import frappe

def execute():
	hub_items = frappe.get_all('Hub Item', fields=['name', 'seller', 'company_name', 'country', 'seller_city'])

	for item in hub_items:
		hub_seller = frappe.get_doc({
			'doctype': 'Hub Seller',
			'user': item.seller,
			'company': item.company_name,
			'country': item.country,
			'city': item.seller_city
		})

		hub_seller.insert(ignore_if_duplicate=True)
		frappe.db.set_value('Hub Item', item.name, 'hub_seller', hub_seller.name, update_modified=False)
