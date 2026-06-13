# DSA Socratic Tutor 

A full-stack backend for an AI-driven DSA tutoring system. Instead of giving direct answers, the chatbot uses a Socratic questioning approach to guide users toward solving problems themselves, with conversation memory, semantic search over past problems (RAG), and a spaced-repetition review tracker.

## Features

- **JWT Authentication** — secure register/login with bcrypt password hashing
- **Socratic AI Tutor** — Groq-powered (Llama 3.3 70B) chatbot that progressively escalates hints instead of giving solutions outright
- **Conversation Memory** — full session history is passed to the model on every message
- **Semantic Search / RAG** — embeddings (sentence-transformers, all-MiniLM-L6-v2) + cosine similarity to retrieve relevant past problems and inject them as context
- **Spaced Repetition** — fixed-interval review ladder (1 → 2 → 5 → 10 → 25 days) to track problems due for revision

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL + SQLAlchemy ORM
- **Auth**: JWT (python-jose) + passlib/bcrypt
- **LLM**: Groq API (Llama 3.3 70B Versatile)
- **Embeddings**: sentence-transformers (local, all-MiniLM-L6-v2)

## How It Works

### Socratic Tutoring
When a user asks for help with a problem, the AI tutor doesn't give code immediately. It follows a structured flow:
1. Asks what approach the user has in mind
2. Asks the user to write out their approach, even roughly
3. Probes for time/space complexity understanding
4. Only after genuine effort (or repeated struggle) does it offer hints, then minimal snippets, then a full solution — followed by a request to explain it back

### Memory + RAG
Every message sent includes the full conversation history for that session, so the model has context of what's been discussed. Additionally, the user's message is embedded and compared (via cosine similarity) against previously stored problem descriptions. If a sufficiently similar past problem is found, it's injected into the system prompt as extra context — e.g. connecting a new problem to one tackled in an earlier session.

### Spaced Repetition
Users can mark problems for review via `/review/add`. Each item starts at stage 0 (due immediately). Completing a review via `/review/{id}/complete` advances it to the next interval in the ladder `[1, 2, 5, 10, 25]` days, mimicking a basic Anki-style scheduling system.

## Setup

1. Clone the repo and create a virtual environment:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On Mac/Linux:
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file with:
   ```env
   DATABASE_URL=postgresql://<user>:<password>@localhost/dsa_chatbot
   SECRET_KEY=<your-secret-key>
   GROQ_API_KEY=<your-groq-api-key>
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

4. Open `http://localhost:8000/docs` for interactive API documentation.


### Example: Send a Message

**Request** — `POST /chat/session/3/message`
```json
{
  "content": "I have an array and need to find two numbers that add up to a target. How should I approach this?"
}
```

**Response**
```json
{
  "response": "What approach do you have in mind to solve this problem?"
}
```

## Screenshots

**Chat Session Message**:
<img src="screenshots\chat_session_message.png">

**Chat Session Message Response**:
<img src="screenshots\chat_session_message_response.png">

**Review Due** - shown by stage:0 :
<img src="screenshots\review_due.png">

**Review 1 Complete** - shown by stage:1 :
<img src="screenshots\review_complete.png">

## Roadmap

- React frontend
- Docker 
- pgvector for production-scale similarity search
- Interview mode — timed mock interviews with structured feedback
- Deployment (Render/Neon)