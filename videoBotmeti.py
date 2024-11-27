import streamlit as st
from moviepy.editor import VideoFileClip, vfx
from moviepy.video.fx.all import margin, rotate, speedx
import numpy as np

st.title("Video Bot App")

# Beispiel: Verarbeitung eines Videos
video_path = "dein_video.mp4"
clip = VideoFileClip(video_path)

# Beispiel für einen einfachen Effekt: Helligkeit ändern
clip = clip.fx(vfx.colorx, 1.2)  # Steigerung der Helligkeit um 20%

# Zeige das Video auf Streamlit an
st.video(clip.ipython_display(), format="video/mp4")

import streamlit as st
from moviepy.editor import VideoFileClip, vfx
from moviepy.video.fx.all import margin, rotate, speedx
import numpy as np

# Funktion: Helligkeit, Kontrast und Sättigung anpassen
def adjust_brightness_contrast_saturation(clip, brightness=0, contrast=0, saturation=1):
    brightness_factor = brightness / 10
    contrast_factor = 1 + (contrast / 10)
    saturation_factor = saturation

    def modify_frame(frame):
        frame = np.clip(frame * contrast_factor + brightness_factor, 0, 255)
        hsv = np.dot(frame, [[0.299, 0.587, 0.114], [-0.147, -0.289, 0.436], [0.615, -0.515, -0.100]])
        hsv[:, :, 1] *= saturation_factor
        return np.clip(hsv, 0, 255)

    return clip.fl_image(modify_frame)

# Funktion: Schwarze Balken hinzufügen
def add_letterbox(clip, height=50):
    return margin(clip, top=height, bottom=height, color=(0, 0, 0))

# Hauptprogramm
st.title("Video-Bot mit Streamlit")
st.write("Bearbeite Videos direkt in einer einfachen Web-App!")

uploaded_file = st.file_uploader("Lade dein Video hoch", type=["mp4", "mov", "avi"])
if uploaded_file:
    st.video(uploaded_file)
    input_video_path = uploaded_file.name

    # Benutzeroptionen
    brightness = st.slider("Helligkeit", -10, 10, 0)
    contrast = st.slider("Kontrast", -10, 10, 0)
    saturation = st.slider("Sättigung", 0.5, 2.0, 1.0)
    angle = st.slider("Drehwinkel", -10, 10, -2)
    speed = st.slider("Geschwindigkeit (Faktor)", 0.5, 1.5, 0.98)
    add_bars = st.checkbox("Kinostreifen hinzufügen", value=True)
    export_fps = st.slider("Export-Framerate (FPS)", 24, 60, 50)

    if st.button("Video bearbeiten"):
        with st.spinner("Video wird bearbeitet..."):
            # Video laden
            clip = VideoFileClip(uploaded_file.name)

            # Effekte anwenden
            clip = adjust_brightness_contrast_saturation(clip, brightness, contrast, saturation)
            if add_bars:
                clip = add_letterbox(clip, height=100)
            clip = rotate(clip, angle=angle)
            clip = speedx(clip, factor=speed)

            # Video exportieren
            output_video_path = "output_video.mp4"
            clip.write_videofile(output_video_path, fps=export_fps)

            st.success("Video erfolgreich bearbeitet!")
            st.video(output_video_path)
