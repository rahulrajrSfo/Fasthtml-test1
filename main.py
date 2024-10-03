import os

from datetime import datetime
import pytz
from supabase import create_client
from dotenv import load_dotenv

from fasthtml.common import *

TIMESTAMP_FMT = "%Y-%m-%d %I:%M:%S %p CET"
load_dotenv()

supabase = create_client(os.getenv("SUPABASE_URL"),os.getenv("SUPABASE_KEY"))

app,rt = fast_app(
    hdrs=(Link(rel="icon",type="assets/x-icon",href="/assets/favicon.png"),),
)

def get_time():
    cet_tz = pytz.timezone("CET")
    return datetime.now(cet_tz)

def add_message(name,message):
    timestamp = get_time().strftime(TIMESTAMP_FMT)
    supabase.table("SampleTable").insert(
        {"name":name,"message":message,"timestamp":timestamp}
    ).execute(),


def get_message():
    response = (
        supabase.table("SampleTable").select("*").order("id",desc=true).execute()
    )
    print(response)
    return response.data


@rt('/')
def get(): 
    return Div(P('Hello World!'), hx_get="/change")

def render_message(entry):
    return(
    Article(
            Header(f"Name: {entry['name']}"),
            P(f"Message: {entry['message']} "),
            Footer(f"Time: {entry['timestamp']}")
        )
    )

    
def render_message_list():
    # messages=[
    #     {"name":"Tester1", "message":"Message1", "timestamp":"now"},
    #     {"name":"Tester2", "message":"Message2", "timestamp":"yesterday"}
    # ]

    messages = get_message()

    return Div(
        *[render_message(entry) for entry in messages],
        id="message-list"
    )

def render_content():
    form = Form(
        Fieldset(
            Input(
                type="text",
                name="name",
                placeholder="name",
                required=true
            ),
            Input(
                type="text",
                name="message",
                placeholder="messagex",
                required=true
            ),
            Button(
                "Submit",type = "submit"
            )
        ),
        method="post",
        hx_post = "/submit-message",
        hx_target="#message-list",
        hx_swap="outerHTML",
        hx_on_after_request="this.reset()"
    )
    return Div(
        P(Em("Here is some content....")),
        form,
        render_message_list()

    )

@rt("/submit-message",methods=["POST"])
def post(name:str, message:str):
    add_message(name,message)
    return render_message_list()

@rt('/new')
def get(): 
    return Titled("Sample content 😊",render_content())

@rt('/change')
def get(): 
    return P('Nice to be here!')

serve()