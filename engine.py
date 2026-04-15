from transformers import pipeline
class EmpathyEngine:
    def __init__(self):
        # Loading a model that detects 28 granular emotions (GoEmotions)
        # This runs locally on your CPU
        print("Loading Emotion Engine... please wait.")
        self.classifier = pipeline(
            "text-classification", 
            model="SamLowe/roberta-base-go_emotions", 
            top_k=None
        )

    def get_vocal_params(self, text):
        results = self.classifier(text)[0]
        
        # Top detected emotion
        top_emotion = results[0]['label']
        score = results[0]['score'] # This is 'Intensity' (0.0 to 1.0)

        # Mapping: Pitch, Rate, Volume
        # Logic: Base Change * Intensity Score
        # engine.py update
        params = {
        # THE ENTHUSIASTS
        "joy": {"voice": "en-US-AvaNeural", "pitch": "+10Hz", "rate": "+15%", "vol": "+10%"},
        "excitement": {"voice": "en-US-AvaNeural", "pitch": "+15Hz", "rate": "+25%", "vol": "+15%"},
        
        # THE ASSERTIVES
        "anger": {"voice": "en-US-ChristopherNeural", "pitch": "-6Hz", "rate": "+20%", "vol": "+20%"},
        "annoyance": {"voice": "en-US-ChristopherNeural", "pitch": "-2Hz", "rate": "+12%", "vol": "+10%"},
        
        # THE EMPATHS
        "sadness": {"voice": "en-US-AndrewNeural", "pitch": "-10Hz", "rate": "-20%", "vol": "-15%"},
        "remorse": {"voice": "en-GB-LibbyNeural", "pitch": "-12Hz", "rate": "-25%", "vol": "-15%"},
        "disappointment": {"voice": "en-GB-LibbyNeural", "pitch": "-5Hz", "rate": "-15%", "vol": "-8%"},
        
        # THE WARM/PROFESSIONAL
        "optimism": {"voice": "en-US-EmmaNeural", "pitch": "+5Hz", "rate": "+8%", "vol": "+5%"},
        "admiration": {"voice": "en-US-EmmaNeural", "pitch": "+3Hz", "rate": "+5%", "vol": "+2%"},
        
        # THE UNCERTAIN
        "fear": {"voice": "en-US-AndrewNeural", "pitch": "+12Hz", "rate": "+15%", "vol": "-5%"},
        "nervousness": {"voice": "en-US-AndrewNeural", "pitch": "+10Hz", "rate": "+12%", "vol": "-5%"},
        
        # THE BASELINE
        "neutral": {"voice": "en-US-AndrewNeural", "pitch": "+1Hz", "rate": "+1%", "vol": "+0%"}
        }

        # Default to neutral if emotion isn't in our map
        mapping = params.get(top_emotion, params["neutral"])
        
        return top_emotion, score, mapping
