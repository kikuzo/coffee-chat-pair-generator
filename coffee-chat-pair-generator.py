#!/usr/bin/python3

import random
import urllib.request
import json
import os
import sys

notion_api_url = "https://api.notion.com"
notion_property_id = "fbRJ"


def get_notion_property(pageid, propertyid):
    try:
        notion_api_token = os.environ['NOTION_API_TOKEN']
    except KeyError as e:
        print(e, '環境変数が設定されていません')
        exit(0)

    url = notion_api_url + "/v1/pages/" + pageid + "/properties/" + propertyid
    headers = {
        'Authorization': "Bearer " + notion_api_token,
        'Notion-Version': "2022-06-28"
    }
    request = urllib.request.Request(url, None, headers)
    # print(url)

    with urllib.request.urlopen(request) as response:
        return(response.read().decode("utf-8"))


def get_notion_database(databaseid):
    url = notion_api_url + "/v1/databases/" + databaseid
    headers = {
        'Authorization': "Bearer " + notion_api_token,
        'Notion-Version': "2022-06-28"
    }
    request = urllib.request.Request(url, None, headers)

    with urllib.request.urlopen(request) as response:
        return(response.read().decode("utf-8"))


def retrieve_notion_page(pageid):
    url = notion_api_url + "/v1/pages/" + pageid
    headers = {
        'Authorization': "Bearer " + notion_api_token,
        'Notion-Version': "2022-06-28"
    }
    request = urllib.request.Request(url, None, headers)

    with urllib.request.urlopen(request) as response:
        return(response.read().decode("utf-8"))


def send_message_to_slack(msg):
    try:
        slack_channel = os.environ["SLACK_CHANNEL"]
        slack_hook_url = os.environ["SLACK_HOOK_URL"]
    except KeyError as e:
        print('Slackに出力する場合は出力先を環境変数で指定してください', e)
        exit(0)

    # make slack message body
    send_data = {
        "channel": slack_channel,
        "username": "coffee chat pair generator",
        "text": msg
    }
    payload = "payload=" + json.dumps(send_data)
    slack_request = urllib.request.Request(
        slack_hook_url,
        data=payload.encode("utf-8"),
        method="POST"
    )
    with urllib.request.urlopen(slack_request) as slack_response:
        response_body = slack_response.read().decode("utf-8")

# ここよりメインルーチン


def main():
    # コマンドライン引数を取得
    arguments = sys.argv
    if len(arguments) == 1:
        print('引数で参加者リスト取得先Notion Pageを指定してください')
        exit(0)
    else:
        # print(arguments[1])
        notion_page_id = arguments[1]

    # 参加者リストを取得する
    properties = json.loads(get_notion_property(
        notion_page_id, notion_property_id))
    #member_list = properties['results'][2]['people']['name']
    members = []
    for i in properties['results']:
        members.append(i['people']['name'])

    # ペアを生成する
    random.shuffle(members)
    msg = ""
    for no, i in enumerate(range(0, len(members), 2)):
        if len(members) <= 1:
            msg += (f"no pair!")
            break
        if i+1 >= len(members):  # if the number of members is odd number
            checker = random.choice(members[:-1])
            #print(f"room {no}: {members[i]} + {checker}(checker)")
            msg += (f"room {no}: {members[i]} + {checker}(checker)\n")
        else:
            #print(f"room {no}: {members[i]} + {members[i+1]}")
            msg += (f"room {no}: {members[i]} + {members[i+1]}\n")

    # 結果を出力
    msg += "\n相手がいない場合は談話コーナーにどうぞ."
    print(msg)
    send_message_to_slack(msg)


if __name__ == "__main__":
    main()
