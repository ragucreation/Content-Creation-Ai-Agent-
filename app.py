import streamlit as st
from PIL import Image
from agent import process_content_request

st.set_page_config(
    page_title="Multi-Modal Content Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🤖 Chat with Content Creator")
st.markdown("**(Vision + Text + Strategy)** - Powered by `qwen3-vl:8b` via Ollama")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Agent Settings")
    st.markdown("Configure how the agent responds.")
    
    platform = st.selectbox("Select Platform", ["Instagram 📸", "LinkedIn 💼", "YouTube 🎥", "Shorts/Reels 🎬"])
    content_type = st.selectbox("Content Type", ["Image Post", "Carousel", "Video/Reel", "Advertisement"])
    tone = st.selectbox("Select Tone", ["Viral & Engaging 🔥", "Professional & Clean 💼", "Funny & Meme-like 🤣", "Emotional & Storytelling 🥲"])
    
    st.markdown("---")
    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message and message["image"] is not None:
            st.image(message["image"], width=300)

# React to user input
if prompt := st.chat_input("Ask the agent to generate content...", accept_file=True, file_type=["png", "jpg", "jpeg"]):
    # Safely handle the prompt based on its type
    if isinstance(prompt, str):
        user_text = prompt
        files = []
    else:
        user_text = prompt.text if hasattr(prompt, "text") else prompt.get("text", "")
        files = prompt.files if hasattr(prompt, "files") else prompt.get("files", [])

    # Read the attached image if one exists
    pil_image = None
    if files and len(files) > 0:
        pil_image = Image.open(files[0])

    # Add user message to chat history
    user_message = {"role": "user", "content": user_text}
    if pil_image is not None:
        user_message["image"] = pil_image
        
    st.session_state.messages.append(user_message)

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_text)
        if pil_image is not None:
            st.image(pil_image, caption="Included Image Context", width=300)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        stream = process_content_request(
            image_pil=pil_image,
            text_input=user_text,
            platform=platform,
            content_type=content_type,
            tone=tone
        )
        response = st.write_stream(stream)
            
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
