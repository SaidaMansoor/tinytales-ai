# AI Kids Story Generator (Powered by Gemini 2.0 Flash)

A professional Streamlit application that generates age-appropriate stories for children using Google's Gemini 2.0 Flash AI, designed like picture books with engaging content and proper story structure.

## Features

- **Powered by Gemini 2.0 Flash**: Uses Google's latest and fastest AI model for story generation
- **Age-Appropriate Content**: Specialized prompts for different age groups (3-5, 5-7, 7-9 years)
- **Multiple Genres**: Adventure, Fantasy, Educational, Friendship, Animal Stories, Mystery, Science Fiction
- **Picture Book Format**: Stories formatted like picture books with 2-3 lines per page
- **Story Customization**: Choose genre, character gender, story length, and add custom descriptions
- **Story Library**: Save and manage generated stories with metadata
- **Professional UI**: Clean, child-friendly interface with proper styling
- **Export Functionality**: Export stories to text files
- **Safety First**: Built-in content safety filters to ensure child-appropriate content

## Why Gemini 2.0 Flash?

- **Faster Generation**: Lightning-fast response times
- **Better Understanding**: Superior context understanding for nuanced storytelling
- **Safety Built-in**: Advanced safety filters for child-appropriate content
- **Cost Effective**: More affordable than other premium AI models
- **Latest Technology**: Access to Google's newest AI capabilities

## Project Structure

```
ai-story-generator/
├── main.py                 # Main Streamlit application
├── requirements.txt        # Python dependencies
├── config.py              # Configuration settings
├── README.md              # This file
├── src/                   # Source modules
│   ├── __init__.py
│   ├── story_generator.py # Core story generation logic (Gemini-powered)
│   ├── prompts.py         # Age-appropriate prompts
│   ├── ui_components.py   # UI components and forms
│   └── database.py        # Story storage and retrieval
├── data/                  # Generated stories storage
│   └── stories.json       # Story database
|   └── story_count.json   # Keeps stories count
└── exports/               # Exported story files
```

## Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Google AI API Key**:
   - Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a `.streamlit/secrets.toml` file in your project root
   - Add your Google AI API key:
     ```toml
     GOOGLE_AI_API_KEY = "your-api-key-here"
     ```
   - Alternatively, you can enter it directly in the app interface

4. **Run the application**:
   ```bash
   streamlit run main.py
   ```

## Usage

### Generating Stories

1. **Select Story Parameters**:
   - Choose genre (Adventure, Fantasy, etc.)
   - Select main character gender
   - Pick target age group
   - Set story length (5-8 pages)

2. **Optional Customization**:
   - Add a story description for more personalized content
   - Enable advanced options like moral lessons or rhyming

3. **Generate and Save**:
   - Click "Generate Story" to create your story
   - Review the generated content
   - Save to your story library

### Story Library

- View all saved stories
- Read stories in picture book format
- Export stories to text files
- Filter stories by metadata

##  Story Format

Stories are generated in picture book format with:
- **2-3 lines per page** (suitable for illustrations)
- **Age-appropriate vocabulary** and sentence structure
- **Engaging narrative flow** with clear beginning, middle, and end