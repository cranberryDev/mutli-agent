from dotenv import load_dotenv
load_dotenv()

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
import getpass
import os
from IPython.display import Image, display



if "AZURE_OPENAI_API_KEY" not in os.environ:
    print('inside if')
    os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass(
        os.environ["AZURE_OPENAI_API_KEY"]
    )
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://ragha-meisspfj-eastus2.cognitiveservices.azure.com/"

class State(TypedDict):
    # messages have the type "list".
    # The add_messages function appends messages to the list, rather than overwriting them
    messages: Annotated[list, add_messages]
graph_builder = StateGraph(State)


llm = AzureChatOpenAI(
    azure_deployment="gpt-4o-mini",  # or your deployment
    api_version="2024-12-01-preview",  # or your api version
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}
# ‘’’The first argument is the unique node name
# The second argument is the function or object that will be called whenever the node is used.’’’
graph_builder.add_node("chatbot", chatbot)

# Set entry and finish points
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")



graph = graph_builder.compile()
try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    pass

# Run the chatbot
while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        print("Goodbye!")
        break
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)