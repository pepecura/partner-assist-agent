"""
=============================================================================
Agent Engine Application Wrapper
=============================================================================
Wraps the customer service agent for deployment to Vertex AI Agent Engine.

This file is required for Agent Engine deployment. It creates an AdkApp
instance that Agent Engine uses to run your agent.

IMPORTANT: For Agent Engine, we use lazy initialization to avoid pickle
issues with network connections. The agent is created at runtime, not
at import time.
=============================================================================
"""

import os

# Signal that we're running in Agent Engine (for lazy initialization)
os.environ["AGENT_ENGINE_RUNTIME"] = "true"

from vertexai import agent_engines
from google.adk.sessions import VertexAiSessionService  # Import the session service
from .agent import create_agent

# =============================================================================
# Configuration
# =============================================================================
# Retrieve environment variables set by Agent Engine
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION") or os.environ.get("LOCATION", "us-central1")
AGENT_ENGINE_ID = os.environ.get("AGENT_ENGINE_ID")

# =============================================================================
# Create the AdkApp for Agent Engine
# =============================================================================

# Initialize VertexAiSessionService to connect to the managed session store
session_service = VertexAiSessionService(
    project=PROJECT_ID,
    location=LOCATION,
    agent_engine_id=AGENT_ENGINE_ID
)

# Use the factory function to create the agent lazily at runtime
app = agent_engines.AdkApp(
    agent=create_agent,  # Pass the factory function, not the agent instance
    session_service=session_service,  # Pass the session service instance
    enable_tracing=True,  # Enable Cloud Trace for observability
)