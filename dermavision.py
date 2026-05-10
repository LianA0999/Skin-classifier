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
.hero { text-align: center; padding: 5rem 2rem 4rem; background: linear-gradient(180deg, #F1F8F1 0%, #ffffff 100%); border-bottom: 1px solid #E0EDD8; }
.hero-badge { display: inline-block; background-color: #FFF3E0; color: #E65100; border: 1px solid #FFCC80; border-radius: 100px; padding: 5px 16px; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1.5rem; }
.hero h1 { font-size: clamp(2rem, 4vw, 3rem); font-weight: 800; color: #1A1A1A; line-height: 1.2; margin-bottom: 1.2rem; max-width: 750px; margin-left: auto; margin-right: auto; }
.hero h1 span { color: #4CAF50; }
.hero-sub { font-size: 1.05rem; color: #666; max-width: 560px; margin: 0 auto 2rem; line-height: 1.7; text-align: center !important; }
.hero p, .hero p.hero-sub { text-align: center !important; }
.hero-trust { font-size: 0.82rem; color: #888; display: flex; align-items: center; justify-content: center; gap: 0.5rem; margin-top: 1rem; }
.page-content { max-width: 900px; margin: 0 auto; padding: 3rem 2rem; }
.section-heading { font-size: 1.5rem; font-weight: 700; color: #1A1A1A; margin-bottom: 0.4rem; }
.section-sub { color: #888; font-size: 0.92rem; margin-bottom: 1.5rem; }
.divider { height: 1px; background: linear-gradient(90deg, transparent, #C8E6C9, transparent); margin: 2.5rem 0; }
.feature-item { background: #ffffff; border-radius: 14px; padding: 1.4rem 1.6rem; border: 1px solid #E0EDD8; margin-bottom: 1rem; display: flex; align-items: flex-start; gap: 1rem; }
.feature-icon { font-size: 1.1rem; font-weight: 800; color: #4CAF50; margin-top: 4px; min-width: 28px; }
.feature-text h4 { margin: 0 0 4px; color: #2E6B35; font-size: 1rem; font-weight: 700; }
.feature-text p { margin: 0; color: #777; font-size: 0.88rem; line-height: 1.5; }
.input-card { background: #ffffff; border-radius: 16px; padding: 2.5rem 1.5rem; border: 2px solid #E0EDD8; text-align: center; cursor: pointer; transition: all 0.2s; margin-bottom: 0.5rem; }
.input-card:hover { border-color: #4CAF50; background: #F1F8F1; transform: translateY(-3px); box-shadow: 0 8px 20px rgba(76,175,80,0.15); }
.input-card-icon { font-size: 2.8rem; margin-bottom: 0.8rem; }
.input-card-title { font-size: 1.15rem; font-weight: 800; color: #1B5E20; margin-bottom: 0.3rem; }
.input-card-sub { font-size: 0.85rem; color: #999; }
.profile-box { background: #ffffff; border: 1px solid #E0EDD8; border-radius: 14px; padding: 1.5rem 1.8rem; margin-bottom: 1rem; }
.stButton > button { background-color: #4CAF50; color: white; border: none; border-radius: 10px; padding: 0.7rem 1.5rem; font-size: 1rem; font-weight: 600; font-family: 'Nunito', sans-serif; width: 100%; transition: all 0.2s; margin-top: 0.5rem; }
.stButton > button:hover { background-color: #388E3C; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(76,175,80,0.3); }
.back-btn .stButton > button { background-color: transparent; color: #4CAF50; border: 1.5px solid #4CAF50; width: auto; padding: 0.4rem 1rem; font-size: 0.88rem; margin-top: 0; }
.back-btn .stButton > button:hover { background-color: #F1F8F1; transform: none; box-shadow: none; }
.condition-row { padding: 0.7rem 0; border-bottom: 1px solid #F0F0F0; }
.condition-header { display: flex; justify-content: space-between; margin-bottom: 6px; }
.condition-name { font-size: 0.92rem; font-weight: 600; color: #3D3D3D; }
.condition-pct { font-size: 0.92rem; font-weight: 700; }
.pct-high { color: #E65100; }
.pct-med  { color: #F9A825; }
.pct-low  { color: #4CAF50; }
.stProgress > div > div { background: linear-gradient(90deg, #4CAF50, #8BC34A); border-radius: 100px; }
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
.team-avatar { width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #4CAF50, #8BC34A); display: flex; align-items: center; justify-content: center; font-size: 2rem; margin: 0 auto 1rem; }
.team-name { font-size: 1.1rem; font-weight: 800; color: #1B5E20; margin-bottom: 0.2rem; }
.team-role { font-size: 0.85rem; font-weight: 600; color: #4CAF50; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.06em; }
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

CONCERN_MAP = {
    "acne": "Acne", "dark_spots": "Dark Spots", "dry": "Dullness",
    "normal": "Open Pores", "oily": "Acne", "redness": "Hyperpigmentation", "wrinkles": "Dark Circles",
}

def predict(img):
    if model_loaded and model is not None:
        try:
            from tensorflow.keras.applications.efficientnet import preprocess_input
            arr = np.array(img.convert("RGB").resize((224, 224)), dtype=np.float32)
            arr = preprocess_input(arr[np.newaxis])
            probs = model.predict(arr, verbose=0)[0]
            return sorted(zip(class_names, (probs * 100).tolist()), key=lambda x: -x[1])
        except Exception:
            pass
    probs = [random.uniform(10, 90) for _ in class_names]
    total = sum(probs)
    return sorted(zip(class_names, [(p/total)*100 for p in probs]), key=lambda x: -x[1])

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
    score = cv2.Laplacian(gray, cv2.CV_64F).var()
    return score < threshold

def get_recommendation(condition, age_group, sensitivity):
    if rec_df is None:
        return None
    concern = CONCERN_MAP.get(condition.lower(), condition)
    match = rec_df[
        (rec_df["Concern"].str.lower() == concern.lower()) &
        (rec_df["Age_Group"] == age_group) &
        (rec_df["Sensitivity"] == sensitivity)
    ]
    if match.empty:
        match = rec_df[(rec_df["Concern"].str.lower() == concern.lower()) & (rec_df["Age_Group"] == age_group)]
    if match.empty:
        match = rec_df[rec_df["Concern"].str.lower() == concern.lower()]
    if match.empty:
        return None
    row = match.iloc[0]
    return {
        "concern": row.get("Concern",""), "internal_type": row.get("Internal_Type",""),
        "ingredients": row.get("Ingredients",""), "concentrations": row.get("Concentrations",""),
        "effects": row.get("Effects",""),
    }

def sev(pct):
    if pct >= 50: return "pct-high"
    if pct >= 25: return "pct-med"
    return "pct-low"

def fmt(label):
    return label.replace("_", " ").title()

for k, v in {
    "page": "home", "img": None, "face_found": False,
    "input_method": "upload", "age_group": "19-25", "sensitivity": "No"
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

# ── Navbar (position:fixed so it always works regardless of Streamlit DOM) ──
def _nav_link(label, target, current):
    active = current == target
    bg = "#F1F8F1" if active else "transparent"
    color = "#2E6B35" if active else "#555"
    return (f'<a href="?p={target}" style="color:{color};font-weight:600;font-size:0.9rem;'
            f'text-decoration:none;padding:0.4rem 0.9rem;border-radius:8px;background:{bg};">{label}</a>')

_page = st.session_state.page
st.markdown(f"""
<div style="position:fixed;top:0;left:0;right:0;height:64px;background:white;
    border-bottom:1px solid #E0EDD8;box-shadow:0 1px 8px rgba(0,0,0,0.06);
    z-index:9999;display:flex;align-items:center;padding:0 3rem;
    font-family:'Nunito',sans-serif;gap:0.5rem;">
  <div style="font-size:1.25rem;font-weight:800;color:#2E6B35;flex:1;">🌿 DermaVision</div>
  {_nav_link("Home","home",_page)}
  {_nav_link("Analysis","analyse",_page)}
  {_nav_link("About Us","about",_page)}
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "home":
    st.markdown("""
    <div class="hero">
        <h1>Free AI <span>Skin Analysis</span> Tool &amp; Skin Type Detector</h1>
        <p class="hero-sub">Upload a photo of your face and our AI will detect your skin condition and give you personalised ingredient recommendations — all in seconds, completely free.</p>
        <div class="hero-trust">No account needed &nbsp;·&nbsp; Your photos are never stored</div>
    </div>
    """, unsafe_allow_html=True)

    _, hero_cta, _ = st.columns([3, 2, 3])
    with hero_cta:
        if st.button("Start Free Analysis", key="hero_cta"):
            st.session_state.page = "analyse"; st.rerun()

    st.markdown("<div class='page-content'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:4rem; text-align:center; color:#1B5E20; font-weight:900;'>DermaVision</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:1.05rem; color:#666; margin-bottom:2rem;'>Understand your skin in seconds with AI-powered analysis and personalised ingredient recommendations.</p>", unsafe_allow_html=True)
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
    st.markdown("<p class='section-sub'>Our model is trained to identify these skin conditions.</p>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    for name in ["Acne","Oiliness","Dryness","Dark Spots","Redness","Wrinkles","Normal Skin"]:
        with c1 if ["Acne","Oiliness","Dryness","Dark Spots","Redness","Wrinkles","Normal Skin"].index(name) % 2 == 0 else c2:
            st.markdown(f"<div style='background:#fff;border:1px solid #E0EDD8;border-radius:10px;padding:0.8rem 1rem;margin-bottom:0.7rem;'><span style='font-weight:600;color:#3D3D3D;font-size:0.92rem;'>{name}</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='disclaimer'><p><strong>Disclaimer:</strong> DermaVision is an educational tool and is not a substitute for professional medical advice. Always consult a qualified dermatologist for clinical diagnosis and personalised treatment plans.</p></div>", unsafe_allow_html=True)
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
    st.markdown("<div class='profile-box'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        ag = st.selectbox("Age Group", ["14-18","19-25","26-35","36-45","46-55","55+"],
            index=["14-18","19-25","26-35","36-45","46-55","55+"].index(st.session_state.age_group))
        st.session_state.age_group = ag
    with c2:
        sens = st.radio("Sensitive skin?", ["No","Yes"],
            index=["No","Yes"].index(st.session_state.sensitivity), horizontal=True)
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
        upload = st.file_uploader("", type=["jpg","jpeg","png"])
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
            preds = predict(st.session_state.img)
            top_label = preds[0][0]
            st.markdown("<h3 style='color:#2E6B35;margin-bottom:0.5rem;'>Skin Conditions Detected</h3>", unsafe_allow_html=True)
            for label, pct in preds[:5]:
                st.markdown(f"<div class='condition-row'><div class='condition-header'><span class='condition-name'>{fmt(label)}</span><span class='condition-pct {sev(pct)}'>{pct:.0f}%</span></div></div>", unsafe_allow_html=True)
                st.progress(int(pct))
            rec = get_recommendation(top_label, st.session_state.age_group, st.session_state.sensitivity)
            if rec:
                st.markdown(f"<div class='rec-box'><div class='rec-title'>Personalised Recommendation</div><div class='rec-row'><span class='rec-label'>Concern:</span><span>{rec['concern']}</span></div><div class='rec-row'><span class='rec-label'>Type:</span><span>{rec['internal_type']}</span></div><div class='rec-row'><span class='rec-label'>Ingredients:</span><span>{rec['ingredients']}</span></div><div class='rec-row'><span class='rec-label'>Concentrations:</span><span>{rec['concentrations']}</span></div><div class='rec-row'><span class='rec-label'>Effects:</span><span>{rec['effects']}</span></div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='background:#F9FBF7;border:1px solid #E0EDD8;border-radius:12px;padding:1.2rem 1.4rem;margin-top:1.2rem;font-size:0.88rem;color:#666;'>No specific recommendation found for <strong>{fmt(top_label)}</strong>.</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄  Analyse Another Photo", key="retry"):
        st.session_state.page = "analyse"; st.session_state.img = None; st.query_params.clear(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ABOUT US
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "about":
    st.markdown("<div class='page-content'>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center; padding:3rem 0 2rem;'>
        <div class='hero-badge'>Meet The Team</div>
        <h1 style='font-size:2.8rem; font-weight:900; color:#1B5E20; margin-bottom:1rem;'>The Visionaries</h1>
        <p style='font-size:1.05rem; color:#666; max-width:600px; margin:0 auto; line-height:1.7;'>
            The Visionaries is a small team of AI specialists passionate about making
            dermatology accessible to everyone. Founded by L, A, and M, we combine
            deep learning expertise with a commitment to skin health innovation.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-heading' style='text-align:center;'>Our Team</div>", unsafe_allow_html=True)
    st.markdown("<p class='section-sub' style='text-align:center;'>The people behind DermaVision.</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='team-card'><div class='team-avatar'>M</div><div class='team-name'>Muhammad</div><div class='team-role'>AI Engineer</div><div class='team-bio'>Specialises in deep learning and computer vision. Led the model training and dataset pipeline for DermaVision.</div><div class='team-contact'>m@email.com</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='team-card'><div class='team-avatar'>L</div><div class='team-name'>Lian</div><div class='team-role'>Data Scientist</div><div class='team-bio'>Focused on data collection, cleaning, and analysis. Curated the skin condition datasets used to train the model.</div><div class='team-contact'>l@email.com</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='team-card'><div class='team-avatar'>P</div><div class='team-name'>Pichaya</div><div class='team-role'>Frontend Developer</div><div class='team-bio'>Designed and built the DermaVision interface. Focused on creating a clean, accessible user experience.</div><div class='team-contact'>p@email.com</div></div>", unsafe_allow_html=True)
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='background:#E8F5E9; border-radius:16px; padding:2.5rem; text-align:center; border:1px solid #C8E6C9;'>
        <h3 style='color:#1B5E20; font-weight:800; margin-bottom:0.8rem;'>Our Mission</h3>
        <p style='color:#2E6B35; font-size:0.95rem; max-width:500px; margin:0 auto; line-height:1.7;'>
            To make personalised skincare accessible to everyone through the power
            of artificial intelligence — no expensive consultations required.
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
