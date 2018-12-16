# nullbot-twitch-chatbot

Hello, this is my project of creating **chat bot for Twitch**. Its built on Python 3.6 and sockets module. My goal is to make it fast and functional but keeping code small and readable. Currently its the only one python twitch bot which **supports SSL**.

Current version: **v0.2**

**How to use**:
1. Input all necessary data in config.py (all strings are commented there)
2. Add your commands in nulbot.py
3. Add functions for commands in commands.py
4. Start bot with `python3 nullbot.py`

**RoadMap**:
1. Make creating custom commands user-friendly
2. Add SSL support - DONE
3. Add Twitch API support and some functions to use it