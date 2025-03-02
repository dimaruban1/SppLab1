from google.cloud import videointelligence
from google.oauth2 import service_account

key_path = "D:\\python_source\\video_api\\able-imprint-451305-r3-6592ed14f7c9.json"

credentials = service_account.Credentials.from_service_account_file(key_path)

client = videointelligence.VideoIntelligenceServiceClient(credentials=credentials)

def speech_transcription(video_uri, video_name, language="en-US"):
    operation = client.annotate_video(
        request={
            "input_uri": video_uri,
            "features": [videointelligence.Feature.SPEECH_TRANSCRIPTION],
            "video_context": videointelligence.VideoContext(
                speech_transcription_config=videointelligence.SpeechTranscriptionConfig(
                    language_code=language,
                    enable_automatic_punctuation=True
                )
            ),
        }
    )

    print(f"Processing '{video_name}' for speech transcription...")
    result = operation.result(timeout=600)

    annotation_result = result.annotation_results[0]

    print("\nSpeech Transcription Results:")
    for speech_transcription in annotation_result.speech_transcriptions:
        for alternative in speech_transcription.alternatives:
            print(f"Transcript: {alternative.transcript}")
            print(f"Confidence: {alternative.confidence:.2f}\n")


if __name__ == "__main__":
    videos = [
        {"name": "RAINBOW DASH EATS DIRT", "url": "gs://my-video-bucket-lab/Rainbow Dash eating dirt.mp4"},
    ]

    print("------------------------------SPEECH TRANSCRIPTION------------------------------")
    for video in videos:
        speech_transcription(video["url"], video["name"])
    print()
