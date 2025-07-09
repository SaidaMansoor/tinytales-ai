# src/story_generator.py
import google.generativeai as genai
import streamlit as st
from datetime import datetime
import os
from .story_counter import get_next_story_id
from .prompts import get_gemini_optimized_prompt
from dotenv import load_dotenv


class StoryGenerator:
    def __init__(self):
        load_dotenv()  

        self.api_key = os.getenv("GOOGLE_API_KEY")

        if not self.api_key:
            st.warning("Please provide Google AI API Key to generate stories")
            self.model = None  # Avoid attribute error later
            return
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception as e:
            st.error(f"Error configuring Gemini: {e}")
            self.model = None
    
    def generate_story(self, story_params):
        """Generate a story based on the provided parameters"""
        try:
            # Get Gemini-optimized prompt
            system_prompt = get_gemini_optimized_prompt(story_params['age_group'], story_params)
            
            # Build user prompt
            user_prompt = self._build_user_prompt(story_params)
            
            # Combine prompts for Gemini
            # full_prompt = f"{system_prompt}\n\nSTORY REQUEST:\n{user_prompt}"
            full_prompt = f"{system_prompt}\n\nSTORY REQUEST:\n{user_prompt}\n\nSeed: {datetime.now().timestamp()}"
            
            # Configure generation parameters optimized for Gemini 2.0 Flash
            generation_config = genai.types.GenerationConfig(
                temperature=0.8,         # Slightly lower for more consistent formatting
                max_output_tokens=2000,  # Increased for longer stories
                top_p=0.9,
                top_k=32,
                candidate_count=1,
                stop_sequences=None
            )
            
            # Call Gemini API with safety settings
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH", 
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                }
            ]
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            # Check if response was blocked
            if response.candidates[0].finish_reason.name == 'SAFETY':
                st.error("Story generation was blocked for safety reasons. Please try different parameters.")
                return None
                
            story_text = response.text
            
            # Parse the story into pages
            story_pages = self._parse_story_pages(story_text)
            
            # Create story data
            story_data = {
            "story": story_pages,
            "metadata": {
                "id": f"story_{get_next_story_id()}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "title": self._extract_title(story_text),
                "genre": story_params['genre'],
                "gender": story_params['gender'],
                "age_group": story_params['age_group'],
                "story_length": story_params['story_length'],
                "description": story_params.get('description', ''),
                "created_at": datetime.now().isoformat(),
                "total_pages": len(story_pages)
            }
        }
            
            return story_data
            
        except Exception as e:
            st.error(f"Error generating story: {str(e)}")
            # Log more details for debugging
            if hasattr(e, 'response'):
                st.error(f"API Response: {e.response}")
            return None
    
    def _build_user_prompt(self, params):
        """Build the user prompt based on story parameters"""
        prompt_parts = []
        
        prompt_parts.append(f"Create a {params['story_length']}-page children's picture book story with these details:")
        prompt_parts.append(f"• Genre: {params['genre']}")
        prompt_parts.append(f"• Main character gender: {params['gender']}")
        prompt_parts.append(f"• Target age: {params['age_group']}")
        
        if params.get('description'):
            prompt_parts.append(f"• Story concept: {params['description']}")
        
        # Add specific requirements based on parameters
        requirements = []
        if params.get('include_moral'):
            requirements.append("include a gentle life lesson")
        if params.get('include_dialogue'):
            requirements.append("include character conversations")
        if params.get('rhyming'):
            requirements.append("include some rhyming where natural")
            
        if requirements:
            prompt_parts.append(f"• Please {', '.join(requirements)}")
        
        prompt_parts.append("\nRemember to follow the exact page format specified above!")
        
        return "\n".join(prompt_parts)
    
    def _parse_story_pages(self, story_text):
        """Parse the generated story into individual pages"""
        pages = []
        lines = story_text.split('\n')
        current_page = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            if line.startswith('Title:'):
                continue
            elif line.startswith('Page '):
                if current_page is not None and current_content:
                    pages.append({
                        'page_number': current_page,
                        'content': '\n'.join(current_content)
                    })
                current_page = len(pages) + 1
                current_content = []
            else:
                if current_page is not None:
                    current_content.append(line)
        
        # Add the last page
        if current_page is not None and current_content:
            pages.append({
                'page_number': current_page,
                'content': '\n'.join(current_content)
            })
        
        return pages
    
    def _extract_title(self, story_text):
        """Extract title from the generated story"""
        lines = story_text.split('\n')
        for line in lines:
            if line.startswith('Title:'):
                return line.replace('Title:', '').strip()
        return "Untitled Story"
