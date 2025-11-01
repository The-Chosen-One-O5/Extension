#!/usr/bin/env python3
"""
Session String Generator for Telethon

This script helps you generate a session string for the bot.
You'll need to provide your API_ID, API_HASH, and phone number.
"""

import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

def print_banner():
    print("=" * 60)
    print("Telegram Session String Generator")
    print("=" * 60)
    print()

async def main():
    print_banner()
    
    print("Enter your API credentials from https://my.telegram.org")
    print()
    
    try:
        api_id = int(input("API_ID: "))
        api_hash = input("API_HASH: ")
        
        print()
        print("Connecting to Telegram...")
        print()
        
        async with TelegramClient(StringSession(), api_id, api_hash) as client:
            session_string = client.session.save()
            
            print()
            print("=" * 60)
            print("SUCCESS! Your session string:")
            print("=" * 60)
            print()
            print(session_string)
            print()
            print("=" * 60)
            print()
            print("Copy this string and add it to your .env file as:")
            print(f"SESSION_STRING={session_string}")
            print()
            print("Keep this string secure and never share it publicly!")
            print("=" * 60)
            
    except ValueError:
        print("Error: API_ID must be a number")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
