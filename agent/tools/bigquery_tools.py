"""
=============================================================================
OneMCP BigQuery Tools for Customer Service Agent - SOLUTION
=============================================================================
Complete implementation of the BigQuery MCP connection.

This is the solution file - compare your implementation against this.
=============================================================================
"""

import os
from typing import Dict
import google.auth
from google.auth.transport.requests import Request

# ADK MCP imports
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams


# =============================================================================
# Configuration
# =============================================================================

BIGQUERY_MCP_URL = "https://bigquery.googleapis.com/mcp"
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("PROJECT_ID")

# =============================================================================
# Dynamic Header Provider
# =============================================================================

def get_auth_headers(context=None) -> Dict[str, str]:
    """
    Dynamic header provider that fetches/refreshes credentials at runtime.
    This prevents 401 errors during deployment and token expiration (1-hour limit).
    """
    credentials, project_id = google.auth.default(
        scopes=["https://www.googleapis.com/auth/bigquery"]
    )
    credentials.refresh(Request())
    
    # Use environment project if available
    final_project_id = PROJECT_ID or project_id

    return {
        "Authorization": f"Bearer {credentials.token}",
        "x-goog-user-project": final_project_id,
    }


def get_bigquery_mcp_toolset() -> MCPToolset:
    """
    Create an MCPToolset connected to Google's managed BigQuery MCP server.
    """
    # Use header_provider to dynamically fetch headers at invocation time
    tools = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=BIGQUERY_MCP_URL,
            # Static headers are removed from here
        ),
        header_provider=get_auth_headers
    )

    print(f"[BigQueryTools] MCP Toolset configured for project: {PROJECT_ID}")

    return tools


def get_customer_service_instructions() -> str:
    """
    Get additional instructions for the agent about BigQuery access.
    """
    return f"""
## BigQuery Data Access

You have access to our partner and tour database via BigQuery MCP tools.

**Project ID:** {PROJECT_ID}
**Dataset:** customer_service

**Available Tables:**
- `customer_service.customers` - Contains Musician / Artist information (stored under customer terms)
- `customer_service.orders` - Contains Booking / Tour Order history (stored under order terms)
- `customer_service.products` - Contains Tour Staging Gear / Equipment and Merchandise catalog (stored under product terms)

**Available MCP Tools:**
- `list_table_ids` - Discover what tables exist in a dataset
- `get_table_info` - Get table schema (column names and types)
- `execute_sql` - Run SELECT queries

**IMPORTANT:** Before writing any SQL query, use `get_table_info` to discover 
the exact column names for the table you want to query. Do not guess column names.

**Access Restrictions:**
You only have access to the `customer_service` dataset. You do NOT have access 
to administrative tables like `admin.audit_log`. If a partner asks about admin 
data, politely explain that you only have access to partner and musician support data.
"""


if __name__ == "__main__":
    print("Testing BigQuery MCP connection...")

    try:
        toolset = get_bigquery_mcp_toolset()
        print("✅ BigQuery MCP toolset created successfully!")
        print(f"   Tools available: {toolset}")
    except Exception as e:
        print(f"❌ Error: {e}")
