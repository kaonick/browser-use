from langchain_openai import ChatOpenAI
from langchain_openai import AzureChatOpenAI
from litellm import completion
from dotenv import load_dotenv
import os
# load_dotenv()
BASEDIR = os.path.abspath(os.path.dirname(__file__))
# Connect the path with your '.env' file name
load_dotenv(os.path.join(BASEDIR, '.env'))


def openai():
    llm = ChatOpenAI(base_url=os.getenv("OPENAI_BASE_URL"),
                     api_key=os.getenv("OPENAI_API_KEY"),
                     model="gpt-4o")
    return llm

def openai_azure():
    os.environ["AZURE_OPENAI_API_KEY"] = os.getenv("llm_api_key")
    os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv("llm_api_url")
    os.environ["OPENAI_API_VERSION"] = os.getenv("llm_api_version")
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        # openai_api_version=settings.llm_api_version,
        # 2023-08-01-preview",  # "2023-07-01-preview",  # "2023-03-15-preview",
        azure_deployment=os.getenv("llm_completions_deployment_name"),  # "dp-gpt4",  # "gpt4",
        openai_api_type="azure",  # "azure",  # "azure",
        temperature=0,
        streaming=True,
        # max_tokens=4096,
        # max_tokens=2048
    )
    return llm


def litellm_azure_openai():
    # Set environment variables (or hardcode for testing)
    def get_llm_response(messages):
        deployment_name=os.getenv("llm_completions_deployment_name")
        model=f"azure/{deployment_name}"
        response = completion(
            model=model,  # e.g., "azure/my-gpt4o-deployment"
            api_key=os.getenv("llm_api_key"),
            api_base=os.getenv("llm_api_url"),
            api_version=os.getenv("llm_api_version"),  # Specify the API version (check Azure docs for latest)
            messages=messages
        )
        return response.choices[0].message.content

    return get_llm_response

# llm=litellm_azure_openai()
# llm=openai()
llm=openai_azure()


if __name__ == '__main__':
    print(llm.invoke([{"role":"user","content":"你好!"}]))