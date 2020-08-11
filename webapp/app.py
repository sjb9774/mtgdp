from flask import Flask
import os
app = Flask(__name__)


def get_pricing_directory():
	return 'pricing'


def get_price_filenames(provider_name=None, date=None, set_code=None):
	filenames = []
	for date_dir in os.listdir(get_pricing_directory()):
		relative_date_dir = f"{get_pricing_directory()}{os.sep}{date_dir}"
		for filename in os.listdir(relative_date_dir):
			relative_filename = f"{relative_date_dir}{os.sep}{filename}"
			if set_code and set_code.lower() not in filename:
				continue
			if provider_name and provider_name.lower() not in filename:
				continue
			filenames.append(relative_filename)
	return filenames
