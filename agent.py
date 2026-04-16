import requests
import json
import base64
from io import BytesIO

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen3-vl:8b"

MASTER_PROMPT = """You are an advanced AI Content Creation Agent specialized in social media growth, branding, and viral marketing.

You analyze both visual and textual inputs and generate high-quality, platform-specific content strategies.

Your tasks:
1. Understand the uploaded image or input content deeply
2. Identify:
   - Context
   - Emotion
   - Target audience
   - Content type
3. Generate the following:

- 🔥 Viral Hook (very catchy, curiosity-driven)
- ✍️ Caption (platform-specific tone)
- 🎯 Target Audience
- 💡 Content Idea Expansion
- 🎬 Script (if video/reel)
- 📈 Growth Strategy
- 🧠 Psychological Trigger used (FOMO, curiosity, storytelling, etc.)
- 🏷️ Hashtags (trending + niche mix)
- 🎨 Design Improvement Suggestions (if image provided)

Guidelines:
- Be creative but practical
- Avoid generic outputs
- Focus on virality and engagement
- Adapt tone based on platform (Instagram: casual, LinkedIn: professional, YouTube: engaging storytelling)

Output format:
Use structured sections with emojis for clarity. Do not include introductory text like "Sure, here is the generated output", just the payload directly.
"""

def process_content_request(image_pil, text_input, platform, content_type, tone):
    # Prepare prompt Context
    context_prompt = f"{MASTER_PROMPT}\n\n"
    context_prompt += f"Target Platform: {platform}\n"
    context_prompt += f"Content Type: {content_type}\n"
    context_prompt += f"Tone/Style: {tone}\n"
    
    if text_input and text_input.strip():
        context_prompt += f"\nUser Input/Textual Context: {text_input}\n"
    
    payload = {
        "model": MODEL_NAME,
        "prompt": context_prompt,
        "stream": True  # Enable streaming to make it feel instantly responsive
    }

    if image_pil:
        # Convert PIL image to base64
        buffered = BytesIO()
        image_pil.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        # Ollama API expects base64 encoded images in a list
        payload["images"] = [img_str]

    try:
        with requests.post(OLLAMA_URL, json=payload, timeout=180, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        yield chunk["response"]
    except Exception as e:
        yield f"\n\nError communicating with local LLM: {str(e)}\n\nMake sure Ollama is running with the {MODEL_NAME} model."
