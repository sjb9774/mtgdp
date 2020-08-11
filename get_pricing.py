#! /usr/bin/env python
from argparse import ArgumentParser
from providers.scryfall import ScryfallPricing
from providers.tcgplayer import TcgPlayerPricing
from recorders.pricerecorder import JSONCardPriceRecorder, DBPriceRecorder
from product.identity import CardIdentity
import json
import datetime
from pathlib import Path


if __name__ == "__main__":
	argparser = ArgumentParser()
	argparser.add_argument('-s', '--set-codes', nargs='+', required=True)
	argparser.add_argument('-p', '--pricing-providers', nargs='+', required=True, choices=['scryfall', 'tcgplayer'])
	args = argparser.parse_args()
	now = datetime.datetime.now()
	date_timestamp = now.strftime('%Y-%m-%d')
	datetime_timestamp = now.strftime('%Y-%m-%d_%H:%M:%S')

	provider_map = {
		'scryfall': ScryfallPricing(),
		'tcgplayer': TcgPlayerPricing()
	}

	for provider in args.pricing_providers:
		pricing_provider = provider_map.get(provider)
		if pricing_provider:
			for set_code in args.set_codes:
				print(f"Retrieving pricing for {set_code} from '{provider}' provider")
				set_pricing = pricing_provider.get_pricing(card_set=set_code)
				recorders = {
					'json': JSONCardPriceRecorder(filepath=f'pricing/{date_timestamp}/FULL-SET_{set_code}-{provider}-{datetime_timestamp}.json'),
					'db': DBPriceRecorder()
				}
				recorder = recorders.get('json')
				recorder.record_prices(set_pricing)

				print(f"Finished writing pricing for {set_code} from '{provider}' provider with recorder '{recorder}'")