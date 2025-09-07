from IPython.display import Image, display


graph_builder = StateGraph(State)

graph = graph_builder.compile()
from IPython.display import Image, display
try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    pass