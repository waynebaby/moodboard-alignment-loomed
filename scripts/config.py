"""Centralized configuration for moodboard-alignment scripts."""
import os

# Generic image API, defaulting to Agnes OpenAI-compatible Images API.
# Users with another OpenAI-compatible /images/generations endpoint can set:
#   IMAGE_BASE_URL, IMAGE_API_KEY, DEFAULT_IMAGE_MODEL
AGNES_BASE_URL = os.environ.get("AGNES_BASE_URL", "https://apihub.agnes-ai.com/v1")
AGNES_API_KEY = os.environ.get("AGNES_API_KEY")
IMAGE_BASE_URL = os.environ.get("IMAGE_BASE_URL", AGNES_BASE_URL)
IMAGE_API_KEY = os.environ.get("IMAGE_API_KEY", AGNES_API_KEY or "")

# Generic audio API, defaulting to Mimo chat-audio compatible TTS.
# Users with another compatible endpoint can set:
#   AUDIO_BASE_URL, AUDIO_API_KEY, DEFAULT_AUDIO_MODEL
MIMO_BASE_URL = os.environ.get("MIMO_BASE_URL", "https://token-plan-cn.xiaomimimo.com/v1")
MIMO_API_KEY = os.environ.get("MIMO_API_KEY")
AUDIO_BASE_URL = os.environ.get("AUDIO_BASE_URL", MIMO_BASE_URL)
AUDIO_API_KEY = os.environ.get("AUDIO_API_KEY", MIMO_API_KEY or "")
AUDIO_PROVIDER = os.environ.get("AUDIO_PROVIDER", "mimo_chat_audio")

# Default models. Keep Agnes/Mimo defaults so same-stack users only need API keys.
DEFAULT_IMAGE_MODEL = os.environ.get("DEFAULT_IMAGE_MODEL", "agnes-image-2.1-flash")
DEFAULT_AUDIO_MODEL = os.environ.get("DEFAULT_AUDIO_MODEL", "mimo-v2.5-tts-voicedesign")

# Image generation
IMAGE_SIZES = {
    "1:1": "1024x1024",
    "16:9": "1792x1024",
    "9:16": "1024x1792",
    "4:3": "1024x768",
    "3:4": "768x1024",
}
