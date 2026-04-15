import asyncio
import edge_tts
import re

class VoiceEngine:
    def __init__(self):
        # Fallback voice
        self.default_voice = "en-US-AndrewNeural" 

    def _massage_text(self, text, emotion):
        """
        Directs the AI's 'performance' by injecting punctuation that triggers 
        neural breathing, hesitations, and natural inflections.
        """
        text = text.strip().rstrip('.')

        # THE REMORSE/SADNESS LOGIC: Simulates 'heavy' breathing and hesitation
        if emotion in ["remorse", "sadness", "grief", "disappointment"]:
            # Start with an ellipse to trigger a soft 'intake of breath'
            text = f"... {text}"
            # Use a semicolon + space to force a reset of the vocal rhythm
            if "," in text:
                text = text.replace(",", "... ;")
            else:
                # If no comma, force a mid-sentence break
                words = text.split()
                if len(words) > 4:
                    words.insert(len(words)//2, "... ;")
                    text = " ".join(words)
            text += "..."

        # THE EXCITEMENT LOGIC: High energy, zero-pause 'rushing'
        elif emotion in ["excitement", "joy"]:
        # Instead of stripping everything, replace commas with '!' 
        # to keep the pitch high, and add '...' for a quick intake of breath.
            text = text.replace(",", "!")
            words = text.split()
            if len(words) > 6:
                # Inject a 'gasp' (ellipse) near the end to simulate being out of breath
                words.insert(-3, "...") 
                text = " ".join(words)
            text += "!!!"

        # THE ANGER LOGIC
        elif emotion in ["anger", "annoyance"]:
            text = text.replace("--", "").replace("...", "")
            # Neural engines interpret '!' as a pitch-raise (happy/shouting), 
            # while '.' creates a downward, serious inflection (cold/angry).
            text = text.strip("!").strip(".") + "."

        # THE NERVOUSNESS LOGIC
        elif emotion in ["nervousness", "fear", "confusion"]:
            # High frequency of rising tones and trailing thoughts
            if "," in text:
                text = text.replace(",", "? ...")
            if not text.endswith("?"):
                text += "? ..."

        return text

    async def generate_audio(self, text, params, emotion, output_path="speech_output.mp3"):
        # Select voice identity based on emotion mapping
        voice = params.get("voice", self.default_voice)
        rate = params.get("rate", "+0%")
        pitch = params.get("pitch", "+0Hz")
        volume = params.get("vol", "+0%")

        # Apply human-like text massaging
        massaged_text = self._massage_text(text, emotion)

        # Create the synthesis object
        communicate = edge_tts.Communicate(
            massaged_text, 
            voice, 
            rate=rate, 
            pitch=pitch, 
            volume=volume
        )
        
        await communicate.save(output_path)
        return output_path
