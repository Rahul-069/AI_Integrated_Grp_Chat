# ai_helper.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')

def summarize_messages(messages):
    """
    Summarize a list of chat messages
    messages: list of dicts with 'username' and 'message' keys
    """
    if not messages:
        return "No messages to summarize."
    
    # Format messages for AI
    chat_text = "\n".join([f"{msg['username']}: {msg['message']}" for msg in messages])
    
    prompt = f"""Summarize the following chat conversation in 2-3 concise sentences. 
Focus on the main topics discussed and key points:

{chat_text}

Summary:"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error generating summary: {str(e)}"


def answer_question(messages, question):
    """
    Answer a question based on chat history
    """
    if not messages:
        return "No chat history available to answer questions."
    
    # Format messages for context
    chat_text = "\n".join([f"{msg['username']}: {msg['message']}" for msg in messages])
    
    prompt = f"""Based on the following chat conversation, answer this question concisely:

Chat History:
{chat_text}

Question: {question}

Answer:"""
    
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"


def generate_smart_replies(recent_messages, max_suggestions=3):
    """
    Generate smart reply suggestions based on recent messages
    """
    if not recent_messages:
        return ["Hello!", "How are you?", "Thanks!"]
    
    # Get last few messages for context
    context = "\n".join([f"{msg['username']}: {msg['message']}" for msg in recent_messages[-5:]])
    
    prompt = f"""Based on this chat conversation, suggest {max_suggestions} short (5-10 words), 
natural reply options that would make sense as responses. 
Return ONLY the suggestions, one per line, without numbering or extra text.

Chat:
{context}

Suggestions:"""
    
    try:
        response = model.generate_content(prompt)
        suggestions = [line.strip() for line in response.text.strip().split('\n') if line.strip()]
        # Clean up any numbering
        suggestions = [s.lstrip('1234567890.-) ') for s in suggestions]
        return suggestions[:max_suggestions]
    except Exception as e:
        return ["Got it!", "Interesting!", "Tell me more"]


def get_conversation_insights(messages):
    """
    Get insights about the conversation (sentiment, topics, etc.)
    """
    if not messages:
        return {"sentiment": "neutral", "topics": [], "summary": "No messages yet."}
    
    chat_text = "\n".join([f"{msg['username']}: {msg['message']}" for msg in messages])
    
    prompt = f"""Analyze this chat conversation and provide:
1. Overall sentiment (positive/neutral/negative)
2. Main topics discussed (comma-separated list)
3. Brief summary (one sentence)

Chat:
{chat_text}

Format your response as:
Sentiment: [sentiment]
Topics: [topic1, topic2, topic3]
Summary: [one sentence summary]"""
    
    try:
        response = model.generate_content(prompt)
        lines = response.text.strip().split('\n')
        
        insights = {
            "sentiment": "neutral",
            "topics": [],
            "summary": "No summary available"
        }
        
        for line in lines:
            if line.startswith("Sentiment:"):
                insights["sentiment"] = line.split(":", 1)[1].strip().lower()
            elif line.startswith("Topics:"):
                topics_str = line.split(":", 1)[1].strip()
                insights["topics"] = [t.strip() for t in topics_str.split(",")]
            elif line.startswith("Summary:"):
                insights["summary"] = line.split(":", 1)[1].strip()
        
        return insights
    except Exception as e:
        return {"error": str(e)}