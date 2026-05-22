# AI Blog Generator 🤖

A full stack web app that converts any YouTube video into a professional blog article instantly using AI.

## 💡 How It Works
1. Paste any YouTube link into the app
2. yt-dlp downloads the audio from the video
3. AssemblyAI transcribes the audio into text
4. Google Gemini generates a professional blog article from the transcript
5. Blog article is displayed instantly on the page

## 🛠 Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Django (Python)
- **Database:** PostgreSQL
- **Audio Download:** yt-dlp
- **AI Transcription:** AssemblyAI
- **AI Blog Generation:** Google Gemini

## ⚙️ Setup & Installation

Requirements: Python 3.11+

# Clone the repo
git clone https://github.com/Cheabea/ai-blog-generator.git
cd ai-blog-generator

# Install dependencies
pip3.11 install django yt-dlp assemblyai google-genai psycopg2-binary

# Add your API keys in .env file
ASSEMBLYAI_API_KEY=your_key_here
GEMINI_API_KEY=your_key_here

# Run the server
python3.11 manage.py runserver --settings=ai_blog_app.settings

## ✨ Features
- YouTube audio extraction
- AI speech-to-text transcription
- AI blog article generation
- User authentication (login/signup)
- Clean minimal frontend
- PostgreSQL database

## 👨‍💻 Built By
Ayush — https://github.com/Cheabea
Built from scratch in 1 week
