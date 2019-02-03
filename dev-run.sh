#!/bin/bash

docker build -t beholder-bot-server .
docker run \
	-v beholder-bot-cache:/cache \
	-e TELEGRAM_TOKEN='YOUR_BOT_TOKEN_HERE' \
	--rm \
  	beholder-bot-server 
