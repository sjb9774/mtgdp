from webapp.app import app, get_price_filenames
import json
from operator import itemgetter
from flask import render_template


@app.route('/pricing/chart/<set_code>/<collector_number>')
def get_chart_pricing(set_code, collector_number):
	pricing_files = get_price_filenames(provider_name='tcgplayer', set_code=set_code)
	pricing_json = []
	i = 0
	for filename in pricing_files:
		i += 1
		with open(filename, 'r') as f:
			pricing_data = json.loads(f.read())
			for price_datum in pricing_data:
				if price_datum.get('collector_number') == collector_number and price_datum.get('pricing').get('subTypeName') == 'Normal':
					# TODO: Break out foil and normal pricing
					pricing_json.append(price_datum)
		pricing_json = sorted(pricing_json, key=itemgetter('date'))
	return json.dumps(pricing_json)


@app.route('/prices/<set_code>/<collector_number>')
def pricing_page(set_code, collector_number):
	return render_template('index.html', set_code=set_code, collector_number=collector_number)