import clashroyale
import json
from copy import deepcopy

client = clashroyale.OfficialAPI("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9."
                                 "eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjU2MmNjYjBhLWU2NjEtNDVjMC05YTRiLWNlYzgxMWU4M2I4MSIsImlhdCI6MT"
                                 "U0MjE2NTYwNywic3ViIjoiZGV2ZWxvcGVyLzI0NzI0NDFhLTk0OGEtY2E0Yy1lM2IwLWJkZWNhYjg3MzJlYyIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0"
                                 "aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIyLjUxLjE4Ni41Il0sInR5cGUiOiJjbGllbnQifV19.J3uL8dn3wc2Cs"
                                 "Wjvjgva4SD063RYu1uMzfDB4MDnXOT0eqVEONQL0zOocPMPmBs9qCMEyvovTJLemEVZgDaprQ")

with open('clans.json') as json_data:
    tags = json.load(json_data)

saved_tags = deepcopy(tags)
for tag in saved_tags:
    try:
        print(tags[tag])
    except UnicodeEncodeError:
        tags.pop(tag)
        with open('clans.json', 'w') as outfile:
            json.dump(tags, outfile, indent=2)
        continue

    try:
        clan = client.get_clan(tag.strip("#"))
    except Exception as e:
        print(e)
    else:
        try:
            if not ((20 < clan.members < 40) and (clan.type == 'open') and (clan.required_trophies <= 4000) and (600 < clan.clan_war_trophies < 3000)):
                tags.pop(tag)
            print(tags[tag])
            with open('clans.json', 'w') as outfile:
                json.dump(tags, outfile, indent=2)
        except Exception as e:
            print(e)
