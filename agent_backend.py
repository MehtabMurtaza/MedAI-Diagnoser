from fastapi import FastAPI, Request
from uagents import Bureau, Context
from agents_communication import inputagent, questionagent, webscrapeagent, recommendationagent, displayagent

app = FastAPI()

# Add your agents to the bureau
bureau = Bureau()
bureau.add(inputagent)
bureau.add(questionagent)
bureau.add(webscrapeagent)
bureau.add(recommendationagent)
bureau.add(displayagent)

# Run your bureau in the background (asynchronous)
@app.on_event("startup")
async def start_bureau():
    bureau.run_async()

# Define an endpoint for receiving symptoms
@app.post("/symptoms")
async def receive_symptoms(request: Request):
    # Parse the incoming JSON data (symptoms input)
    data = await request.json()
    symptoms = data.get("symptoms", "")

    # Mock response for now
    # Send symptoms to inputagent and start agent communication here
    diagnosis = await process_symptoms_with_agents(symptoms)

    # Return the diagnosis as a JSON response
    return {"diagnosis": diagnosis}

# A placeholder function to simulate agent processing for now
# In reality, this function will handle agent-to-agent message passing and return the final result
async def process_symptoms_with_agents(symptoms: str) -> str:
    """
    This function will eventually handle communication between agents.
    For now, it returns a mock response. Later, agent event handling will replace this.
    """
    print(f"Processing symptoms: {symptoms}")

    # Simulate agent message-passing logic (this should be handled in agents themselves)
    # Example: inputagent -> questionagent -> webscrapeagent -> recommendationagent -> displayagent
    # This will be replaced by actual logic using ctx.send and event handlers in your agents.
    if "headache" in symptoms.lower():
        diagnosis = "It looks like you may have a tension headache. uhh"
    else:
        diagnosis = "We need more information to make a confident diagnosis."

    # Example of how you can mock back-and-forth agent logic
    if "uhh" in diagnosis.lower():
        return "We need more details before we can proceed with a confident diagnosis."
    
    # Return the mock diagnosis
    return diagnosis

