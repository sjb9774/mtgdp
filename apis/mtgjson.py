import zipfile
import json
import requests
import os


class MtgJsonApiClient:

	API_URL = 'https://mtgjson.com/api/'
	FILENAME_ALL_PRINTINGS = 'AllPrintings.json'
	FILENAME_ALL_PRINTINGS_ARCHIVED = 'AllPrintings.json.zip'
	FILENAME_ALL_PRICES = 'AllPrices.json'
	FILENAME_ALL_PRICES_ARCHIVED = 'AllPrices.json.zip'

	def __init__(self, version='5'):
		self.version = version

	def __write_temp_file(self, file_name, content):
		with open(f'/tmp/{file_name}', 'wb') as f:
			f.write(content)

	def __unzip_file(self, file_src, file_dest):
		with zipfile.ZipFile(file_src, 'r') as f:
			f.extractall(file_dest)

	def __get_json_file_contents(self, json_file_path):
		with open(json_file_path, 'r') as f:
			data = json.loads(f.read())
		return data

	def __download_file_from_api(self, filename):
		response = self.get_api_response(filename)
		self.__write_temp_file(filename, response.content)

	def __get_archive_contents(self, archive_name, unarchived_name, force_refresh=False):
		if not os.path.exists(f'/tmp/{archive_name}') or force_refresh:
			self.__download_file_from_api(archive_name)
			self.__unzip_file(f'/tmp/{archive_name}', f'/tmp/')
		return self.__get_json_file_contents(f'/tmp/{unarchived_name}')

	def get_api_response(self, filename):
		response = requests.get(f'{self.API_URL}/v{self.version}/{filename}')
		return response

	def get_all_printings(self, force_refresh=False):
		return self.__get_archive_contents(
			self.FILENAME_ALL_PRINTINGS_ARCHIVED,
			self.FILENAME_ALL_PRINTINGS,
			force_refresh=force_refresh
		)

	def get_all_prices(self, force_refresh=False):
		return self.__get_archive_contents(
			self.FILENAME_ALL_PRICES_ARCHIVED,
			self.FILENAME_ALL_PRICES,
			force_refresh=force_refresh
		)
