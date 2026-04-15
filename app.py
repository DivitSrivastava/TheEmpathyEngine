import gradio as gr
import asyncio
import os
from engine import EmpathyEngine
from voices import VoiceEngine

# Initialize Engines
emotion_engine = EmpathyEngine()
voice_engine = VoiceEngine()

# Archetype Samples
SAMPLES = {
    "Remorse & Grief (Empath) - [RECOMMENDED]": "I'm so deeply sorry for the pain I've caused you, is there anything I can do to make it up to you.",
    "Nervousness & Fear (Vulnerable)": "I think I heard something move in the attic, but I'm too afraid to go up there and check by myself.",
    "Joy & Excitement (Enthusiast)": "Oh my god! I just found out I got the concert tickets! I am so excited to attend it!",
    "Anger & Annoyance (Assertive)": "How dare you talk to me like that ? I am going to report you to the authorities.",
    "Optimism & Admiration (Warm)": "I am so incredibly proud of everything you have achieved this year, your hard work is finally paying off.",
    "Sadness & Disappointment (Heaviness)": "I am missing my friends, it feels very empty without them.",
    "Neutral (Baseline)": "The weather today is partially cloudy with a slight chance of rain in the late evening."
}

async def process_empathy(input_text):
    if not input_text or len(input_text.strip()) < 2:
        return None, "⏳ Status: Awaiting Input...", None, gr.update(interactive=False)
    
    try:
        # 1. Affective Computing Analysis (RoBERTa-base)
        emotion, score, params = emotion_engine.get_vocal_params(input_text)
        
        # 2. Dynamic Intensity Scaling
        # Scales the modulation depth based on model confidence (0.5 to 1.0 multiplier)
        intensity_multiplier = 0.5 + (float(score) * 0.5)
        
        # 3. Neural Audio Synthesis (Edge-TTS)
        filename = "vocal_asset.mp3"
        await voice_engine.generate_audio(input_text, params, emotion, filename)
        
        # 4. Technical Parameter Telemetry Formatting
        telemetry = (
            f"IDENTIFIED_STATE: {emotion.upper()}\n"
            f"CONFIDENCE_SCORE: {score:.4f}\n"
            f"NEURAL_VOICE: {params['voice']}\n"
            f"PITCH_SHIFT: {params['pitch']}\n"
            f"RATE_ADJUST: {params['rate']}\n"
            f"MODULATION_INTENSITY: {intensity_multiplier:.2f}x"
        )
        
        # Return filename for audio player, telemetry for textbox, 
        # score for label, and filename to the download button
        return filename, telemetry, {emotion: float(score)}, gr.update(value=filename, interactive=True)

    except Exception as e:
        return None, f"⚠️ System Error: {str(e)}", None, gr.update(interactive=False)

# --- GRADIO UI LAYOUT ---
darwix_css = """
.gradio-container {background-color: #0f172a; color: white;} 
.gr-button-primary {background: linear-gradient(90deg, #00d2ff, #3a7bd5) !important; border: none !important;}
footer {display: none !important;}
"""

custom_theme = gr.themes.Soft()

with gr.Blocks(theme=custom_theme, css=darwix_css, title="The Empathy Engine") as demo:
    # --- 1. HEADER & DYNAMIC STATUS ---
    gr.Markdown("# 🎙️ The Empathy Engine: Giving AI a Human Voice - By Divit Srivastava")
    status_display = gr.Markdown("⏳ **Status:** Initializing Empathy Engine...")
    gr.Markdown("---")

    # --- 2. ABOUT THE APP ---
    gr.Markdown("""
    ## About This App
    The **Empathy Engine** is a specialized AI application designed to resolve the "Uncanny Valley" in digital speech. It transforms static text into emotionally resonant vocal assets by dynamically modulating speech patterns.

    It offers two distinct pillars of value:
    1. **Empathic Synthesis** 🎙️: Generates high-fidelity audio that shifts its tone, pitch, and speed based on human emotion.
    2. **Vocal Telemetry** 📊: Provides deep technical insights into how emotional intent maps to specific vocal parameters.

    The application leverages the **GoEmotions** dataset (28 granular labels), applying sophisticated **Neural Timbre Switching**, **Prosody Modulation**, and **Contextual Text Massaging**. By injecting **SSML-driven disfluencies** (like micro-pauses and breath resets) and utilizing **Dynamic Intensity Scaling** (where modulation depth is calculated relative to model confidence scores), the system achieves a level of realism beyond standard TTS.

    Developed using **Python 🐍**, the app integrates **Gradio 🎨** for its interactive interface, **RoBERTa-base 🤗** for deep affective computing, and **Microsoft Neural Voices 🔊** via the **Edge-TTS** engine. **This powerful fusion of sentiment intelligence, linguistic pre-processing, and neural synthesis transforms robotic audio into precise, human-centric communication.**
    """)

    # --- 3. HOW TO USE ---
    with gr.Accordion("📖 How to Use", open=False):
        gr.Markdown("""
        **Method 1: Manual Input** ✍️  
        Enter your own custom dialogue or narrative text directly into the **'Source Text Box'**.
        
        **Method 2: Emotional Archetype Library** 📚  
        Select a category from the **'Archetype Selector'** dropdown and click the **'🔄 Use Sample'** button to instantly load pre-configured, high-performance emotional text.
        
        **After Input (using either method):** 1. Press the **'⚡ SYNTHESIZE HUMAN VOICE'** button to initiate the affective mapping and synthesis.
        2. View the **Technical Telemetry** to see the exact neural modulations applied.
        3. Listen to the generated audio. 4. Click **'📥 DOWNLOAD'** to save the generated vocal asset.
        """)

    # --- 4. ENGINE TABS ---
    with gr.Tabs():
        # TAB 1: Core Modulation
        with gr.Tab("Core Modulation Engine"):
            gr.Markdown("### 🔮 Generate Empathic Speech")
            with gr.Row():
                # Inputs
                with gr.Column(scale=1):
                    sample_selector = gr.Dropdown(
                        label="Select Emotional Archetype:", 
                        choices=list(SAMPLES.keys()),
                        interactive=True
                    )
                    sample_btn = gr.Button("🔄 Use Sample")
                    text_in = gr.Textbox(
                        label="Source Text Box (Dialogue Input)", 
                        lines=8, 
                        placeholder="Enter narrative dialogue..."
                    )
                    run_btn = gr.Button("⚡ SYNTHESIZE HUMAN VOICE", variant="primary")

                # Outputs
                with gr.Column(scale=1):
                    audio_out = gr.Audio(label="Synthesized Vocal Asset", type="filepath")
                    telemetry_out = gr.Textbox(label="Vocal Parameter Telemetry (Logic Output)", lines=6)
                    emotion_label = gr.Label(label="Neural Emotion Classification")
                    file_out = gr.DownloadButton("📥 DOWNLOAD VOCAL ASSET", variant="secondary", interactive=False)

            # Execution Logic
            run_btn.click(
                fn=lambda text: asyncio.run(process_empathy(text)),
                inputs=text_in,
                outputs=[audio_out, telemetry_out, emotion_label, file_out]
            )
            sample_btn.click(fn=lambda choice: SAMPLES.get(choice, ""), inputs=sample_selector, outputs=text_in)

        # TAB 2: Methodology
        with gr.Tab("Methodology"):
            gr.Markdown("### 🛠️ Affective Computing Strategy")
            gr.Markdown("""
            - **Timbre Switching:** Swaps between 5 unique neural identities (Ava, Christopher, Libby, Andrew, Emma) to match vocal texture to mood.
            - **Dynamic Intensity Scaling:** Automatically adjusts the depth of Pitch and Rate modulations based on the model's confidence probability.
            - **Disfluency Injection:** Injects 'Neural Triggers' (hesitations and breaths) using SSML to mimic natural human cardiac-vocal patterns.
            """)

    # --- 5. FOOTER ---
    gr.Markdown("""
    ---
    *Developed by **Divit Srivastava** using **Python** 🐍, **Hugging Face Transformers** 🤗 (for emotion extraction), **RoBERTa-base** 🧠 (for affective computing), **Edge-TTS** 🔊 (for neural synthesis), **Gradio** 🎨 (for UI), and **Microsoft Neural Voices** 🎙️ (for human-centric vocal delivery).*
    """)

    # Dynamic status update
    demo.load(fn=lambda: "✅ **Status:** Empathy Engine Operational", outputs=status_display)

if __name__ == "__main__":
    demo.launch()
