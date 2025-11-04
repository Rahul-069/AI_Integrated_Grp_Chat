FROM ollama/ollama:latest

# Install curl (optional for healthcheck)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Expose API port
EXPOSE 11434

ENV OLLAMA_ORIGINS="*"
ENV OLLAMA_HOST="0.0.0.0"

# Copy startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

ENTRYPOINT ["/start.sh"]
