from dotenv import load_dotenv
load_dotenv()
import getpass
import os
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
if not os.getenv("HUGGINGFACEHUB_API_TOKEN"):
    os.environ["HUGGINGFACEHUB_API_TOKEN"] = getpass.getpass("Enter your token: ")

def get_agent_response(user_input: str) -> str:
    # llm = HuggingFaceEndpoint(
    #     repo_id="deepseek-ai/DeepSeek-R1-0528",
    #     task="text-generation",
    #     max_new_tokens=512,
    #     do_sample=False,
    #     repetition_penalty=1.03,
    #     provider="auto",  # let Hugging Face choose the best provider for you
    # )
    callbacks = [StreamingStdOutCallbackHandler()]
    llm = HuggingFaceEndpoint(
                # endpoint_url="http://localhost:8010/",
                repo_id="deepseek-ai/DeepSeek-R1-0528",
                max_new_tokens=512,
                top_k=10,
                top_p=0.95,
                typical_p=0.95,
                temperature=0.01,
                repetition_penalty=1.03,
                callbacks=callbacks,
                streaming=True,
                huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
            )

    chat_model = ChatHuggingFace(llm=llm)

    messages = [
        SystemMessage(content= "You are an expert assistant specializing in resume analysis and job matching. "
                                "You will receive a job description and a candidate's resume. "
                                "Your tasks are:\n"
                                "1. Analyze the resume to identify relevant skills, experience, and qualifications that match the job description.\n"
                                "2. Highlight specific examples from the resume that demonstrate suitability for the role.\n"
                                "3. Point out any gaps or missing requirements compared to the job description.\n"
                                "4. Provide a clear, concise, and informative summary explaining the candidate's fit for the job.\n"
                                "Your response should help the user understand the strengths and weaknesses of the candidate in relation to the job requirements."),
        HumanMessage(
            content=user_input
        ),
    ]
    
    output = ""
    text= ""
    # ai_msg = chat_model.invoke(messages)
    for chunk in chat_model.stream(messages):
        text += str(chunk.content)
        print(str(chunk.content), end='', flush=True)

    while "<think>" in text and "</think>" in text:
        start = text.find("<think>")
        end = text.find("</think>") + len("</think>")
        text = text[:start] + text[end:]
    output += text   
    return output.strip()

    
   
