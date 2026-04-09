# LM Studio CLI Agent

A lightweight CLI agent for chatting with local LLM models via LM Studio.

## Setup

1. **Install LM Studio** from https://lmstudio.ai/
2. **Download & load a model** in LM Studio
3. **Start Local Server** (port 1234)
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the agent**:
   ```bash
   python main.py
   ```

## Features

- ✅ Multi-turn conversations with history
- ✅ Model selection and switching
- ✅ Session tracking (messages, time, model)
- ✅ Colorized terminal output
- ✅ Local execution (no cloud API needed)

## Commands

| Command | Description |
|---------|-------------|
| `clear` | Clear conversation history |
| `models` | List available models |
| `model` | Switch to different model |
| `info` | Show session info |
| `quit` | Exit agent |

## Configuration

Edit `.env` to customize:
```
LM_STUDIO_URL=http://127.0.0.1:1234
```

## Troubleshooting

- **Cannot connect**: Make sure LM Studio is running and local server is started
- **No models found**: Download and load a model in LM Studio first
- **Slow responses**: Enable GPU in LM Studio settings or use a smaller model

## Example Usage

```
You: Hello! What is Python?
🤔 Thinking...
Agent: Python is a high-level programming language...

You: models
Models:
  ✓ mistral-7b
    llama2-13b

You: quit
👋 Goodbye!
```

See [SETUP.md](SETUP.md) for detailed setup instructions.
