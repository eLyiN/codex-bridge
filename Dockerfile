FROM node:20-slim

# Set working directory
WORKDIR /app

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Codex CLI globally
RUN npm install -g @openai/codex

# Copy Python project files
COPY pyproject.toml ./
COPY src/ ./src/

# Install Python dependencies
RUN pip3 install .

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT=8080
ENV CODEX_BRIDGE_TIMEOUT=60

# Health check to verify Codex CLI is available
RUN codex --version

# Expose port
EXPOSE $PORT

# Run the MCP server
CMD ["python3", "-m", "src"]