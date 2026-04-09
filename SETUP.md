# Setup Instructions

## 1. Install LM Studio

Download from: https://lmstudio.ai/

## 2. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed requests-2.31.0 python-dotenv-1.0.0
```

## 4. Setup LM Studio

1. Open LM Studio
2. Click **Search** tab
3. Search for a model (e.g., "mistral" or "llama")
4. Click **Download** on a model
5. Wait for download to complete
6. Click **⬆️ Load** next to the model
7. Go to **Local Server** tab
8. Click **Start Server**
9. You should see: `Server listening at http://127.0.0.1:1234`

## 5. Run the Agent

```bash
python main.py
```

Expected output:
```
======================================================================
🤖 LM Studio CLI Agent
======================================================================
Server: http://127.0.0.1:1234

Commands:
  • Type your message and press Enter to chat
  • 'clear' - Clear conversation history
  • 'model' - Change or view current model
  • 'models' - List available models
  • 'info' - Show session information
  • 'system <prompt>' - Set system prompt
  • 'quit' or 'exit' - Exit the agent
----------------------------------------------------------------------

📡 Testing connection to LM Studio...
✅ Connected to LM Studio!
📦 Fetching available models...
✅ Using model: mistral-7b

You: 
```

## 6. Start Chatting!

```
You: Hello! What's your name?
🤔 Thinking...
Agent: Hello! I'm an AI assistant. I don't have a personal name, but you can call me whatever you'd like. How can I help you today?
[1.2s]

You: 
```

Type `quit` to exit.

## Troubleshooting

### "Cannot connect to LM Studio"
- [ ] LM Studio is open?
- [ ] Local Server is running? (check Local Server tab)
- [ ] A model is loaded? (check the status)
- [ ] Try port 1234 in browser: http://127.0.0.1:1234/v1/models

### "No models available"
- [ ] Download a model in LM Studio (Search tab)
- [ ] Load the model (click ⬆️)
- [ ] Wait for it to fully load (progress bar completes)
- [ ] Start the server (Local Server tab → Start Server)

### "Connection timeout"
- [ ] Is the model still loading? Wait a moment
- [ ] Is your RAM low? Close other applications
- [ ] Try a smaller model (7B instead of 13B)

## Next Steps

- Read [README_DETAILED.md](README_DETAILED.md) for full documentation
- Try different models to compare quality/speed
- Modify the agent in main.py to add new features
- Check [ISSUES.md](ISSUES.md) for common problems

Happy chatting! 🤖
