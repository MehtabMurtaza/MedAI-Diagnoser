

# import reflex as rx
# from rxconfig import config

# class State(rx.State):
#     """The app state."""
    
#     symptoms: str = ""

#     def submit_symptoms(self):
#         # This could trigger a diagnosis processing (e.g., call an API or process the input)
#         print(f"Symptoms submitted: {self.symptoms}")

# def index() -> rx.Component:
#     # Welcome Page (Index)
#     return rx.container(
#         rx.color_mode.button(position="top-right"),
#         rx.vstack(
#             rx.heading("Get your diagnosis!", size="9"),
#             rx.text(
#                 "Please input your symptoms",
#                 size="5",
#             ),
#             # Add a textbox for user input, binding it to the symptoms state
#             rx.input(placeholder="Enter your symptoms here...", on_change=State.set_symptoms),
#             # Add a button that will submit the symptoms
#             rx.button("Submit", on_click=State.submit_symptoms),
#             spacing="5",
#             justify="center",
#             min_height="85vh",
#         ),
#         rx.logo(),
#     )

# app = rx.App()
# app.add_page(index)



######################


import reflex as rx
from rxconfig import config
from groq import Groq  # Importing the Groq SDK

# Initialize the Groq client with your API key
client = Groq(
    api_key="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",
)

class State(rx.State):
    """The app state."""
    
    symptoms: str = ""
    diagnosis: str = ""  # This will hold the response from Groq

    def submit_symptoms(self):
        """Send the symptoms to Groq API and get the diagnosis."""
        # Print symptoms for debug
        print(f"Symptoms submitted: {self.symptoms}")
        
        # Use Groq client to send the symptoms and get the diagnosis
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": self.symptoms,  # Sending the user's symptoms as input
                }
            ],
            model="llama3-8b-8192",  # Model you want to use
        )

        # Extract the response and set it as the diagnosis
        self.diagnosis = chat_completion.choices[0].message.content


def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Get your diagnosis!", size="9"),
            rx.text("Please input your symptoms", size="5"),
            # Add a textbox for user input, binding it to the symptoms state
            rx.input(placeholder="Enter your symptoms here...", on_change=State.set_symptoms),
            # Add a button that will submit the symptoms and trigger the API call
            rx.button("Submit", on_click=State.submit_symptoms),
            # Display the diagnosis after the API response
            rx.cond(
                State.diagnosis != "",  # If diagnosis is available
                rx.text(State.diagnosis, size="5", color="green"),
                rx.text("No diagnosis available", size="5", color="black")
            ),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )

app = rx.App()
app.add_page(index)



