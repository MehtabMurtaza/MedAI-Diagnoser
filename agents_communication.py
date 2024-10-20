from uagents import Agent, Bureau, Context, Model

GROQ_API_KEY = "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"
import os
from groq import Groq
client = Groq(
    api_key=GROQ_API_KEY,
)
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "What category of diseases are there?",
#         }
#     ],
#     model="llama3-8b-8192",
# )
#print(chat_completion.choices[0].message.content)

def askgroq(question):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
        model="llama3-8b-8192",
    )
    return(chat_completion.choices[0].message.content)
 
class Message(Model):
    message: str
 
inputagent = Agent(name="inputagent", seed="inputagent")
questionagent = Agent(name="questionagent", seed="questionagent")
webscrapeagent = Agent(
    mailbox="c23aaa14-7320-4283-a2df-fd1a013c03da",
    seed = "asdfhadflgwlirebfadswlerjhbf"
)
recommendationagent = Agent(name="recommendationagent", seed="recommendationagent")
displayagent = Agent(name="displayagent", seed="displayagent")
#@sigmar.on_interval(period=3.0)
@inputagent.on_event("startup")
async def send_message(ctx: Context):
   
   input = "whateva"

   await ctx.send(questionagent.address, Message(message=input))
 
@inputagent.on_message(model=Message)
async def inputagent_message_handler(ctx: Context, sender: str, msg: Message):

    ctx.logger.info(f"Received message from {sender}: {msg.message}") #message is new question

    #display question, wait for new input

    #get new input 

    newinput = "uhhhhhh"

    await ctx.send(questionagent.address, Message(message=newinput))
 
@questionagent.on_message(model=Message)
async def questionagent_message_handler(ctx: Context, sender: str, msg: Message):

    ctx.logger.info(f"Received message from {sender}: {msg.message}") #message is user input

    question = "given these symptoms, what other information would you need to diagnose this patient with 95 percent confidence? If you're not confident, output the word uhh "
    #words = input()
    question = question

    answer = askgroq(question)

#gets answer to prev question
    sure = True
    #pass answer to groq
    print("hi")
    #change sure boolean if sure
    #update quesiton if new question
    #update diagnosis if sure

    if not sure:

        question = answer

        await ctx.send(inputagent.address, Message(message=question)) #sends question to input agent
    
    else:

        diagnosis = answer

        # use groq to find a reputable website that can be web scraped?

        website = "website.com"

        await ctx.send(webscrapeagent.address, Message(message=website)) #sends website to website scraper



#web scraper
class WebsiteScraperRequest(Model):
    url: str


class WebsiteScraperResponse(Model):
    text: str


AI_AGENT_ADDRESS = "agent1qwnjmzwwdq9rjs30y3qw988htrvte6lk2xaak9xg4kz0fsdz0t9ws4mwsgs"

website_url = "https://en.wikipedia.org/wiki/Atopic_dermatitis"

#print(webscrapeagent.address)


@webscrapeagent.on_message(model=Message)
async def questionagent_message_handler(ctx: Context, sender: str, msg: Message):

    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    #website_url = msg.message

    await ctx.send(AI_AGENT_ADDRESS, WebsiteScraperRequest(url=website_url))
    ctx.logger.info(f"Sent request for scraping the Website: {website_url}")


@webscrapeagent.on_message(WebsiteScraperResponse)
async def handle_response(ctx: Context, sender: str, msg: WebsiteScraperResponse):
    ctx.logger.info(f"Received response from {sender[-10:]}:")
    ctx.logger.info(msg.text)
    
    #synthesize msg.text

    #with groq

    synthesis = "fewworddotrick"

    await ctx.send(recommendationagent.address, Message(message=synthesis)) #send synthesis to recommendationagent


@recommendationagent.on_message(model=Message)
async def recommendationagent_message_handler(ctx: Context, sender: str, msg: Message):

    ctx.logger.info(f"Received message from {sender}: {msg.message}") #message is synthesis

    #use synthesis with groq to make recommendation

    recommendation = "kys"

    await ctx.send(displayagent.address, Message(message=recommendation)) #send recommendation to displayagent

@displayagent.on_message(model=Message)
async def displayagent_message_handler(ctx: Context, sender: str, msg: Message):

    ctx.logger.info(f"Received message from {sender}: {msg.message}") #message is recommendation

    #use llama to ensure safe display

    display = "DONT kys"

    print("finaldisplay", display)

    #send back to ui




#if __name__ == "__main__":
#    webscrapeagent.run()
    
    
 
bureau = Bureau()
bureau.add(inputagent)
bureau.add(questionagent)
bureau.add(webscrapeagent)
bureau.add(recommendationagent)
 
if __name__ == "__main__":
    bureau.run()