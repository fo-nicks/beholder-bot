#!/bin/bash

docker build -t beholder-bot-server .
docker run --restart unless-stopped \
			  -v beholder-bot-cache:/cache \
			  -e TELEGRAM_TOKEN='YOUR_BOT_TOKEN_HERE' \
			  -d beholder-bot-server 

