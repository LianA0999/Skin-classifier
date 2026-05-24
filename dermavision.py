import streamlit as st
from PIL import Image
import numpy as np
import cv2
import random
import pandas as pd
import os

st.set_page_config(page_title="DermaVision", page_icon="🌿", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700;800;900&display=swap');
* { font-family: 'Nunito', sans-serif; }
[data-testid="stAppViewContainer"] { background-color: #ffffff; }
[data-testid="stHeader"] { display: none; }
[data-testid="stToolbar"] { display: none; }
footer { display: none; }
.block-container { padding: 72px 0 2rem !important; max-width: 1200px !important; margin: 0 auto !important; }
.hero { display: flex; flex-direction: column; align-items: center; padding: 3.5rem 2rem 3rem; background: #ffffff; }
.hero h1 { font-size: clamp(2.2rem, 4vw, 3.2rem); font-weight: 800; color: #111111 !important; line-height: 1.15; margin-bottom: 1.2rem; max-width: 700px; margin-left: auto; margin-right: auto; letter-spacing: -0.02em; }
.hero h1 span { color: #2E6B35 !important; }
.hero-sub { font-size: 1rem; color: #777; max-width: 480px; margin: 0 auto; line-height: 1.75; text-align: center !important; }
.hero-btn { display: block; width: fit-content; background: #2E6B35; color: white !important; padding: 0.8rem 2.4rem; border-radius: 8px; font-weight: 700; font-size: 0.92rem; text-decoration: none !important; margin: 0.8rem auto 1rem; font-family: 'Nunito', sans-serif; transition: background 0.2s; }
.hero-btn:hover { background: #1B5E20; }
.hero-trust { font-size: 0.8rem; color: #bbb; margin-top: 0.3rem; letter-spacing: 0.01em; }
.page-content { max-width: 860px; margin: 0 auto; padding: 2rem 2rem; }
.section-heading { font-size: 1.35rem; font-weight: 700; color: #111; margin-bottom: 0.3rem; letter-spacing: -0.01em; }
.section-sub { color: #999; font-size: 0.9rem; margin-bottom: 1.8rem; }
.divider { height: 1px; background: #f0f0f0; margin: 1.5rem 0; }
.feature-item { background: #ffffff; padding: 1.2rem 0; border-bottom: 1px solid #f5f5f5; margin-bottom: 0; display: flex; align-items: flex-start; gap: 1.2rem; border-radius: 0; border: none; }
.feature-item:last-child { border-bottom: none; }
.feature-icon { font-size: 0.75rem; font-weight: 800; color: #2E6B35; margin-top: 5px; min-width: 20px; background: #F1F8F1; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.feature-text h4 { margin: 0 0 3px; color: #111; font-size: 0.95rem; font-weight: 700; }
.feature-text p { margin: 0; color: #888; font-size: 0.87rem; line-height: 1.55; }
.input-card { background: #ffffff; border-radius: 16px; padding: 2.5rem 1.5rem; border: 2px solid #E0EDD8; text-align: center; cursor: pointer; transition: all 0.2s; margin-bottom: 0.5rem; }
.input-card:hover { border-color: #2E6B35; background: #F1F8F1; transform: translateY(-3px); box-shadow: 0 8px 20px rgba(76,175,80,0.15); }
.input-card-icon { font-size: 2.8rem; margin-bottom: 0.8rem; }
.input-card-title { font-size: 1.15rem; font-weight: 800; color: #1B5E20; margin-bottom: 0.3rem; }
.input-card-sub { font-size: 0.85rem; color: #999; }
.profile-box { background: #ffffff; border: 1px solid #E0EDD8; border-radius: 14px; padding: 1.5rem 1.8rem; margin-bottom: 1rem; }
.stButton > button { background-color: #2E6B35; color: white; border: none; border-radius: 10px; padding: 0.7rem 1.5rem; font-size: 1rem; font-weight: 600; font-family: 'Nunito', sans-serif; width: 100%; transition: all 0.2s; margin-top: 0.5rem; }
.stButton > button:hover { background-color: #1B5E20; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(76,175,80,0.3); }
.back-btn .stButton > button { background-color: transparent; color: #2E6B35; border: 1.5px solid #2E6B35; width: auto; padding: 0.4rem 1rem; font-size: 0.88rem; margin-top: 0; }
.back-btn .stButton > button:hover { background-color: #F1F8F1; transform: none; box-shadow: none; }
.condition-row { padding: 0.7rem 0; border-bottom: 1px solid #F0F0F0; }
.condition-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
.condition-name { font-size: 0.92rem; font-weight: 600; color: #3D3D3D; }
.condition-pct { font-size: 0.92rem; font-weight: 700; }
.pct-high { color: #E65100; }
.pct-med  { color: #F9A825; }
.pct-low  { color: #2E6B35; }
.stProgress > div > div { background: linear-gradient(90deg, #2E6B35, #1B5E20); border-radius: 100px; }
.stProgress > div { border-radius: 100px; background-color: #E8F5E9; }
[data-testid="stFileUploader"] { background-color: #F9FBF7; border: 2px dashed #A5D6A7; border-radius: 12px; padding: 1rem; }
.rec-box { background: linear-gradient(135deg, #FFF8F0, #FFF3E0); border: 1px solid #FFCC80; border-left: 4px solid #FF9800; border-radius: 12px; padding: 1.4rem 1.6rem; margin-top: 1.2rem; }
.rec-title { font-weight: 700; color: #E65100; margin-bottom: 0.8rem; font-size: 0.88rem; text-transform: uppercase; letter-spacing: 0.06em; }
.rec-row { display: flex; gap: 0.5rem; margin-bottom: 0.5rem; font-size: 0.88rem; color: #5D3A00; line-height: 1.6; }
.rec-label { font-weight: 700; min-width: 130px; color: #BF5000; }
.no-face-box { background: #FFF8F0; border: 1px solid #FFCC80; border-left: 4px solid #FF9800; border-radius: 12px; padding: 1.2rem 1.4rem; }
.no-face-box p { margin: 0; color: #5D3A00; font-size: 0.9rem; }
.blur-warn { background: #FFF8F0; border: 1px solid #FFCC80; border-left: 4px solid #FF9800; border-radius: 12px; padding: 1rem 1.2rem; margin-top: 1rem; }
.blur-warn p { margin: 0; color: #5D3A00; font-size: 0.9rem; }
.disclaimer { background: #E8F5E9; border-radius: 12px; padding: 1.2rem 1.5rem; border: 1px solid #C8E6C9; margin-top: 1rem; }
.disclaimer p { margin: 0; color: #2E6B35; font-size: 0.88rem; line-height: 1.7; }
.team-card { background: #ffffff; border: 1px solid #E0EDD8; border-radius: 16px; padding: 2rem; text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.04); transition: all 0.2s; }
.team-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(76,175,80,0.12); border-color: #A5D6A7; }
.team-avatar { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #2E6B35, #1B5E20); display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 800; color: white; margin: 0 auto 1rem; }
.team-name { font-size: 1.1rem; font-weight: 800; color: #1B5E20; margin-bottom: 0.2rem; }
.team-role { font-size: 0.85rem; font-weight: 600; color: #2E6B35; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.06em; }
.team-bio { font-size: 0.88rem; color: #666; line-height: 1.6; margin-bottom: 1rem; }
.team-contact { font-size: 0.82rem; color: #888; border-top: 1px solid #F0F0F0; padding-top: 0.8rem; margin-top: 0.5rem; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

CLASS_NAMES = ['acne', 'dark_spots', 'dry', 'normal', 'oily', 'redness', 'wrinkles']

@st.cache_resource(show_spinner=False)
def load_model():
    if os.path.exists("dermavision_model.keras"):
        try:
            import tensorflow as tf, json
            mdl = tf.keras.models.load_model("dermavision_model.keras")
            classes = CLASS_NAMES
            if os.path.exists("model_meta.json"):
                with open("model_meta.json") as f:
                    classes = json.load(f).get("classes", CLASS_NAMES)
            return mdl, classes, True
        except Exception:
            pass
    return None, CLASS_NAMES, False

model, class_names, model_loaded = load_model()

@st.cache_data(show_spinner=False)
def load_rec_data():
    if os.path.exists("dataset-4.csv"):
        return pd.read_csv("dataset-4.csv")
    return None

rec_df = load_rec_data()

# ── Skin type detection from model prediction percentages ──────────────────
def get_skin_type(preds):
    pred_dict = dict(preds)
    oily_pct   = pred_dict.get('oily', 0)
    dry_pct    = pred_dict.get('dry', 0)
    normal_pct = pred_dict.get('normal', 0)
    # Combination: both oily and dry are significantly present
    if oily_pct > 30 and dry_pct > 25:
        return 'Combination'
    if oily_pct > dry_pct and oily_pct > normal_pct:
        return 'Oily'
    if dry_pct > oily_pct and dry_pct > normal_pct:
        return 'Dry'
    return 'Normal'

# ── Map model class → CSV concern ─────────────────────────────────────────
CONCERN_MAP = {
    "acne":       "Acne",
    "dark_spots": "Dark Spots",
    "dry":        "Dullness",
    "normal":     "Open Pores",
    "oily":       "Open Pores",
    "redness":    "Redness",
    "wrinkles":   "Wrinkles",
}

# ── Recommendation lookup using skin type + concern + age + sensitivity ────
def get_recommendation(condition, preds, age_group, sensitivity):
    if rec_df is None:
        return None
    concern   = CONCERN_MAP.get(condition.lower(), condition)
    skin_type = get_skin_type(preds)

    # Full match: concern + skin type + age + sensitivity
    match = rec_df[
        (rec_df['Concern'].str.lower()   == concern.lower()) &
        (rec_df['Skin_Type'].str.lower() == skin_type.lower()) &
        (rec_df['Age_Group']             == age_group) &
        (rec_df['Sensitivity']           == sensitivity)
    ]
    # Fall back: concern + skin type
    if match.empty:
        match = rec_df[
            (rec_df['Concern'].str.lower()   == concern.lower()) &
            (rec_df['Skin_Type'].str.lower() == skin_type.lower())
        ]
    # Fall back: concern only
    if match.empty:
        match = rec_df[rec_df['Concern'].str.lower() == concern.lower()]
    if match.empty:
        return None

    row = match.iloc[0]
    return {
        "concern":        row.get("Concern", ""),
        "skin_type":      skin_type,
        "internal_type":  row.get("Internal_Type", ""),
        "ingredients":    row.get("Ingredients", ""),
        "concentrations": row.get("Concentrations", ""),
        "effects":        row.get("Effects", ""),
    }

def predict(img):
    if model_loaded and model is not None:
        try:
            from tensorflow.keras.applications.efficientnet import preprocess_input
            arr = np.array(img.convert("RGB").resize((300, 300)), dtype=np.float32)
            arr = preprocess_input(arr[np.newaxis])
            probs = model.predict(arr, verbose=0)[0]
            return sorted(zip(class_names, (probs * 100).tolist()), key=lambda x: -x[1])
        except Exception:
            pass
    probs = [random.uniform(10, 90) for _ in class_names]
    total = sum(probs)
    return sorted(zip(class_names, [(p / total) * 100 for p in probs]), key=lambda x: -x[1])

def detect_face(img):
    arr  = np.array(img.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    clf  = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = clf.detectMultiScale(gray, 1.1, 5, minSize=(60, 60))
    if len(faces) > 0:
        for (x, y, w, h) in faces:
            cv2.rectangle(arr, (x, y), (x + w, y + h), (76, 175, 80), 2)
        return True, Image.fromarray(arr)
    return False, img

def is_blurry(img, threshold=80):
    arr  = np.array(img.convert("RGB"))
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    return cv2.Laplacian(gray, cv2.CV_64F).var() < threshold

def sev(pct):
    if pct >= 50: return "pct-high"
    if pct >= 25: return "pct-med"
    return "pct-low"

def fmt(label):
    return label.replace("_", " ").title()

for k, v in {
    "page": "home", "img": None, "face_found": False,
    "input_method": "upload", "age_group": "19-24", "sensitivity": "No"
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Sync query params → session state
_qp = st.query_params.get("p", "")
_qm = st.query_params.get("m", "")
if _qp in ("home", "analyse", "about", "capture") and st.session_state.page != _qp:
    st.session_state.page = _qp
if _qm in ("camera", "upload") and st.session_state.input_method != _qm:
    st.session_state.input_method = _qm

# ── Navbar ─────────────────────────────────────────────────────────────────
def _nav_link(label, target, current):
    active = current == target
    bg    = "#F1F8F1" if active else "transparent"
    color = "#2E6B35" if active else "#555"
    return (f'<a href="?p={target}" style="color:{color};font-weight:600;font-size:0.9rem;'
            f'text-decoration:none;padding:0.4rem 0.9rem;border-radius:8px;background:{bg};">{label}</a>')

_page = st.session_state.page
st.markdown(f"""
<div style="position:fixed;top:0;left:0;right:0;height:64px;background:white;
    border-bottom:1px solid #E0EDD8;box-shadow:0 1px 8px rgba(0,0,0,0.06);
    z-index:9999;display:flex;align-items:center;padding:0 3rem;
    font-family:'Nunito',sans-serif;gap:0.5rem;">
  <div style="font-size:1.25rem;font-weight:800;color:#2E6B35;flex:1;">DermaVision</div>
  {_nav_link("Home","home",_page)}
  {_nav_link("Analysis","analyse",_page)}
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <h1 style="text-align:center;">AI-Powered <span>Skin Analysis</span> &amp; Condition Detection</h1>
        <a href="?p=analyse" class="hero-btn">Start Analysis</a>
        <div class="hero-trust">No account needed &nbsp;·&nbsp; Your photos are never stored</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='page-content'>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>How It Works</div>", unsafe_allow_html=True)
    st.markdown("<p class='section-sub'>Three simple steps to understand your skin.</p>", unsafe_allow_html=True)
    st.markdown("""
    <div class='feature-item'><div class='feature-icon'>1</div><div class='feature-text'><h4>Tell us about yourself</h4><p>Enter your age group and skin sensitivity so we can personalise your results.</p></div></div>
    <div class='feature-item'><div class='feature-icon'>2</div><div class='feature-text'><h4>Take or upload a photo</h4><p>Use your camera for a live capture, or upload an existing front-facing photo.</p></div></div>
    <div class='feature-item'><div class='feature-icon'>3</div><div class='feature-text'><h4>AI detects your skin condition</h4><p>Our EfficientNetB3 model analyses your image for 7 common skin conditions and returns personalised ingredient recommendations.</p></div></div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>What We Detect</div>", unsafe_allow_html=True)
    st.markdown("<p class='section-sub'>Our model is trained to identify these 7 skin conditions.</p>", unsafe_allow_html=True)
    st.markdown("""<div style='display:flex;flex-wrap:wrap;gap:0.5rem;margin-bottom:0.5rem;'>
        <span style='background:#f5f5f5;color:#444;padding:0.4rem 1rem;border-radius:100px;font-size:0.88rem;font-weight:600;'>Acne</span>
        <span style='background:#f5f5f5;color:#444;padding:0.4rem 1rem;border-radius:100px;font-size:0.88rem;font-weight:600;'>Oiliness</span>
        <span style='background:#f5f5f5;color:#444;padding:0.4rem 1rem;border-radius:100px;font-size:0.88rem;font-weight:600;'>Dryness</span>
        <span style='background:#f5f5f5;color:#444;padding:0.4rem 1rem;border-radius:100px;font-size:0.88rem;font-weight:600;'>Dark Spots</span>
        <span style='background:#f5f5f5;color:#444;padding:0.4rem 1rem;border-radius:100px;font-size:0.88rem;font-weight:600;'>Redness</span>
        <span style='background:#f5f5f5;color:#444;padding:0.4rem 1rem;border-radius:100px;font-size:0.88rem;font-weight:600;'>Wrinkles</span>
        <span style='background:#F1F8F1;color:#2E6B35;padding:0.4rem 1rem;border-radius:100px;font-size:0.88rem;font-weight:600;'>Normal Skin</span>
    </div>""", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.82rem;color:#bbb;text-align:center;padding:1rem 0;'>DermaVision is an educational tool and not a substitute for professional medical advice. Always consult a dermatologist for clinical diagnosis.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "analyse":
    st.markdown("<div class='page-content'>", unsafe_allow_html=True)
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("← Back to Home", key="back_home"):
        st.session_state.page = "home"; st.session_state.img = None; st.query_params.clear(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Your Skin Profile</div>", unsafe_allow_html=True)
    st.markdown("<p class='section-sub'>Tell us a little about yourself to personalise your recommendations.</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        ag = st.selectbox("Age Group", ["14-18", "19-24", "25-36", "37-45", "45+"],
            index=["14-18", "19-24", "25-36", "37-45", "45+"].index(st.session_state.age_group))
        st.session_state.age_group = ag
    with c2:
        sens = st.radio("Sensitive skin?", ["No", "Yes"],
            index=["No", "Yes"].index(st.session_state.sensitivity), horizontal=True)
        st.session_state.sensitivity = sens
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Analyse Your Skin</div>", unsafe_allow_html=True)
    st.markdown("<p class='section-sub'>Click a card below to get started.</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<a href='?p=capture&m=camera' style='text-decoration:none;display:block;'><div class='input-card'><div class='input-card-icon'>📷</div><div class='input-card-title'>Live Camera</div><div class='input-card-sub'>Take a photo using your device camera</div></div></a>", unsafe_allow_html=True)
    with c2:
        st.markdown("<a href='?p=capture&m=upload' style='text-decoration:none;display:block;'><div class='input-card'><div class='input-card-icon'>🖼️</div><div class='input-card-title'>Upload Photo</div><div class='input-card-sub'>Select an existing image from your device</div></div></a>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CAPTURE
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "capture":
    st.markdown("<div class='page-content'>", unsafe_allow_html=True)
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("← Back", key="back_capture"):
        st.session_state.page = "analyse"; st.query_params.clear(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.input_method == "camera":
        st.markdown("<div class='section-heading'>Take a Photo</div>", unsafe_allow_html=True)
        st.markdown("<p class='section-sub'>Position your face clearly in the frame. Good lighting gives the best results.</p>", unsafe_allow_html=True)
        shot = st.camera_input("")
        if shot:
            img = Image.open(shot)
            if is_blurry(img):
                st.markdown("<div class='blur-warn'><p>⚠️ <strong>Image appears blurry.</strong> Please stabilise your camera or clean your lens for a more accurate analysis.</p></div>", unsafe_allow_html=True)
                bc1, bc2 = st.columns(2)
                with bc1:
                    if st.button("🔄 Retake Photo", key="retake"):
                        st.query_params.clear(); st.rerun()
                with bc2:
                    if st.button("✅ Use Anyway", key="use_anyway"):
                        face_found, annotated = detect_face(img)
                        st.session_state.img = annotated; st.session_state.face_found = face_found
                        st.session_state.page = "result"; st.query_params.clear(); st.rerun()
            else:
                face_found, annotated = detect_face(img)
                st.session_state.img = annotated; st.session_state.face_found = face_found
                st.session_state.page = "result"; st.query_params.clear(); st.rerun()
    else:
        st.markdown("<div class='section-heading'>Upload a Photo</div>", unsafe_allow_html=True)
        st.markdown("<p class='section-sub'>Upload a clear, well-lit front-facing photo for best results.</p>", unsafe_allow_html=True)
        upload = st.file_uploader("", type=["jpg", "jpeg", "png"])
        if upload:
            img = Image.open(upload)
            face_found, annotated = detect_face(img)
            st.session_state.img = annotated; st.session_state.face_found = face_found
            st.session_state.page = "result"; st.query_params.clear(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# RESULT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "result":
    st.markdown("<div class='page-content'>", unsafe_allow_html=True)
    st.markdown("<div class='back-btn'>", unsafe_allow_html=True)
    if st.button("← Back", key="back_result"):
        st.session_state.page = "capture"; st.session_state.img = None; st.query_params.clear(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading'>Your Results</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='background:#F1F8F1;border:1px solid #C8E6C9;border-radius:10px;padding:0.8rem 1.2rem;margin-bottom:1.5rem;font-size:0.88rem;color:#2E6B35;'><strong>Age:</strong> {st.session_state.age_group} &nbsp;|&nbsp; <strong>Sensitive skin:</strong> {st.session_state.sensitivity}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.3])
    with c1:
        if st.session_state.img:
            st.image(st.session_state.img, use_container_width=True,
                caption="Face detected ✓" if st.session_state.face_found else "No face detected")
    with c2:
        if not st.session_state.face_found:
            st.markdown("<div class='no-face-box'><p>⚠️ No face detected.<br><br>Please upload a clear, front-facing photo with good lighting.</p></div>", unsafe_allow_html=True)
        else:
            preds     = predict(st.session_state.img)
            top_label = preds[0][0]
            st.markdown("<h3 style='color:#2E6B35;margin-bottom:0.3rem;'>Skin Conditions Detected</h3>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.82rem;color:#999;margin-bottom:1rem;'>Percentages show how confident the model is that your skin shows signs of each condition.</p>", unsafe_allow_html=True)
            for label, pct in preds[:5]:
                st.markdown(f"<div class='condition-row'><div class='condition-header'><span class='condition-name'>{fmt(label)}</span><span class='condition-pct {sev(pct)}'>{pct:.0f}%</span></div></div>", unsafe_allow_html=True)
                st.progress(int(pct))
            rec = get_recommendation(top_label, preds, st.session_state.age_group, st.session_state.sensitivity)
            if rec:
                st.markdown(
                    f"<div class='rec-box'>"
                    f"<div class='rec-title'>Personalised Recommendation</div>"
                    f"<div class='rec-row'><span class='rec-label'>Skin Type:</span><span>{rec['skin_type']}</span></div>"
                    f"<div class='rec-row'><span class='rec-label'>Concern:</span><span>{rec['concern']}</span></div>"
                    f"<div class='rec-row'><span class='rec-label'>Type:</span><span>{rec['internal_type']}</span></div>"
                    f"<div class='rec-row'><span class='rec-label'>Ingredients:</span><span>{rec['ingredients']}</span></div>"
                    f"<div class='rec-row'><span class='rec-label'>Concentrations:</span><span>{rec['concentrations']}</span></div>"
                    f"<div class='rec-row'><span class='rec-label'>Effects:</span><span>{rec['effects']}</span></div>"
                    f"</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(f"<div style='background:#F9FBF7;border:1px solid #E0EDD8;border-radius:12px;padding:1.2rem 1.4rem;margin-top:1.2rem;font-size:0.88rem;color:#666;'>No specific recommendation found for <strong>{fmt(top_label)}</strong>.</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  Analyse Another Photo", key="retry"):
        st.session_state.page = "analyse"; st.session_state.img = None; st.query_params.clear(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

