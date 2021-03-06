from CommunityEntryValidators import CommunityEntryValidators
import asyncio
import aiohttp
import re
import helpers


class HttpException(Exception):
	pass


class CommunityFinder(CommunityEntryValidators):
	session = None
	semaphore = None

	@classmethod
	def _init(cls):
		"""
			Adding regex's for search urls
		"""
		for x in CommunityEntryValidators.__dict__.keys():
			if x.endswith('_regex'):
				regex = getattr(cls, x)
				if 're_find' in regex:
					break
				# modify pattern for fulltext search
				find_pattern = regex['re'].pattern.replace('$', '').replace('^', '')
				regex['re_find'] = re.compile(find_pattern)
				setattr(cls, x, regex)

	@classmethod
	def init_session(cls, session=None, referer='google.com'):
		cls.semaphore = asyncio.Semaphore(5)
		async def _init_session():
			if cls.session:
				cls.close_session()

			if session:
				cls.session = session
			else:
				headers = helpers.chrome_headers(referer)
				cls.session = aiohttp.ClientSession(headers=headers)
		asyncio.get_event_loop().run_until_complete(_init_session())

	@classmethod
	def close_session(cls):
		if cls.session:
			asyncio.get_event_loop().run_until_complete(cls.session.close())
			cls.session = None

	def __init__(self, url):
		CommunityFinder._init()
		self.url = url
		self.data = {
			'url': url,
			'community': {}
		}
		self.raw_page = None

	def get_matches(self, community):
		return getattr(self, community + '_regex')['re_find'].findall(self.raw_page)

	async def fetch(self):
		async with self.semaphore:
			async with self.session.get(self.url) as res:
				if str(res.status) in ['4', '5']:
					raise HttpException(f'HTTP Error: {res.status}')
				return await res.text()

	def update_community(self, community, data):
		# add links
		self.data['community'][community] = data

	def find_community(self, community_name):
		matches = self.get_matches(community_name)
		if not matches:
			return
		# get url constructor for community
		url_constructor = getattr(self, f'_{community_name}_constructor')
		# create valid urls
		data = [url_constructor(groups) for groups in matches]
		# clean data, find uniq urls and remove links to static
		data = self.clean_data(data)
		self.update_community(community_name, data)

	def clean_data(self, data):
		cleaned_data = set()

		for url in data:
			if any(url.endswith(x) for x in ['.css', '.js']):  # if static
				continue
			cleaned_data.add(url)
		return list(cleaned_data)

	def find(self):
		# get communities by url constructor methods
		communities = [
			x.split('_')[1] for x in dir(self) if x.endswith('_constructor')
		]
		# find communities in raw_page
		for community in communities:
			self.find_community(community)

	async def find_communities(self):
		# run this method for fetch page and find social links
		try:
			self.raw_page = await self.fetch()
			self.find()
		except HttpException as e:
			self.data['error'] = e.args[0]
		return self.data

	# url constructors:
	# override if the link format changes

	def _facebook_constructor(self, x):
		return f'{x[1]}/{x[2]}'

	def _reddit_constructor(self, x):
		return f'reddit.com/{x[1]}/{x[2]}'

	def _github_constructor(self, x):
		return f'github.com/{x[1]}'

	def _twitter_constructor(self, x):
		return f'twitter.com/{x[1]}'

	def _telegram_constructor(self, x):
		return f"{x[1]}/{x[2]}{x[3]}"

	def _discord_constructor(self, x):
		return f"{x[1]}/{x[2]}{x[3]}"

	def _medium_constructor(self, x):
		return f'medium.com/{x[1]}'

	def _steemit_constructor(self, x):
		return f'steemit.com/@{x[1]}'

	def _instagram_constructor(self, x):
		return f'instagram.com/{x[1]}'

	def _vk_constructor(self, x):
		return f'vk.com/{x[1]}'

	def _bitcointalk_constructor(self, x):
		return f'bitcointalk.org/index.php?topics={x[1]}'

	def _linkedin_constructor(self, x):
		return f'linkedin.com/company/{x[1]}'
