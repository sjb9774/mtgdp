from webapp.app import app
from webapp.views.home import index
from webapp.views.pricing import get_chart_pricing, pricing_page

app.run(debug=True)
