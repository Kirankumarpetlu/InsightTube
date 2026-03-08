"""
Video Agent - AutoGen agent responsible for extracting transcripts from YouTube videos.
Uses the transcript tool to fetch and return raw transcript text.
Compatible with autogen-agentchat 0.4+ API.
"""

from autogen_agentchat.agents import AssistantAgent
from config.llm_config import get_model_client
from tools.transcript_tool import get_video_transcript
from tools.youtube_utils import extract_video_id


def create_video_agent() -> AssistantAgent:
    """
    Create and return an AutoGen AssistantAgent configured for video processing.
    """
    video_agent = AssistantAgent(
        name="VideoAgent",
        model_client=get_model_client(),
        system_message=(
            "You are a video processing agent. Your job is to extract transcripts "
            "from YouTube videos. When given a video URL, extract the video ID, "
            "fetch the transcript, and return the raw transcript text."
        ),
    )
    return video_agent


def process_video(video_url: str) -> dict:
    """
    Process a YouTube video URL and extract its transcript.
    Uses the transcript extraction tool as the core functionality.

    Args:
        video_url: The YouTube video URL or text containing a YouTube URL.

    Returns:
        A dict with 'success' status, 'transcript' text, and 'video_id'.
    """
    try:
        # Step 1: Extract video ID
        video_id = extract_video_id(video_url)
        if not video_id:
            return {
                "success": False,
                "error": "Could not extract a valid YouTube video ID from the provided URL.",
                "transcript": None,
                "video_id": None,
            }

        # Step 2: Fetch transcript using the transcript tool
        transcript = get_video_transcript(video_url)

        if not transcript or transcript.strip() == "":
            return {
                "success": False,
                "error": "The video transcript is empty. The video may not have captions.",
                "transcript": None,
                "video_id": video_id,
            }

        # Step 3: Return the extracted transcript
        return {
            "success": True,
            "transcript": transcript,
            "video_id": video_id,
            "error": None,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "transcript": None,
            "video_id": None,
        }
