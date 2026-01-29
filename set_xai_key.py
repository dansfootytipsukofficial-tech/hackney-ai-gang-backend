#!/usr/bin/env python3
import os
import getpass

env_path = os.path.join(os.path.dirname(__file__), '.env')

print('This will securely prompt for your xAI (Grok) API key and write it to', env_path)
key = getpass.getpass('Enter XAI API key: ')
if not key:
    print('No key entered, aborting.')
    raise SystemExit(1)

# Read existing .env if present
lines = []
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

# Update or append
found = False
for i, line in enumerate(lines):
    if line.strip().startswith('XAI_API_KEY='):
        lines[i] = f'XAI_API_KEY={key}\n'
        found = True
        break

if not found:
    if lines and not lines[-1].endswith('\n'):
        lines[-1] = lines[-1] + '\n'
    lines.append(f'XAI_API_KEY={key}\n')

with open(env_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Wrote XAI_API_KEY to', env_path)
print('Now run the restart script to apply the change:')
print('  ./restart_and_test.sh')
