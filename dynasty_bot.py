import os
import time
import numpy as np
import re
import datetime
from slackclient import SlackClient as sc

def post_message(channel, t):
    slack_client.api_call('chat.postMessage', channel=channel, text=t)

def parse_bot_commands(slack_events):
 """
 Handling the posts and answer to them
 :param slack_events: slack_client.rtm_read()
 """
 for event in slack_events:
     # only message from users
     if event['type'] == 'message' and not "subtype" in event:
         # get the user_id and the text of the post
         user_id, text_received, channel = event['user'], event['text'], event['channel']
         # the bot is activated only if we mention it
         if '@%s' % dynasty_bot_id in text_received:
             # Activate help if 'help' or 'sos' in the post
             if any([k in text_received for k in ['help', 'sos']]):
                   post_annotation(token, text=help_text, channel=channel)
             # Activate Google Maps if 'distance' or 'time' 
             elif any([k in text_received for k in ['distance', 'time']]):
               # search the users names in the post
               r = re.compile(r'\bELIE\b | \bELIOTT\b | \bALEX\b | \bMY PLACE\b', flags=re.I | re.X)
               matched = r.findall(text_received)
               # replace 'my place' by the user name
               if 'my place' in matched:
                    matched[matched.index('moi')] = ids[user_id]
               # check if we have the addresses of all users
               if all([k in adress for k in matched]):
                   name_dest = matched[1].title()
                   # Compute direction
                   directions_text = get_directions_duration( adress[matched[0]], adress[matched[1]], name_dest)
                   # Post message
                   post_annotation(token, text=directions_text, channel=channel)
 
             # Activate annotations information
             else:
                post_annotation(token, channel=channel)

var_dic = open('app-env.txt','r').read()
var_dic = eval(var_dic)

token = var_dic['bot_auth_token']

bot_id = None

##rtm_read_delay = 1
##example_command = 'do'
##mention_regex = '^<@(|[WU].+?)>(.*)'

slack_client = sc(token)
bool = slack_client.rtm_connect(with_team_state=False)
events = slack_client.rtm_read()
# events = [{'type': XXX, 'text': YYY, 'user': ZZZ}, ...]




if __name__ == '__main__':
   slack_client = sc(token)
   if slack_client.rtm_connect(with_team_state=False):
       dynasty_bot_id = slack_client.api_call('auth.test')['user_id']
       while True:
           parse_bot_commands(slack_client.rtm_read())
           time.sleep(1)
