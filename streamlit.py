import json
import subprocess
import streamlit as st

# Function to get stories from Ollama
def get_stories_from_ollama(prompt):
    command = f'ollama run llama3 "{prompt}"'
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        result.check_returncode()
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

# Function to get images from the model based on the story prompt
def get_images_from_model(prompt):
    command = f'ollama run image_model "{prompt}"'  # Hypothetical model for images
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        result.check_returncode()
        return result.stdout.strip().split('\n')  # Assuming model returns image URLs
    except subprocess.CalledProcessError as e:
        return []

# Load or save default language
def load_default_language():
    try:
        with open("default_language.json", "r") as file:
            data = json.load(file)
            return data.get("default_language", "English")
    except FileNotFoundError:
        return "English"

def save_default_language(language):
    with open("default_language.json", "w") as file:
        json.dump({"default_language": language}, file)

# Function to select language
def select_language():
    languages = {
        "English": "English",
        "Telugu": "Telugu",
        "Tamil": "Tamil",
        "Kannada": "Kannada",
        "Malayalam": "Malayalam"
    }
    return st.selectbox("Select Language:", options=list(languages.keys()), key="language")

# Function to get the user's interest
def get_user_interest():
    interests = {
        "animals": "Animals",
        "adventure": "Adventure",
        "magic": "Magic",
        "friendship": "Friendship",
        "science": "Science",
        "space": "Space",
        "superheroes": "Superheroes",
        "mystery": "Mystery",
        "historical": "Historical",
        "educational": "Educational"
    }
    return st.selectbox("Select Interest:", options=list(interests.keys()), key="interest")

# Function to select story length
def select_story_length():
    lengths = {
        "Short": "Short",
        "Medium": "Medium",
        "Long": "Long"
    }
    return st.selectbox("Select Story Length:", options=list(lengths.keys()), key="length")

# Function to generate a downloadable file
def create_downloadable_story(story, language, interest):
    filename = f"{language}_{interest}_story.txt"
    return filename, story

# Main Streamlit application
def main():
    st.set_page_config(page_title="Story Generator", layout="centered")

    # Custom CSS for styling
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f4f8;
            color: #003366;
            font-family: 'Arial', sans-serif;
        }
        .stButton>button {
            border: 2px solid #007acc;  /* Border color */
            background-color: transparent; /* Remove background color */
            color: #007acc;              /* Text color */
            font-weight: bold;           /* Make text bold */
        }
        .stSelectbox, .stTextInput {
            background-color: #ffffff;
            border: 2px solid #007acc;
            border-radius: 5px;
        }
        .stDownloadButton>button {
            background-color: #005999;
            color: white;
            border: 2px solid #007acc;
        }
        .history-container {
            border: 2px solid #007acc;
            padding: 10px;
            border-radius: 5px;
            background-color: #e3f2fd;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🌟 Story Generator 🌟")
    st.sidebar.header("History")
    history_container = st.sidebar.container()

    # Show history (if any)
    if "story_history" not in st.session_state:
        st.session_state.story_history = []

    with history_container:
        st.markdown("<div class='history-container'>", unsafe_allow_html=True)
        st.subheader("Generated Stories:")
        for story in st.session_state.story_history:
            st.write(story)
        st.markdown("</div>", unsafe_allow_html=True)

    default_language = load_default_language()  # Load default language
    st.write(f"Current default language is: **{default_language}**")

    # User inputs
    language = select_language()  # Select language
    interest = get_user_interest()  # Get user interest
    length = select_story_length()  # Select story length
    keywords = st.text_input("Add specific keywords or themes (comma-separated):", key="keywords")

    # Button to generate story
    if st.button("Generate Story", key="generate_button"):
        prompt = f"Generate a {length.lower()} story in {language} about {interest.lower()}."
        if keywords:
            prompt += f" Include keywords: {keywords}."
        
        story = get_stories_from_ollama(prompt)
        st.subheader(f"Story in **{language}** about **{interest}**:")
        st.write(story)

        # Store generated story in history
        st.session_state.story_history.append(story)

        # Fetch and display related images from the model
        images = get_images_from_model(prompt)
        if images:
            for img in images:
                st.image(img, caption="Related Image", use_column_width=True)
        else:
            st.write("No related images found.")

        # Save option
        filename, story_content = create_downloadable_story(story, language, interest)
        st.download_button("Download Story", story_content, filename=filename, mime="text/plain", key="download_button")

    # Save the selected language as default
    if st.button("Save Default Language"):
        save_default_language(language)
        st.success(f"Default language has been set to **{language}**.")

# Run the app
if __name__ == "__main__":
    main()
