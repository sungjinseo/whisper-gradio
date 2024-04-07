import gradio
import os

# Define the inputs that will be shown in the web GUI
import gradio as gr
import whisper

paramfp16=False # Set to True if you want to use fp16 precision on GPU
def transcribe(audio):
    model = whisper.load_model("base")
    result = model.transcribe(audio,fp16=paramfp16)
    print(result["text"])
    return result["text"]

paramfp16=False # Set to True if you want to use fp16 precision on GPU

def processAudio(audio1,audio2,selModel):

    model = whisper.load_model(selModel)
    if audio1 is None and audio2 is None:
        return "No audio inputs were provided."
    elif audio1 is None:
        # Process only the second audio input
        # Your audio processing code here
        # For this example, we'll just return the second audio input
        audioOk = audio2
    elif audio2 is None:
        # Process only the first audio input
        # Your audio processing code here
        # For this example, we'll just return the first audio input
        audioOk = audio1
    else:
        audioOk = audio1
    result = model.transcribe(audioOk,fp16=paramfp16)
    return result["text"]

demo = gr.Interface(
    processAudio, 
    [
        gr.Audio(sources="microphone", type="filepath", label="Record Audio", show_label=True),
        gr.Audio(sources="upload", type="filepath", label="Upload Audio", show_label=True),
        gr.Dropdown(label="Model", value="base", choices=["tiny", "base", "small", "medium", "large"]),
    ], 
    "textbox",
    title="Whisper(STT) for Phd.Sim",
    description="Record your speech via microphone or upload an audio file and press the Submit button to transcribe it into text. Please, note that the size of the audio file should be less than 25 MB."
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8000)
