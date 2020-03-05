#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import requests
import json
from dotenv import load_dotenv


dotenv_path = '../.env'
load_dotenv(dotenv_path)
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
DEVELOPER_API_BASE_URL = os.environ.get("DEVELOPER_API_BASE_URL")
ACCESS_TOKEN_PUBLISH_URL = os.environ.get("ACCESS_TOKEN_PUBLISH_URL")


def auth():
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8"
    }

    data = {
        "grantType": "client_credentials",
        "clientId": CLIENT_ID,
        "clientSecret": CLIENT_SECRET
    }
    r = requests.post(ACCESS_TOKEN_PUBLISH_URL,
                      headers=headers,
                      data=json.dumps(data))
    return r.json()["access_token"]


def parse(text, access_token):
    base_url = DEVELOPER_API_BASE_URL
    headers = {
        "Content-Type": "application/json",
        "charset": "UTF-8",
        "Authorization": "Bearer {}".format(access_token)
    }
    data = {
        "sentence": text,
        "type": "default"
    }
    r = requests.post(base_url + "v1/parse",
                      headers=headers,
                      data=json.dumps(data))

    data = {
        "sentence": text,
        "type": "default"
    }
    r_type = requests.post(base_url + "v1/sentence_type",
                           headers=headers,
                           data=json.dumps(data))
    return r.json(), r_type.json()


def judge_directive(res):
    directive = False
    if res["result"]['dialog_act'] == ['directive']:
        directive = True
    return directive

def convert(r_parse,r_type):
    response = 'んんん？'
    if judge_directive(r_type):
        for word in r_parse["result"]:
            verv = ''
            for token in word["tokens"]:
                if token['pos'] == '動詞語幹':
                    verv = token['form']
                    v_type = token['features']
        if verv != '':
            response = verv + 'な~~い!'

    return response



    






if __name__ == '__main__':
    text = 'ごはん食べなさい。'
    access_token = auth()
    r_parse, r_type = parse(text, access_token)
    print(convert(r_parse, r_type))
    text = input()
    access_token = auth()
    r_parse, r_type = parse(text, access_token)
    print(convert(r_parse, r_type))
