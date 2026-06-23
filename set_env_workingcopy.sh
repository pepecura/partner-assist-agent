#!/bin/bash
# =============================================================================
# Secure Customer Service Agent - Environment Variables
# Generated: Tue Jun  9 03:49:11 PM UTC 2026
# =============================================================================

export GOOGLE_CLOUD_PROJECT="ai-london"
export GOOGLE_CLOUD_LOCATION="us-central1"
export PROJECT_ID="ai-london"
export LOCATION="us-central1"

# Required for ADK to use Vertex AI backend
export GOOGLE_GENAI_USE_VERTEXAI="true"

# BigQuery datasets
export BQ_CUSTOMER_DATASET="customer_service"
export BQ_ADMIN_DATASET="admin"

# Model Armor template (will be set after running create_template.py)
export TEMPLATE_NAME="projects/ai-london/locations/us-central1/templates/cs_agent_security_20260609_155112"

# Agent Engine (will be set after deployment)
export AGENT_ENGINE_ID=""

# Staging bucket for deployment
export STAGING_BUCKET="gs://secure-cs-agent-staging-ai-london"

export AGENT_ENGINE_ID="5338250448887349248"
export AGENT_IDENTITY="principal://agents.global.org-680181529320.system.id.goog/resources/aiplatform/projects/108525214404/locations/us-central1/reasoningEngines/5338250448887349248"

echo "✅ Environment variables loaded for project: ${PROJECT_ID}"


