# src/database.py
import json
from pathlib import Path

# Create data directory if it doesn't exist
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
STORIES_FILE = DATA_DIR / "stories.json"

def save_story(story_pages, metadata):
    """Save a story to the JSON database"""
    try:
        # Load existing stories
        stories = load_stories()
        
        # Create story data
        story_data = {
            "story": story_pages,
            "metadata": metadata
        }
        
        # Add to stories dictionary
        story_id = metadata['id']
        stories[story_id] = story_data
        
        # Save to file
        with open(STORIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(stories, f, indent=2, ensure_ascii=False)
        
        return story_id
        
    except Exception as e:
        print(f"Error saving story: {str(e)}")
        return None

def load_stories():
    """Load all stories from the JSON database"""
    try:
        if STORIES_FILE.exists():
            with open(STORIES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        print(f"Error loading stories: {str(e)}")
        return {}

# def get_story(story_id):
#     """Get a specific story by ID"""
#     stories = load_stories()
#     return stories.get(story_id, None)

# def delete_story(story_id):
#     """Delete a story by ID"""
#     try:
#         stories = load_stories()
#         if story_id in stories:
#             del stories[story_id]
#             with open(STORIES_FILE, 'w', encoding='utf-8') as f:
#                 json.dump(stories, f, indent=2, ensure_ascii=False)
#             return True
#         return False
#     except Exception as e:
#         print(f"Error deleting story: {str(e)}")
#         return False

# def get_stories_by_filter(genre=None, age_group=None, gender=None):
#     """Get stories filtered by criteria"""
#     all_stories = load_stories()
#     filtered_stories = {}
    
#     for story_id, story_data in all_stories.items():
#         metadata = story_data['metadata']
        
#         # Apply filters
#         if genre and metadata.get('genre') != genre:
#             continue
#         if age_group and metadata.get('age_group') != age_group:
#             continue
#         if gender and metadata.get('gender') != gender:
#             continue
            
#         filtered_stories[story_id] = story_data
    
#     return filtered_stories

# def export_story_to_text(story_id, output_dir="exports"):
#     """Export a story to a text file"""
#     try:
#         story_data = get_story(story_id)
#         if not story_data:
#             return False
        
#         # Create export directory
#         export_path = Path(output_dir)
#         export_path.mkdir(exist_ok=True)
        
#         # Create filename
#         title = story_data['metadata']['title'].replace(' ', '_').replace('/', '_')
#         filename = f"{title}_{story_id[:8]}.txt"
#         filepath = export_path / filename
        
#         # Write story to file
#         with open(filepath, 'w', encoding='utf-8') as f:
#             metadata = story_data['metadata']
#             f.write(f"Title: {metadata['title']}\n")
#             f.write(f"Genre: {metadata['genre']}\n")
#             f.write(f"Age Group: {metadata['age_group']}\n")
#             f.write(f"Created: {metadata['created_at']}\n")
#             if metadata.get('description'):
#                 f.write(f"Description: {metadata['description']}\n")
#             f.write("\n" + "="*50 + "\n\n")
            
#             for page in story_data['story']:
#                 f.write(f"Page {page['page_number']}:\n")
#                 f.write(f"{page['content']}\n\n")
        
#         return str(filepath)
        
#     except Exception as e:
#         print(f"Error exporting story: {str(e)}")
#         return False