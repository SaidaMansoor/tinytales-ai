# src/groq_story.py
import os
from datetime import datetime
import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from .story_counter import get_next_story_id
from .prompts import get_gemini_optimized_prompt


class StoryGenerator:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GROQ_API_KEY")
        self.generated_stories = []
        self.similarity_threshold = 0.75

        if not self.api_key:
            st.warning("Please provide Groq API Key to generate stories")
            self.client = None
            return

        try:
            self.client = Groq(api_key=self.api_key)
            self.model = "llama3-8b-8192"
        except Exception as e:
            st.error(f"Error initializing Groq client: {e}")
            self.client = None

    def generate_story(self, story_params):
        """Generate a story using Groq + LLaMA3"""
        try:
            if not self.client:
                return None

            system_prompt = get_gemini_optimized_prompt(story_params['age_group'], story_params)
            user_prompt = self._build_user_prompt(story_params)
            full_prompt = f"{system_prompt}\n\nSTORY REQUEST:\n{user_prompt}"

            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "user", "content": full_prompt}
                ],
                model=self.model,
                temperature=0.7,
                max_tokens=2000,
                top_p=0.9,
                stop=None,
                stream=False
            )

            story_text = chat_completion.choices[0].message.content.strip()

            # Show raw story text for debugging
            st.text_area("🧾 Raw Story Text from Groq", story_text, height=400)

            # Check for duplicates
            is_dup, score = self.is_duplicate(story_text)
            if is_dup:
                st.warning(f"Generated story is similar to a previous one (similarity={score:.2f}). Retrying may help.")

            self.add_story_to_history(story_text)

            # Parse pages (with fallback logic)
            story_pages = self._parse_story_pages(story_text)

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
            return None

    def _build_user_prompt(self, params):
        prompt_parts = []
        prompt_parts.append(f"Create a {params['story_length']}-page children's picture book story with these details:")
        prompt_parts.append(f"• Genre: {params['genre']}")
        prompt_parts.append(f"• Main character gender: {params['gender']}")
        prompt_parts.append(f"• Target age: {params['age_group']}")

        if params.get('description'):
            prompt_parts.append(f"• Story concept: {params['description']}")

        requirements = []
        if params.get('include_moral'):
            requirements.append("include a gentle life lesson")
        if params.get('include_dialogue'):
            requirements.append("include character conversations")
        if params.get('rhyming'):
            requirements.append("include some rhyming where natural")

        if requirements:
            prompt_parts.append(f"• Please {', '.join(requirements)}")

        # 👇 Key improvement to encourage proper formatting
        prompt_parts.append(
            "\nFormat the story with clear page markers like 'Page 1', 'Page 2', etc. "
            "Each page should be ~4-5 sentences. Title should appear as 'Title: ...'"
        )

        return "\n".join(prompt_parts)

    def _parse_story_pages(self, story_text):
        pages = []
        lines = story_text.split('\n')
        current_page = None
        current_content = []

        for line in lines:
            line = line.strip()
            if not line:
                continue

            if line.lower().startswith('title:'):
                continue
            elif line.lower().startswith('page '):
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

        # Final page
        if current_page is not None and current_content:
            pages.append({
                'page_number': current_page,
                'content': '\n'.join(current_content)
            })

        # Fallback: split into N pages if no page markers found
        if not pages:
            paragraphs = [p.strip() for p in story_text.split('\n\n') if p.strip()]
            for i, para in enumerate(paragraphs, start=1):
                pages.append({
                    'page_number': i,
                    'content': para
                })

        return pages

    def _extract_title(self, story_text):
        lines = story_text.split('\n')
        for line in lines:
            if line.lower().startswith('title:'):
                return line.replace('Title:', '').strip()
        return "Untitled Story"

    def is_duplicate(self, new_story_text):
        def jaccard_similarity(text1, text2):
            set1 = set(text1.lower().split())
            set2 = set(text2.lower().split())
            intersection = set1.intersection(set2)
            union = set1.union(set2)
            return len(intersection) / len(union) if union else 0

        for old_story in self.generated_stories:
            similarity = jaccard_similarity(new_story_text, old_story)
            if similarity >= self.similarity_threshold:
                return True, similarity
        return False, None

    def add_story_to_history(self, story_text):
        self.generated_stories.append(story_text.strip())
