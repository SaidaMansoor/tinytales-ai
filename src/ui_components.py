import streamlit as st

def render_story_form():
    """Render the story generation form and return parameters"""
    
    with st.form("story_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Genre selection
            genre = st.selectbox(
                "Story Genre",
                ["Adventure", "Fantasy", "Educational", "Friendship", "Animal Stories", "Mystery", "Science Fiction"],
                help="Choose the type of story you'd like to create"
            )
            
            # Main character gender
            gender = st.selectbox(
                "Main Character Gender",
                ["Boy", "Girl", "Non-binary", "Animal Character", "Mixed Group"],
                help="Choose the gender of your main character"
            )
            
            # Age group
            age_group = st.selectbox(
                "Target Age Group",
                ["3-5 years", "5-7 years", "7-9 years"],
                help="Select the age group this story is intended for"
            )
        
        with col2:
            # Story length
            story_length = st.selectbox(
                "Story Length",
                ["5 pages", "6 pages", "7 pages", "8 pages"],
                index=1,  # Default to 6 pages
                help="Choose how many pages your story should have"
            )
            
            # Optional description
            description = st.text_area(
                "Story Description (Optional)",
                placeholder="Describe what kind of story you want. For example: 'A story about a little mouse who discovers a magical garden' or 'An adventure about making new friends at school'",
                help="Provide additional details about the story you want to create. This is optional but helps create a more personalized story."
            )
            
            # Advanced options
            with st.expander("Advanced Options"):
                include_moral = st.checkbox("Include a life lesson/moral", value=True)
                include_dialogue = st.checkbox("Include character dialogue", value=True)
                rhyming = st.checkbox("Make it rhyme (when possible)", value=False)
        
        # Form submission
        submitted = st.form_submit_button("Generate Story", use_container_width=True, type="primary")
        
        if submitted:
            # Clean story length to get just the number
            length_num = story_length.split()[0]
            
            return {
                "genre": genre,
                "gender": gender,
                "age_group": age_group,
                "story_length": length_num,
                "description": description if description.strip() else None,
                "include_moral": include_moral,
                "include_dialogue": include_dialogue,
                "rhyming": rhyming
            }
    
    return None


def display_story(story_pages, metadata):
    """Display a generated story in picture book format"""
    
    # Story header
    st.markdown(f"## 📖 {metadata['title']}")
    
    # Story metadata
    with st.expander("Story Details"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"**Genre:** {metadata['genre']}")
            st.write(f"**Age Group:** {metadata['age_group']}")
        with col2:
            st.write(f"**Main Character:** {metadata['gender']}")
            st.write(f"**Total Pages:** {metadata['total_pages']}")
        with col3:
            st.write(f"**Created:** {metadata['created_at'][:10]}")
            if metadata.get('description'):
                st.write(f"**Description:** {metadata['description']}")
    
    st.divider()
    
    # Display story pages
    for i, page in enumerate(story_pages):
        # Create a container for each page that looks like a book page
        with st.container():
            # Page styling
            st.markdown(
                f"""
                <div style="
                    background-color: #f8f9fa;
                    border: 2px solid #dee2e6;
                    border-radius: 10px;
                    padding: 20px;
                    margin: 10px 0;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <h4 style="color: #495057; margin-bottom: 15px;">📄 Page {page['page_number']}</h4>
                    <div style="
                        font-size: 18px;
                        line-height: 1.6;
                        color: #343a40;
                        font-family: 'Georgia', serif;
                        white-space: pre-line;
                    ">
                        {page['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Add space between pages
            if i < len(story_pages) - 1:
                st.markdown("<br>", unsafe_allow_html=True)


def display_story_card(story_data, story_id):
    """Display a story as a card in the library"""
    
    metadata = story_data['metadata']
    
    with st.container():
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.subheader(metadata['title'])
            st.write(f"Genre: {metadata['genre']} | Age: {metadata['age_group']}")
            if metadata.get('description'):
                st.write(f"_{metadata['description'][:100]}{'...' if len(metadata['description']) > 100 else ''}_")
        
        with col2:
            st.write(f"**Pages:** {metadata['total_pages']}")
            st.write(f"**Created:** {metadata['created_at'][:10]}")
        
        with col3:
            if st.button("📖 Read", key=f"read_{story_id}"):
                st.session_state[f"show_story_{story_id}"] = True
        
        # Show full story if button was clicked
        if st.session_state.get(f"show_story_{story_id}", False):
            st.divider()
            display_story(story_data['story'], metadata)
            if st.button("Hide Story", key=f"hide_{story_id}"):
                st.session_state[f"show_story_{story_id}"] = False
