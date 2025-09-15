from murf import Murf

client = Murf(
    api_key="ap2_5f1b1f03-645f-45c1-a96d-18f8d4d3ec4a" # Not required if you have set the MURF_API_KEY environment variable
)

res = client.text_to_speech.generate(
    text="There is much to be said",
    voice_id="en-US-terrell",
)

print(res.audio_file)

