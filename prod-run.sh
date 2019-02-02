#!/bin/bash

docker build -t beholder-bot-server .
docker run --restart unless-stopped -e TELEGRAM_TOKEN='YOUR_BOT_TOKEN_HERE' -d beholder-bot-server 

