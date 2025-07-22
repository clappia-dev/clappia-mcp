import os
from clappia_api_tools import SubmissionClient, AppDefinitionClient

CLAPPIA_EXTERNAL_API_BASE_URL = "https://api-public-v3.clappia.com"

submission_client = SubmissionClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    workplace_id=os.getenv("CLAPPIA_WORKPLACE_ID"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL,
)

app_definition_client = AppDefinitionClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    workplace_id=os.getenv("CLAPPIA_WORKPLACE_ID"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL,
)