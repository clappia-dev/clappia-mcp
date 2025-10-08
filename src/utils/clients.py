import os
from clappia_api_tools import (
    SubmissionAPIKeyClient as SubmissionClient,
    AppDefinitionAPIKeyClient as AppDefinitionClient,
    WorkflowDefinitionAPIKeyClient as WorkflowDefinitionClient,
    AnalyticsAPIKeyClient as AnalyticsClient,
    WorkplaceAPIKeyClient as WorkplaceClient,
)
CLAPPIA_EXTERNAL_PREPROD_API_BASE_URL = "https://preprod-public-v4.clappia.com"
CLAPPIA_EXTERNAL_API_BASE_URL = "https://api-public-v3.clappia.com"
CLAPPIA_EXTERNAL_API_BASE_URL_V4 = "https://api-public-v4.clappia.com"

submission_client = SubmissionClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL_V4,
)

app_definition_client = AppDefinitionClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    base_url=f"{CLAPPIA_EXTERNAL_API_BASE_URL_V4}/appdefinitionv2",
)

workflow_definition_client = WorkflowDefinitionClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL_V4,
)

analytics_client = AnalyticsClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL_V4,
)

workplace_client = WorkplaceClient(
    api_key=os.getenv("CLAPPIA_API_KEY"),
    base_url=CLAPPIA_EXTERNAL_API_BASE_URL_V4,
)
