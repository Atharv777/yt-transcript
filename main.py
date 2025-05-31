from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, CouldNotRetrieveTranscript

app = Flask(__name__)
CORS(app)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    languages = request.args.getlist('lang') or ['en', 'hi']

    if not video_id:
        return jsonify({"error": "Missing video_id parameter"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
        return jsonify(transcript)

    except TranscriptsDisabled as e:
        return jsonify({"error": "Transcripts are disabled for this video", "cause" : e}), 403

    except CouldNotRetrieveTranscript as e:
        return jsonify({"error": "Could not retrieve transcript for this video", "cause" : e}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
