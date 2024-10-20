from uagents import Agent, Context, Model
 
 
class Message(Model):
    message: str
 
 
RECIPIENT_ADDRESS = (
    "agent1qtwrtgetufhv5d8ulu604elgam960rhvhhr3xqkuc576hlymmzchg6dett6"
)
 
SenderAgent = Agent(
    name="SenderAgent",
    port=8000,
    seed="ragh",
    endpoint=["http://127.0.0.1:8000/submit"],
)
 
print(SenderAgent.address)
 
@SenderAgent.on_interval(period=2.0)
async def send_message(ctx: Context):
    await ctx.send(RECIPIENT_ADDRESS, Message(message="Hi there. Let's start our conversation!"))
 
 
@SenderAgent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
 
 
if __name__ == "__main__":
    SenderAgent.run()