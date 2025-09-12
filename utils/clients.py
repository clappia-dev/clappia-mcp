import os
from clappia_api_tools import (
    SubmissionClient,
    AppDefinitionClient,
    WorkflowDefinitionClient,
    AnalyticsClient,
    WorkplaceClient,
)

CLAPPIA_EXTERNAL_API_BASE_URL = "https://api-public-v4.clappia.com"

submission_client = SubmissionClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL,
)

app_definition_client = AppDefinitionClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL,
)

workflow_definition_client = WorkflowDefinitionClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL,
)

analytics_client = AnalyticsClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL,
)

workplace_client = WorkplaceClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL,
)
