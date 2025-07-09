import streamlit as st
from datetime import datetime

# Import our custom modules
from src.story_generator import StoryGenerator
from src.database import save_story, load_stories
from src.ui_components import render_story_form, display_story

# Page configuration
st.set_page_config(
    page_title="TinyTales AI",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("TinyTales AI")
    st.markdown("Create magical stories for children with AI!")

    # Initialize session state
    if 'generated_story' not in st.session_state:
        st.session_state.generated_story = None
    if 'story_metadata' not in st.session_state:
        st.session_state.story_metadata = None

    # Create tabs
    tab1, tab2 = st.tabs(["Generate Story", "Story Library"])

    with tab1:
        generate_story_tab()

    with tab2:
        story_library_tab()


def generate_story_tab():
    st.header("Create Your Story")

    story_params = render_story_form()  

    if story_params:
        with st.spinner("Creating your magical story..."):
            generator = StoryGenerator()
            story_data = generator.generate_story(story_params)

            if story_data:
                st.session_state.generated_story = story_data['story']
                st.session_state.story_metadata = story_data['metadata']
                st.success("Story generated successfully!")
            else:
                st.error("Failed to generate story. Please try again.")

    # Display generated story
    if st.session_state.generated_story:
        st.divider()
        display_story(st.session_state.generated_story, st.session_state.story_metadata)

        # Save or regenerate
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Save Story", use_container_width=True):
                story_id = save_story(
                    st.session_state.generated_story,
                    st.session_state.story_metadata
                )
                st.success(f"Story saved with ID: {story_id}")

        with col2:
            if st.button("Generate New Story", use_container_width=True):
                st.session_state.generated_story = None
                st.session_state.story_metadata = None
                st.rerun()


def story_library_tab():
    st.header("Story Library")
    stories = load_stories()

    if not stories:
        st.info("No stories saved yet. Generate your first story!")
        return

    for story_id, story_data in stories.items():

        # Use button to toggle visibility
        key = f"show_{story_id}"

        read_clicked = st.button(f"📖 Read: {story_data['metadata']['title']}", key=f"read_{story_id}")
        hide_clicked = st.button("Hide Story", key=f"hide_{story_id}")

        # Toggle visibility using a temporary variable
        visible_key = f"show_story_{story_id}"

        # Initialize once
        if visible_key not in st.session_state:
            st.session_state[visible_key] = False

        # Toggle logic
        if read_clicked:
            st.session_state[visible_key] = True
        if hide_clicked:
            st.session_state[visible_key] = False

        # Render story
        if st.session_state[visible_key]:
            st.divider()
            display_story(story_data['story'], story_data['metadata'])



if __name__ == "__main__":
    main()
