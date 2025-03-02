from google.cloud import videointelligence
from google.oauth2 import service_account

# Path to your service account JSON key file
key_path = "D:\\python_source\\video_api\\able-imprint-451305-r3-6592ed14f7c9.json"

# Load credentials from the JSON key file
credentials = service_account.Credentials.from_service_account_file(key_path)

# Create the Video Intelligence client with explicit credentials
client = videointelligence.VideoIntelligenceServiceClient(credentials=credentials)

def label_detection(video_uri, video_name):
    operation = client.annotate_video(
        input_uri=video_uri,
        features=[videointelligence.Feature.LABEL_DETECTION],
    )

    print(f"Processing '{video_name}' for label detection...")
    result = operation.result(timeout=180)

    annotation_result = result.annotation_results[0]

    print("Label detection results:")
    for label_annotation in annotation_result.segment_label_annotations:
        description = label_annotation.entity.description
        for segment in label_annotation.segments:
            start_time = segment.segment.start_time_offset.total_seconds()
            end_time = segment.segment.end_time_offset.total_seconds()
            confidence = segment.confidence
            print(
                f"Label: {description}, "
                f"Segment: {start_time}.{start_time}, "
                f"to {end_time}.{end_time}, "
                f"Confidence: {confidence:.2f}"
            )


def explicit_content_detection(video_uri, video_name):
    operation = client.annotate_video(
        input_uri=video_uri,
        features=[videointelligence.Feature.EXPLICIT_CONTENT_DETECTION],
    )

    print(f"Processing '{video_name}' for explicit content detection...")
    result = operation.result(timeout=300)

    annotation_result = result.annotation_results[0]

    print("Explicit content detection results:")
    for frame in annotation_result.explicit_annotation.frames:
        time_offset = frame.time_offset.total_seconds()
        likelihood = videointelligence.Likelihood(frame.pornography_likelihood).name
        print(f"Time: {time_offset:.2f}s, Likelihood: {likelihood}")

def shot_change_detection(video_uri, video_name):
    operation = client.annotate_video(
        input_uri=video_uri,
        features=[videointelligence.Feature.SHOT_CHANGE_DETECTION],
    )

    print(f"Processing {video_name} for shot change detection...")
    result = operation.result(timeout=300)

    annotation_result = result.annotation_results[0]

    print("Shot change detection results:")
    for shot in annotation_result.shot_annotations:
        start_time = shot.start_time_offset.total_seconds()
        end_time = shot.end_time_offset.total_seconds()
        print(f"Shot from {start_time:.2f}s to {end_time:.2f}s")

    
def speech_transcription(video_uri, video_name, language="en-US"):
    operation = client.annotate_video(
        input_uri=video_uri,
        features=[videointelligence.Feature.SPEECH_TRANSCRIPTION],
        video_context=videointelligence.VideoContext(
            speech_transcription_config=videointelligence.SpeechTranscriptionConfig(
                language_code=language,
                enable_automatic_punctuation=True  # Adds commas, periods, etc.
            )
        ),
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
    gcs_uri = "gs://my-video-bucket-lab/Rainbow Dash eating dirt.mp4"
    videos = [
        {"name": "CAPYBARA FAMILY", "url": "gs://my-video-bucket-lab/A Capybara Family's Day at Play - Deadly Game.mp4"},
        {"name": "RAINBOW DASH EATS DIRT", "url": "gs://my-video-bucket-lab/Rainbow Dash eating dirt.mp4"},
        {"name": "USYK-FURY HIGHLIGHTS", "url": "gs://my-video-bucket-lab/UNDISPUTED CHAMPION CROWNED _ Tyson Fury vs. Oleksandr Usyk Fight Highlights (Ring of Fire).mp4"},
        {"name": "OUTDOOR BOYS LAWYER AD", "url": "gs://my-video-bucket-lab/Virginia Traffic Attorney Luke J Nichols.mov.mp4"},
        {"name": "METALLICA MUSIC VIDEO", "url": "gs://my-video-bucket-lab/Metallica_ Enter Sandman (Official Music Video).mp4"}
    ]

    print("------------------------------LABEL DETECTION----------------------------------")
    for video in videos:
        label_detection(video["url"], video["name"])
    print()

    print("------------------------------EXPLICIT CONTENT----------------------------------")
    for video in videos:
        explicit_content_detection(video["url"], video["name"])
    print()
    
    print("------------------------------SHOT CHANGE---------------------------------------")
    for video in videos:
        shot_change_detection(video["url"], video["name"])
    print()
    

    print("------------------------------SPEECH TRANSCRIPTION------------------------------")
    for video in videos:
        speech_transcription(video["url"], video["name"])
    print()
    