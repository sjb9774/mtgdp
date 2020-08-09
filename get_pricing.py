#! /usr/bin/env python
from argparse import ArgumentParser
from providers.scryfall import ScryfallPricing
import json

if __name__ == "__main__":
	argparser = ArgumentParser()
	argparser.add_argument('-s', '--set-codes', nargs='+', required=True)
	argparser.add_argument('-p', '--pricing-providers', nargs='+', required=True, choices=['scryfall'])
	args = argparser.parse_args()

	provider_map = {
		'scryfall': ScryfallPricing()
	}
	for provider in args.pricing_providers:
		pricing_provider = provider_map.get(provider)
		if pricing_provider:
			for set_code in args.set_codes:
				print(f"Retrieving pricing for {set_code} from '{provider}' provider")
				set_pricing = pricing_provider.get_pricing(card_set=set_code)
				pricing_json = json.dumps(set_pricing)
				pricing_date = set_pricing[0].get("date")
				pricing_path = f'pricing/FULL-SET_{set_code}-{provider}-{pricing_date}.json'
				with open(pricing_path, 'w+') as f:
					f.write(pricing_json)
				print(f"Finished writing pricing for {set_code} from '{provider}' provider to '{pricing_path}'")