from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import yt_dlp
import os
import assemblyai as aai
from google import genai

# Create your views here.

@login_required
def user_index(request):
    return render(request, 'index.html')

@csrf_exempt
def generate_blog(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            yt_link = data['link']
        except (json.JSONDecodeError, KeyError):
            return JsonResponse({'error': 'Invalid data sent'}, status=400)
        
        # 1. Download the file locally using your fresh, unblocked Hotspot/VPN IP
        audio_path = download_audio_locally(yt_link)
        if not audio_path or not os.path.exists(audio_path):
            return JsonResponse({'error': 'Failed to download audio. Check your Hotspot/VPN connection.'}, status=500)
        
        title = "AI Generated Blog Article"

        # 2. Upload and transcribe the physical local file (Bypasses all YouTube URL blocks!)
        transcription = get_transcript_from_local_file(audio_path)
        
        # 3. Clean up and delete the local file immediately so your Mac doesn't save media files
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        if not transcription:
            return JsonResponse({'error': 'Failed to transcribe audio file'}, status=500)
        
        # 4. Hand off transcript text to Gemini
        blog_content = generate_blog_content(transcription)
        if not blog_content:
            return JsonResponse({'error': 'Failed to generate blog content'}, status=500)
        
        return JsonResponse({'title': title, 'content': blog_content})

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def download_audio_locally(link):
    try:
        # Clear any old stuck audio files first
        if os.path.exists('audio.mp3'):
            os.remove('audio.mp3')
            
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'audio.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return 'audio.mp3'
    except Exception as e:
        print(f"Local download error: {str(e)}")
        return None

def get_transcript_from_local_file(file_path):
    aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    transcriber = aai.Transcriber()
    try:
        # Uploading the real file directly avoids the HTML transcoding bug completely
        config = aai.TranscriptionConfig(speech_models=["universal-2"])  # speech_models is a list of strings
        transcript = transcriber.transcribe(file_path, config=config)
        if transcript.error:
            print(f"AssemblyAI Error: {transcript.error}")
            return None
        return transcript.text
    except Exception as e:
        print(f"AssemblyAI upload exception: {str(e)}")
        return None

def generate_blog_content(transcription):
    client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    prompt = f"Based on the following transcript, write a short blog article. Use bullet points. Max 300 words. No fluff, straight to the point:\n\n{transcription}\n\nArticle:"

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",  # Confirmed available model as of May 2026
            contents=prompt,
        )
        return response.text
    except Exception as e:
        print(f"Gemini generation error: {str(e)}")
        return None

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'Login.html', {'error_message': "Invalid username or password"})
    return render(request, 'Login.html')

def user_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repeatPassword = request.POST['repeatpassword']
        if password == repeatPassword:
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                return render(request, 'signup.html', {'error_message': "Username already exists"}) 
        else:
            return render(request, 'signup.html', {'error_message': "Passwords do not match"})
    return render(request, 'signup.html')

def user_logout(request):
    logout(request)
    return redirect('login')