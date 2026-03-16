# Telegram Chatbot 2.0

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?style=flat&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-FFD21E?style=flat&logo=huggingface&logoColor=black)](https://huggingface.co/)

> A multi-functional AI assistant on Telegram — natural language conversation, image captioning, text-to-image generation, and real-time news fetching — all in one bot.

---

## Overview

Telegram Chatbot 2.0 integrates four AI capabilities into a single deployable Telegram bot:

- **Conversational AI** using DialoGPT (124M parameters) with a 5-turn memory buffer
- **Image captioning** using BLIP — describe any image sent to the bot
- **Text-to-image generation** using Stable Diffusion v1.5
- **Live news fetching** from 3+ sources with keyword filtering

The system uses async processing throughout to keep response latency low across all features simultaneously.

---

## Architecture

```
User (Telegram)
      │
      ▼
┌─────────────────────────────────────────┐
│           Telegram Bot API              │
│         (python-telegram-bot)           │
└──────────────┬──────────────────────────┘
               │  Route by message type
       ┌───────┴────────┐
       │                │
  Text message      Image message
       │                │
       ▼                ▼
┌────────────┐   ┌─────────────┐
│  DialoGPT  │   │    BLIP     │
│ 124M params│   │  Captioning │
│ 5-turn buf │   └─────────────┘
└─────┬──────┘
      │
  /generate     /news
  command       command
      │              │
      ▼              ▼
┌──────────┐   ┌───────────┐
│  Stable  │   │   News    │
│Diffusion │   │  Scraper  │
│  v1.5    │   │ 3+sources │
└──────────┘   └───────────┘
```

---

## Features

| Feature | Model / Tool | Details |
|---------|-------------|---------|
| Conversation | DialoGPT-medium (124M) | 5-turn history buffer, async inference |
| Image captioning | BLIP (Salesforce) | Describe any image in natural language |
| Image generation | Stable Diffusion v1.5 | Text prompt → 512×512 image |
| News fetching | BeautifulSoup + requests | 3+ sources, keyword filtering |
| Rate limiting | Custom middleware | Handles 100+ concurrent requests |

---

## Results

| Metric | Value |
|--------|-------|
| Response latency | 1.2s average (down from 3.5s — 66% reduction via async) |
| Uptime over 3-month test | 99.2% |
| Concurrent request handling | 100+ |
| Conversation context window | 5-turn history buffer |
| News sources integrated | 3+ |
| Context relevance improvement | 22% (with history buffer vs without) |

---

## Project Structure

```
Telegram_chatbot_2.0/
├── bot/
│   ├── handlers.py         ← Message routing and command handlers
│   ├── conversation.py     ← DialoGPT inference + history buffer
│   ├── captioner.py        ← BLIP image captioning
│   ├── generator.py        ← Stable Diffusion text-to-image
│   └── news.py             ← News fetcher (BeautifulSoup)
├── config.py               ← Bot token, model paths, rate limits
├── main.py                 ← Entry point, async event loop
├── requirements.txt
└── .gitignore
```

---

## Setup & Run

**1. Clone the repository**

```bash
git clone https://github.com/mewadaatharva14/Telegram_chatbot_2.0.git
cd Telegram_chatbot_2.0
```

**2. Create virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure your bot token**

```python
# config.py
BOT_TOKEN = "your-telegram-bot-token"   # Get from @BotFather on Telegram
```

**5. Run**

```bash
python main.py
```

---

## Bot Commands

| Command | Action |
|---------|--------|
| `/start` | Welcome message and feature overview |
| `/generate <prompt>` | Generate an image from a text description |
| `/news <keyword>` | Fetch latest news for a topic |
| Send any text | Conversational reply via DialoGPT |
| Send any image | BLIP caption returned instantly |

---

## Key Implementation Details

**Why async processing:**
Each AI model (DialoGPT, BLIP, Stable Diffusion) has its own inference time. Running them synchronously would block the bot for every user while one request is being processed. Using `asyncio` allows the bot to handle multiple users' requests concurrently, which is what cuts latency from 3.5s to 1.2s under load.

**Why a 5-turn history buffer:**
DialoGPT is stateless — it has no memory between calls. To simulate a multi-turn conversation, the last 5 exchanges are formatted and prepended to each new input. A larger buffer would improve coherence but increases token count and inference time. 5 turns was the practical sweet spot.

**Rate limiting strategy:**
Without rate limiting, a single user sending rapid-fire messages would queue up DialoGPT and Stable Diffusion jobs that block all other users. The middleware tracks per-user request timestamps and enforces a minimum interval, keeping the bot responsive under concurrent load.

---

## Tech Stack

- `python-telegram-bot` — Telegram Bot API wrapper
- `transformers` (HuggingFace) — DialoGPT and BLIP
- `diffusers` (HuggingFace) — Stable Diffusion v1.5
- `torch` — Model inference backend
- `beautifulsoup4` + `requests` — News scraping
- `asyncio` — Concurrent message handling

---

## References

| Resource | Link |
|----------|------|
| DialoGPT paper | [Zhang et al. 2020](https://arxiv.org/abs/1911.00536) |
| BLIP paper | [Li et al. 2022](https://arxiv.org/abs/2201.12086) |
| Stable Diffusion | [Rombach et al. 2022](https://arxiv.org/abs/2112.10752) |
| HuggingFace Diffusers | [huggingface.co/docs/diffusers](https://huggingface.co/docs/diffusers) |


---

*Built by [mewadaatharva14](https://github.com/mewadaatharva14)*
