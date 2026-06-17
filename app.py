import streamlit as st
import time
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question

load_dotenv()

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: #3E2A47 !important;
    color: #f5f0ff !important;
}

.stApp {
    background: #3E2A47 !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }
.block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1100px !important;
}

/* ── Header ── */
.ava-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid rgba(167,123,202,0.3);
    margin-bottom: 1.75rem;
}
.ava-logo {
    display: flex;
    align-items: center;
    gap: 12px;
}
.ava-logo-icon {
    width: 40px;
    height: 40px;
    background: #A77BCA;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    line-height: 1;
}
.ava-logo-name {
    font-size: 17px;
    font-weight: 600;
    color: #E8D8E0;
    line-height: 1.2;
}
.ava-logo-sub {
    font-size: 11px;
    color: #A77BCA;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.ava-version {
    background: rgba(167,123,202,0.18);
    border: 1px solid rgba(167,123,202,0.3);
    color: #A77BCA;
    font-size: 11px;
    font-weight: 500;
    padding: 4px 12px;
    border-radius: 999px;
    letter-spacing: 0.05em;
}

/* ── Pipeline strip ── */
.pipeline-strip {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.pipe-step {
    display: flex;
    align-items: center;
    gap: 6px;
    background: rgba(91,63,141,0.4);
    border: 1px solid rgba(167,123,202,0.25);
    border-radius: 999px;
    padding: 5px 13px;
    font-size: 12px;
    font-weight: 500;
    color: #9b7fc4;
    transition: all 0.3s ease;
}
.pipe-step.active {
    background: rgba(167,123,202,0.3);
    border-color: #A77BCA;
    color: #E8D8E0;
}
.pipe-step.done {
    background: rgba(122,91,157,0.35);
    border-color: #7A5B9D;
    color: #d4b8f0;
}
.pipe-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: rgba(167,123,202,0.3);
    flex-shrink: 0;
}
.pipe-step.active .pipe-dot {
    background: #E8D8E0;
    box-shadow: 0 0 0 2px rgba(232,216,224,0.25);
}
.pipe-step.done .pipe-dot { background: #A77BCA; }
.pipe-arrow { color: rgba(167,123,202,0.4); font-size: 13px; }

/* ── Input Area ── */
.stTextInput > div > div > input {
    background: rgba(122,91,157,0.25) !important;
    border: 1px solid rgba(167,123,202,0.3) !important;
    border-radius: 12px !important;
    color: #f5f0ff !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input::placeholder { color: #9b7fc4 !important; }
.stTextInput > div > div > input:focus {
    border-color: #A77BCA !important;
    box-shadow: none !important;
}

.stSelectbox > div > div {
    background: rgba(122,91,157,0.25) !important;
    border: 1px solid rgba(167,123,202,0.3) !important;
    border-radius: 12px !important;
    color: #f5f0ff !important;
}

label { color: #9b7fc4 !important; font-size: 12px !important; font-weight: 500 !important; letter-spacing: 0.04em !important; }

.stButton > button {
    background: #A77BCA !important;
    border: none !important;
    border-radius: 12px !important;
    color: #2a1a38 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: background 0.2s, transform 0.15s !important;
    letter-spacing: 0.02em !important;
}
.stButton > button:hover {
    background: #E8D8E0 !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: rgba(167,123,202,0.12) !important;
    border: 1px solid rgba(167,123,202,0.3) !important;
    color: #A77BCA !important;
}
.stButton > button[kind="secondary"]:hover {
    background: rgba(167,123,202,0.22) !important;
}

/* ── Cards ── */
.ava-card {
    background: rgba(91,63,141,0.38);
    border: 1px solid rgba(167,123,202,0.28);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
    height: 100%;
}
.ava-card-label {
    font-size: 10px;
    font-weight: 600;
    color: #9b7fc4;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.ava-card-label .icon { font-size: 14px; }
.ava-card-title {
    font-size: 17px;
    font-weight: 600;
    color: #E8D8E0;
    line-height: 1.4;
}
.ava-card-body {
    font-size: 13px;
    line-height: 1.8;
    color: #c4aee0;
}
.ava-card-body ul { padding-left: 16px; margin: 0; }
.ava-card-body li { margin-bottom: 4px; }

/* ── Transcript expander ── */
.stExpander {
    background: rgba(91,63,141,0.38) !important;
    border: 1px solid rgba(167,123,202,0.28) !important;
    border-radius: 14px !important;
}
.stExpander summary {
    color: #9b7fc4 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
}
.transcript-inner {
    background: rgba(62,42,71,0.55);
    border: 1px solid rgba(167,123,202,0.2);
    border-radius: 10px;
    padding: 14px;
    font-size: 12px;
    line-height: 1.85;
    color: #9b7fc4;
    max-height: 220px;
    overflow-y: auto;
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Chat ── */
.chat-shell {
    background: rgba(62,42,71,0.45);
    border: 1px solid rgba(167,123,202,0.25);
    border-radius: 14px;
    padding: 18px 20px;
    margin-bottom: 14px;
}
.chat-section-label {
    font-size: 10px;
    font-weight: 600;
    color: #9b7fc4;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 6px;
}
.chat-window {
    background: rgba(62,42,71,0.6);
    border: 1px solid rgba(167,123,202,0.18);
    border-radius: 10px;
    padding: 14px;
    min-height: 180px;
    max-height: 320px;
    overflow-y: auto;
    margin-bottom: 12px;
    display: flex;
    flex-direction: column;
    gap: 10px;
}
.chat-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 140px;
    color: #7a5b9d;
    font-size: 13px;
    gap: 6px;
    text-align: center;
}
.chat-msg-wrap {
    display: flex;
    flex-direction: column;
    gap: 3px;
    max-width: 80%;
}
.chat-msg-wrap.user { align-self: flex-end; align-items: flex-end; }
.chat-msg-wrap.bot  { align-self: flex-start; align-items: flex-start; }
.chat-msg-label {
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
.chat-msg-wrap.user .chat-msg-label { color: #A77BCA; }
.chat-msg-wrap.bot  .chat-msg-label { color: #7a5b9d; }
.chat-bubble {
    padding: 9px 14px;
    border-radius: 12px;
    font-size: 13px;
    line-height: 1.7;
}
.user-bubble {
    background: rgba(167,123,202,0.25);
    border: 1px solid rgba(167,123,202,0.4);
    color: #E8D8E0;
}
.bot-bubble {
    background: rgba(91,63,141,0.45);
    border: 1px solid rgba(167,123,202,0.2);
    color: #c4aee0;
}

/* ── Empty / landing ── */
.landing {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 60px 20px;
    text-align: center;
    gap: 14px;
}
.landing-orb {
    width: 80px;
    height: 80px;
    background: rgba(167,123,202,0.15);
    border: 1px solid rgba(167,123,202,0.3);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 34px;
    margin-bottom: 8px;
}
.landing-title {
    font-size: 18px;
    font-weight: 600;
    color: #E8D8E0;
}
.landing-desc {
    font-size: 13px;
    line-height: 1.75;
    color: #9b7fc4;
    max-width: 400px;
}
.landing-pills {
    display: flex;
    gap: 8px;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 8px;
}
.pill {
    background: rgba(167,123,202,0.15);
    border: 1px solid rgba(167,123,202,0.28);
    color: #A77BCA;
    font-size: 11px;
    font-weight: 500;
    padding: 5px 13px;
    border-radius: 999px;
}

/* ── Alerts ── */
.stAlert { border-radius: 10px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(167,123,202,0.3); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: #A77BCA; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #A77BCA !important; }

/* ── Progress ── */
.stProgress > div > div > div { background: #A77BCA !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────
for k, v in {
    "result": None,
    "chat_history": [],
    "pipeline_steps": {},
    "pipeline_done": False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="ava-header">
  <div class="ava-logo">
    <div class="ava-logo-icon">🎬</div>
    <div>
      <div class="ava-logo-name">AI Video Assistant</div>
      <div class="ava-logo-sub">Meeting Intelligence</div>
    </div>
  </div>
  <span class="ava-version">v1.0</span>
</div>
""", unsafe_allow_html=True)

# ─── Input Row ───────────────────────────────────────────────────────────────
col_url, col_lang, col_btn = st.columns([5, 1.5, 1.2], gap="small")
with col_url:
    source = st.text_input("Source", placeholder="YouTube URL or /path/to/file.mp4", label_visibility="collapsed")
with col_lang:
    language = st.selectbox("Language", ["english", "hinglish"], label_visibility="collapsed")
with col_btn:
    run = st.button("⚡  Analyse", use_container_width=True)

# ─── Pipeline Strip ──────────────────────────────────────────────────────────
STEPS = [
    ("audio",      "🔊", "Audio"),
    ("transcript", "📝", "Transcribe"),
    ("title",      "🏷️", "Title"),
    ("summary",    "📋", "Summarise"),
    ("extract",    "🔍", "Extract"),
    ("rag",        "🧠", "RAG"),
]

def _step_cls(key):
    s = st.session_state.pipeline_steps.get(key, "pending")
    return "active" if s == "active" else ("done" if s == "done" else "")

if st.session_state.pipeline_done or st.session_state.pipeline_steps:
    parts = []
    for i, (key, icon, label) in enumerate(STEPS):
        cls = _step_cls(key)
        parts.append(
            f'<div class="pipe-step {cls}"><span class="pipe-dot"></span>{icon} {label}</div>'
        )
        if i < len(STEPS) - 1:
            parts.append('<span class="pipe-arrow">›</span>')
    st.markdown(f'<div class="pipeline-strip">{"".join(parts)}</div>', unsafe_allow_html=True)

# ─── Run Pipeline ────────────────────────────────────────────────────────────
if run:
    if not source.strip():
        st.error("Enter a YouTube URL or file path to get started.")
    else:
        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.pipeline_done = False
        st.session_state.pipeline_steps = {k: "pending" for k, _, _ in STEPS}

        status = st.empty()

        def mark(key, state):
            st.session_state.pipeline_steps[key] = state

        try:
            status.info("Pipeline running…")

            mark("audio", "active"); st.rerun() if False else None
            chunks = process_input(source)
            mark("audio", "done")

            mark("transcript", "active")
            transcript = transcribe_all(chunks, language)
            mark("transcript", "done")

            mark("title", "active")
            title = generate_title(transcript)
            mark("title", "done")

            mark("summary", "active")
            summary = summarize(transcript)
            mark("summary", "done")

            mark("extract", "active")
            action_items = extract_action_items(transcript)
            decisions    = extract_key_decisions(transcript)
            questions    = extract_questions(transcript)
            mark("extract", "done")

            mark("rag", "active")
            rag_chain = build_rag_chain(transcript)
            mark("rag", "done")

            st.session_state.result = {
                "title": title,
                "transcript": transcript,
                "summary": summary,
                "action_items": action_items,
                "key_decisions": decisions,
                "open_questions": questions,
                "rag_chain": rag_chain,
            }
            st.session_state.pipeline_done = True
            status.success("✅ Analysis complete!")
            time.sleep(0.6)
            status.empty()
            st.rerun()

        except Exception as e:
            for k, _, _ in STEPS:
                if st.session_state.pipeline_steps.get(k) == "active":
                    st.session_state.pipeline_steps[k] = "pending"
            status.error(f"❌ {e}")

# ─── Results ─────────────────────────────────────────────────────────────────
if st.session_state.result:
    r = st.session_state.result

    # Title card
    st.markdown(f"""
    <div class="ava-card">
      <div class="ava-card-label"><span class="icon">📌</span> Session title</div>
      <div class="ava-card-title">{r['title']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Summary + Transcript
    col_sum, col_tr = st.columns([3, 2], gap="medium")

    with col_sum:
        st.markdown(f"""
        <div class="ava-card">
          <div class="ava-card-label"><span class="icon">📋</span> Summary</div>
          <div class="ava-card-body">{r['summary']}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_tr:
        with st.expander("📝 Full Transcript", expanded=False):
            st.markdown(f'<div class="transcript-inner">{r["transcript"]}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # Action items / Decisions / Questions
    c1, c2, c3 = st.columns(3, gap="medium")

    with c1:
        st.markdown(f"""
        <div class="ava-card">
          <div class="ava-card-label"><span class="icon">✅</span> Action items</div>
          <div class="ava-card-body">{r['action_items']}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="ava-card">
          <div class="ava-card-label"><span class="icon">🔑</span> Key decisions</div>
          <div class="ava-card-body">{r['key_decisions']}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="ava-card">
          <div class="ava-card-label"><span class="icon">❓</span> Open questions</div>
          <div class="ava-card-body">{r['open_questions']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    # ── Chat ──────────────────────────────────────────────────────────────
    st.markdown('<div class="chat-shell">', unsafe_allow_html=True)
    st.markdown('<div class="chat-section-label"><span>💬</span> Chat with your meeting</div>', unsafe_allow_html=True)

    # Build chat HTML
    if st.session_state.chat_history:
        bubbles = ""
        for msg in st.session_state.chat_history:
            role = msg["role"]
            who = "You" if role == "user" else "Assistant"
            cls_wrap = "user" if role == "user" else "bot"
            cls_bubble = "user-bubble" if role == "user" else "bot-bubble"
            bubbles += f"""
            <div class="chat-msg-wrap {cls_wrap}">
              <span class="chat-msg-label">{who}</span>
              <div class="chat-bubble {cls_bubble}">{msg['content']}</div>
            </div>"""
        st.markdown(f'<div class="chat-window">{bubbles}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="chat-window">
          <div class="chat-empty">
            💬<br>Ask anything about your meeting
          </div>
        </div>
        """, unsafe_allow_html=True)

    # Chat input
    inp_col, btn_col = st.columns([6, 1], gap="small")
    with inp_col:
        user_q = st.text_input("Question", placeholder="What were the main decisions made?", label_visibility="collapsed", key="chat_q")
    with btn_col:
        send = st.button("Send →", use_container_width=True)

    if send and user_q.strip():
        with st.spinner("Thinking…"):
            answer = ask_question(r["rag_chain"], user_q.strip())
        st.session_state.chat_history.append({"role": "user",      "content": user_q.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state.chat_history:
        if st.button("🗑️ Clear chat", type="secondary"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ─── Landing / Empty State ───────────────────────────────────────────────────
else:
    st.markdown("""
    <div class="landing">
      <div class="landing-orb">🎬</div>
      <div class="landing-title">Ready to analyse</div>
      <div class="landing-desc">
        Paste a YouTube URL or a local file path above, pick a language, and hit <strong>Analyse</strong>.
        You'll get a full transcript, summary, action items, decisions, and a chat interface — all in one place.
      </div>
      <div class="landing-pills">
        <span class="pill">📝 Transcription</span>
        <span class="pill">📋 Summarisation</span>
        <span class="pill">✅ Action items</span>
        <span class="pill">🧠 RAG Chat</span>
      </div>
    </div>
    """, unsafe_allow_html=True)