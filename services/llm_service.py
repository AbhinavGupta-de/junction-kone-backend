# services/llm_service.py
import openai


async def process_description(description):
    response = openai.chat.completions.create(
        engine="gpt-4",
        prompt=f"Parse this description into structured JSON with tags: {
            description}",
        max_tokens=150
    )
    structured_data = response.choices[0].text.strip()
    # Extract flags based on LLM analysis (adjust as needed)
    flags = extract_flags(structured_data)
    return structured_data, flags


def extract_flags(structured_data):
    # Example flag extraction logic
    flags = []
    if "manufacturer" in structured_data:
        flags.append("has_manufacturer")
    if "serial_number" in structured_data:
        flags.append("has_serial_number")
    return flags
