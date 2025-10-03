import pyaudio
import wave
import numpy as np
import threading
import time
from typing import Optional, Callable
from config import Config

class AudioCapture:
    """Real-time audio capture using PyAudio"""
    
    def __init__(self, sample_rate: int = None, chunk_size: int = None):
        self.sample_rate = sample_rate or Config.SAMPLE_RATE
        self.chunk_size = chunk_size or Config.CHUNK_SIZE
        self.format = pyaudio.paInt16
        self.channels = 1  # Mono audio
        
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.is_recording = False
        self.recording_thread = None
        
        # Single latest file approach
        self.latest_audio_file = None
        self.lock = threading.Lock()
        
        # Voice activity detection
        self.silence_threshold = 100  # Lower threshold for better sensitivity
        self.silence_duration = 1.0  # seconds of silence before stopping
        self.min_recording_duration = 0.5  # minimum recording duration
        
        # Speech detection parameters
        self.speech_threshold = 150  # Minimum volume to consider as speech
        self.min_speech_duration = 0.3  # Minimum duration of speech to process
        self.max_background_noise = 100  # Maximum volume for background noise
        
    def start_recording(self, callback: Optional[Callable] = None):
        """Start recording audio in a separate thread"""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.recording_thread = threading.Thread(
            target=self._record_audio, 
            args=(callback,)
        )
        self.recording_thread.daemon = True
        self.recording_thread.start()
        
    def stop_recording(self):
        """Stop recording audio"""
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join(timeout=2.0)
            
    def _record_audio(self, callback: Optional[Callable] = None):
        """Internal method to record audio continuously"""
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                stream_callback=self._audio_callback if callback else None
            )
            
            if not callback:
                # Manual recording mode
                self._manual_recording()
            else:
                # Callback mode
                self.stream.start_stream()
                while self.is_recording:
                    time.sleep(0.1)
                    
        except Exception as e:
            print(f"Error in audio recording: {e}")
        finally:
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                
    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback for real-time audio processing"""
        if self.is_recording:
            # Store audio data for processing
            pass
        return (in_data, pyaudio.paContinue)
        
    def _manual_recording(self):
        """Manual recording with voice activity detection"""
        frames = []
        silence_start = None
        recording_start = None
        
        while self.is_recording:
            try:
                data = self.stream.read(self.chunk_size, exception_on_overflow=False)
                frames.append(data)
                
                # Convert to numpy array for analysis
                audio_data = np.frombuffer(data, dtype=np.int16)
                # Calculate volume with error handling
                if len(audio_data) > 0:
                    volume = np.sqrt(np.mean(audio_data.astype(np.float64)**2))
                    if np.isnan(volume) or np.isinf(volume):
                        volume = 0.0
                else:
                    volume = 0.0
                
                current_time = time.time()
                
                if volume > self.silence_threshold:
                    # Voice detected
                    if recording_start is None:
                        recording_start = current_time
                        print(f"🎤 Voice detected! Volume: {volume:.1f}")
                    silence_start = None
                else:
                    # Silence detected
                    if silence_start is None:
                        silence_start = current_time
                    elif recording_start and (current_time - silence_start) > self.silence_duration:
                        # End of speech detected
                        recording_duration = current_time - recording_start
                        if recording_duration >= self.min_recording_duration:
                            # Check if this was actual speech or just background noise
                            if self._is_actual_speech(frames):
                                print(f"💾 Saving speech audio chunk ({recording_duration:.1f}s)")
                                self._save_audio_chunk(frames)
                            else:
                                print(f"🔇 Ignoring background noise ({recording_duration:.1f}s)")
                        frames = []
                        recording_start = None
                        silence_start = None
                        
            except Exception as e:
                print(f"Error in manual recording: {e}")
                break
                
    def _is_actual_speech(self, frames):
        """Analyze audio frames to determine if they contain actual speech"""
        try:
            if not frames:
                return False
                
            # Combine all frames
            audio_data = b''.join(frames)
            audio_array = np.frombuffer(audio_data, dtype=np.int16)
            
            if len(audio_array) == 0:
                return False
            
            # Calculate various audio characteristics
            volume = np.sqrt(np.mean(audio_array.astype(np.float64)**2))
            if np.isnan(volume) or np.isinf(volume):
                volume = 0.0
            
            # Check if volume is above speech threshold
            if volume < self.speech_threshold:
                return False
            
            # Calculate dynamic range (difference between max and min)
            dynamic_range = np.max(audio_array) - np.min(audio_array)
            
            # Calculate zero crossing rate (indicates speech vs noise)
            zero_crossings = np.sum(np.diff(np.sign(audio_array)) != 0)
            zero_crossing_rate = zero_crossings / len(audio_array)
            
            # Speech typically has:
            # - Higher volume than background noise
            # - Higher dynamic range
            # - Moderate zero crossing rate (not too high like noise, not too low like silence)
            
            is_speech = (
                volume > self.speech_threshold and
                dynamic_range > 1000 and  # Minimum dynamic range for speech
                0.01 < zero_crossing_rate < 0.3  # Zero crossing rate typical of speech
            )
            
            return is_speech
            
        except Exception as e:
            print(f"Error analyzing speech: {e}")
            return False
    
    def _save_audio_chunk(self, frames):
        """Save audio chunk, replacing the previous one"""
        timestamp = int(time.time() * 1000)
        filename = f"temp_audio_{timestamp}.wav"
        
        try:
            with self.lock:
                # Delete old file if it exists
                if self.latest_audio_file:
                    try:
                        import os
                        os.unlink(self.latest_audio_file)
                        print(f"🗑️ Deleted old audio: {self.latest_audio_file}")
                    except:
                        pass
                
                # Save new file
                with wave.open(filename, 'wb') as wf:
                    wf.setnchannels(self.channels)
                    wf.setsampwidth(self.audio.get_sample_size(self.format))
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(b''.join(frames))
                    
                # Update latest file
                self.latest_audio_file = filename
                print(f"💾 Saved new audio: {filename}")
                
        except Exception as e:
            print(f"Error saving audio chunk: {e}")
            
    def get_latest_audio_file(self) -> Optional[str]:
        """Get the latest audio file"""
        with self.lock:
            return self.latest_audio_file
            
    def clear_latest_audio(self):
        """Clear the latest audio file"""
        with self.lock:
            if self.latest_audio_file:
                try:
                    import os
                    os.unlink(self.latest_audio_file)
                except:
                    pass
                self.latest_audio_file = None
            
    def cleanup(self):
        """Clean up resources"""
        self.stop_recording()
        if self.audio:
            self.audio.terminate()
            
    def __enter__(self):
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
