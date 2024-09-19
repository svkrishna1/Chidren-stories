import json
import subprocess
import streamlit as st
import pyttsx3

# Function to get stories from Ollama
def get_stories_from_ollama(prompt):
    command = f'ollama run phi3 "{prompt}"'
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        result.check_returncode()
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"

# Function for text-to-speech
def narrate_story(story, language):
    engine = pyttsx3.init()

    # Set language voice if available
    voices = engine.getProperty('voices')

    # Attempt to find a voice for the specified language
    for voice in voices:
        if language.lower() in voice.languages:
            engine.setProperty('voice', voice.id)
            break

    # Use pyttsx3 to narrate the story
    engine.say(story)
    engine.runAndWait()

# Function to load or save default language
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
    languages = ["English", "Telugu", "Tamil", "Kannada", "Malayalam"]
    return st.selectbox("Select Language:", options=languages, index=0)

# Function to get the user's interest
def select_interest():
    interests = ["animals", "adventure", "magic", "friendship", "science", 
                 "space", "superheroes", "mystery", "historical", "educational"]
    return st.selectbox("Select Interest:", options=interests, index=0)

# Function to generate a downloadable file
def create_downloadable_story(story, language, interest):
    filename = f"{language}_{interest}_story.txt"
    return filename, story

# Main Streamlit application
def main():
    st.set_page_config(page_title="Story Generator", layout="centered")

    # Custom CSS for attractive styling
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f8ff;
            color: #003366;
            font-family: 'Arial', sans-serif;
        }
        .stButton button {
            background-color: #007acc;
            color: white;
            border: 2px solid #005999;
            border-radius: 10px;
            font-size: 16px;
            padding: 10px;
        }
        .stDownloadButton button {
            background-color: #28a745;
            color: white;
            border: 2px solid #007acc;
            border-radius: 10px;
            font-size: 16px;
        }
        .stSelectbox, .stTextInput {
            background-color: #ffffff;
            border: 2px solid #007acc;
            border-radius: 10px;
            margin: 5px 0;
        }
        .history-container {
            border: 2px solid #007acc;
            padding: 10px;
            border-radius: 10px;
            background-color: #e3f2fd;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("🌟 Story Narrator🎤")

    # Sidebar for history
    st.sidebar.header("📝 Generated Stories History")
    history_container = st.sidebar.container()

    # Initialize story history
    if "story_history" not in st.session_state:
        st.session_state.story_history = []

    with history_container:
        st.markdown("<div class='history-container'>", unsafe_allow_html=True)
        if st.session_state.story_history:
            for story in st.session_state.story_history:
                st.write(story)
        else:
            st.write("No stories generated yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Load the default language
    default_language = load_default_language()
    st.write(f"Current default language: **{default_language}**")

    # Language, Interest, and Keywords input
    language = select_language()
    interest = select_interest()
    keywords = st.text_input("Add specific keywords or themes (comma-separated):")

    # Button to generate a story
    if st.button("Generate Story"):
        prompt = f"Generate a story in {language} about {interest}."
        if keywords:
            prompt += f" Include keywords: {keywords}."
        
        story = get_stories_from_ollama(prompt)

        # Display story or error
        if "Error" not in story:
            st.subheader(f"Story in **{language}** about **{interest}**:")
            st.write(story)
            
            # Save the story in the history
            st.session_state.story_history.append(story)

            # Text-to-Speech Narration
            if st.button("Narrate Story"):
                narrate_story(story, language)

            # Download Story
            filename, story_content = create_downloadable_story(story, language, interest)
            st.download_button("Download Story", story_content, filename=filename, mime="text/plain")
        else:
            st.error(story)

    # Button to save the default language
    if st.button("Save Default Language"):
        save_default_language(language)
        st.success(f"Default language has been set to **{language}**.")

# Run the app
if __name__ == "__main__":
    main()
