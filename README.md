# ai-portfolio

> A digital portfolio you can actually talk to.

This chatbot is an AI-powered RAG-based personal portfolio that allows visitors to interact with a knowledge base about Farhan's education, skills, projects, experience, achievements, and other professional information through a conversational interface.

Instead of navigating through a traditional portfolio, visitors can simply ask questions such as:

- "What projects has Farhan worked on?"
- "What are Farhan's technical skills?"
- "Tell me about his experience."
- "What is his best project?"
- "Where does Farhan study?"

The system retrieves the most relevant information from Farhan's personal knowledge base and uses Google's Gemini models to generate a natural response.

---

## ✨ Features

### 🤖 Conversational Portfolio

Visitors can interact with the portfolio just like they would with an AI assistant.

### 🧠 Retrieval-Augmented Generation

The system uses a RAG pipeline to retrieve relevant information from Farhan's personal knowledge base before generating an answer.

This helps the AI answer questions using information specifically documented about Farhan rather than relying purely on the model's general knowledge.

### 🔎 Semantic Search

User questions are converted into embeddings and compared against the stored knowledge-base embeddings to identify the most relevant information.

### 🎯 Keyword Boosting

In addition to semantic similarity, the retrieval system gives additional weight to direct matches in important fields such as:

- Categories
- Titles
- Project names
- Other important keywords

This helps specific questions retrieve the most appropriate information.

### 🌐 Interactive Web Interface

The project includes a custom-designed interface built specifically for the portfolio rather than relying on a traditional chatbot template.

### 💬 Personalized Chat

Visitors can optionally provide their name before starting the conversation, allowing the interface to personalize the chat experience.

### 👤 Profile Identity

The chat interface supports profile-style user and Farhan message identities, creating a more natural conversational experience.

### ⚡ Cached Embeddings

Embeddings are cached locally so they do not need to be regenerated every time the application starts.

The cache is automatically invalidated when the underlying personal data changes.

---

# 🏗️ Architecture


The project follows a relatively simple RAG architecture:

```text
                    ┌─────────────────────┐
                    │      Visitor        │
                    └──────────┬──────────┘
                               │
                               │ Question
                               ▼
                    ┌─────────────────────┐
                    │    Web Interface    │
                    │   HTML / CSS / JS   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Python API       │
                    │   Vercel Function   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Retriever      │
                    │                     │
                    │ Semantic Similarity │
                    │        +            │
                    │  Keyword Boosting   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Personal Knowledge  │
                    │       Base          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Gemini Embeddings │
                    │                     │
                    │  + Gemini LLM       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Final Answer     │
                    └─────────────────────┘
