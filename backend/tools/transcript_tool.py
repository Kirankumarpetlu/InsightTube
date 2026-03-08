"""
YouTube transcript extraction tool.
Uses youtube-transcript-api to fetch and merge video transcripts.
Compatible with youtube-transcript-api v1.0+ (instance-based API).
"""

from youtube_transcript_api import YouTubeTranscriptApi
from tools.youtube_utils import extract_video_id


def get_video_transcript(video_url: str) -> str:
    """
    Fetch the transcript of a YouTube video and return it as a single text string.

    Args:
        video_url: The YouTube video URL or any text containing a YouTube URL.

    Returns:
        The full transcript text merged from all segments.

    Raises:
        ValueError: If the video ID cannot be extracted from the URL.
        Exception: If the transcript cannot be fetched (e.g., no captions available).
    """
    video_id = extract_video_id(video_url)

    if not video_id:
        raise ValueError(
            f"Could not extract a valid YouTube video ID from: {video_url}"
        )

    try:
        # Use instance-based API (v1.0+)
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)

        # Merge all transcript snippets into a single text
        transcript_text = " ".join(
            snippet.text for snippet in transcript
        )

        return transcript_text

    except Exception as e:
        raise Exception(
            f"Could not fetch transcript for video ID '{video_id}'. "
            f"The video may not have captions available. Error: {str(e)}"
        )
