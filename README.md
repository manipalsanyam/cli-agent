## Quick Start

```bash
pip install -r requirements.txt
$env:OPENAI_API_KEY="your_api_key_here"
python main.py

This helps someone run your project in 10 seconds. People notice that.

---

## 2. Check your repo looks clean

In VS Code (Explorer), you should have:

- `main.py`  
- `README.md`  
- `ISSUES.md`  
- `requirements.txt`  
- `.gitignore`  
- `venv/` (but NOT pushed to GitHub)

👉 If `venv` is on GitHub, your `.gitignore` didn’t work—tell me, we’ll fix it.

---

## 3. What your repo now communicates

Without you saying anything, it shows:

- You can structure a project  
- You understand input → processing → output  
- You faced real issues and documented them  
- You know basic Git discipline  

That’s exactly what your head is evaluating.

---

## 4. If they ask you to explain (keep it simple)

Say this, calmly:

> “I built a CLI-based agent that takes meeting notes as input and uses an LLM to generate structured summaries and action items.  
> I focused on clearly defining the processing flow and documenting the issues I faced during development.”

That’s enough. Don’t over-explain.

---

If you want, I can now:
- review your actual GitHub repo (line by line)
- or help you add **one more feature** to make it stand out


# MEETING AGENT CLI

Python OpenAI CLI Tool

A lightweight agentic CLI application that converts unstructured meeting notes into structured summaries and actionable insights using LLMs.


## Overview

This project demonstrates a simplified agent pipeline built using OpenAI.  
It follows a clear **input → processing → output** architecture and is designed as a foundation for building production-grade AI assistants.


## Architecture

The system follows a linear agent pipeline:

User Input (CLI)
        ↓
LLM Processing (OpenAI)
        ↓
Structured Output (Summary + Action Items)


## Core Flow

1. User enters raw meeting notes via CLI  
2. Input is sent to OpenAI model  
3. Model processes:
   - Summarization  
   - Action item extraction  
4. Structured response is returned to user  


## Project Structure
cli-agent/
├── main.py CLI entry point
├── requirements.txt Dependencies
├── README.md Documentation
├── ISSUES.md Development issues and learnings
└── .gitignore Ignored files

## Features

- CLI-based interaction  
- Real-time LLM processing  
- Structured output generation  
- Clean input → processing → output pipeline  


## Tech Stack

- Python  
- OpenAI API  
- CLI Interface  


## Setup & Run

pip install -r requirements.txt


### Set API key (PowerShell)


$env:OPENAI_API_KEY="your_api_key_here"


### Run the agent


python main.py


## Example

Input:

Output:

## Issues & Learnings

See `ISSUES.md` for real development challenges faced during implementation.



## Future Scope

- Multi-agent architecture (planner + executor)  
- Integration with Slack / Notion  
- Persistent memory  
- Web-based interface  

---

## Design Principles

- Clear input → processing → output flow  
- Minimal but extensible architecture  
- Focus on clarity over complexity  

---

## Status

Initial CLI version under development