from uagents import Agent, Context, Model


class WebsiteScraperRequest(Model):
    url: str


class WebsiteScraperResponse(Model):
    text: str


agent = Agent(
    mailbox="c23aaa14-7320-4283-a2df-fd1a013c03da",
    seed = "asdfhadflgwlirebfadswlerjhbf"
)


AI_AGENT_ADDRESS = "agent1qwnjmzwwdq9rjs30y3qw988htrvte6lk2xaak9xg4kz0fsdz0t9ws4mwsgs"

website_url = "https://fetch.ai/"

print(agent.address)


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, WebsiteScraperRequest(url=website_url))
    ctx.logger.info(f"Sent request for scraping the Website: {website_url}")


@agent.on_message(WebsiteScraperResponse)
async def handle_response(ctx: Context, sender: str, msg: WebsiteScraperResponse):
    ctx.logger.info(f"Received response from {sender[-10:]}:")
    ctx.logger.info(msg.text)


if __name__ == "__main__":
    agent.run()