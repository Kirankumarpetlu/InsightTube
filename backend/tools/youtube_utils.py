"""
YouTube URL detection and video ID extraction utilities.
Supports various YouTube URL formats including standard, shortened, and embed URLs.
"""

import re
from typing import Optional


# Regex pattern to match YouTube URLs and extract video IDs
YOUTUBE_URL_PATTERN = re.compile(
    r'(?:https?://)?'
    r'(?:www\.)?'
    r'(?:'
    r'youtube\.com/watch\?v='
    r'|youtu\.be/'
    r'|youtube\.com/embed/'
    r'|youtube\.com/v/'
    r'|youtube\.com/shorts/'
    r')'
    r'([a-zA-Z0-9_-]{11})'
)


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract the YouTube video ID from a URL.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    
    Returns:
        The 11-character video ID, or None if not found.
    """
    match = YOUTUBE_URL_PATTERN.search(url)
    if match:
        return match.group(1)
    return None


def is_youtube_url(text: str) -> bool:
    """
    Check if a text string contains a YouTube URL.
    
    Args:
        text: The input text to check.
    
    Returns:
        True if the text contains a YouTube URL, False otherwise.
    """
    return bool(YOUTUBE_URL_PATTERN.search(text))


def extract_youtube_url(text: str) -> Optional[str]:
    """
    Extract the full YouTube URL from a text string.
    
    Args:
        text: The input text to search.
    
    Returns:
        The matched YouTube URL string, or None if not found.
    """
    match = YOUTUBE_URL_PATTERN.search(text)
    if match:
        return match.group(0)
    return None
