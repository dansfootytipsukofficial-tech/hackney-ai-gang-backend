#!/usr/bin/env python3
import os
import getpass

# Get the OpenAI API key securely
api_key = getpass.getpass("Enter your OpenAI API key (starts with 'sk-'): ")

# Update the .env file
env_file = '.env'
with open(env_file, 'r') as f:
    content = f.read()

# Replace the placeholder
content = content.replace('PASTE_YOUR_OPENAI_KEY_HERE', api_key)

with open(env_file, 'w') as f:
    f.write(content)

print("✅ OpenAI API key has been set successfully!")
print("You can now test Hackney Boss AI at http://127.0.0.1:8002")