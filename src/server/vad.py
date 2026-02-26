"""
Voice Activity Detection module.
"""

from typing import Optional
import numpy as np
from loguru import logger


class VoiceActivityDetector:
    """Voice Activity Detection."""
    
    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load VAD model."""
        try:
            import torch
            model, utils = torch.hub.load(
                repo_or_dir='snakers4/silero-vad',
                model='silero_vad',
                force_reload=False,
            )
            self.model = model
            self._get_speech_timestamps = utils[0]
            logger.info("✅ Silero VAD loaded")
        except Exception as e:
            logger.warning(f"VAD not available: {e}")
            self.model = None
    
    def is_speech(self, audio: np.ndarray, sample_rate: int = 16000) -> bool:
        """Check if audio contains speech."""
        if self.model is None:
            return True  # Assume speech if no VAD
        try:
            import torch
            # Silero VAD requires exactly 512 samples at 16kHz (or 256 at 8kHz)
            chunk_size = 512 if sample_rate == 16000 else 256
            audio_tensor = torch.from_numpy(audio.copy()).float()

            # Process in chunk_size windows, speech if any window triggers
            for i in range(0, len(audio_tensor) - chunk_size + 1, chunk_size):
                window = audio_tensor[i:i + chunk_size]
                speech_prob = self.model(window, sample_rate).item()
                if speech_prob > self.threshold:
                    return True
            return False
        except Exception as e:
            logger.error(f"VAD error: {e}")
            return True
