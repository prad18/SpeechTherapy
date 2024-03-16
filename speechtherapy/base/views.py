from django.shortcuts import render , redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import traceback
from openai import OpenAI
import wave
import os
from fuzzywuzzy import fuzz
import random
from .key import API_KEY
import os

# Create your views here.

def loginPage(request):
    page = 'login'
    if request.method=="POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
             messages.error(request, "User doesn't exist!")
        user = authenticate(request,username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('letters')
        else:
            messages.error(request, "Username or Password is incorrect!")

    context={'page':page}
    return render(request, 'login.html', context)

def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            username = form.cleaned_data.get('username')
            return redirect('letters')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")


    return render(request, 'login.html', {'form': form})

def logoutUser(request):
    logout(request)
    return redirect('home')


def register(request):
    return render(request,'register.html')

@login_required(login_url='home')
def letters(request):
    return render(request,'base/letters.html')

client = OpenAI(api_key=API_KEY)

def learn(request):
    if request.method == 'GET':
        # Load the Tamil words from a file
        with open('words.txt', 'r', encoding='utf-8') as file:
            words = file.read().splitlines()

        # Select a random Tamil word
        random_tamil_word = random.choice(words)

        context = {
            'random_tamil_word': random_tamil_word,
        }
        return render(request, 'base/learn.html', context)

    elif request.method == 'POST':
        # Receive the audio file and the word from the client
        audio_file = request.FILES.get('audio_file')
        word = request.POST.get('word')

        # Save the audio file temporarily
        temp_file_path = 'temp.wav'
        with open(temp_file_path, 'wb+') as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)

        try:
            # Transcribe the audio using OpenAI Whisper
            with open(temp_file_path, 'rb') as audio_file:
                transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, language="ta")
            
            # Use fuzzy string matching to compare the text and transcribed text
            similarity_score = fuzz.ratio(word, transcript.text)

            # Remove the temporary file if it exists
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)

            # Return the similarity score as JSON response
            return JsonResponse({'similarity_score': similarity_score})

        except Exception as e:
            # Remove the temporary file if it exists and an error occurs
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            # If an error occurs, return error message as JSON response
            return JsonResponse({'error': str(e)}, status=500)
        
    # Return a 400 Bad Request response if the request method is not supported
    return JsonResponse({'error': 'Bad request'}, status=400)