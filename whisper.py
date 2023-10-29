import requests
import pandas as pd
import time
import os
import base64


def audio_to_base64(audio_filepath):
    with open(audio_filepath, 'rb') as audio_file:
        return base64.b64encode(audio_file.read()).decode('utf-8')


def transcribe_audio(audio_filepath):
    base64_audio = audio_to_base64(audio_filepath)
    print(f"Sending request for {audio_filepath}...")  # Printing the URL being sent
    url = "https://api.runpod.ai/v2/bgc1bptbd1dnqs/runsync"
    payload = {
        "input": {
            "audio_base64": f"{base64_audio}",
            "model": "base.en",
            "transcription": "plain text",
            "translate": False,
            "language": "en",
            "temperature": 0,
            "best_of": 10,
            "beam_size": 20,
            "patience": 1,
            "suppress_tokens": [0, 11, 13, 30],
            "condition_on_previous_text": False,
            "temperature_increment_on_fallback": 0.2,
            "compression_ratio_threshold": 2.4,
            "logprob_threshold": -1,
            "no_speech_threshold": 0.6,
            "word_timestamps": False
        },
        "enable_vad": False
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": ""
    }

    start_time = time.time()
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()

    # Check for transcription key in response_data
    if "transcription" not in response_data:
        print(f"Error for {audio_filepath}: {response_data}")  # Print the whole response data to debug
        return {
            "audio_file": os.path.basename(audio_filepath),
            "transcription": "ERROR",
            "translation_time": "N/A",
            "model": "N/A",
            "time_seconds": "N/A"
        }

    transcription = response_data["transcription"]
    translation_time = response_data["translation_time"]
    model_used = response_data["model"]

    end_time = time.time()
    elapsed_time = end_time - start_time

    # Print statements
    print(f"Transcription for {audio_filepath}: {transcription}")
    print(f"Model used: {model_used}")
    print(f"Translation time for {audio_filepath}: {translation_time} seconds")
    print(f"Total time taken for {audio_filepath}: {elapsed_time} seconds")

    return {
        "audio_file": audio_filepath.split("/")[-1],
        "transcription": transcription,
        "translation_time": translation_time,
        "model": model_used,
        "time_seconds": elapsed_time
    }


# Get audio files from the 'Audio' directory in your PyCharm project
audio_directory = "Audio"
audio_files = [os.path.join(audio_directory, f) for f in os.listdir(audio_directory) if f.endswith('.wav')]

results = []
for audio_file_path in audio_files:
    result = transcribe_audio(audio_file_path)
    results.append(result)

# Convert results to a DataFrame and save to CSV
df = pd.DataFrame(results)
df.to_csv("transcriptions.csv", index=False)
