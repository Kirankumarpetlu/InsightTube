"""
Analysis Agent - AutoGen agent that analyzes YouTube video transcripts using Groq LLM.
Produces structured analysis with description, key topics, and summary.
Uses autogen-agentchat 0.4+ API.
"""

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from config.llm_config import get_model_client


# System prompt for the analysis agent
ANALYSIS_SYSTEM_PROMPT = """You are an expert video content analyst. 
When given a YouTube video transcript, you MUST analyze it and produce a well-structured response.

Your analysis MUST follow this exact format:

**Video Description:**
[Write a clear, concise description of what the video is about in 2-3 sentences]

**Key Topics:**
[List the main topics discussed in the video as bullet points]

**Summary:**
[Write a comprehensive but concise summary of the video content in 3-5 sentences]

Provide ONLY the analysis in the format above. Do not add any extra commentary or the word TERMINATE."""


async def _analyze_transcript_async(transcript: str) -> dict:
    """
    Async implementation: Analyze a video transcript using an AutoGen AssistantAgent.
    """
    try:
        # Truncate very long transcripts to avoid token limits
        max_chars = 15000
        if len(transcript) > max_chars:
            transcript = (
                transcript[:max_chars]
                + "... [transcript truncated for analysis]"
            )

        # Create the AutoGen AssistantAgent with Groq model client
        analysis_agent = AssistantAgent(
            name="AnalysisAgent",
            model_client=get_model_client(),
            system_message=ANALYSIS_SYSTEM_PROMPT,
        )

        # Build the analysis prompt
        analysis_prompt = (
            "Analyze the following YouTube video transcript and produce a "
            "structured analysis with Video Description, Key Topics, and Summary.\n\n"
            f"TRANSCRIPT:\n{transcript}"
        )

        # Send message to the agent and get response
        response = await analysis_agent.on_messages(
            [TextMessage(content=analysis_prompt, source="user")],
            cancellation_token=CancellationToken(),
        )

        analysis = response.chat_message.content

        if not analysis:
            return {
                "success": False,
                "analysis": None,
                "error": "Analysis agent did not produce a response.",
            }

        return {
            "success": True,
            "analysis": analysis,
            "error": None,
        }

    except Exception as e:
        return {
            "success": False,
            "analysis": None,
            "error": f"Failed to analyze transcript: {str(e)}",
        }


def analyze_transcript(transcript: str) -> dict:
    """
    Analyze a video transcript using an AutoGen AssistantAgent powered by Groq LLM.

    Args:
        transcript: The full transcript text of the video.

    Returns:
        A dict with 'success' status and 'analysis' text.
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If called from within an async context (FastAPI), create a task
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, _analyze_transcript_async(transcript))
                return future.result()
        else:
            return asyncio.run(_analyze_transcript_async(transcript))
    except RuntimeError:
        return asyncio.run(_analyze_transcript_async(transcript))
