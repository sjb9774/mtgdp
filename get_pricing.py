#! /usr/bin/env python
from argparse import ArgumentParser
from providers.provider import PriceProvider
from providers.scryfall import ScryfallPricing
from providers.tcgplayer import TcgPlayerPricing
from providers.mtgjson import MtgJsonPricing
from recorders.json import JSONCardPriceRecorder
from recorders.db import DBPriceRecorder
import json
import datetime
from pathlib import Path

from recorders.pricerecorder import PriceRecorder


if __name__ == "__main__":
	provider_map = {
		'scryfall': ScryfallPricing(),
		'tcgplayer': TcgPlayerPricing(),
		'mtgjson': MtgJsonPricing(source='tcgplayer', pricing_type='retail')
	}

	argparser = ArgumentParser()
	argparser.add_argument('-s', '--set-codes', nargs='+', required=True)
	argparser.add_argument('-p', '--pricing-providers', nargs='+', required=True, choices=list(provider_map.keys()))
	argparser.add_argument('-r', '--recorders', nargs='+', required=False, choices=['json', 'db'], default=['json'])
	args = argparser.parse_args()
	now = datetime.datetime.now()
	date_timestamp = now.strftime('%Y-%m-%d')
	datetime_timestamp = now.strftime('%Y-%m-%d_%H:%M:%S')

	for provider in args.pricing_providers:
		pricing_provider: PriceProvider = provider_map.get(provider) # type: ignore
		if pricing_provider:
			for set_code in args.set_codes:
				print(f"Retrieving pricing for {set_code} from '{provider}' provider")
				set_pricing = pricing_provider.get_pricing(card_set=set_code)
				print("Pricing retrieved.")
				recorders = {
					'json': JSONCardPriceRecorder(filepath=f'pricing/{date_timestamp}/FULL-SET_{set_code}-{provider}-{datetime_timestamp}.json'),
					'db': DBPriceRecorder()
				}
				for recorder in args.recorders:
					recorder: PriceRecorder
					print(f"Recording using recorder '{recorder}'")
					recorder = recorders.get(recorder) # type: ignore
					recorder.record_prices(set_pricing)
					print(f"Finished writing pricing for {set_code} from '{provider}' provider with recorder '{recorder}'")
