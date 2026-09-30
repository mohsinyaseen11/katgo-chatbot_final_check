# KatGo Assistant — RAG-Based Customer Support Chatbot

An AI-powered customer support chatbot for **KatGo.Store**, a Pakistani wholesale e-commerce marketplace. It answers customer questions about delivery, payments, returns, sizing, wholesale policy and the product catalog, using **Retrieval-Augmented Generation (RAG)** over the store's own knowledge document, so replies stay grounded in real store information instead of guesses.

**Live Demo:** https://katgo-chatbot-final-check.onrender.com/widget

> The demo runs on Render's free tier, so the first request may take 30–60 seconds while the server wakes up.

---

## Features

- **RAG pipeline**: answers come only from the store's PDF (prices, policies, FAQs, 100-product catalog); no invented prices or policies.
- **Roman Urdu by default**: replies in Roman Urdu, and switches to English when the user writes in English.
- **Conversation history**: the chat session keeps earlier messages so follow-up questions make sense.
- **WhatsApp-style chat widget**: clean, responsive UI with a typing indicator, Enter-to-send and a send button.
- **Graceful fallback**: when the answer is not in the document, the bot points the customer to the support team's WhatsApp.
- **Embeddable**: CORS is configured so the widget can be used on the store's website (`katgo.store`).
- **Error handling**: shows a friendly message if the AI service fails.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask, Flask-CORS |
| LLM | Google Gemini (`google-genai`) |
| Embeddings | Gemini Embedding (`gemini-embedding-001`) via LangChain |
| Document loading & chunking | LangChain (`PyPDFLoader`, `RecursiveCharacterTextSplitter`) |
| Vector store | LangChain `InMemoryVectorStore` |
| Frontend | HTML, CSS, vanilla JavaScript (Fetch API) |
| Deployment | Render + Gunicorn |

---

## How It Works

```
katgo.pdf ──► Load ──► Chunk (1000 chars, 100 overlap) ──► Embed ──► Vector Store
                                                                          │
User question ──► Similarity search (top 4 chunks) ◄──────────────────────┘
                              │
                              ▼
        Context + chat history + question ──► Gemini ──► Reply
```

1. On startup, the PDF is loaded, split into chunks and embedded into an in-memory vector store.
2. When a user sends a message, the 4 most relevant chunks are retrieved.
3. The retrieved context, the session's chat history and the question are sent to Gemini with a strict system prompt.
4. The reply is returned to the widget and shown in the chat window.

---

## Project Structure

```
.
├── E_Commerce_Assistant.py   # Flask app: RAG pipeline + API routes
├── katgo.pdf                 # Knowledge base (policies, FAQs, catalog)
├── templates/
│   └── test.html             # Chat widget UI + JavaScript
├── static/
│   └── test.css              # Widget styling
├── requirements.txt          # Python dependencies
├── Procfile                  # Render / Gunicorn start command
└── .env                      # API keys (not committed)
```

---

## Getting Started (Local Setup)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
Secret_Key=any_long_random_string
```

You can get a Gemini API key from [Google AI Studio](https://aistudio.google.com/).

### 4. Run the app

```bash
python E_Commerce_Assistant.py
```

Open http://127.0.0.1:5000/widget in your browser.

---

## API Reference

### `POST /json`

Sends a customer message and returns the bot's reply.

**Request**

```json
{ "message": "Karachi mein delivery kitne din mein hoti hai?" }
```

**Response**

```json
{ "reply": "Karachi mein delivery 1-2 working days mein hoti hai, delivery charges Rs 150 hain." }
```

### `GET /widget`

Serves the chat widget page.

---

## Deployment (Render)

1. Push the project to GitHub.
2. On [Render](https://render.com), create a new **Web Service** from the repository.
3. Set the build command to `pip install -r requirements.txt`.
4. The start command is read from the `Procfile`:
   ```
   web: gunicorn E_Commerce_Assistant:app --workers 1 --threads 2 --timeout 120
   ```
5. Add `GEMINI_API_KEY` and `Secret_Key` under **Environment Variables**.

---

## Using the Widget on Another Website

The backend allows requests from `https://katgo.store`. To allow a different domain, update the CORS origins in `E_Commerce_Assistant.py`:

```python
CORS(app, origins=["https://your-domain.com"], supports_credentials=True)
```

---

## Customizing the Knowledge Base

Replace `katgo.pdf` with your own document and restart the app. The bot will re-index it automatically on startup. You can also edit the `system_prompt` in `E_Commerce_Assistant.py` to change the bot's tone, language or fallback message.

---

## Possible Improvements

- Persistent vector database (e.g. Chroma) so the index is not rebuilt on every restart
- Streaming responses for faster perceived replies
- Floating chat-bubble launcher for easy embedding on any site
- Admin dashboard to view conversations and unanswered questions

---

## Author

Built by Mohsin Ali — [GitHub] https://github.com/mohsinyaseen11 · [Fiverr]https://www.fiverr.com/mohsin_yaseeen

Open to freelance work on custom AI chatbots for businesses.
