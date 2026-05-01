"""
RasaPlan — The Broke Student Sri Lankan Meal Planner
Main Streamlit Application with full 3D motion graphic UI.
"""

import json
import os
import streamlit as st
from streamlit.components.v1 import html

# Page config — must be first Streamlit call
st.set_page_config(
    page_title="RasaPlan | රිස බාසි | Sri Lankan Meal Planner",
    page_icon="🍛",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 0
if "profile" not in st.session_state:
    st.session_state.profile = {
        "budget_lkr": 2000,
        "diet": "vegetarian",
        "skill": "beginner",
        "store": "Keells",
        "num_people": 1,
    }
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = None
if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("OPENAI_API_KEY", "")

# ─────────────────────────────────────────────────────────────────
# INJECT FULL MOTION GRAPHIC CSS + JS
# ─────────────────────────────────────────────────────────────────
HERO_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>RasaPlan Hero</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Noto+Sans+Sinhala:wght@400;700&family=DM+Mono:wght@400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: 'Syne', sans-serif;
    background: #0a0a0a;
    overflow-x: hidden;
    cursor: none;
  }

  /* Custom cursor */
  .cursor {
    width: 32px; height: 32px;
    position: fixed; top: 0; left: 0;
    pointer-events: none; z-index: 9999;
    transition: transform 0.1s;
    font-size: 24px;
    transform: translate(-50%, -50%);
  }

  /* Particle canvas */
  #particle-canvas {
    position: fixed; top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none; z-index: 0;
  }

  /* ── HERO ── */
  .hero {
    width: 100%; min-height: 100vh;
    display: grid;
    grid-template-columns: 1fr 1fr;
    position: relative;
    overflow: hidden;
  }

  .hero-left {
    background: #F5C842;
    display: flex; flex-direction: column;
    justify-content: center; align-items: flex-start;
    padding: 4rem 3rem;
    position: relative;
    overflow: hidden;
  }

  .hero-left::before {
    content: '';
    position: absolute; top: -100px; right: -100px;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.15);
    border-radius: 50%;
  }

  .hero-right {
    background: #1C2C6B;
    display: flex; flex-direction: column;
    justify-content: center; align-items: flex-end;
    padding: 4rem 3rem;
    position: relative;
    overflow: hidden;
  }

  .hero-right::after {
    content: '';
    position: absolute; bottom: -80px; left: -80px;
    width: 250px; height: 250px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
  }

  /* Brand badge */
  .brand-badge {
    background: rgba(28,44,107,0.15);
    border: 2px solid rgba(28,44,107,0.3);
    color: #1C2C6B;
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    padding: 6px 16px;
    border-radius: 4px;
    margin-bottom: 1.5rem;
    text-transform: uppercase;
    animation: fadeUp 0.8s ease forwards;
    opacity: 0;
  }

  .hero-title {
    font-size: clamp(3rem, 6vw, 5.5rem);
    font-weight: 800;
    color: #1C2C6B;
    line-height: 1.0;
    margin-bottom: 0.5rem;
    animation: slideRight 0.9s ease 0.2s forwards;
    opacity: 0;
    transform: translateX(-40px);
  }

  .hero-title-si {
    font-family: 'Noto Sans Sinhala', sans-serif;
    font-size: clamp(1.8rem, 3.5vw, 3rem);
    font-weight: 700;
    color: rgba(28,44,107,0.7);
    margin-bottom: 1.5rem;
    animation: slideRight 0.9s ease 0.4s forwards;
    opacity: 0;
    transform: translateX(-40px);
  }

  .hero-subtitle {
    font-size: 1.1rem;
    color: rgba(28,44,107,0.8);
    max-width: 360px;
    line-height: 1.6;
    animation: fadeUp 0.9s ease 0.6s forwards;
    opacity: 0;
  }

  /* Floating food emoji 3D elements */
  .food-float {
    position: absolute;
    font-size: 3rem;
    animation: float3d 4s ease-in-out infinite;
    filter: drop-shadow(0 10px 20px rgba(0,0,0,0.2));
    transform-style: preserve-3d;
  }
  .food-float:nth-child(1) { top: 10%; right: 20%; animation-delay: 0s; font-size: 4rem; }
  .food-float:nth-child(2) { top: 40%; right: 5%; animation-delay: 0.8s; font-size: 2.5rem; }
  .food-float:nth-child(3) { bottom: 20%; right: 25%; animation-delay: 1.6s; font-size: 3.5rem; }
  .food-float:nth-child(4) { top: 20%; left: 10%; animation-delay: 0.4s; font-size: 2rem; }
  .food-float:nth-child(5) { bottom: 30%; left: 5%; animation-delay: 1.2s; font-size: 3rem; }

  .right-title {
    font-size: clamp(2rem, 4vw, 3.5rem);
    font-weight: 800;
    color: #ffffff;
    text-align: right;
    line-height: 1.1;
    animation: slideLeft 0.9s ease 0.3s forwards;
    opacity: 0;
    transform: translateX(40px);
  }

  .right-title span { color: #F5C842; }

  .right-stats {
    display: flex; gap: 2rem; margin-top: 2rem;
    animation: fadeUp 0.9s ease 0.7s forwards;
    opacity: 0;
  }

  .stat-item { text-align: center; }
  .stat-num {
    font-size: 2.5rem; font-weight: 800;
    color: #F5C842; line-height: 1;
  }
  .stat-label {
    font-size: 0.75rem; color: rgba(255,255,255,0.6);
    font-family: 'DM Mono', monospace;
    letter-spacing: 1px; text-transform: uppercase;
  }

  /* CTA button */
  .cta-btn {
    display: inline-flex; align-items: center; gap: 10px;
    background: #1C2C6B; color: #F5C842;
    border: none; padding: 1rem 2rem;
    border-radius: 50px; font-size: 1rem;
    font-family: 'Syne', sans-serif; font-weight: 700;
    cursor: pointer; margin-top: 2rem;
    animation: fadeUp 0.9s ease 0.8s forwards; opacity: 0;
    transition: transform 0.2s, box-shadow 0.2s;
    text-decoration: none;
  }
  .cta-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 30px rgba(28,44,107,0.4);
  }

  /* Category nav strip */
  .category-nav {
    background: #ffffff;
    padding: 2rem 4rem;
    display: flex; align-items: center;
    justify-content: center; gap: 2.5rem;
    box-shadow: 0 2px 20px rgba(0,0,0,0.08);
    position: relative; z-index: 10;
    flex-wrap: wrap;
  }

  .nav-item {
    display: flex; flex-direction: column;
    align-items: center; gap: 8px;
    cursor: pointer;
    transition: transform 0.2s;
  }
  .nav-item:hover { transform: translateY(-5px); }
  .nav-item:hover .nav-circle { background: #F5C842; border-color: #F5C842; }

  .nav-circle {
    width: 64px; height: 64px;
    border-radius: 50%; border: 2px solid #e0e0e0;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
    transition: all 0.3s;
    background: #f8f8f8;
  }

  .nav-label {
    font-size: 0.7rem; font-family: 'DM Mono', monospace;
    color: #666; letter-spacing: 1px;
    text-transform: uppercase; text-align: center;
  }

  /* Hot Recommend section */
  .hot-section {
    background: #f8f4ec;
    padding: 5rem 4rem;
    text-align: center;
  }

  .section-script {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem; color: #F5C842; font-weight: 600;
    letter-spacing: 3px; margin-bottom: 0.5rem;
    text-transform: uppercase;
  }

  .section-title {
    font-size: clamp(2rem, 4vw, 3rem);
    font-weight: 800; color: #1C2C6B;
    margin-bottom: 3rem;
  }

  .meal-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap: 1.5rem; max-width: 1100px;
    margin: 0 auto;
  }

  .meal-card {
    background: white;
    border-radius: 16px;
    overflow: hidden;
    cursor: pointer;
    transition: transform 0.3s, box-shadow 0.3s;
    animation: fadeUp 0.6s ease forwards;
    opacity: 0;
    perspective: 1000px;
  }

  .meal-card:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.15); }

  .card-emoji-wrap {
    height: 160px;
    display: flex; align-items: center; justify-content: center;
    font-size: 5rem;
    position: relative;
    overflow: hidden;
  }

  .card-emoji-wrap.gold { background: linear-gradient(135deg, #F5C842, #f0b020); }
  .card-emoji-wrap.navy { background: linear-gradient(135deg, #1C2C6B, #2a3d8f); }
  .card-emoji-wrap.teal { background: linear-gradient(135deg, #0d6e56, #1a9e75); }

  /* Steam animation */
  .steam {
    position: absolute; top: 0; left: 50%;
    transform: translateX(-50%);
    display: flex; gap: 8px;
  }
  .steam-line {
    width: 3px; height: 30px;
    background: rgba(255,255,255,0.4);
    border-radius: 2px;
    animation: steam-rise 2s ease-in-out infinite;
  }
  .steam-line:nth-child(2) { animation-delay: 0.3s; height: 20px; }
  .steam-line:nth-child(3) { animation-delay: 0.6s; height: 25px; }

  .card-body { padding: 1.25rem; text-align: left; }
  .card-name { font-size: 1rem; font-weight: 700; color: #1C2C6B; margin-bottom: 4px; }
  .card-si { font-family: 'Noto Sans Sinhala', sans-serif; font-size: 0.8rem; color: #888; margin-bottom: 8px; }
  .card-meta { display: flex; justify-content: space-between; align-items: center; }
  .card-price { font-size: 1.1rem; font-weight: 700; color: #F5C842; }
  .card-time { font-size: 0.75rem; font-family: 'DM Mono', monospace; color: #999; }

  /* Fresh section */
  .fresh-section {
    background: #1C2C6B;
    padding: 5rem 4rem;
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
    position: relative;
    overflow: hidden;
  }

  .fresh-section::before {
    content: 'Fresh &\A Delicious';
    white-space: pre;
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    font-size: 8vw; font-weight: 800;
    color: rgba(255,255,255,0.03);
    pointer-events: none;
    text-align: center;
  }

  .fresh-title {
    font-size: clamp(2rem, 3.5vw, 2.8rem);
    font-weight: 800; color: white; margin-bottom: 1rem;
  }
  .fresh-title span { color: #F5C842; }

  .fresh-body {
    font-size: 1rem; color: rgba(255,255,255,0.7);
    line-height: 1.8; margin-bottom: 2rem;
  }

  .cert-badges { display: flex; gap: 1rem; flex-wrap: wrap; }
  .cert { background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15);
    color: white; padding: 8px 16px; border-radius: 8px;
    font-size: 0.8rem; font-family: 'DM Mono', monospace; }

  .fresh-visual {
    display: flex; align-items: center; justify-content: center;
    font-size: 8rem;
    animation: float3d 3s ease-in-out infinite;
    filter: drop-shadow(0 20px 40px rgba(0,0,0,0.3));
  }

  /* ── ANIMATIONS ── */
  @keyframes fadeUp {
    to { opacity: 1; transform: translateY(0); }
    from { opacity: 0; transform: translateY(20px); }
  }
  @keyframes slideRight {
    to { opacity: 1; transform: translateX(0); }
  }
  @keyframes slideLeft {
    to { opacity: 1; transform: translateX(0); }
  }
  @keyframes float3d {
    0%, 100% { transform: translateY(0) rotateY(0deg); }
    33% { transform: translateY(-15px) rotateY(5deg); }
    66% { transform: translateY(-8px) rotateY(-3deg); }
  }
  @keyframes steam-rise {
    0% { opacity: 0.7; transform: translateY(0) scaleX(1); }
    100% { opacity: 0; transform: translateY(-40px) scaleX(2); }
  }
  @keyframes particle-float {
    0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    10% { opacity: 0.6; }
    90% { opacity: 0.4; }
    100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
  }
  @keyframes pulse-ring {
    0% { transform: scale(1); opacity: 0.8; }
    100% { transform: scale(1.4); opacity: 0; }
  }

  /* Scroll reveal */
  .reveal { opacity: 0; transform: translateY(30px); transition: opacity 0.7s ease, transform 0.7s ease; }
  .reveal.visible { opacity: 1; transform: translateY(0); }

  /* Wave divider */
  .wave-divider { line-height: 0; background: #f8f4ec; }
  .wave-divider svg { display: block; }

  @media (max-width: 768px) {
    .hero { grid-template-columns: 1fr; }
    .hero-right { align-items: flex-start; }
    .right-title { text-align: left; }
    .fresh-section { grid-template-columns: 1fr; }
    .category-nav { gap: 1rem; padding: 1.5rem 2rem; }
  }
</style>
</head>
<body>

<!-- Custom cursor -->
<div class="cursor" id="cursor">🥄</div>

<!-- Particle canvas -->
<canvas id="particle-canvas"></canvas>

<!-- ── HERO ── -->
<section class="hero" id="hero">
  <!-- Left: Gold -->
  <div class="hero-left">
    <div class="brand-badge">🍛 AI-Powered Meal Planning · KDU · LB3114</div>
    <h1 class="hero-title">RasaPlan</h1>
    <p class="hero-title-si">රිස බාසි</p>
    <p class="hero-subtitle">
      Smart, affordable Sri Lankan meals planned by AI. 
      Tell us your budget — we'll handle the rest. <em>Rasai, beli, and healthy!</em>
    </p>
    <a href="#planner" class="cta-btn" onclick="scrollToPlanner()">
      🍽️ Start Planning  →
    </a>
  </div>

  <!-- Right: Navy -->
  <div class="hero-right">
    <div class="food-float">🍛</div>
    <div class="food-float">🥥</div>
    <div class="food-float">🍜</div>
    <div class="food-float">🌶️</div>
    <div class="food-float">🫘</div>

    <h2 class="right-title">
      Eat Well.<br>
      <span>Spend Less.</span><br>
      Live Better.
    </h2>
    <div class="right-stats">
      <div class="stat-item">
        <div class="stat-num">50+</div>
        <div class="stat-label">SL Recipes</div>
      </div>
      <div class="stat-item">
        <div class="stat-num">LKR 500</div>
        <div class="stat-label">Min Budget</div>
      </div>
      <div class="stat-item">
        <div class="stat-num">7</div>
        <div class="stat-label">Days Planned</div>
      </div>
    </div>
  </div>
</section>

<!-- Wave top -->
<div class="wave-divider" style="background:#ffffff;">
  <svg viewBox="0 0 1440 80" preserveAspectRatio="none">
    <path d="M0,40 C360,80 720,0 1080,40 C1260,60 1350,20 1440,40 L1440,0 L0,0 Z" fill="#1C2C6B"/>
  </svg>
</div>

<!-- ── CATEGORY NAV ── -->
<nav class="category-nav">
  <div class="nav-item"><div class="nav-circle">🍚</div><span class="nav-label">Rice Dishes</span></div>
  <div class="nav-item"><div class="nav-circle">🍜</div><span class="nav-label">Hoppers</span></div>
  <div class="nav-item"><div class="nav-circle">🫘</div><span class="nav-label">Curries</span></div>
  <div class="nav-item"><div class="nav-circle">🥚</div><span class="nav-label">Egg Dishes</span></div>
  <div class="nav-item"><div class="nav-circle">🐟</div><span class="nav-label">Seafood</span></div>
  <div class="nav-item"><div class="nav-circle">🥬</div><span class="nav-label">Vegetables</span></div>
  <div class="nav-item"><div class="nav-circle">🧃</div><span class="nav-label">Drinks</span></div>
</nav>

<!-- ── HOT RECOMMEND ── -->
<section class="hot-section">
  <div class="section-script">Hot Recommend</div>
  <h2 class="section-title reveal">🔥 Budget Favourites This Week</h2>

  <div class="meal-cards">
    <div class="meal-card reveal" style="animation-delay:0.1s">
      <div class="card-emoji-wrap gold">
        <div class="steam"><div class="steam-line"></div><div class="steam-line"></div><div class="steam-line"></div></div>
        🫓
      </div>
      <div class="card-body">
        <div class="card-name">Pol Roti</div>
        <div class="card-si">පොල් රොටී</div>
        <div class="card-meta">
          <span class="card-price">LKR 28/serving</span>
          <span class="card-time">⏱ 20 mins</span>
        </div>
      </div>
    </div>

    <div class="meal-card reveal" style="animation-delay:0.2s">
      <div class="card-emoji-wrap navy">
        <div class="steam"><div class="steam-line"></div><div class="steam-line"></div><div class="steam-line"></div></div>
        🫘
      </div>
      <div class="card-body">
        <div class="card-name">Dhal Curry</div>
        <div class="card-si">පරිප්පු කරිය</div>
        <div class="card-meta">
          <span class="card-price">LKR 27/serving</span>
          <span class="card-time">⏱ 25 mins</span>
        </div>
      </div>
    </div>

    <div class="meal-card reveal" style="animation-delay:0.3s">
      <div class="card-emoji-wrap teal">
        <div class="steam"><div class="steam-line"></div><div class="steam-line"></div><div class="steam-line"></div></div>
        🍛
      </div>
      <div class="card-body">
        <div class="card-name">Rice &amp; Curry</div>
        <div class="card-si">බත් සහ කරිය</div>
        <div class="card-meta">
          <span class="card-price">LKR 60/serving</span>
          <span class="card-time">⏱ 40 mins</span>
        </div>
      </div>
    </div>

    <div class="meal-card reveal" style="animation-delay:0.4s">
      <div class="card-emoji-wrap gold">
        <div class="steam"><div class="steam-line"></div><div class="steam-line"></div><div class="steam-line"></div></div>
        🥚
      </div>
      <div class="card-body">
        <div class="card-name">Egg Roti</div>
        <div class="card-si">බිත්තර රොටී</div>
        <div class="card-meta">
          <span class="card-price">LKR 45/serving</span>
          <span class="card-time">⏱ 20 mins</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- Wave divider -->
<div class="wave-divider" style="background:#1C2C6B;">
  <svg viewBox="0 0 1440 80" preserveAspectRatio="none">
    <path d="M0,40 C360,0 720,80 1080,40 C1260,20 1350,60 1440,40 L1440,80 L0,80 Z" fill="#f8f4ec"/>
  </svg>
</div>

<!-- ── FRESH & DELICIOUS ── -->
<section class="fresh-section">
  <div>
    <p class="section-script" style="color:#F5C842; text-align:left;">Fresh &amp; Delicious</p>
    <h2 class="fresh-title reveal">
      Real Sri Lankan Food,<br><span>Real Student Budget</span>
    </h2>
    <p class="fresh-body reveal">
      RasaPlan uses AI to plan 7-day meal schedules using ingredients from 
      Keells, Arpico, Cargills and local Pola markets — with actual 2025 LKR prices. 
      No generic meal plans. This is food you grew up with, optimised for your wallet.
    </p>
    <div class="cert-badges reveal">
      <span class="cert">🤖 LangChain ReAct</span>
      <span class="cert">🧠 GPT-4o</span>
      <span class="cert">🐍 Python</span>
      <span class="cert">📊 Real LKR Prices</span>
    </div>
  </div>
  <div class="fresh-visual reveal">🍲</div>
</section>

<script>
// ── Cursor tracking
const cursor = document.getElementById('cursor');
document.addEventListener('mousemove', e => {
  cursor.style.left = e.clientX + 'px';
  cursor.style.top = e.clientY + 'px';
});
document.querySelectorAll('a, button, .meal-card, .nav-item').forEach(el => {
  el.addEventListener('mouseenter', () => { cursor.textContent = '🍴'; cursor.style.transform = 'translate(-50%,-50%) scale(1.3)'; });
  el.addEventListener('mouseleave', () => { cursor.textContent = '🥄'; cursor.style.transform = 'translate(-50%,-50%) scale(1)'; });
});

// ── Particle system
const canvas = document.getElementById('particle-canvas');
const ctx = canvas.getContext('2d');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
window.addEventListener('resize', () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; });

const spices = ['✦', '·', '•', '◦', '∗'];
const particles = Array.from({length: 40}, () => ({
  x: Math.random() * canvas.width,
  y: Math.random() * canvas.height + canvas.height,
  size: Math.random() * 6 + 2,
  speed: Math.random() * 0.5 + 0.2,
  opacity: Math.random() * 0.4 + 0.1,
  symbol: spices[Math.floor(Math.random() * spices.length)],
  drift: (Math.random() - 0.5) * 0.5,
  color: Math.random() > 0.5 ? '#F5C842' : '#ffffff',
}));

function animateParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particles.forEach(p => {
    p.y -= p.speed;
    p.x += p.drift;
    if (p.y < -50) {
      p.y = canvas.height + 50;
      p.x = Math.random() * canvas.width;
    }
    ctx.globalAlpha = p.opacity;
    ctx.fillStyle = p.color;
    ctx.font = `${p.size * 3}px serif`;
    ctx.fillText(p.symbol, p.x, p.y);
  });
  ctx.globalAlpha = 1;
  requestAnimationFrame(animateParticles);
}
animateParticles();

// ── Scroll reveal
const reveals = document.querySelectorAll('.reveal');
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('visible'); }
  });
}, { threshold: 0.1 });
reveals.forEach(r => observer.observe(r));

// ── Parallax on hero food floats
document.addEventListener('mousemove', e => {
  const floats = document.querySelectorAll('.food-float');
  const cx = window.innerWidth / 2, cy = window.innerHeight / 2;
  const dx = (e.clientX - cx) / cx, dy = (e.clientY - cy) / cy;
  floats.forEach((f, i) => {
    const strength = (i + 1) * 6;
    f.style.transform = `translate(${dx * strength}px, ${dy * strength}px)`;
  });
});

function scrollToPlanner() {
  window.parent.postMessage({type: 'scrollToPlanner'}, '*');
}
</script>
</body>
</html>
"""


def inject_global_css():
    """Injects global CSS for the Streamlit app sections below the hero."""
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@400;500&display=swap');

    /* Hide Streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .block-container { padding-top: 0 !important; max-width: 100% !important; }

    /* Global font */
    html, body, [class*="css"] { font-family: 'Syne', sans-serif !important; }

    /* Section wrapper */
    .planner-section {
        background: #ffffff;
        padding: 3rem 2rem;
        max-width: 900px;
        margin: 0 auto;
    }

    .section-header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    .section-header .sub {
        font-family: 'DM Mono', monospace;
        font-size: 11px; letter-spacing: 3px;
        color: #F5C842; text-transform: uppercase;
        font-weight: 600; margin-bottom: 8px;
    }
    .section-header h2 {
        font-size: 2rem; font-weight: 800; color: #1C2C6B;
    }

    /* Step cards */
    .step-card {
        background: #f8f4ec;
        border: 2px solid transparent;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s;
    }
    .step-card:hover, .step-card.active {
        border-color: #F5C842;
        background: #fffef5;
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(245,200,66,0.2);
    }
    .step-number {
        background: #1C2C6B; color: #F5C842;
        width: 32px; height: 32px; border-radius: 50%;
        display: inline-flex; align-items: center; justify-content: center;
        font-family: 'DM Mono', monospace; font-size: 14px; font-weight: 600;
        margin-right: 12px;
    }

    /* Diet option cards */
    .diet-grid { display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 1rem; }
    .diet-card {
        flex: 1; min-width: 140px;
        background: white; border: 2px solid #e0e0e0;
        border-radius: 12px; padding: 1.25rem;
        text-align: center; cursor: pointer;
        transition: all 0.2s;
    }
    .diet-card:hover { border-color: #F5C842; background: #fffef5; }
    .diet-card.selected { border-color: #1C2C6B; background: #1C2C6B; color: white; }
    .diet-emoji { font-size: 2rem; display: block; margin-bottom: 8px; }
    .diet-label { font-size: 0.85rem; font-weight: 700; }

    /* Budget slider */
    .budget-display {
        text-align: center; margin: 1rem 0;
        font-size: 2.5rem; font-weight: 800;
        color: #1C2C6B;
    }
    .budget-display span { color: #F5C842; }

    /* Chat styles */
    .chat-container {
        background: #f8f9fa;
        border-radius: 16px;
        padding: 1.5rem;
        max-height: 500px;
        overflow-y: auto;
        margin-bottom: 1rem;
    }
    .msg-user {
        background: #1C2C6B; color: white;
        border-radius: 16px 16px 4px 16px;
        padding: 0.75rem 1rem; margin: 0.5rem 0 0.5rem 20%;
        font-size: 0.9rem; line-height: 1.5;
    }
    .msg-ai {
        background: white; color: #1C2C6B;
        border: 2px solid #F5C842;
        border-radius: 16px 16px 16px 4px;
        padding: 0.75rem 1rem; margin: 0.5rem 20% 0.5rem 0;
        font-size: 0.9rem; line-height: 1.6;
        white-space: pre-wrap;
    }
    .msg-ai .agent-name {
        font-size: 0.7rem; font-family: 'DM Mono', monospace;
        color: #F5C842; font-weight: 600;
        letter-spacing: 1px; display: block; margin-bottom: 6px;
    }

    /* Thinking animation */
    .thinking {
        display: flex; align-items: center; gap: 8px;
        padding: 1rem; color: #1C2C6B;
        font-family: 'DM Mono', monospace; font-size: 0.8rem;
    }
    .dots span {
        display: inline-block; width: 8px; height: 8px;
        background: #F5C842; border-radius: 50%;
        animation: bounce 1.4s infinite;
    }
    .dots span:nth-child(2) { animation-delay: 0.2s; }
    .dots span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes bounce {
        0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
        40% { transform: scale(1); opacity: 1; }
    }

    /* Profile card */
    .profile-card {
        background: #1C2C6B; color: white;
        border-radius: 16px; padding: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .profile-title {
        font-size: 0.7rem; font-family: 'DM Mono', monospace;
        letter-spacing: 2px; color: #F5C842;
        text-transform: uppercase; margin-bottom: 1rem;
    }
    .profile-row { display: flex; justify-content: space-between; margin-bottom: 8px; }
    .profile-key { font-size: 0.8rem; color: rgba(255,255,255,0.6); }
    .profile-val { font-size: 0.8rem; font-weight: 700; color: #F5C842; }

    /* Primary button */
    .stButton > button {
        background: #1C2C6B !important;
        color: #F5C842 !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'Syne', sans-serif !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        transition: all 0.2s !important;
        width: 100%;
    }
    .stButton > button:hover {
        background: #F5C842 !important;
        color: #1C2C6B !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(28,44,107,0.3) !important;
    }

    /* Slider */
    .stSlider > div > div > div { background: #F5C842 !important; }

    /* Input */
    .stTextInput > div > div > input {
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 0.75rem !important;
        font-family: 'Syne', sans-serif !important;
    }
    .stTextInput > div > div > input:focus { border-color: #F5C842 !important; }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 12px !important;
        border: 2px solid #e0e0e0 !important;
    }

    /* Footer */
    .rasaplan-footer {
        background: #1C2C6B; color: rgba(255,255,255,0.6);
        text-align: center; padding: 2rem;
        font-size: 0.8rem; font-family: 'DM Mono', monospace;
        margin-top: 2rem;
    }
    .rasaplan-footer strong { color: #F5C842; }
    </style>
    """, unsafe_allow_html=True)


def show_hero():
    """Renders the full 3D motion graphic hero section."""
    html(HERO_HTML, height=1000, scrolling=False)


def show_profile_card():
    """Renders the student profile card."""
    p = st.session_state.profile
    st.markdown(f"""
    <div class="profile-card">
        <div class="profile-title">🧑‍🎓 Your Profile</div>
        <div class="profile-row"><span class="profile-key">Weekly Budget</span><span class="profile-val">LKR {p['budget_lkr']}</span></div>
        <div class="profile-row"><span class="profile-key">Daily Budget</span><span class="profile-val">LKR {p['budget_lkr']//7:.0f}</span></div>
        <div class="profile-row"><span class="profile-key">Diet</span><span class="profile-val">{p['diet'].title()}</span></div>
        <div class="profile-row"><span class="profile-key">Cooking Skill</span><span class="profile-val">{p['skill'].title()}</span></div>
        <div class="profile-row"><span class="profile-key">Preferred Store</span><span class="profile-val">{p['store']}</span></div>
        <div class="profile-row"><span class="profile-key">People</span><span class="profile-val">{p['num_people']}</span></div>
    </div>
    """, unsafe_allow_html=True)


def show_planner_ui():
    """Multi-step planner UI below the hero."""
    st.markdown('<div class="planner-section">', unsafe_allow_html=True)

    # Header
    st.markdown("""
    <div class="section-header">
        <div class="sub">🤖 AI Meal Planner</div>
        <h2>Build Your Week</h2>
    </div>
    """, unsafe_allow_html=True)

    step = st.session_state.step

    # ── STEP 0: API KEY ──
    if step == 0:
        st.markdown("### 🔑 Enter Your OpenAI API Key")
        st.info("Your API key is used only in this session and never stored.")
        api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.api_key,
            type="password",
            placeholder="sk-...",
            label_visibility="collapsed"
        )
        if st.button("Continue →"):
            if api_key and api_key.startswith("sk-"):
                st.session_state.api_key = api_key
                st.session_state.step = 1
                st.rerun()
            else:
                st.error("Please enter a valid OpenAI API key starting with sk-")

    # ── STEP 1: BUDGET ──
    elif step == 1:
        st.markdown("### 💰 Step 1 — Set Your Weekly Budget")
        budget = st.slider(
            "Weekly budget (LKR)",
            min_value=500,
            max_value=10000,
            step=100,
            value=st.session_state.profile["budget_lkr"],
            label_visibility="collapsed"
        )
        st.session_state.profile["budget_lkr"] = budget

        # Tier preview
        if budget < 700:
            tier_msg = "🔴 Ultra-budget: Rice, dhal & eggs only"
            tier_color = "#dc3545"
        elif budget < 1500:
            tier_msg = "🟡 Budget: Rice, eggs, canned fish, basic curries"
            tier_color = "#F5C842"
        elif budget < 3000:
            tier_msg = "🟢 Moderate: Full variety + occasional chicken"
            tier_color = "#28a745"
        else:
            tier_msg = "🎉 Comfortable: Full Sri Lankan spread!"
            tier_color = "#1C2C6B"

        st.markdown(f"""
        <div class="budget-display">LKR <span>{budget:,}</span> / week</div>
        <div style="text-align:center; background:{tier_color}20; border:2px solid {tier_color}40;
             border-radius:10px; padding:12px; color:{tier_color}; font-weight:700; margin-bottom:1rem;">
            {tier_msg}
        </div>
        """, unsafe_allow_html=True)

        num_people = st.selectbox("Number of people", [1, 2, 3, 4], index=0)
        st.session_state.profile["num_people"] = num_people

        if st.button("Next →"):
            st.session_state.step = 2
            st.rerun()

    # ── STEP 2: DIET ──
    elif step == 2:
        st.markdown("### 🥗 Step 2 — Dietary Preference")

        diet_options = {
            "vegetarian": ("🥬", "Vegetarian", "No meat or seafood"),
            "non-vegetarian": ("🍗", "Non-Vegetarian", "Includes chicken & fish"),
            "vegan": ("🌱", "Vegan", "No animal products"),
        }

        current_diet = st.session_state.profile["diet"]

        cols = st.columns(3)
        for i, (key, (emoji, label, desc)) in enumerate(diet_options.items()):
            with cols[i]:
                selected = current_diet == key
                border = "#1C2C6B" if selected else "#e0e0e0"
                bg = "#1C2C6B" if selected else "white"
                color = "white" if selected else "#1C2C6B"
                st.markdown(f"""
                <div style="background:{bg}; border:2px solid {border}; border-radius:12px;
                     padding:1.5rem; text-align:center; margin-bottom:8px;">
                    <div style="font-size:2.5rem;">{emoji}</div>
                    <div style="font-weight:700; color:{color}; margin:8px 0 4px;">{label}</div>
                    <div style="font-size:0.75rem; color:{'rgba(255,255,255,0.7)' if selected else '#999'};">{desc}</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Select {label}", key=f"diet_{key}"):
                    st.session_state.profile["diet"] = key
                    st.rerun()

        cols2 = st.columns(2)
        with cols2[0]:
            if st.button("← Back"):
                st.session_state.step = 1
                st.rerun()
        with cols2[1]:
            if st.button("Next →"):
                st.session_state.step = 3
                st.rerun()

    # ── STEP 3: SKILL + STORE ──
    elif step == 3:
        st.markdown("### 👨‍🍳 Step 3 — Cooking Skill & Store")

        skill = st.radio(
            "Your cooking skill level",
            ["beginner", "intermediate"],
            format_func=lambda x: "🌱 Beginner (simple recipes)" if x == "beginner" else "⭐ Intermediate (more variety)",
            index=0 if st.session_state.profile["skill"] == "beginner" else 1
        )
        st.session_state.profile["skill"] = skill

        store = st.selectbox(
            "Nearest supermarket / market",
            ["Keells", "Arpico", "Cargills Food City", "Pola Market (Local)"],
            index=["Keells", "Arpico", "Cargills Food City", "Pola Market (Local)"].index(
                st.session_state.profile.get("store", "Keells")
            ) if st.session_state.profile.get("store", "Keells") in ["Keells", "Arpico", "Cargills Food City", "Pola Market (Local)"] else 0
        )
        st.session_state.profile["store"] = store

        cols2 = st.columns(2)
        with cols2[0]:
            if st.button("← Back"):
                st.session_state.step = 2
                st.rerun()
        with cols2[1]:
            if st.button("🍛 Generate My Meal Plan!"):
                st.session_state.step = 4
                st.rerun()

    # ── STEP 4: AGENT CHAT ──
    elif step == 4:
        show_profile_card()

        st.markdown("### 🤖 RasaPlan AI Agent")
        st.markdown("*Ask me to plan your week, suggest recipes, swap meals, or build your shopping list!*")

        # Initialize agent if not done
        if st.session_state.agent is None:
            with st.spinner("🍛 Initialising your AI chef..."):
                try:
                    from agent.meal_agent import create_agent
                    from agent.memory import StudentProfile

                    profile_obj = StudentProfile()
                    profile_obj.update(**st.session_state.profile)
                    agent = create_agent(profile_obj, st.session_state.api_key)
                    st.session_state.agent = agent

                    # Auto-generate initial plan
                    p = st.session_state.profile
                    initial_query = (
                        f"Plan my full week of meals. My budget is LKR {p['budget_lkr']} per week. "
                        f"I am {p['diet']} and a {p['skill']} cook. "
                        f"I shop at {p['store']}. "
                        f"Give me a 7-day plan and a shopping list."
                    )
                    st.session_state.messages.append({"role": "user", "content": initial_query})
                    st.session_state.plan_generated = True

                except Exception as e:
                    st.error(f"Could not initialize agent: {e}")
                    st.info("Check your OpenAI API key and try again.")
                    if st.button("← Re-enter API Key"):
                        st.session_state.step = 0
                        st.session_state.agent = None
                        st.rerun()
                    return

        # Display chat history
        chat_html = '<div class="chat-container" id="chat-box">'
        if not st.session_state.messages:
            chat_html += """
            <div style="text-align:center; padding:2rem; color:#999;">
                <div style="font-size:3rem;">🍛</div>
                <p>Your meal plan will appear here!</p>
            </div>"""

        for msg in st.session_state.messages:
            if msg["role"] == "user":
                chat_html += f'<div class="msg-user">🧑‍🎓 {msg["content"]}</div>'
            else:
                content = msg["content"].replace("<", "&lt;").replace(">", "&gt;")
                chat_html += f'<div class="msg-ai"><span class="agent-name">🍛 RASAPLAN AI</span>{content}</div>'

        chat_html += '</div>'
        st.markdown(chat_html, unsafe_allow_html=True)

        # Generate response for pending user message
        pending = [m for m in st.session_state.messages if m["role"] == "user" and
                   (len(st.session_state.messages) <= 1 or
                    st.session_state.messages[-1]["role"] == "user")]

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
            last_user_msg = st.session_state.messages[-1]["content"]
            with st.spinner("🧠 RasaPlan is thinking..."):
                st.markdown("""
                <div class="thinking">
                    <span>🍳 Consulting the AI chef</span>
                    <div class="dots"><span></span><span></span><span></span></div>
                </div>
                """, unsafe_allow_html=True)
                try:
                    response = st.session_state.agent.run(last_user_msg)
                except Exception as e:
                    response = f"⚠️ Hmm, something went wrong: {str(e)}. Try again!"

                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

        # Chat input
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_input(
                "Ask RasaPlan...",
                placeholder="e.g. Swap Wednesday lunch, show me the Pol Roti recipe, add more protein...",
                label_visibility="collapsed"
            )
            cols = st.columns([4, 1])
            with cols[1]:
                send = st.form_submit_button("Send 🍽️")

        if send and user_input.strip():
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.rerun()

        # Quick action buttons
        st.markdown("**Quick actions:**")
        qa_cols = st.columns(3)
        quick_actions = [
            ("📅 Full Week Plan", f"Create my full 7-day meal plan for LKR {st.session_state.profile['budget_lkr']}"),
            ("🛒 Shopping List", "Generate my complete shopping list with LKR totals"),
            ("🔄 Swap a Meal", "Suggest alternatives for today's dinner"),
        ]
        for i, (label, query) in enumerate(quick_actions):
            with qa_cols[i]:
                if st.button(label, key=f"qa_{i}"):
                    st.session_state.messages.append({"role": "user", "content": query})
                    st.rerun()

        qa_cols2 = st.columns(3)
        quick_actions2 = [
            ("🥗 Nutrition Check", "What are the nutritional values of my meals this week?"),
            ("💰 Budget Check", f"Am I within my LKR {st.session_state.profile['budget_lkr']} budget?"),
            ("🍳 Recipe Help", "Give me the full recipe for Pol Roti with steps"),
        ]
        for i, (label, query) in enumerate(quick_actions2):
            with qa_cols2[i]:
                if st.button(label, key=f"qa2_{i}"):
                    st.session_state.messages.append({"role": "user", "content": query})
                    st.rerun()

        # Reset button
        st.markdown("---")
        if st.button("🔄 Start Over"):
            st.session_state.step = 1
            st.session_state.messages = []
            st.session_state.agent = None
            st.session_state.plan_generated = False
            st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="rasaplan-footer">
        <strong>RasaPlan | රිස බාසි</strong> · Built for LB3114 · KDU · Intake 41<br>
        Powered by <strong>LangChain</strong> · <strong>GPT-4o</strong> · <strong>Streamlit</strong> · Real Sri Lankan LKR Prices 🍛
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────
def main():
    inject_global_css()
    show_hero()
    show_planner_ui()


if __name__ == "__main__":
    main()
