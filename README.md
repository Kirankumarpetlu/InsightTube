# InsightTube

InsightTube is an AI-powered YouTube video analysis chatbot project. It comprises a robust Python FastAPI backend leveraging [AutoGen](https://microsoft.github.io/autogen/) and the [Groq API](https://groq.com/) for natural language processing, combined with a modern React frontend.

## Features

- **YouTube Video Analysis**: Paste a YouTube link, and the chatbot will automatically fetch its transcript and summarize the video content.
- **Conversational AI**: Uses the powerful and fast Groq LLM to handle conversational interactions in a natural way.
- **Agentic Workflow**: Backend utilizes AutoGen coordinator and video agents to orchestrate tool-calling (e.g., extracting YouTube transcripts) and routing.
- **Modern UI**: A responsive, intuitive chat interface built with React, Tailwind CSS, and Shadcn UI.

---

## Project Structure

The repository is divided into two main parts:

1. **`backend/`**: A Python FastAPI server handling AI inference, agents, and API endpoints.
2. **`chrono-muse-93-main/chrono-muse-93-main/`**: The frontend directory containing the React + TypeScript application built with Vite.

---

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js & npm**
- **Groq API Key** (Get one at [console.groq.com](https://console.groq.com/))

### 1. Setting up the Backend

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `backend` directory and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```
5. Start the backend server:
   ```bash
   python main.py
   ```
   *The backend will be available at `http://localhost:8000`.*

### 2. Setting up the Frontend

1. Navigate to the frontend directory:
   ```bash
   cd chrono-muse-93-main/chrono-muse-93-main
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   *The frontend will be available at `http://localhost:8080` (or `5173`).*

---

## Usage

1. Ensure both the backend and frontend servers are running.
2. Open the frontend address (`http://localhost:8080`) in your web browser.
3. Start chatting! Try asking general questions or paste a YouTube URL to get an AI summary of the video.

## Technologies Used

- **Backend**: FastAPI, Python, AutoGen, Groq AI, Pydantic, YouTube Transcript API
- **Frontend**: React, TypeScript, Vite, Tailwind CSS, Shadcn UI, Radix UI

## License

This project is licensed under the MIT License.
