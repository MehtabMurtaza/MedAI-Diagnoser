

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
from CalHacksApp import app_style

# Initialize the Groq client with your API key
client = Groq(
    api_key="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",
)
bg_color = "var(--sky-1)"

class State(rx.State):
    """The app state."""
    
    symptoms: str = ""
    diagnosis: str = ""  # This will hold the response from Groq
    chat_history: list[tuple[str, str]]

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
        self.chat_history.append((self.symptoms, self.diagnosis))
        self.symptoms = ""

def q_ans(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.box(
            rx.text(question, style=app_style.question_style,
                    background_color="var(--sky-2)",),
            text_align="right",
        ),
        rx.box(
            rx.text(answer, style=app_style.answer_style,
                    background_color="var(--sky-4)"),
            text_align="left",
        ),
        margin_y="1em",
        width="100%",
    )

def heading() -> rx.Component:
    return rx.heading("Hello! This is MedAI", size = "7", margin="15px",
                      style={
                          "position":"fixed",
                          "top":"0",
                          #"padding":"20",
                          #"backgroundColor":bg_color,
                      },
                      )

def nightshift() -> rx.Component:
    return rx.color_mode.button(position="top-right")


def chat() -> rx.Component:
    return rx.box(
        rx.foreach(
            State.chat_history,
            lambda messages: q_ans(messages[0], messages[1]),
        ),
        style={
            "marginTop":"50px",
            "marginBottom":"130px",
            "padding":"15",
            "backgroundColor":bg_color,
        },
    )
    
def message_bar() -> rx.Component:
    return rx.hstack(
        rx.input(placeholder="What are you feeling?",
                 border_width="0px",
                 padding="1em",
                 width="350px",
                 value=State.symptoms,
                 on_change=State.set_symptoms),
        rx.button(
            "Ask",
            border_radius="5em",
            background_image="linear-gradient(144deg,#A9DAED,#8DCAE3)",
            box_sizing = "border-box",
            color = "white",
            opacity = 1,
            _hover ={"opacity": 0.5,},
            on_click=State.submit_symptoms), #button submits symptoms and triggers API call
        style={
            "position":"fixed",
            "bottom":"0",
            "marginBottom": "110px",
            #"backgroundColor":bg_color,
        },

    )

def disclaimer() -> rx.Component:
    return rx.text("This tool is not meant to provide professional medical advice but to be a self-service tool for better understanding health! Please see a doctor or healthcare professional if you require help.", 
                   size="0", color="var(--gray-4)", align="center",
                   style={
                       "position":"fixed",
                        "bottom":"0",
                        "marginBottom": "52px",
                        #"backgroundColor":bg_color,
                   },)

def logo() -> rx.Component:
    return rx.logo(
        style={
            "position":"fixed",
            "bottom":"0",
            #"backgroundColor":bg_color,
        },
    )

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            heading(),
            nightshift(),
            chat(),
            message_bar(),
            disclaimer(),
            logo(),
            align="center",
        ),
        style={
            "backgroundColor":bg_color,
        },
    )

app = rx.App()
app.add_page(index)


# def index() -> rx.Component:
    
#     return rx.container(

#         rx.vstack(

#             rx.heading("Get your diagnosis!", size="9"),
#             rx.text("Please input your symptoms", size="15"),
#             # Add a textbox for user input, binding it to the symptoms state
#             rx.input(placeholder="Enter your symptoms here...", size="15", on_change=State.set_symptoms),

#             # Display the diagnosis after the API response
#             rx.cond(
#                 State.diagnosis != "",  # If diagnosis is available
#                 rx.text(State.diagnosis, size="5", color="var(--black-10)"),
#                 rx.text("No diagnosis available", size="5", color="black"),
#             ),

#             #spacing="5",
#             #max_height="100%",
#             #max_width="100%",
#             justify="center",
#             min_height="85vh",
#             width="100%",
#             background_color="var(--mint-1)",

#         ),
#         rx.logo(),
        # )



