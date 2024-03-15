import random
import sys
import pyaudio
import wave
import os
import keyboard
from openai import OpenAI

def display_random_tamil_word(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = file.read().splitlines()
        random_word = random.choice(words)
        return random_word

def check_pronunciation(text):
    client = OpenAI(api_key="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")
    
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Start recording audio
    stream = audio.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024)

    print("Start speaking...")
    frames = []
    try:
        while True:
            data = stream.read(1024)
            frames.append(data)

            # Check for a pause in the audio stream
            if len(data) == 0:
                break
                
            if keyboard.is_pressed(' '):
                print("Recording stopped.")
                break

        # Save the recorded audio to a temporary WAV file
        with wave.open("temp.wav", "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wav_file.setframerate(16000)
            wav_file.writeframes(b''.join(frames))

        # Open the temporary WAV file and transcribe using the Whisper model
        with open("temp.wav", "rb") as audio_file:
            transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, language="ta")

        # Remove the temporary WAV file
        os.remove("temp.wav")
        
        # Stop recording and release resources
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # Return True if the text matches the transcribed text, False otherwise
        return text == transcript.text

    except KeyboardInterrupt:
        pass

    # Stop recording and release resources
    stream.stop_stream()
    stream.close()
    audio.terminate()

# Set encoding to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Example usage:
file_path = 'words.txt'  # Update with the path to your text file
random_tamil_word = display_random_tamil_word(file_path)
print("Randomly selected Tamil word:", random_tamil_word)

# Check pronunciation of the randomly generated word
pronunciation_correct = check_pronunciation(random_tamil_word)

if pronunciation_correct:
    print("The pronunciation of the word is correct.")
else:
    print("The pronunciation of the word is incorrect.")