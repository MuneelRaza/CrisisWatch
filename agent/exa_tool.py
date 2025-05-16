import os
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()

from langchain.tools import Tool
from exa_py import Exa



exa = Exa(api_key=os.environ["EXA_API_KEY"])

class CrisisSearchInput(BaseModel):
    query: str


CRISIS_CONTEXT = "global conflict, humanitarian crisis, war, disaster, emergency response, peacekeeping, UN, relief, refugee situation"


def extract_content_only(search_response):
    all_texts = []
    for result in search_response.results:
        if result.text:
            clean_text = result.text.strip()
            all_texts.append(clean_text)
    return "\n\n---\n\n".join(all_texts)


def search_and_contents(query: str):
    """
    Perform a crisis-focused search using Exa.
    Adds context keywords to bias the search toward crisis-related topics.
    """
    print(f"🔍 Running search for query: {query}")
    full_query = f"{query} related to ({CRISIS_CONTEXT})"
    search_response = exa.search_and_contents(
        full_query,
        use_autoprompt=True,
        num_results=3,
        text=True,
        highlights=True
    )
    return search_response


exa_search_tool = Tool(
    name="Crisis_Centric_Search",
    func=search_and_contents,
    description=(
        "Use this tool when the user asks about recent, current, or ongoing crisis events. "
        "This includes conflicts, wars, natural disasters, humanitarian aid updates, and emergencies. "
        "The tool returns live information from trusted sources (UN, Reuters, ReliefWeb, etc.)."
    ),
    args_schema=CrisisSearchInput
)


# def test_search():
#     query = "current situation in Gaza"
#     result = search_and_contents(query)
#     print("Search result:\n", result)

# if __name__ == "__main__":
#     test_search()
