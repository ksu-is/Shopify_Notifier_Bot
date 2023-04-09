# Shopify Notifier Bot

Setup instructions:

1. Add the desired product URLs to `list.txt`. When adding items with multiple variants make sure to add or remove the `?variant=` at the end of the URL if you want to track a single variant or all variants.

2. Add your webhook URL to `config.cfg`. The delay between checking items (in seconds) and the message to be sent when items are in stock can also be configured.

3. Run `stock_state_tracker.py`.