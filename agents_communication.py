from uagents import Agent, Bureau, Context, Model
from urllib.parse import quote_plus

GROQ_API_KEY = "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"
import os
from groq import Groq
client = Groq(
    api_key=GROQ_API_KEY,
)

text_history = []

def askgroq(question, history):
    # Combine the history of conversation to give context to Groq
    messages = [{"role": "system", "content": "This is a medical diagnostic system."}]
    for msg in history:
        role = "user" if msg["sender"] == "user" else "assistant"
        messages.append({"role": role, "content": msg["content"]})

    messages.append({"role": "user", "content": question})
    
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.1-70b-versatile",
    )
    
    return chat_completion.choices[0].message.content

# Fresh instance of Groq for summarizing web-scraped data
def summarize_data(data):
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Summarize the following medical information, Make sure to keep the summary very short and very simple so that people with little knowledge can understand it:"},
            {"role": "user", "content": data}
        ],
        model="llama-3.1-70b-versatile",
    )
    return chat_completion.choices[0].message.content

# Generate a dynamic Google search URL
def generate_google_search_url(query):
    search_query = quote_plus(query)
    return f"https://www.google.com/search?q={search_query}"
 
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

    initial_input = "Initial input from user. Here the user inputs the symptoms"
    # Adding initial user input to history
    text_history.append({"sender": "user", "content": initial_input})

    await ctx.send(questionagent.address, Message(message=initial_input))

 
@inputagent.on_message(model=Message)
async def inputagent_message_handler(ctx: Context, sender: str, msg: Message):

    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    # Simulate user input; you can replace this with actual user input later
    new_input = input("Please provide your next input: ")
    text_history.append({"sender": "user", "content": new_input})

    await ctx.send(questionagent.address, Message(message=new_input))
 
@questionagent.on_message(model=Message)
async def questionagent_message_handler(ctx: Context, sender: str, msg: Message):

    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    question = """Given these symptoms, what other information would you need to diagnose this patient with 95 percent confidence? If you're not confident, output the word 'uhh'.
     Also write 'uhh' until you get symptoms, duration, location, severity"""
    
    # Adding question to history
    text_history.append({"sender": "assistant", "content": question})

    # Ask Groq with the question and history
    answer = askgroq(question, text_history)
    ctx.logger.info(f"Groq responded: {answer}")
    
    # Adding the response to history
    text_history.append({"sender": "assistant", "content": answer})

    # Determine whether the model is satisfied or needs more input
    sure = "uhh" not in answer.lower()  # if 'uhh' is present (case insensitive), we are not sure

    if not sure:
        # Send the next question to input agent for user input
        await ctx.send(inputagent.address, Message(message=answer))
    else:
        # If satisfied, this would be the final diagnosis
        diagnosis = answer
        ctx.logger.info(f"Diagnosis reached: {diagnosis}")

        website = "website.com"

        await ctx.send(webscrapeagent.address, Message(message=website))


#web scraper
class WebsiteScraperRequest(Model):
    url: str


class WebsiteScraperResponse(Model):
    text: str


AI_AGENT_ADDRESS = "agent1qwnjmzwwdq9rjs30y3qw988htrvte6lk2xaak9xg4kz0fsdz0t9ws4mwsgs"

website_url = "https://en.wikipedia.org/wiki/Atopic_dermatitis"

#print(webscrapeagent.address)


@webscrapeagent.on_message(model=Message)
async def webscrapergent_message_handler(ctx: Context, sender: str, msg: Message):

    ctx.logger.info(f"Received message from {sender}: {msg.message}")

    #website_url = msg.message

    await ctx.send(AI_AGENT_ADDRESS, WebsiteScraperRequest(url=website_url))
    #ctx.logger.info(f"Sent request for scraping the Website: {website_url}")


@webscrapeagent.on_message(WebsiteScraperResponse)
async def handle_response(ctx: Context, sender: str, msg: WebsiteScraperResponse):
    #ctx.logger.info(f"Received response from {sender[-10:]}: {msg.text}")

    # Summarize the scraped website data
    summarized_data = summarize_data(msg.text)

    # Log the summarized data (optional)
    #ctx.logger.info(f"Summarized data: {summarized_data}")

    # Send the summarized data to the recommendation agent for further processing
    await ctx.send(recommendationagent.address, Message(message=summarized_data))


@recommendationagent.on_message(model=Message)
async def recommendationagent_message_handler(ctx: Context, sender: str, msg: Message):

    # Process the summarized data to form a recommendation
    recommendation = f"Based on the summarized data: {msg.message}, here is the final recommendation and diagnosis."

    # Send the recommendation to the display agent
    await ctx.send(displayagent.address, Message(message=recommendation))


@displayagent.on_message(model=Message)
async def displayagent_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received final recommendation for display: {msg.message}")

    display = msg.message  # Ensure safe display




    
    
 
bureau = Bureau()
bureau.add(inputagent)
bureau.add(questionagent)
bureau.add(webscrapeagent)
bureau.add(recommendationagent)
bureau.add(displayagent)
 
if __name__ == "__main__":
    bureau.run()
