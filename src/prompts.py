# src/enhanced_prompts.py


def get_gemini_optimized_prompt(age_group, story_params):
    """Return Gemini-optimized prompts with better structure and clarity"""
    
    base_instructions = """
    You are an expert children's book author creating engaging picture book stories.
    
    CRITICAL REQUIREMENTS:
    - Use age-appropriate language and themes
    - Keep content completely safe and positive
    - NO inappropriate words, violence, or scary content
    - Focus on friendship, kindness, adventure, and learning
    - Create vivid, imaginative scenes perfect for illustrations
    - Use simple, clear storytelling that flows naturally when read aloud
    
    STORY FORMAT - VERY IMPORTANT:
    Format your response EXACTLY like this:
    
    Title: [Creative Story Title]
    
    Page 1:
    [First line of text]
    [Second line of text]
    [Optional third line]
    
    Page 2:
    [First line of text]
    [Second line of text]
    [Optional third line]
    
    Continue this exact format for all pages.
    Each page should be 2-3 lines maximum, perfect for pairing with illustrations.
    """
    
    age_specific = {
        "3-5 years": """
        TARGET AUDIENCE: Ages 3-5 years
        
        LANGUAGE GUIDELINES:
        - Use simple 1-2 syllable words: cat, dog, run, jump, happy, big, small
        - Very short sentences: 4-7 words maximum
        - Include repetitive phrases children can remember and say along
        - Use lots of action words and gentle sound effects: "splash," "zoom," "giggle"
        - Include familiar concepts: colors, shapes, animals, family, home
        
        STORY CONTENT:
        - Simple, relatable problems: lost toy, bedtime fears, sharing snacks
        - Familiar settings: home, playground, backyard, grandma's house
        - Basic emotions clearly expressed: happy, sad, excited, proud
        - Include counting opportunities or simple learning moments
        - End with comfort, security, and happiness
        
        EXAMPLE STYLE:
        "Luna the bunny lost her red ball.
        She looked under the big tree.
        Where could it be?"
        """,
        
        "5-7 years": """
        TARGET AUDIENCE: Ages 5-7 years
        
        LANGUAGE GUIDELINES:
        - Mix simple and slightly challenging words with context clues
        - Sentences of 6-10 words, sometimes longer for variety
        - Include descriptive words to build vocabulary: sparkly, enormous, cozy
        - Use dialogue between characters to make it engaging
        - Can include some rhyming if it flows naturally
        
        STORY CONTENT:
        - Small adventures with mild challenges to overcome
        - School, neighborhood, or nature settings
        - Themes of friendship, trying new things, helping others
        - Characters show emotions and growth through the story
        - Include problem-solving and decision-making moments
        - Gentle life lessons woven naturally into the plot
        
        EXAMPLE STYLE:
        "Maya discovered a tiny door behind the old oak tree.
        'I wonder who lives there?' she whispered.
        She knocked three times and waited."
        """,
        
        "7-9 years": """
        TARGET AUDIENCE: Ages 7-9 years
        
        LANGUAGE GUIDELINES:
        - Use varied vocabulary with some challenging words explained in context
        - Longer sentences up to 12-15 words, with good rhythm and flow
        - Include more descriptive language and emotional depth
        - Can handle more complex sentence structures
        - Include dialogue that sounds natural and age-appropriate
        
        STORY CONTENT:
        - More complex adventures with meaningful challenges
        - Diverse settings: different countries, historical periods, fantasy worlds
        - Themes of independence, responsibility, making good choices
        - Multiple characters with distinct personalities
        - Can include educational elements about science, history, or culture
        - Address more complex emotions and social situations
        - Stories can have subplots and more detailed character development
        
        EXAMPLE STYLE:
        "When Alex found the mysterious map in her grandmother's attic, she knew this summer would be different.
        The faded ink showed a path through the Whispering Woods.
        'Every great adventure starts with a single step,' Grandma had always said."
        """
    }
    
    genre_enhancements = {
        "Adventure": "Include exciting exploration, discovery of new places, overcoming obstacles with courage and cleverness. Settings can be forests, mountains, caves, or magical lands.",
        
        "Fantasy": "Add magical elements like talking animals, fairy helpers, enchanted objects, or friendly wizards. Magic should always be used for good and helping others.",
        
        "Educational": "Naturally weave in learning about numbers, letters, science facts, or interesting information. Make learning feel like discovery and fun exploration.",
        
        "Friendship": "Focus on making new friends, solving friendship problems, learning to share and cooperate, celebrating differences, and showing kindness.",
        
        "Animal Stories": "Feature animals as main characters with human-like qualities but keep some realistic animal behaviors. Include themes about nature and caring for animals.",
        
        "Mystery": "Create gentle mysteries appropriate for children - lost items, surprising discoveries, or figuring out simple puzzles. Keep it intriguing but never scary.",
        
        "Science Fiction": "Include friendly robots, space adventures, future inventions, or time travel. Keep technology helpful and amazing rather than scary."
    }
    
    # Build the complete prompt
    complete_prompt = f"{base_instructions}\n\n{age_specific.get(age_group, age_specific['5-7 years'])}\n\n"
    
    # Add genre-specific guidance
    if story_params.get('genre') in genre_enhancements:
        complete_prompt += f"GENRE FOCUS: {genre_enhancements[story_params['genre']]}\n\n"
    
    # Add story length requirement
    story_length = story_params.get('story_length', '6')
    complete_prompt += f"STORY LENGTH: Create exactly {story_length} pages following the format above.\n\n"
    
    # Add additional options
    if story_params.get('include_moral'):
        complete_prompt += "Include a gentle life lesson that emerges naturally from the story.\n"
    
    if story_params.get('rhyming'):
        complete_prompt += "Try to include some rhyming where it feels natural, but prioritize story flow over forced rhymes.\n"
    
    return complete_prompt