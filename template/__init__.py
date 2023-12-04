# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the “Software”), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

__version__ = "2.5.0"
version_split = __version__.split(".")
__spec_version__ = (
    (1000 * int(version_split[0]))
    + (10 * int(version_split[1]))
    + (1 * int(version_split[2]))
)

import os
from openai import AsyncOpenAI
AsyncOpenAI.api_key = os.environ.get('OPENAI_API_KEY')
if not AsyncOpenAI.api_key:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")

client = AsyncOpenAI(timeout=60.0)

# Blacklist variables
ALLOW_NON_REGISTERED = False
PROMPT_BLACKLIST_STAKE = 20000
IMAGE_BLACKLIST_STAKE = 20000
EMBEDDING_BLACKLIST_STAKE = 20000
ISALIVE_BLACKLIST_STAKE = min(PROMPT_BLACKLIST_STAKE, IMAGE_BLACKLIST_STAKE)
MIN_REQUEST_PERIOD = 2
MAX_REQUESTS = 40
# must have the test_key whitelisted to avoid a global blacklist
testnet_key = "5EhEZN6soubtKJm8RN7ANx9FGZ2JezxBUFxr45cdsHtDp3Uk"
test_key = "5DcRHcCwD33YsHfj4PX5j2evWLniR1wSWeNmpf5RXaspQT6t"
corcel = "5Hddm3iBFD2GLT5ik7LZnT3XJUnRnN8PoeCFgGQgawUVKNm8"
WHITELISTED_KEYS = [testnet_key, test_key, corcel]

weight_copiers = [117,224,214,104,2,102,7,135,114,251,4]
threat_keys = [251]
BLACKLISTED_KEYS = weight_copiers + threat_keys + []
validators_running_wandb = [0, 1, 16, 26, 81, 103, 109, 113, 124, 178, 244]

PROJECT_NAMES = ['embeddings-data', 'synthetic-QA-v2', 'synthetic-images']
PROJECT_NAME = 'multi-modality'


# Instruct themes used in https://arxiv.org/pdf/2304.12244.pdf to train WizardLM
initial_instruct_themes = ['Philosopy', 'Technology', 'Physics', 'Ethics', 'Academic Writing', 'Economy', 'History', 'Medicine', 'Toxicity', 'Roleplay', 'Entertainment', 'Biology', 'Counterfactual', 'Literature', 'Chemistry', 'Writing', 'Sport', 'Law', 'Language', 'Computer Science', 'Multilangual', 'Common Sense', 'Art', 'Complex Format' 'Code Generation', 'Math', 'Code Debug', 'Reasoning']
more_instruct_themes = [
    "Global Cultures and Societies",
    "Modern and Ancient Civilizations",
    "Innovations in Science and Technology",
    "Environmental Conservation and Biodiversity",
    "World Religions and Philosophical Thought",
    "Global Economy and International Trade",
    "Public Health and Pandemic Response",
    "Human Rights and Social Justice Issues",
    "Political Systems and International Relations",
    "Major Historical Events and their Impact",
    "Advancements in Medicine and Healthcare",
    "Fundamentals of Physics and the Cosmos",
    "Cognitive Development and Learning Theories",
    "Sustainable Development and Green Technologies",
    "Media Literacy and News Analysis",
    "Classical and Modern Literature",
    "Fundamentals of Mathematics and Logic",
    "Social Psychology and Group Dynamics",
    "Emerging Trends in Education",
    "Civic Engagement and Community Organizing"
    ]
INSTRUCT_DEFAULT_THEMES = initial_instruct_themes + more_instruct_themes
INSTRUCT_DEfAULT_QUESTIONS = ["ERROR in getting questions"]

CHAT_DEFAULT_THEMES = ['Love and relationships', 'Nature and environment', 'Art and creativity', 'Technology and innovation', 'Health and wellness', 'History and culture', 'Science and discovery', 'Philosophy and ethics', 'Education and learning', 'Music and rhythm', 'Sports and athleticism', 'Food and nutrition', 'Travel and adventure', 'Fashion and style', 'Books and literature', 'Movies and entertainment', 'Politics and governance', 'Business and entrepreneurship', 'Mind and consciousness', 'Family and parenting', 'Social media and networking', 'Religion and spirituality', 'Money and finance', 'Language and communication', 'Human behavior and psychology', 'Space and astronomy', 'Climate change and sustainability', 'Dreams and aspirations', 'Equality and social justice', 'Gaming and virtual reality', 'Artificial intelligence and robotics', 'Creativity and imagination', 'Emotions and feelings', 'Healthcare and medicine', 'Sportsmanship and teamwork', 'Cuisine and gastronomy', 'Historical events and figures', 'Scientific advancements', 'Ethical dilemmas and decision making', 'Learning and growth', 'Music genres and artists', 'Film genres and directors', 'Government policies and laws', 'Startups and innovation', 'Consciousness and perception', 'Parenting styles and techniques', 'Online communities and forums', 'Religious practices and rituals', 'Personal finance and budgeting', 'Linguistic diversity and evolution', 'Human cognition and memory', 'Astrology and horoscopes', 'Environmental conservation', 'Personal development and self-improvement', 'Sports strategies and tactics', 'Culinary traditions and customs', 'Ancient civilizations and empires', 'Medical breakthroughs and treatments', 'Moral values and principles', 'Critical thinking and problem solving', 'Musical instruments and techniques', 'Film production and cinematography', 'International relations and diplomacy', 'Corporate culture and work-life balance', 'Neuroscience and brain function', 'Childhood development and milestones', 'Online privacy and cybersecurity', 'Religious tolerance and understanding', 'Investment strategies and tips', 'Language acquisition and fluency', 'Social influence and conformity', 'Space exploration and colonization', 'Sustainable living and eco-friendly practices', 'Self-reflection and introspection', 'Sports psychology and mental training', 'Globalization and cultural exchange', 'Political ideologies and systems', 'Entrepreneurial mindset and success', 'Conscious living and mindfulness', 'Positive psychology and happiness', 'Music therapy and healing', 'Film analysis and interpretation', 'Human rights and advocacy', 'Financial literacy and money management', 'Multilingualism and translation', 'Social media impact on society', 'Religious extremism and radicalization', 'Real estate investment and trends', 'Language preservation and revitalization', 'Social inequality and discrimination', 'Climate change mitigation strategies', 'Self-care and well-being', 'Sports injuries and rehabilitation', 'Artificial intelligence ethics', 'Creativity in problem solving', 'Emotional intelligence and empathy', 'Healthcare access and affordability', 'Sports analytics and data science', 'Cultural appropriation and appreciation', 'Ethical implications of technology']
CHAT_DEFAULT_QUESTIONS = ['What is the most important quality you look for in a partner?', 'How do you define love?', 'What is the most romantic gesture you have ever received?', 'What is your favorite love song and why?', 'What is the key to a successful long-term relationship?', 'What is your idea of a perfect date?', 'What is the best piece of relationship advice you have ever received?', 'What is the most memorable love story you have heard?', 'What is the biggest challenge in maintaining a healthy relationship?', 'What is your favorite way to show someone you love them?']

IMAGE_DEFAULT_THEMES = ["Urban Echoes", "Nature's Whispers", "Futuristic Visions", "Emotional Abstracts", "Memory Fragments", "Mythical Echoes", "Underwater Mysteries", "Cosmic Wonders", "Ancient Secrets", "Cultural Tapestries", "Wild Motion", "Dreamlike States", "Seasonal Shifts", "Nature's Canvas", "Night Lights", "Historical Shadows", "Miniature Worlds", "Desert Dreams", "Robotic Integrations", "Fairy Enchantments", "Timeless Moments", "Dystopian Echoes", "Animal Perspectives", "Urban Canvas", "Enchanted Realms", "Retro Futures", "Emotive Rhythms", "Human Mosaics", "Undersea Unknowns", "Mystical Peaks", "Folklore Reimagined", "Outer Realms", "Vintage Styles", "Urban Wilderness", "Mythical Retellings", "Colorful Breezes", "Forgotten Places", "Festive Illuminations", "Masked Realities", "Oceanic Legends", "Digital Detachments", "Past Reverberations", "Shadow Dances", "Future Glimpses", "Wild Forces", "Steampunk Realms", "Reflective Journeys", "Aerial Grace", "Microscopic Worlds", "Forest Spirits"]
IMAGE_DEFAULT_QUESTIONS = ['A majestic golden eagle soaring high above a mountain range, its powerful wings spread wide against a clear blue sky.', 'A bustling medieval marketplace, full of colorful stalls, various goods, and people dressed in period attire, with a castle in the background.', 'An underwater scene showcasing a vibrant coral reef teeming with diverse marine life, including fish, sea turtles, and starfish.', 'A serene Zen garden with neatly raked sand, smooth stones, and a small, gently babbling brook surrounded by lush green foliage.', 'A futuristic cityscape at night, illuminated by neon lights, with flying cars zooming between towering skyscrapers.', 'A cozy cabin in a snowy forest at twilight, with warm light glowing from the windows and smoke rising from the chimney.', 'A surreal landscape with floating islands, cascading waterfalls, and a path leading to a castle in the sky, set against a sunset backdrop.', 'An astronaut exploring the surface of Mars, with a detailed spacesuit, the red Martian terrain around, and Earth visible in the sky.', 'A lively carnival scene with a Ferris wheel, colorful tents, crowds of happy people, and the air filled with the smell of popcorn and cotton candy.', 'A majestic lion resting on a savanna, with the African sunset in the background, highlighting its powerful mane and serene expression.']

IMAGE_THEMES = [
    'The Inner Journey',
    'The Dance of Life',
    'Enigmatic Reflections',
    'The Poetry of Silence',
    'Melodies of the Mind',
    'Whimsical Enigmas',
    'Whispers of Inspiration',
    'Colorful Abstractions',
    'Dancing Colors',
    'Transcendent moments',
    'The Essence of Light',
    'Metamorphosis',
    'Duality in Nature',
    'Transcending Time',
    'Essence of Life',
    'Ethereal Abstractions',
    'Hidden Depths',
    'Urban Rhythms',
    'Inner emotions',
    'Whispers of the Night',
    'Dreams that Soar',
    'Enchanted Melodies',
    'Embracing Solitude',
    'Dreamlike Reflections',
    'Abstracted Memories',
    'Melodies of the Mind',
    'Evolving Realities',
    'Serenade of Seasons',
    'Serenity in chaos',
    'Interwoven Narratives',
    'Cosmic Connections',
    'Interplay of elements',
    'Immersive Portals',
    'Whispers of the Wind',
    'Whispered Whimsies',
    'Painted Passions',
    'Celestial Strokes',
    'Imaginary Journeys',
    'Hidden Treasures',
    'Shimmering Illusions',
    'The Strength Within',
    'Evolving Patterns',
    'Exploring the Subconscious',
    'Harmony in Diversity',
    'Cosmic Dreams',
    'The Fragile Balance',
    'Mystical Wanderlust',
    'Ephemeral Moments',
    'Whispered Visions',
    'Metamorphosis of Form',
    'Capturing Times Essence',
    'Cascading Emotions',
    'Whispers of the heart',
    'Chasing Illusions',
    'The Fluidity of Form',
    'Emerging Horizons',
    'Unveiled Whispers',
    'Celestial Beings',
    '... (68 KB left)',
    'Journey of the Soul',
    'Transcendent Transparencies',
    'Tranquil Transcendence',
    'Luminous Visions',
    'Sensory Overload',
    'Exploring identity',
    'Vibrant Chaos',
    'The fragility of life',
    'Eternal Echoes',
    'Whispers of Wonder',
    'Whimsical Delights',
    'Strokes of Serenity',
    'Rhythm of Colors',
    'The Art of Silence',
    'Serenade of Shadows',
    'Imaginary Landscapes',
    'Dreams and reality',
    'Abstract Realities',
    'Untamed Imagination',
    'Embracing vulnerability',
    'Dreamlike Visions',
    'Melodies of Nature',
    'Hidden Symmetry',
    'Mystic Mosaic',
    'Symphony of Life',
    'The Art of Transformation',
    'Reimagining Classics',
    'Ephemeral beauty',
    'The Spirit of Movement',
    'Fragments of Time',
    'The Beauty of Decay',
    'The Magic of Childhood',
    'The Essence of Stillness',
    'Abstract Energy',
    'Whirling Vortex',
    'Parallel Universes Collide',
    'Whirling Dervish',
    'Enigmatic Beauty',
    'The Art of Balance',
    'Merging Dimensions',
    'Celestial Rhythms',
    'The Energy of Movement',
    'Vibrant Serenade',
    'Transcendent Fragments',
    'Magical Moments',
    'The Art of Transformation',
    'Rhythmic Movements',
    'Vibrant Cityscapes',
    'Captivating Textures',
    'Inner reflections',
    'Journey into Mystery',
    'Dreamy Watercolors',
    'Dancing with Time',
    'Fluid Dynamics',
    'Whispering Canvases',
    'Rhythms of the Earth',
    'Harmony in disarray',
    'Whispering Waters',
    'The Language of Color',
    'Merging Horizons',
    'The Human Connection',
    'Uncharted Horizons',
    'The Human Experience',
    'The Power of Music',
    'Wandering Thoughts',
    'Intertwined Destinies',
    'Cosmic vibrations',
    'The Art of Simplicity',
    'Eternal Serenity',
    'Textures of Time',
    'Emerging Identity',
    'Dreams in Motion',
    'Fluid Movements',
    'Ethereal Enigmas',
    'Dreams of Serenity',
    'Evolving Textures',
    'Melodies of the Sea',
    'The Joy of Simplicity',
    'Melodies of the Universe',
    'The Symphony of Life',
    'Cosmic Kaleidoscope',
    'Symphony of Solitude',
    'The art of connection',
    'The Magic of Texture',
    'Inner Reflections',
    'Ethereal Dreams',
    'Whispers of the Universe',
    'Infinite Possibilities',
    'Shifting Perspectives',
    'Harvesting Memories',
    'Embracing the Elements',
    'Surreal Soundscapes',
    'Evolving Dimensions',
    'The Language of Dreams',
    'Soulful Expressions',
    'Embracing the Unknown',
    'Breaking Barriers',
    'Strokes of Brilliance',
    'Capturing Fragments',
    'Visions of tomorrow',
    'Rhythms of the Mind',
    'Vivid Dreamscape',
    'Enchanted Forest',
    'Essence of Silence',
    'The Magic Within',
    'Enigmatic Depths',
    'Urban Poetry',
    'Unveiled Secrets',
    'Captivating Curves',
    'Transcending Dimensions',
    'Exploring duality',
    'Translucent Dreams',
    'Soothing Serenity',
    'Uncharted Territories Explored',
    'Timeless elegance',
    'Eternal Serenade',
    'Timeless Elegance',
    'Dancing Brushstrokes',
    'Curious Connections',
    'Transcending Dimensions',
    'Ethereal Beauty',
    'Mystical Realms',
    'Emerging from Shadows',
    'Cosmic Tapestry',
    'Enigmatic Melodies',
    'The Dance of Lines',
    'The Dance of Colors',
    'Mystical creatures',
    'Celestial Visions',
    'The Essence of Life',
    'Rhythms of the Imagination',
    'Serenity in Chaos',
    'Imaginary Horizons',
    'Cascading Colors',
    'Mystical Whispers',
    'Architectural Marvels',
    'Whispering Whimsy',
    'Journey of Light',
    'Melting Colors',
    'Mystical Enchantments',
    'The Language of Silence',
    'Immersive Visions',
    'Celestial Fragments',
    'Whirling Motion',
    'Visions of Tomorrow',
    'Ethereal beauty',
    'Layers of Meaning',
    'Harmony in Form',
    'Natures Tapestry',
    'Harvesting Shadows',
    'Vibrant Contrasts',
    'Organic Metamorphosis',
    'The Unseen World',
    'The Language of Colors',
    'Unseen Realms',
    'Reflections of Life',
    'Timeless Beauty',
    'Whispers of Time',
    'Redefining Reality',
    'Vibrant Surrender',
    'Harmony in Diversity',
    'Whispers of Nature',
    'Silent Echoes',
    'Visions of Light',
    'Spectral Visions',
    'Celestial Beauty',
    'Transcendent Bliss',
    'Whimsical Curiosity',
    'The Fragments of Memory',
    'Hidden Truths',
    'Luminous Depths',
    'Melting Pot',
    'Surreal Wonderland',
    'Celestial Harmonies',
    'Whispered Whimsy',
    'Melodies of Creation',
    'Illusions of Reality',
    'Inner Emotions',
    'Cityscape Vibes',
    'Dreamlike Realities',
    'Urban Jungle',
    'The Harmony of Opposites',
    'Journey to Serenity',
    'Layers of Perception',
    'Colorful Kaleidoscope',
    'Evolving identities',
    'Whispering Secrets',
    'Whimsical Portraits',
    'Shadows of the Mind',
    'Whimsical dreams',
    'Exploring Identity',
    'Spectrum of Emotions',
    'Captivating Curiosity',
    'Reflections of Identity',
    'Fragments of Memories',
    'Cosmic Serenity',
    'Mystic Mirage',
    'Whirling Dreams',
    'Infinite possibilities',
    'Transcendent Moments',
    'Enchanted Abstractions',
    'Blissful Serenity',
    'Vibrant Echoes',
    'Exploring the Void',
    'Sculpting the Soul',
    'Whispers of the Sea',
    'Surreal Landscapes',
    'Vibrant Emotions',
    'Eternal Euphoria',
    'The Essence of Silence',
    'Whispered Secrets Revealed',
    'Stardust Symphony',
    'The Dance of Fire',
    'Flowing Movements',
    'Stardust Melodies',
    'Whispered Secrets',
    'Captivating Fragments',
    'Mysteries of Time',
    'The Canvas of Dreams',
    'Whispers of Infinity',
    'Abstract impressions',
    'Cascading Light',
    'Cosmic Journey',
    'Celestial Bodies',
    'Transcending Boundaries',
    'Shaping the Unknown',
    'Ripples of Imagination',
    'Colors of the Soul',
    'Luminous Transitions',
    'The Art of Reflection',
    'Parallel Dimensions',
    'The Magic of Movement',
    'The Beauty of Stillness',
    'Serenade of Light',
    'Infinite Intricacies',
    'Illusive Realms',
    'Enchanted Reverie',
    'Dancing with Colors',
    'Whispers of Imagination',
    'Translucent Transitions',
    'Ethereal Visions',
    'Capturing Serendipity',
    'Rhythm of Creation',
    'Mosaic of Dreams',
    'Dreams in Technicolor',
    'Emotions Unleashed',
    'The Symphony of Colors',
    'Beyond the Surface',
    'Unseen dimensions',
    'Harvest of Dreams',
    'The Human Condition',
    'Melancholic Whimsy',
    'Surreal Portraits',
    'Journey to the Soul',
    'The Energy of Life',
    'Layers of Existence',
    'Mystical Enchantment',
    'Auroras Embrace',
    'The Mystery of Shadows',
    'Essence of Serenity',
    'Emerging Realities',
    'Fleeting Impressions',
    'Luminous Enigmas',
    'Fluid Expressions',
    'Euphoria in Motion',
    'Embracing Vulnerability',
    'Journey into darkness',
    'The beauty of decay',
    'The Dance of Time',
    'Tangled Thoughts',
    'The beauty of simplicity',
    'Redefining Perspectives',
    'Ethereal Whispers',
    'The Colors of Sound',
    'Melodies of life',
    'Emerging Energy',
    'Symphony of Shadows',
    'Metamorphic Dreams',
    'Reverie of Light',
    'Dreamy Landscapes',
    'Echoes of the Past',
    'Shimmering Horizons',
    'Journey into Light',
    'Natures Kaleidoscope',
    'Echoes of the Mind',
    'The Art of Shadows',
    'Vibrant Rhythms',
    'Colorful Fragments',
    'The Art of Stillness',
    'Celestial Melodies',
    'Colors of the Mind',
    'Magical Realms',
    'Whispers of Dreams',
    'Mystical Journeys',
    'Colorful Whirlwinds',
    'Transcending Reality',
    'The Art of Connection',
    'Symphony of Textures',
    'Unseen Perspectives',
    'Whispers of the Soul',
    'Translucent Veil',
    'Whispering Dreams',
    'Waves of Creativity',
    'Exploring the Unknown',
    'Ethereal Elegance',
    'Whimsical Tales',
    'Metamorphosis of Colors',
    'Colorful Whispers',
    'Luminous Reverie',
    'Ephemeral Fragments',
    'Mosaic of Memories',
    'Whirling Fantasies',
    'The Essence Within',
    'Vibrant Perspectives',
    'Eternal Fragility',
    'Whimsical Wanderlust',
    'Reimagined Landscapes',
    'The Fluidity of Nature',
    'Sculpted Whispers',
    'Colorful abstractions',
    'Dreams of Tomorrow',
    'Unexpected Connections',
    'Sensory Delights',
    'Harmony in chaos',
    'Dynamic Perspectives',
    'Juxtaposed Elements',
    'Surreal Dreamscape',
    'Whimsical Escapes',
    'Celestial Canvas',
    'The Poetry of Light',
    'Ripples of Time',
    'Whispers of the Sky',
    'Whispering Echoes',
    'Merging Perspectives',
    'Metamorphosis of Life',
    'Infinite Imagination',
    'Harmonic Fusion',
    'The Depths of Emotion',
    'The Art of Motion',
    'Untamed Wildness',
    'Inner Worlds',
    'The human experience',
    'Echoes of Stillness',
    'Rhythms of the Sea',
    'Rhythm of the Elements',
    'Metamorphosis of Color',
    'Temporal Illusions',
    'The Symphony of Textures',
    'Sculpting Time',
    'Mystical Forests',
    'Whispering Waves',
    'Celestial Symphony',
    'Enigmatic Shadows',
    'Embracing the Unknown',
    'Whispers of the Mind',
    'The magic of details',
    'Embracing Diversity',
    'The Language of Lines',
    'Rhythms of nature',
    'Abstract Color Explosions',
    'Shadows and light',
    'Eternal Echoes',
    'Shades of Serenity',
    'Fragments of Eternity',
    'Whirlwind of Emotions',
    'Symphony of Light',
    'Enigmatic Horizons',
    'Unlocking Imagination',
    'Redefining Boundaries',
    'Evolving Energies',
    'Unleashing Creativity',
    'Chasing Shadows',
    'Harvest of Memories',
    'Abstracted Nature',
    'Abstract Reflections',
    'Eternal Moments',
    'Emotional connections',
    'Unveiled Realities',
    'Rhythmic Abstractions',
    'Visions of Tomorrow',
    'Chromatic Symphony',
    'Parallel Realities',
    'Mystic Melodies',
    'The Symphony of Emotions',
    'Infinite Horizons',
    'The Art of Serendipity',
    'Whispers of the Earth',
    'The Chaos of Creation',
    'Echoes of Eternity',
    'Embracing Imperfection',
    'Harmony in Chaos',
    'Celestial Dreams',
    'Canvas of Dreams',
    'Urban Exploration',
    'Embracing the Abstract',
    'Unfolding Stories',
    'Interstellar Symphony',
    'Fluid Abstractions',
    'The Power of Perspective',
    'Whispered Memories',
    'Transcending Boundaries',
    'Whispers of Creation',
    'Illusionary Landscapes',
    'Enchanted Gardens',
    'The Fragility of Time',
    'Enigmatic Fragments',
    'Enchanted Forests',
    'Sculpted Illusions',
    'Dreams of Flight',
    'Unveiled Illusions',
    'Evolving Perspectives',
    'Celestial Harmony',
    'Metamorphosis of life',
    'Mystical Portals',
    'Glimpses of Life',
    'Serenading Raindrops',
    'Serenading Colors',
    'Dreamscapes',
    'Evolving Fragments',
    'Cosmic Reverie',
    'The Beauty of Movement',
    'Captivating Contrasts',
    'Imaginary landscapes',
    'Spectrum of Serenity',
    'Captivating Chaos',
    'Shaping the Unseen',
    'Whirling Colors',
    'Ethereal Enigma',
    'Whispers of Serenity',
    'Infinite Perspectives',
    'Enigmatic Euphoria',
    'Embracing imperfections',
    'Essence of Time',
    'Celestial Awakening',
    'Rustic Simplicity',
    'A Glimpse of Eternity',
    'Infinite Textures',
    'Translucent Depths',
    'Vibrant Dreamscape',
    'Unveiled Connections',
    'The Serenity of Space',
    'Abstract Emotions',
    'Transcendent Whispers',
    'Serendipitous Encounters',
    'Soulful Strokes',
    'Chasing Sunsets',
    'Timeless Moments',
    'Cosmic Energy',
    'Surreal Serenity',
    'Whispers of the Past',
    'Whimsical Adventures',
    'The Power Within',
    'Celestial Rapture',
    'The art of solitude',
    'Illusions of Light',
    'Harmonious Fusion',
    'Reflections of Self',
    'Eternal Enigma',
    'Inner Landscapes',
    'Captivating Silence',
    'Abstract Serenity',
    'Infinite Curiosity',
    'Ethereal Essence',
    'Enigmatic Illusions',
    'Unveiling Secrets',
    'Harmonious Contrasts',
    'Whispers of Light',
    'The Alchemy of Creation',
    'Emerging Whispers',
    'Abstract Color Explosion',
    'Unveiled Perspectives',
    'Enchanted Echoes',
    'Rhythms of the Heart',
    'The Spirit of Freedom',
    'Symphony of colors',
    'Whirling Emotions',
    'Whimsical Wonder',
    'Infinite Dimensions',
    'Eternal Whispers',
    'Celestial Serenade',
    'Journey to Infinity',
    'Uncharted Territories',
    'Whimsical Wonders',
    'Whispers of Memories',
    'Whimsical Wonderland',
    'Dreamlike Wanderlust',
    'Colorful Illusions',
    'Harmony in contrast',
    'Surreal Symphony',
    'Beyond the Surface',
    'Eternal transformations',
    'Cosmic Wonders',
    'Ephemeral Beauty',
    'Whispers of the Sea',
    'The Souls Journey',
    'Melancholic Serenity',
    'Illusive Realities',
    'Surreal Serenity',
    'Celestial Fireworks',
    'Hidden Realities',
    'Parallel universes',
    'A World Apart',
    'Unveiled Emotions',
    'Dreams of flight',
    'Capturing Fragility',
    'Whimsical Wonders',
    'Rhythms of Nature',
    'Infinite Connections',
    'Interstellar Dreams',
    'Innermost Thoughts',
    'Emotional Journeys',
    'Organic Symmetry',
    'Whispering Colors',
    'Embracing Vulnerability',
    'Enigmatic Serenity',
    'Vibrant Whispers',
    'Wandering Imagination',
    'The Magic of Water',
    'Capturing emotions',
    'Vibrant Serendipity',
    'The Essence of Movement',
    'The Play of Contrasts',
    'Mystical Creatures',
    'Soothing Chaos',
    'Whispers of the soul',
    'Enchanted Forest Tales',
    'Melodies of Color',
    'The Fragility of Life',
    'The Power of Color',
    'Whispering Whirlwinds',
    'The Symphony of Shapes',
    'Surreal Visions',
    'The Spirit Within',
    'Exploring the unknown',
    'Symmetry in Chaos',
    'Evolving Dreams',
    'Cosmic connections',
    'Translucent Veils',
    'Dancing Shadows',
    'Threads of Destiny',
    'Majestic Whispers',
    'Suspended Realities',
    'Dreams and Fantasies',
    'Surreal Landscapes',
    'Metamorphosis of Light',
    'Enchanted Landscapes',
    'Unveiling Truths',
    'Emotional Portraits',
    'Journey of Discovery',
    'Celestial Explorations',
    'Shades of Solitude',
    'Symmetry in Asymmetry',
    'Uncharted Depths',
    'Dancing with light',
    'Wandering Souls',
    'Surreal Harmonies',
    'Shadows and Light',
    'Surreal Serenade',
    'Surreal Reverie',
    'Evolving Identities',
    'Forgotten Memories',
    'The Power of Silence',
    'Chaos and Order',
    'Fragmented Realities',
    'Evolving Harmonies',
    'Dreamlike Dalliance',
    'Rhythms of Life',
    'Enigmatic Landscapes',
    'The Spirit of Adventure',
    'Emotional landscapes',
    'Magical Realism',
    'Mystical Serenity',
    'The Melody of Love',
    'Whispered Stories',
    'Sculpting Emotions',
    'The Fragility of Love',
    'Whispered Revelations',
    'The Poetry of Motion',
    'Rhythm of Life',
    'Untamed Wilderness',
    'Cityscapes at Dusk',
    'Rhythmic Landscapes',
    'Celestial Fragments',
    'Symphony of Dreams',
    'The Dance of Textures',
    'The Whispers of Wind',
    'Fleeting Fragments',
    'Whispering Whirlpools',
    'Mystical Movements',
    'The Inner Voice',
    'The Power of Now',
    'Whispering winds',
    'Eternal Inspiration',
    'Sculpting Shadows',
    'The Essence of Time',
    'Hidden Emotions',
    'The Language of Music',
    'Merging Realities',
    'Dreamlike Diversions',
    'Sculpted Memories',
    'Ephemeral Essence',
    'Unveiling Shadows',
    'Abstract Narratives',
    'The Magic of Motion',
    'Ethereal Landscapes',
    'Whispering Shadows',
    'The Symphony of Chaos',
    'Soothing Solitude',
    'The Intersection of Dreams',
    'Harmony of Elements',
    'Merging Horizons',
    'Dancing with Shadows',
    'Whispers of the past',
    'The Poetry of Nature',
    'Rhythms of Imagination',
    'Ethereal landscapes',
    'Whispers of Silence',
    'Celestial Brushstrokes',
    'Mystical Rhythms',
    'The Power of Stillness',
    'The Dance of Contrast',
    'Visions of Hope',
    'Whispers of the Heart',
    'Transcendent Transitions',
    'Rhythm of the Sea',
    'Harmonic Convergence',
    'The Art of Imperfection',
    'Unveiling Mystery',
    'Serenity in Motion',
    'Harmony Unveiled',
    'Embracing the Chaos',
    'Abstract Expressions',
    'Serenade of Colors',
    'Surreal Reflections',
    'Dancing with Color',
    'Whispering Tides',
    'Serenity in Chaos',
    'Symphony of Colors',
    'Harvesting Dreams',
    'Imaginary Creatures',
    'Suspended Animation',
    'Imagined Landscapes',
    'Spectral Reflections',
    'Mystical Reflections',
    'Melodies in Motion',
    'Harmony in Nature',
    'Abstract Whispers',
    'Urban Jungle Dreams',
    'Dancing with Light',
    'Whimsy and Wonder',
    'Reflections of Light',
    'Unraveling Mysteries',
    'Euphoric Elegance',
    'Shaping Time',
    'Exploring Contrasts',
    'Tangled Emotions',
    'Fleeting Moments Frozen',
    'The Magic of Details',
    'Whispered secrets',
    'Essence of life',
    'Unveiling the Unknown',
    'Layers of Identity',
    'Echoes of silence',
    'Spectral Whispers',
    'The Tapestry of Life',
    'Enchanted Realms',
    'Celestial Fusion',
    'Journey Through Time',
    'Soulful Melodies',
    'Emerging Dimensions',
    'The Poetry of Color',
    'Whimsical Wanderlust',
    'The Kaleidoscope of Thoughts',
    'Surreal Realities',
    'Symphony of Life',
    'Emotional Landscapes',
    'Whirling Energies',
    'Unseen perspectives',
    'Shades of Wonder',
    'Journey to the Unknown',
    'Unveiling Beauty',
    'The Alchemy of Creation',
    'Melodies of nature',
    'Whispers of Memory',
    'Fragments of Life',
    'Human Connections',
    'Echoes of Time',
    'Melodies of Light',
    'Surreal visions',
    'Luminous Shadows',
    'Shades of Serendipity',
    'Rhythmic Patterns',
    'Captured Moments',
    'Whimsical Creatures',
    'Embracing Imperfections',
    'Echoes of the Soul',
    'Hidden Dimensions',
    'The rhythm of nature',
    'Rhythms of the Soul',
    'Perpetual Motion',
    'Exploring Inner Landscapes',
    'Magical realism',
    'The Essence of Love',
    'Eternal Flames',
    'The Power of Emotion',
    'Cosmic Wonder',
    'Emerging Patterns',
    'Lyrical Brushstrokes',
    'Unveiling the Invisible',
    'Surreal Symmetry',
    'Mystical Melodies',
    'Melodic Vibrations',
    'Infinite Love',
    'Vibrant Fusion',
    'Captured Essence',
    'Sculpting Dreams',
    'Cosmic Dreamscape',
    'Shades of Emotion',
    'Unseen Dimensions',
    'Surreal Wonder',
    'Mystical Mosaics',
    'The Rhythm of Life',
    'Invisible Connections',
    'Cultural Fusion',
    'Evolving Identity',
    'Immersed in Texture',
    'The power of words',
    'Abstracting Reality',
    'Reflections of Time',
    'Liberating Limitations',
    'Cosmic Rhythms',
    'Exploring Duality',
    'Surreal Whispers',
    'Reimagined Realities',
    'Euphoric Euphony',
    'Shattered Illusions',
    'Unspoken Emotions',
    'Ethereal Explorations',
    'Vibrant Reverie',
    'The essence of time',
    'The Beauty of Solitude',
    'Harmony in Motion',
    'Metamorphosis of Self',
    'Abstract landscapes',
    'Mystic Mosaics',
    'The Harmony of Shapes',
    'The Fragments of Time',
    'Eternal Connections',
    'The Language of Symbols',
    'The Power of Light',
    'Journey Within',
    'Dreamlike Journeys',
    'Ephemeral Essence',
    'Unveiling the Unseen',
    'Vibrant Abstractions',
    'Hidden Messages',
    'Enigmatic portraits',
    'Rhythm of the Universe',
    'Capturing Timelessness',
    'Unlocking Creativity',
    'Eternal Metamorphosis',
    'The Souls Canvas',
    'Spectrum of Dreams',
    'Urban Melodies',
    'Dancing Fireflies',
    'Vibrant Energy',
    'Vibrant Reflections',
    'Serenade of Silence',
    'The Beauty of Imperfection',
    'Serenade of Serenity',
    'Imaginary Portraits',
    'Urban reflections',
    'Dreams and Nightmares',
    'Melting Pot of Cultures',
    'Celestial Serenity',
    'The Complexity of Silence',
    'Enigmatic Visions',
    'The Souls Reflection',
    'Starry Nightscapes',
    'Whispering Landscapes',
    'Whirling Energy',
    'The Magic of Lines',
    'Fragments of Memory',
    'Mystical Waters',
    'The souls journey"',
    'Shattered Realities',
    'Mystic Reverie',
    'Whimsical Wonderlands',
    'Spectral Illusions',
    'Theatrical Illusions',
    'Celestial wonders',
    'Emerald Dreamscape',
    'Into the Abyss',
    'Surreal Wonderlands',
    'Whispered Echoes',
    'Ephemeral Echoes',
    'Imaginary Worlds',
    'Cosmic Exploration',
    'Chasing Rainbows',
    'Eternal Reflections',
    'Unveiling Illusions',
    'The Dance of Elements',
    'The Fragments of Dreams',
    'Enchanting Abstractions',
    'Cosmic Harmony',
    'The Mystery Within',
    'Harmonious Fusion',
    'Enchanted Horizons',
    'Melting Boundaries',
    'The power of silence',
    'Harmony in Disarray',
    'Dancing with shadows',
    'Melting Horizons',
    'Journey into Silence',
    'Parallel Universes Unveiled',
    'Rhythm of the Rain',
    'Whirling Dervishes',
    'Celestial Whispers',
    'Vibrant Whirlwind',
    'Capturing Essence',
    'Fusion of Elements',
    'The Power of Imagination',
    'Surreal Symphony',
    'Fragments of memories',
    'Enigmatic Elegance',
    'Reflections of the Soul',
    'Journey to the Stars',
    'Captured Fragments',
    'Ethereal Euphoria',
    'Luminous Whispers',
    'Dancing with Fire',
    'Exploring Boundaries',
    'Melodies of the Soul',
    'Visions of Tranquility',
    'Uncharted territories',
    'Unseen Realities',
    'Embracing Imperfections',
    'The Whirlwind of Inspiration',
    'Mystic Visions',
    'Textures of existence',
    'Abstract Realities',
    'Fleeting Eternity',
    'Sculpted Soundwaves',
    'Vibrant energy',
    'Vibrant Serenity',
    'Evolving Emotions',
    'Redefining Beauty',
    'Chromatic Whispers',
    'Evolving Whispers',
    'Hidden Beauty',
    'Transcendent Whispers',
    'Abstract Alchemy',
    'The Power of Words',
    'The Symphony of Senses',
    'The Essence of Dreams',
    'Vibrant Reverberations',
    'Serenading Shadows',
    'Emotional Resonance',
    'Transcendent Silence',
    'Uncharted Realms',
    'Journey into Abstraction',
    'Echoes of Nature',
    'The Unseen Universe',
    'Sculpted Dreams',
    'Melodies of the Heart',
    'Colorful chaos',
    'Whispering Horizons',
    'Mosaic of Life',
    'Melting Time',
    'Ephemeral Eternity',
    'Serenade of Textures',
    'Timeless moments',
    'Unseen Connections',
    'Sculpting Memories',
    'Temporal Fragments',
    'Harmonious Chaos',
    'Abstract Euphoria',
    'Whimsical Abstractions',
    'Ethereal Watercolors',
    'Harmony of Colors',
    'Rhythm of the Soul',
    'Unspoken Stories',
    'Curious Contradictions',
    'Luminous Reflections',
    'Infinite Echoes',
    'Exploring Fragility',
    'The Intersection of Cultures',
    'Serenading Sunsets',
    'Ethereal Serenity',
    'Eternal Fragments',
    'The Art of Connection',
    'Embracing Shadows',
    'Celestial Landscapes',
    'The Power of Contrast',
    'Abstract Reverie',
    'Tales Untold',
    'Symphony of Shapes',
    'Chromatic Kaleidoscope',
    'Ethereal Enchantment',
    'The Transcendent Journey',
    'Melancholic Melodies',
    'Infinite Horizons',
    'Alchemy of Expression',
    'Unveiling mysteries',
    'Organic Abstractions',
    'Colorful Chaos',
    'Unraveling Time',
    'Infinite Depths',
    'Whirlwind of Thoughts',
    'Inner Strength',
    'Vibrant Visions',
    'Echoes of Emotion',
    'Rhythms of the city',
    'Evolving Horizons',
    'Metamorphosis of nature',
    'Whimsical Dreams',
    'Rhythmic Rapture',
    'Emerging Realities',
    'Harmony of Contrasts',
    'Luminous Journeys',
    'The dance of colors',
    'Celestial Wonders',
    'Hidden Worlds Revealed',
    'Whirlwind of Colors',
    'Celestial Reflections',
    'Luminous Illusions',
    'Temporal Echoes',
    'Urban Tapestry',
    'Sensory Explorations',
    'Harvesting Hope',
    'Harmony in Contrast',
    'Eternal Motion',
    'Whimsical Journey',
    'Enigmatic Portraits',
    'Ethereal Reflections',
    'Urban Illusions',
    'Abstracted Emotions',
    'Urban rhythms',
    'Unspoken narratives',
    'Journey of Colors',
    'Spectral Melodies',
    'Celestial Rhapsody',
    'Vibrant Brushstrokes',
    'Journey of the Soul',
    'Sonic Landscapes',
    'Celestial Mosaics',
    'Translucent Dreams',
    'Textures of Life',
    'Exploring Dimensions',
    'Dreamlike Landscapes',
    'Spiraling Visions',
    'Ancient Mysteries',
    'Mysterious Abandon',
    'Shimmering Dreamscape',
    'Captivating Illusions',
    'Transcendent Echoes',
    'Hidden Meanings',
    'Metamorphosis of Time',
    'Reimagining Reality',
    'The Language of Shapes',
    'Hidden Beauty Revealed',
    'Enchanted Visions',
    'Uncharted Territories',
    'Journey of self',
    'The Beauty Within',
    'Shaping Memories',
    'Cosmic Whispers',
    'Embracing Chaos',
    'Fleeting Moments',
    'The Ebb and Flow',
    'Underwater Fantasies',
    'Parallel Universes',
    'The Language of Dreams',
    'The Dance of Light',
    'The Melody of Light',
    'The Dance of Nature',
    'Transcendent Reflections',
    'Whispers of Inspiration',
    'Ethereal Landscapes',
    'Ephemeral Whispers',
    'Shadows of Tomorrow',
    'Infinite Horizon',
    'Dreams Unleashed',
    'The Dance of Shadows',
    'Abstracted Realities',
    'Rhythmic Reverie',
    'Abstracted Movements',
    'Spiraling Energy',
    'Enchanted Whispers',
    'Abstract Harmony',
    'Whispering Winds',
    'Ethereal Dreamscape',
    'Imaginary Realms',
    'Uncharted Waters',
    'Embracing the wild',
    'Transcendent Beauty',
    'Curiosity Unleashed',
    'Synchronized Chaos',
    'Whispering Whispers',
    'Serenading Silence',
    'Captivating Rhythms',
    'Abstract Illusions',
    'Shaping Perspectives',
    'Mystic Reflections',
    'Surreal fantasies',
    'Surreal Visions Unveiled',
    'Abstract Landscapes',
    'The Essence of Freedom',
    'Whimsical Whispers',
    'Colors in Motion',
    'The language of dreams',
    'Surreal Symphonies',
    'Ethereal Echoes',
    'Infinite Reflections',
    'The Poetry of Light',
    'Luminous Landscapes',
    'Whimsical wonders',
    'Sculpted Emotions',
    'Echoes of Silence',
    'Cosmic Serenade',
    'Evolving Perspectives',
    'Unseen Emotions',
    'Melancholic Whispers',
    'Urban Melancholy',
    'Whispered Whispers',
    'Eternal Transcendence',
    'Journey to Nowhere',
    'Infinite Fragments',
    'Ethereal Essence',
    'Melodies of Life',
    'Mystical Mosaic',
    'Euphorias Embrace',
    'The Wonder of Discovery',
    'Vivid Imagination',
    'Shadows of the Mind',
    'Unveiling Emotions',
    'Journey of Shadows',
    'Journey of Self-Discovery',
    'Exploring Connections',
    'Cosmic Vibrations',
    'The Language of Flowers',
    'Mystical Landscapes'
]


# Import all submodules.
from . import protocol
from . import reward
from . import utils
