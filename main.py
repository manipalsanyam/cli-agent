#!/usr/bin/env python3
"""CLI Agent using LM Studio LLM - http://127.0.0.1:1234"""

import sys
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("LM_STUDIO_URL", "http://127.0.0.1:1234")
API = f"{URL}/v1/chat/completions"
MODELS_API = f"{URL}/v1/models"

# Colors
CL = {
    'B': '\033[94m', 'C': '\033[96m', 'G': '\033[92m',
    'Y': '\033[93m', 'R': '\033[91m', 'BD': '\033[1m', 'E': '\033[0m'
}


class Agent:
    """LM Studio CLI Agent."""
    
    def __init__(self):
        self.history = []
        self.model = None
        self.start = datetime.now()
        self.count = 0
    
    def test(self):
        """Test connection."""
        try:
            return requests.get(MODELS_API, timeout=5).status_code == 200
        except:
            return False
    
    def get_models(self):
        """Get available models."""
        try:
            r = requests.get(MODELS_API, timeout=5)
            return [m["id"] for m in r.json().get("data", [])] if r.status_code == 200 else []
        except:
            return []
    
    def set_model(self, name=None):
        """Set active model."""
        if name:
            self.model = name
        else:
            models = self.get_models()
            self.model = models[0] if models else None
    
    def chat(self, msg):
        """Send message and get response."""
        if not self.model:
            return "Error: No model selected"
        
        try:
            self.history.append({"role": "user", "content": msg})
            payload = {
                "model": self.model,
                "messages": self.history,
                "temperature": 0.7,
                "max_tokens": 2048
            }
            r = requests.post(API, json=payload, timeout=120)
            
            if r.status_code == 200:
                reply = r.json()["choices"][0]["message"]["content"]
                self.history.append({"role": "assistant", "content": reply})
                self.count += 1
                return reply
            return f"Error: {r.status_code}"
        except requests.exceptions.ConnectionError:
            return f"Error: Cannot connect to {URL}"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear(self):
        """Clear history."""
        self.history = []
    
    def info(self):
        """Get session info."""
        dur = str(datetime.now() - self.start).split('.')[0]
        return f"Model: {self.model} | Messages: {self.count} | Time: {dur}"


def main():
    """Main CLI loop."""
    print(f"\n{CL['BD']}{CL['B']}{'='*55}")
    print(f"🤖 LM Studio CLI Agent{CL['E']}")
    print(f"{CL['BD']}{CL['B']}{'-'*55}{CL['E']}\n")
    
    agent = Agent()
    
    # Test connection
    print(f"{CL['Y']}📡 Testing...{CL['E']}")
    if not agent.test():
        print(f"{CL['R']}❌ Cannot connect to {URL}{CL['E']}")
        sys.exit(1)
    
    print(f"{CL['G']}✅ Connected!{CL['E']}")
    
    # Get models
    models = agent.get_models()
    if not models:
        print(f"{CL['R']}❌ No models found{CL['E']}")
        sys.exit(1)
    
    agent.set_model(models[0])
    print(f"{CL['G']}✅ Using: {agent.model}{CL['E']}\n")
    print(f"{CL['C']}Commands: clear | models | model | info | quit{CL['E']}\n")
    
    # Chat loop
    while True:
        try:
            usr = input(f"{CL['B']}You:{CL['E']} ").strip()
            
            if not usr:
                continue
            if usr.lower() in ['quit', 'exit', 'q']:
                print(f"\n{CL['G']}👋 Goodbye!{CL['E']}\n")
                break
            if usr.lower() == 'clear':
                agent.clear()
                print(f"{CL['G']}✓ History cleared{CL['E']}\n")
                continue
            if usr.lower() == 'info':
                print(f"{CL['C']}{agent.info()}{CL['E']}\n")
                continue
            if usr.lower() == 'models':
                print(f"{CL['C']}Models:{CL['E']}")
                for m in models:
                    print(f"  {'✓' if m == agent.model else ' '} {m}")
                print()
                continue
            if usr.lower() == 'model':
                print(f"{CL['C']}Models:{CL['E']}")
                for i, m in enumerate(models, 1):
                    print(f"  {i}. {m}")
                try:
                    idx = int(input(f"{CL['C']}Select:{CL['E']} ")) - 1
                    if 0 <= idx < len(models):
                        agent.set_model(models[idx])
                        print(f"{CL['G']}✓ Changed to {agent.model}{CL['E']}\n")
                except:
                    print(f"{CL['R']}Invalid{CL['E']}\n")
                continue
            
            # Chat
            print(f"{CL['Y']}🤔 Thinking...{CL['E']}", end="", flush=True)
            resp = agent.chat(usr)
            print(f"\r{' '*50}\r{CL['C']}Agent:{CL['E']} {resp}\n")
        
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{CL['G']}👋 Goodbye!{CL['E']}\n")
            break


if __name__ == "__main__":
    main()
