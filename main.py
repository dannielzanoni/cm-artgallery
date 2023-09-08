import tweepy
from PIL import Image, ImageDraw
import pandas as pd
import os
import random
import requests
import json

bearer_token = ''
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# V1 Twitter API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# V2 Twitter API Authentication
client = tweepy.Client(
    bearer_token,
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret,
    wait_on_rate_limit=True,
)

path_templates = './templates/'
path_assets = './assets/'
templates_available = os.listdir(path_templates)
assets_available = os.listdir(path_assets)

template_image = Image.open(os.path.join(path_templates, random.choice(templates_available)))

templates_cord = 'templates.json'
with open(templates_cord, 'r') as arquivo:
    read_templates = json.load(arquivo)

chosen_coord_template = random.choice(read_templates)
x = chosen_coord_template['x']
y = chosen_coord_template['y']
tamX = chosen_coord_template['tamX']
tamY = chosen_coord_template['tamY']

point_file_name = os.path.basename(chosen_coord_template['imagem'])

#find template
templates_with_name = [template for template in templates_available if point_file_name in template]

if templates_with_name:
    chosen_template = random.choice(templates_with_name)
    template_path = os.path.join(path_templates, chosen_template)
    template_image = Image.open(template_path)

    assets_available = [os.path.join(path_assets, nome) for nome in os.listdir(path_assets)]    
    random.shuffle(assets_available)

    assets_path = assets_available.pop()
    random_aseet = Image.open(assets_path)
    random_aseet = random_aseet.resize((tamX, tamY))
    final_image = template_image.copy()
    final_image = template_image.convert('RGB')
    final_image.paste(random_aseet, (x, y))
    final_image.save('Result.jpg')

media_id = api.media_upload("Result.jpg").media_id_string
print(media_id)
client.create_tweet(media_ids=[media_id])