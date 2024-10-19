# """Welcome to Reflex! This file outlines the steps to create a basic app."""

# import reflex as rx

# from rxconfig import config


# class State(rx.State):
#     """The app state."""

#     ...


# def index() -> rx.Component:
#     # Welcome Page (Index)
#     return rx.container(
#         rx.color_mode.button(position="top-right"),
#         rx.vstack(
#             rx.heading("Get your diagnosis!", size="9"),
#             rx.text(
#                 "Please input your symptoms",
#                 rx.code(f"{config.app_name}/{config.app_name}.py"),
#                 size="5",
#             ),
#             rx.link(
#                 rx.button("Check out our docs!"),
#                 href="https://reflex.dev/docs/getting-started/introduction/",
#                 is_external=True,
#             ),
#             spacing="5",
#             justify="center",
#             min_height="85vh",
#         ),
#         rx.logo(),
#     )


# app = rx.App()
# app.add_page(index)



import reflex as rx
from rxconfig import config

class State(rx.State):
    """The app state."""
    
    symptoms: str = ""

    def submit_symptoms(self):
        # This could trigger a diagnosis processing (e.g., call an API or process the input)
        print(f"Symptoms submitted: {self.symptoms}")

def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.container(
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Get your diagnosis!", size="9"),
            rx.text(
                "Please input your symptoms",
                size="5",
            ),
            # Add a textbox for user input, binding it to the symptoms state
            rx.input(placeholder="Enter your symptoms here...", on_change=State.set_symptoms),
            # Add a button that will submit the symptoms
            rx.button("Submit", on_click=State.submit_symptoms),
            spacing="5",
            justify="center",
            min_height="85vh",
        ),
        rx.logo(),
    )

app = rx.App()
app.add_page(index)

