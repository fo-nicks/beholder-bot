#!/bin/bash

docker build -t beholder-bot-server .
docker run -e TELEGRAM_TOKEN='YOUR_BOT_TOKEN_HERE' --rm beholder-bot-server 
