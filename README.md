# mtg-spoiler-bot
This bot scans mythicspoilers.com for new cards and posts them to a discord webhook.  


## Todo
+ Better error handling
  + Retry Discord messages with exponential backoff
+ Better documentation

## Usage
Setting the `WEBHOOK_URL` environment variable to your Discord Webhook URL allows the bot to send messages directly to the Discord channel.  
You can also set `TIMER` as a value in seconds to change the sleep value between checks (defaults to `300` seconds).  
Lastly, changing `CARD_JSON` will allow you to overwrite where the last scanned card is stored. This is needed to prevent the bot from continuously looping through all the cards and posting them to Discord.

| Variable | Type | Default |
| -------- | ---- | ------- |
| `WEBHOOK_URL` | String | N/A |
| `TIMER` | Number | `300` |
| `CARD_JSON` | String | `/tmp/cards/cards.json` |