FROM ollama/ollama:latest

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

EXPOSE 11434

# Set environment variables for CORS
ENV OLLAMA_ORIGINS="*"
ENV OLLAMA_HOST="0.0.0.0:11434"

# Create a simple startup script inline
RUN echo '#!/bin/bash\n\
echo "Starting Ollama server..."\n\
/bin/ollama serve &\n\
OLLAMA_PID=$!\n\
echo "Waiting for Ollama to start..."\n\
sleep 10\n\
echo "Ollama is running on PID $OLLAMA_PID"\n\
wait $OLLAMA_PID' > /start.sh && chmod +x /start.sh

CMD ["/bin/bash", "/start.sh"]
