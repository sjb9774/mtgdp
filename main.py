import csv
from providers.scryfall import ScryfallPricing
import datetime
import os
import json


if __name__ == '__main__':
	now = datetime.datetime.now()
	now_str = now.strftime('%Y-%m-%d_%H:%m:%s')
	pricing_provider = ScryfallPricing()
	for inventory_file in os.listdir('inventory'):
		with open(f'inventory/{inventory_file}', 'r') as inv:
			inventory_content = csv.reader(inv)
			columns = next(inventory_content)
			results = []

			for row in inventory_content:
				pricing = pricing_provider.get_pricing(**dict(zip(columns, row)))
				result = {}
				for i, column in enumerate(columns):
					result[column] = row[i]
				result['pricing'] = pricing
				results.append(result)

		with open(f'pricing/{now_str}-{inventory_file}', 'w+') as results_file:
			results_file.write(json.dumps(results))
