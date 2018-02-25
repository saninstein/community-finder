import re


class CommunityEntryValidators:
    # TODO add reconstruct by origin id
    facebook_regex = {
        "re": re.compile(r'^(www\.)?(facebook\.com|fb\.me|fb\.com)\/([a-zA-Z0-9\-\_\.]+)\/?$'),
        "resource_id_position": 2
    }
    reddit_regex = {
        "re": re.compile(r'^(www\.)?reddit\.com\/(r|user)\/([a-zA-Z0-9\-\_]+)\/?$'),
        "resource_id_position": 2
    }
    github_regex = {
        "re": re.compile(r'^(www\.)?github\.com\/([a-zA-Z0-9\-\_]+(\/[a-zA-Z0-9\-\_]+)?)\/?$'),
        "resource_id_position": 1
    }
    twitter_regex = {
        "re": re.compile(r'^(www\.)?twitter\.com\/\@?([a-zA-Z0-9(\_\.\?)?]+)\/?$'),
        "resource_id_position": 1
    }
    telegram_regex = {
        "re": re.compile(r'^(www\.)?(telegram\.com|telegram\.me|t\.me)\/(joinchat/)?([a-zA-Z0-9\-\_]+)\/?$'),
        "resource_id_position": 3
    }
    discord_regex = {
        "re": re.compile(r'^(www\.)?(discord\.gg|discordapp\.com)\/(invite/)?([a-zA-Z0-9\-\_]+)\/?$'),
        "resource_id_position": 3
    }
    medium_regex = {
        "re": re.compile(r'^(www\.)?medium\.com\/(\@?[a-zA-Z0-9\-\_\.]+)\/?$'),
        "resource_id_position": 1
    }
    steemit_regex = {
        "re": re.compile(r'^(www\.)?steemit\.com\/\@([a-zA-Z0-9\-\_]+)\/?$'),
        "resource_id_position": 1
    }
    instagram_regex = {
        "re": re.compile(r'^(www\.)?instagram\.com\/([a-zA-Z0-9\_\.]+)\/?$'),
        "resource_id_position": 1
    }
    vk_regex = {
        "re": re.compile(r'^(www\.)?vk\.com\/([a-zA-Z0-9\_\.]+)\/?$'),
        "resource_id_position": 1
    }
    bitcointalk_regex = {
        "re": re.compile(r'^(www\.)?bitcointalk\.org\/index\.php\?topic=([\d]+)(\.0)?$'),
        "resource_id_position": 1,
    }
    linkedin_regex = {
        "re": re.compile(r'^(www\.)?linkedin\.com\/company\/([a-zA-Z0-9\-\_]+)\/?$'),
        "resource_id_position": 1,
    }
