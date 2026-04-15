from openai import OpenAI
import requests

openai_client = OpenAI()


def speech_to_text(audio_binary):
    base_url = '...'
    api_url = base_url + '/speech-to-text/api/v1/recognize'

    params = {'model': 'en-US_Multimedia'}

    stt_response = requests.post(api_url, params=params, data=audio_binary).json()

    if stt_response.get('results'):
        return stt_response['results'][0]['alternatives'][0]['transcript']

    return None

def text_to_speech(text, voice=""):
    base_url = '...'
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'

    if voice and voice != "default":
        api_url += "&voice=" + voice

    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

    return requests.post(api_url, headers=headers, json={'text': text}).content


def openai_process_message(user_message):
    prompt = (
        "Act like a personal assistant. Keep responses concise (2–3 sentences)."
    )

    openai_response = openai_client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_completion_tokens=1000
    )

    return openai_response.choices[0].message.content
