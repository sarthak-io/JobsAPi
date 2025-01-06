from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

def get_video_transcript(video_id):
    try:
        # Fetch the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Extract only the text (without timestamps)
        transcript_text = "\n".join([entry['text'] for entry in transcript])
        
        return transcript_text

    except Exception as e:
        return str(e)

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    data = request.get_json()
    
    # Extract video ID from request
    video_id = data.get('video_id')
    
    if not video_id:
        return jsonify({'error': 'Video ID is required'}), 400

    # Get the transcript
    transcript = get_video_transcript(video_id)

    if 'Error' in transcript:
        return jsonify({'error': transcript}), 400

    return jsonify({'transcript': transcript})

if __name__ == "__main__":
    app.run(debug=True)
