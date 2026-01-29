#!/usr/bin/env python3
"""Simple CLI chat client for Hackney Boss AI.

Usage: python hackney_chat.py

It prompts for a message and sends it to the local backend `/chat` endpoint.
Default model is `grok-code-fast-1` (if you set XAI_API_KEY) or `github-copilot`.
"""
import os
import sys
import json
import requests

API_URL = os.getenv('HACKNEY_API_URL', 'http://127.0.0.1:8002/chat')

def prompt():
    print('\nHackney Boss CLI Chat — type a message (empty to quit)')
    model = input('Model (press Enter for default grok-code-fast-1): ').strip() or 'grok-code-fast-1'
    while True:
        msg = input('\nYou: ').strip()
        if not msg:
            print('Goodbye.')
            return
        payload = {
            'message': msg,
            'model': model,
            'temperature': 0.7,
            'max_tokens': 400
        }
        try:
            r = requests.post(API_URL, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            # response_model ChatResponse { response: str, model_used: str }
            resp = data.get('response') if isinstance(data, dict) else None
            if resp is None:
                print('Unexpected reply format:', data)
            else:
                print('\nHackney Boss:', resp)
        except Exception as e:
            print('Error calling backend:', str(e))
            print('Tip: make sure the backend is running and XAI/API keys are set if using grok.')
            return

if __name__ == '__main__':
    prompt()
