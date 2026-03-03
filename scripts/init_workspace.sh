#!/usr/bin/env bash
# The Foundry - Workspace Initialization Script
# Creates the runtime workspace directory structure that agents will use

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Workspace directory (from .env or default)
WORKSPACE_DIR="${FOUNDRY_WORKSPACE:-$HOME/.openclaw/workspace/foundry}"

echo -e "${GREEN}🏭 The Foundry - Workspace Initialization${NC}"
echo ""

# Create main workspace directory
echo -e "${YELLOW}Creating workspace structure...${NC}"
mkdir -p "$WORKSPACE_DIR"

# Create subdirectories
mkdir -p "$WORKSPACE_DIR/archive"          # Old build data
mkdir -p "$WORKSPACE_DIR/research"         # Trend Researcher forecasts
mkdir -p "$WORKSPACE_DIR/analysis"         # Consensus Analyst outputs
mkdir -p "$WORKSPACE_DIR/social"           # Social media content
mkdir -p "$WORKSPACE_DIR/social/assets"    # Visual content

# Initialize history.json if it doesn't exist
HISTORY_FILE="$WORKSPACE_DIR/history.json"
if [ ! -f "$HISTORY_FILE" ]; then
    echo -e "${YELLOW}Initializing history.json...${NC}"
    cat > "$HISTORY_FILE" << 'EOF'
{
  "schema_version": 1,
  "builds": [],
  "rejections": [],
  "dedup_window_days": 30
}
EOF
    echo -e "${GREEN}✓ Created $HISTORY_FILE${NC}"
else
    echo -e "${GREEN}✓ history.json already exists${NC}"
fi

# Initialize metrics.jsonl if it doesn't exist
METRICS_FILE="$WORKSPACE_DIR/metrics.jsonl"
if [ ! -f "$METRICS_FILE" ]; then
    echo -e "${YELLOW}Initializing metrics.jsonl...${NC}"
    touch "$METRICS_FILE"
    echo -e "${GREEN}✓ Created $METRICS_FILE${NC}"
else
    echo -e "${GREEN}✓ metrics.jsonl already exists${NC}"
fi

# Create builds directory (where Builder creates projects)
BUILDS_DIR="${FOUNDRY_BUILDS:-$HOME/projects/foundry}"
if [ ! -d "$BUILDS_DIR" ]; then
    echo -e "${YELLOW}Creating builds directory...${NC}"
    mkdir -p "$BUILDS_DIR"
    echo -e "${GREEN}✓ Created $BUILDS_DIR${NC}"
else
    echo -e "${GREEN}✓ Builds directory exists: $BUILDS_DIR${NC}"
fi

# Summary
echo ""
echo -e "${GREEN}✅ Workspace initialized successfully${NC}"
echo ""
echo "Workspace: $WORKSPACE_DIR"
echo "  ├── history.json           (deduplication tracking)"
echo "  ├── metrics.jsonl          (nightly performance log)"
echo "  ├── archive/               (old build data)"
echo "  ├── research/              (trend forecasts)"
echo "  ├── analysis/              (consensus evaluations)"
echo "  └── social/                (content drafts)"
echo ""
echo "Builds: $BUILDS_DIR"
echo "  (Builder will create: YYYYMMDD-project-name/)"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "1. Copy .env.example to .env and fill in credentials"
echo "2. Run: pip install -r requirements.txt"
echo "3. Verify agents are registered in OpenClaw config"
echo "4. Ready to start Epic 1.1 (Trend Scout)"
