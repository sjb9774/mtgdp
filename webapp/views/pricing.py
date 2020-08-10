from webapp.app import app


@app.route('pricing/chart/<set_code>/<card_name>')
def get_chart_pricing(set_code, card_name):
	pass
