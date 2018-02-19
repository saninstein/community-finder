from community_finder import CommunityFinder
import helpers
import json
import asyncio


def test(test):
	def _wrapper(self = None):
		print('-' * 5, test.__name__, '-' * 5)
		test(self) 
		print('-' * 5, test.__name__, ' END', '-' * 5, '\n')
	return _wrapper


URLS = [
	'https://bitcoin.org/',
	'https://www.ethereum.org/',
	'https://ripple.com/',
	'https://www.bitcoincash.org/'
]


class CommunityFinderTests:

	def __init__(self):
		[getattr(self, x)() for x in dir(self) if x.startswith('test')]

	@test
	def test_example_use_with_downloading_a_page(self):
		CommunityFinder.init_session()

		tasks = []
		for url in URLS:
			community_finder = CommunityFinder(url)
			task = asyncio.ensure_future(community_finder.find_communities())
			tasks.append(task)

		loop = asyncio.get_event_loop()
		res = loop.run_until_complete(asyncio.gather(*tasks))
		CommunityFinder.close_session()
		helpers.print_dict(res)

	@test
	def test_on_coins(self):
		projects = json.load(open('coins.json'))
		total_error = 0
		res = []
		for project in projects:
			r = {
				'id': project['id']
			}

			if 'community' in project:
				r['community'] = project['community']

			c = CommunityFinder('')
			c.raw_page = json.dumps(project) 
			c.find()
			r['finded'] = c.data['community']
			delta_community = 0
			delta_count = 0
			for x in r['community']:
				if not (x == 'medium_www' or x == 'whitepaper'):
					if x not in r['finded']:
						delta_community += 1
					else:
						delta_count += abs(len(r['community'][x]) - len(r['finded'][x]))

			r['delta_community'] = delta_community
			r['delta_count'] = delta_count

			total_error += delta_count + delta_community
			res.append(r)

		print('Errors count:', total_error)
		print('Errors: ')
		helpers.print_dict([x for x in res if x['delta_community'] != 0 or x['delta_count'] != 0])


CommunityFinderTests()
