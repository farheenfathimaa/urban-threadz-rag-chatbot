# RAG Business Chatbot

A reusable, multi-tenant Retrieval-Augmented Generation (RAG) chatbot for small businesses.

## Features
- Role-based access (Admin / User)
- Business-specific document isolation
- PDF, DOCX, TXT support
- Gemini embeddings
- Groq (LLaMA3) + Gemini fallback
- Streamlit UI
- Freelancer-ready architecture

## Who this is for
Small business owners who want instant answers from their documents without searching PDFs.

## What you get
- Secure document chatbot
- Private admin-only answers
- Fast AI responses
- Hosted web app

## Typical use cases
- Invoice queries
- Policy clarification
- Internal knowledge base

## Packages Supported
- Basic: Single document chatbot
- Standard: Admin uploads + private docs
- Premium: Unlimited docs + API (extendable)

## Setup

1. Clone repository
2. Create `.env` file with API keys
3. Install dependencies

```bash
pip install -r requirements.txt
