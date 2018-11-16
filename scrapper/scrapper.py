import clashroyale
import json

client = clashroyale.OfficialAPI("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9."
                                 "eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImVjMzIzODMzLWYwYjMtNDFiOS1hZ"
                                 "mJlLTg2ZjVjNzlhOThiNyIsImlhdCI6MTU0MTM0NTQxNiwic3ViIjoiZGV2ZWxvcGVyLzI0NzI0NDFhLTk0OGEtY2E0Yy1lM2I"
                                 "wLWJkZWNhYjg3MzJlYyIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsI"
                                 "nR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyIyLjUxLjE4LjE1MyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.odnEmjRPi1L"
                                 "TsXlifqcfjB_t2mojFvmi97kvvDHMcjAkNPRXjcKRd9XZiJXVRWITcmyKJFKB-w7SFdHn1KcUKg")

with open('clans.json') as json_data:
    tags = json.load(json_data)

for tag in tags:
    try:
        warlog = client.get_clan_war_log(tag)
    except Exception:
        pass
    else:
        for war in warlog:
            for clan in war.standings:
                try:
                    tags[clan.tag] = clan.name
                    print(clan.tag)
                    with open('clans.json', 'w') as outfile:
                        json.dump(tags, outfile)
                except Exception:
                    pass
