# Truti AI Bridge

Truti AI Bridge is a lightweight Python microservice that acts as the strategic intelligence layer for the Truti Robot Operating System.

It reads raw sensor data from the hardware (C++ layer), evaluates it against a configurable set of rules, and queries a Large Language Model (LLM) to generate intelligent, dynamic responses. Finally, it formats the output into a strict JSON payload that the C++ OS can execute.

## Core Features
- **Decoupled Architecture:** Keeps the slow AI processing completely separate from the fast, real-time C++ hardware control loop.
- **Model Agnostic:** Uses the standard OpenAI Python SDK, allowing it to connect to any compatible API (OpenAI, Gemini, Groq, local Ollama).
- **YAML Configuration:** AI behavior, sensor thresholds, and system prompts are defined in a simple YAML file, requiring no code changes to update logic.

## Setup

1. Create a virtual environment and install the required packages:
```bash
python -m venv venv
source venv/bin/activate
pip install openai pyyaml python-dotenv
```

2. Create a `.env` file in the root directory and add your API key and endpoint:
```env
GEMINI_API_KEY="your-api-key-here"
BASE_URL="[https://generativelanguage.googleapis.com/v1beta/openai/](https://generativelanguage.googleapis.com/v1beta/openai/)"
```

## How to Customize for Your Own Use

You can easily adapt this bridge for different sensors, graphics, or AI personalities by editing the `config/behavior.yaml` file.

### Example `config/behavior.yaml`:
```yaml
llm:
  model: "gemini-3.8-flash"
  temperature: 0.2

sensors:
  mpu6050:
    events:
      - state: "tipping_forward"
        condition: "pitch > 45.0"
        graphic_id: 101
        prompt: "The robot is tipping forward. Return a 1-word panicked reaction."
      - state: "stable"
        condition: "-5.0 < pitch < 5.0"
        graphic_id: 102
        prompt: "The robot is perfectly balanced. Return a short, cool greeting."
```

### Steps to Modify:
1. **Change the Model:** Update the `model` field to any supported string (e.g., `gpt-4o-mini`, `llama3.2`).
2. **Add New Sensors:** Create a new block under `sensors`.
3. **Define Custom Logic:** Add new rules under `events`. The `condition` evaluates the incoming sensor data.
4. **Map Outputs:** Change the `graphic_id` to match the enums in your specific C++ hardware, and adjust the `prompt` to change the AI's personality.

## Running the Bridge
```bash
python src/simulator.py
```

## How to Create an "Umbrella" for Truti OS

To link both repositories together so they look like one professional project to a company, create a GitHub Organization:
1. Go to your GitHub homepage.
2. Click the **"+"** icon in the top right corner and select **New organization**.
3. Choose the **Free** plan and name it something like **Truti-Robotics**.
4. Go to the Settings of your `truti-os` and `truti-ai-bridge` repositories, scroll to the bottom (Danger Zone), and click **Transfer ownership** to move them into your new organization.

This makes your GitHub profile look incredibly professional, showing you know how to split a complex system into multiple interconnected microservices.