import os
import yaml
import json
from openai import OpenAI
from dotenv import load_dotenv

def load_config():
    with open('config/behavior.yaml', 'r') as file:
        return yaml.safe_load(file)


def simulate_event(client, model_name, sensor, pitch_value, config):
    #read the yaml rules
    events = config['sensors'][sensor]['events']
    triggered_event = None

    for event in events:
        if eval(event['condition'].replace('pitch', str(pitch_value))):
            triggered_event = event
            break

    if not triggered_event:
        return "[System] No event triggered for this sensor data."


    #query the open ai api
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are Truti OS Agent, an agent controlling the Truti Robot Operating System. Follow instructions exactly."},
                {"role": "user", "content": triggered_event['prompt']}
            ]
        )
        llm_text = response.choices[0].message.content.strip()
    except Exception as e:
        llm_text = f"Error connecting to OpenAI: {e}"    

    # format the json payload for the C++ event bus
    cxx_payload = {
        "target": "oled_service",
        "action": "update_display",
        "payload": {
            "graphic_id": triggered_event['graphic_id'],
            "llm_text": llm_text
        }
    }

    return json.dumps(cxx_payload, indent = 2)

if __name__ == "__main__":

    load_dotenv()

    client = OpenAI(
        api_key = os.getenv("GEMINI_API_KEY"),
        base_url = os.getenv("BASE_URL")
    )
    config = load_config()
    model = config['llm']['model']

    print(f"--- Testing Stable Pitch (0.0) with {model} ---")
    print(simulate_event(client, model, 'mpu6050', 0.0, config))

    print(f"\n--- Testing Falling Pitch (60.0) with {model} ---")
    print(simulate_event(client, model, 'mpu6050', 60.0, config))

    print(f"\n--- Testing random Pitch (160.0) with {model} ---")
    print(simulate_event(client, model, 'mpu6050', 160.0, config))