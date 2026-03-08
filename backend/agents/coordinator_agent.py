"""
Coordinator Agent - Main orchestrator for the InsightTube chatbot.
Uses AutoGen agents to route user messages to the appropriate workflow:
- YouTube URL detected → Video Agent → Analysis Agent → Structured response
- Normal message → AutoGen AssistantAgent conversational response via Groq

Compatible with autogen-agentchat 0.4+ / pyautogen 0.10+ API.
"""

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from config.llm_config import get_model_client
from tools.youtube_utils import is_youtube_url
from agents.video_agent import process_video
from agents.analysis_agent import analyze_transcript


# System prompt for the conversational assistant
CHAT_SYSTEM_PROMPT = """You are InsightTube AI, a helpful and friendly chatbot assistant. 
You can have normal conversations and also analyze YouTube videos when users share links.
Be conversational, helpful, and engaging in your responses.
Keep your responses concise but informative.
Do NOT include the word TERMINATE in your response."""


def create_coordinator_agent() -> AssistantAgent:
    """
    Create and return the main AutoGen coordinator AssistantAgent.
    This agent handles general conversation using Groq LLM.
    """
    coordinator = AssistantAgent(
        name="CoordinatorAgent",
        model_client=get_model_client(),
        system_message=CHAT_SYSTEM_PROMPT,
    )
    return coordinator


async def _handle_chat_async(user_message: str) -> str:
    """
    Async implementation: Handle normal conversational messages
    using an AutoGen AssistantAgent powered by Groq LLM.
    """
    try:
        coordinator = create_coordinator_agent()

        # Send message and get response
        response = await coordinator.on_messages(
            [TextMessage(content=user_message, source="user")],
            cancellation_token=CancellationToken(),
        )

        result = response.chat_message.content
        if result:
            # Clean up any TERMINATE tokens that might appear
            result = result.replace("TERMINATE", "").strip()
        return result or "I'm sorry, I couldn't generate a response. Please try again."

    except Exception as e:
        return (
            f"❌ **Error:**\n\n"
            f"I encountered an issue while processing your message: {str(e)}"
        )


def _run_async(coro):
    """
    Helper to run an async coroutine from sync context.
    Handles the case where an event loop is already running (e.g. in FastAPI).
    """
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, coro)
                return future.result()
        else:
            return asyncio.run(coro)
    except RuntimeError:
        return asyncio.run(coro)


def handle_message(user_message: str) -> str:
    """
    Main entry point for processing user messages.
    Determines the workflow based on message content and returns the response.

    Workflow:
        1. If YouTube URL detected → Video Agent extracts transcript →
           Analysis Agent summarizes → Return structured analysis
        2. Otherwise → Coordinator Agent generates conversational response

    Args:
        user_message: The user's input message.

    Returns:
        The response string to send back to the user.
    """
    if is_youtube_url(user_message):
        return _handle_youtube_workflow(user_message)
    else:
        return _run_async(_handle_chat_async(user_message))


def _handle_youtube_workflow(user_message: str) -> str:
    """
    Handle the YouTube video analysis workflow using AutoGen agents.

    Pipeline:
        1. Video Agent extracts the transcript
        2. Analysis Agent analyzes the transcript via Groq LLM
        3. Return the structured analysis
    """
    # Step 1: Video Agent extracts transcript
    video_result = process_video(user_message)

    if not video_result["success"]:
        return (
            f"❌ **Error processing video:**\n\n"
            f"{video_result['error']}\n\n"
            f"Please make sure the YouTube link is valid and the video has captions available."
        )

    transcript = video_result["transcript"]
    video_id = video_result["video_id"]

    # Step 2: Analysis Agent analyzes transcript
    analysis_result = analyze_transcript(transcript)

    if not analysis_result["success"]:
        return (
            f"❌ **Error analyzing video:**\n\n"
            f"{analysis_result['error']}\n\n"
            f"The transcript was extracted successfully but analysis failed."
        )

    # Step 3: Return the structured analysis
    response = (
        f"🎬 **YouTube Video Analysis** (ID: `{video_id}`)\n\n"
        f"---\n\n"
        f"{analysis_result['analysis']}"
    )

    return response
