#!/usr/bin/env python
# -*- coding: utf-8 -*-
from slackclient import SlackClient
import time
import search
import config

# unicode fix
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# get your personal token from https://api.slack.com/web
api_key = config.SLACK_TOKEN
client = SlackClient(api_key)

if client.rtm_connect():
    while True:
        last_read = client.rtm_read()
        if last_read:
            print last_read
            try:
                parsed = last_read[0]['text']
                # get channel
                message_channel = last_read[0]['channel']
                if parsed and parsed.startswith("docbot search"):
                    # do the search thing
                    query = parsed.split("docbot search", 1)[1].strip()
                    results = search.search_docs(query)
                    # print results
                    client.rtm_send_message(message_channel, "\n")
                    client.rtm_send_message(message_channel, "Hi! I found these links for you. I hope they help!\n---------------------")
                    client.rtm_send_message(message_channel, '\n'.join(map(str, results)))
                    client.rtm_send_message(message_channel, "---------------------\n")
                # if parsed and parsed.lower().startswith(" who are you"):
                #    client.rtm_send_message(message_channel, "I'm a friendly \
                #    bot that helps you search the docs without leaving Slack. \
                #    Let me know if I can help! Just type `@docbot searchquery`\
                #     and I'll go search for you.")
            except Exception as e:
                print e
                pass
        time.sleep(1)
