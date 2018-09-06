import requests
import frappe
from hub.hub.utils import save_remote_file_locally

def execute():
	for item in frappe.db.get_all('Hub Item', fields=['name', 'image']):
		image_url = item.image

		print('item', item.name)

		if not image_url: continue

		if image_url.startswith('/files/'): continue

		if image_url.startswith('//'):
			image_url = 'http:' + image_url

		invalid_url = False
		try:
			image_file = save_remote_file_locally(image_url, 'Hub Item', item.name)
			if image_file:
				frappe.db.set_value('Hub Item', item.name, 'image', image_file.file_url, update_modified=False)
		except requests.exceptions.ConnectionError:
			invalid_url = True
		except requests.exceptions.MissingSchema:
			invalid_url = True

		if not image_file:
			invalid_url = True

		if invalid_url:
			frappe.db.set_value('Hub Item', item.name, 'image', '', update_modified=False)

		frappe.db.commit()

