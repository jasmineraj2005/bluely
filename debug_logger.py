#!/usr/bin/env python3
"""
Debug Logger for STT-TTS System
Logs all transcriptions and responses for debugging
"""

import os
import json
import time
from datetime import datetime
from typing import Optional, Dict, Any

class DebugLogger:
    """Debug logger for transcript and response tracking"""
    
    def __init__(self, log_file: str = "debug_log.json"):
        self.log_file = log_file
        self.session_id = int(time.time())
        self.logs = []
        
    def log_audio_capture(self, audio_file: str, volume: float = None):
        """Log audio capture event"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event": "audio_capture",
            "audio_file": audio_file,
            "volume": volume,
            "file_size": os.path.getsize(audio_file) if os.path.exists(audio_file) else 0
        }
        self.logs.append(log_entry)
        print(f"🎤 DEBUG: Audio captured - {audio_file} (Volume: {volume})")
        
    def log_transcription(self, audio_file: str, transcribed_text: str, confidence: float = None):
        """Log transcription results"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event": "transcription",
            "audio_file": audio_file,
            "transcribed_text": transcribed_text,
            "text_length": len(transcribed_text),
            "confidence": confidence,
            "is_empty": not transcribed_text.strip()
        }
        self.logs.append(log_entry)
        print(f"🗣️ DEBUG: Transcription - '{transcribed_text}' (Length: {len(transcribed_text)})")
        
    def log_ai_response(self, input_text: str, ai_response: str, intent: str = None):
        """Log AI processing results"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event": "ai_response",
            "input_text": input_text,
            "ai_response": ai_response,
            "intent": intent,
            "response_length": len(ai_response)
        }
        self.logs.append(log_entry)
        print(f"🤖 DEBUG: AI Response - '{ai_response}' (Intent: {intent})")
        
    def log_tts_output(self, text: str, voice_id: str = None, success: bool = True):
        """Log TTS output"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event": "tts_output",
            "text": text,
            "voice_id": voice_id,
            "success": success
        }
        self.logs.append(log_entry)
        print(f"🔊 DEBUG: TTS Output - '{text}' (Success: {success})")
        
    def log_error(self, error_type: str, error_message: str, context: str = None):
        """Log error events"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event": "error",
            "error_type": error_type,
            "error_message": error_message,
            "context": context
        }
        self.logs.append(log_entry)
        print(f"❌ DEBUG: Error - {error_type}: {error_message}")
        
    def log_system_event(self, event: str, details: Dict[str, Any] = None):
        """Log system events"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event": "system",
            "system_event": event,
            "details": details or {}
        }
        self.logs.append(log_entry)
        print(f"⚙️ DEBUG: System - {event}")
        
    def save_logs(self):
        """Save all logs to file"""
        try:
            with open(self.log_file, 'w') as f:
                json.dump(self.logs, f, indent=2)
            print(f"💾 DEBUG: Logs saved to {self.log_file}")
        except Exception as e:
            print(f"❌ DEBUG: Failed to save logs: {e}")
            
    def get_recent_logs(self, count: int = 10) -> list:
        """Get recent log entries"""
        return self.logs[-count:] if self.logs else []
        
    def clear_logs(self):
        """Clear all logs"""
        self.logs = []
        print("🗑️ DEBUG: Logs cleared")

# Global debug logger instance
debug_logger = DebugLogger()
