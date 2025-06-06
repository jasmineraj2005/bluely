import whisper
import os
import librosa
import soundfile as sf


def transcribe_audio(audio_file_path, model):
    """Transcribes an audio file using Whisper."""
    try:
        # Load audio using librosa, which handles various formats better
        audio, sr = librosa.load(audio_file_path, sr=16000)  # Whisper expects 16kHz
        print(f"Audio loaded successfully. Sample rate: {sr}")

        # Convert to mono if it's stereo
        if len(audio.shape) > 1:
            audio = librosa.to_mono(audio)

        # Ensure the data type is float32
        audio = audio.astype("float32")

        print("Transcribing...")
        result = model.transcribe(audio)
        return result["text"]

    except Exception as e:
        print(f"Error during transcription: {e}")
        return None


def main():
    """Main function to transcribe an audio file and print the transcript."""
    audio_file = "/Users/jasminebaldevraj/Desktop/bluely_voiceAI/bluely/Bluely.mp3"  
    model_name = "medium" 

    try:
        model = whisper.load_model(model_name)
        print(f"Model '{model_name}' loaded successfully.")

        transcript = transcribe_audio(audio_file, model)

        if transcript:
            print("\nTranscription:\n")
            print(transcript)
        else:
            print("Transcription failed.")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
