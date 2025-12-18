import sys
import os
sys.path.append(os.path.abspath('..'))
from app.agent import root_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

print("Setup session and runner")
session_service = InMemorySessionService()
session = session_service.create_session_sync(user_id="notebook_user", app_name="notebook_app")
runner = Runner(agent=root_agent, session_service=session_service, app_name="notebook_app")

query_text = "What is the weather in SF?"
message = types.Content(role="user", parts=[types.Part.from_text(text=query_text)])
print(f"User: {query_text}")

events = list(runner.run(
    new_message=message,
    user_id="notebook_user",
    session_id=session.id
))

print("Agent:")
for event in events:
    if event.content and event.content.parts:
        for part in event.content.parts:
            if part.text:
                print(part.text)
