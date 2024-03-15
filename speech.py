from openai import OpenAI
import pyaudio
import wave
import os
import keyboard
from key import API_KEY

# Set up OpenAI API key
client = OpenAI(api_key=API_KEY)

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
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, language="ta" )

    # Print the transcribed text
    print(transcript.text )

    # Remove the temporary WAV file
    os.remove("temp.wav")

except KeyboardInterrupt:
    pass

# Stop recording and release resources
stream.stop_stream()
stream.close()
audio.terminate()