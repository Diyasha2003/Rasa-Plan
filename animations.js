/* ═══════════════════════════════════════════════════════
   RasaPlan | animations.js
   All GSAP animations, particle system, planner interactions
   ═══════════════════════════════════════════════════════ */

gsap.registerPlugin(ScrollTrigger);

/* ════════════════════════════════════
   1. CUSTOM CURSOR
════════════════════════════════════ */
const cursor   = document.getElementById('cursor');
const follower = document.getElementById('cursor-follower');
let mx = 0, my = 0, fx = 0, fy = 0;

document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  cursor.style.left = mx + 'px';
  cursor.style.top  = my + 'px';
});

(function animateFollower() {
  fx += (mx - fx) * 0.10;
  fy += (my - fy) * 0.10;
  follower.style.left = fx + 'px';
  follower.style.top  = fy + 'px';
  requestAnimationFrame(animateFollower);
})();

document.querySelectorAll('a, button, .meal-card, .cat-item, .diet-card, .skill-card, .store-btn').forEach(el => {
  el.addEventListener('mouseenter', () => {
    cursor.textContent = '🍴';
    cursor.style.transform = 'translate(-50%,-50%) scale(1.4)';
    follower.style.transform = 'translate(-50%,-50%) scale(1.5)';
    follower.style.borderColor = 'var(--gold)';
  });
  el.addEventListener('mouseleave', () => {
    cursor.textContent = '🥄';
    cursor.style.transform = 'translate(-50%,-50%) scale(1)';
    follower.style.transform = 'translate(-50%,-50%) scale(1)';
    follower.style.borderColor = 'var(--gold)';
  });
});

/* ════════════════════════════════════
   2. PARTICLE SYSTEM
════════════════════════════════════ */
const canvas = document.getElementById('particle-canvas');
const ctx    = canvas.getContext('2d');

function resizeCanvas() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

const SYMBOLS = ['✦', '·', '•', '◦', '∗', '◌'];
const COLORS  = ['rgba(245,200,66,', 'rgba(255,255,255,'];

const particles = Array.from({ length: 55 }, () => ({
  x:      Math.random() * window.innerWidth,
  y:      Math.random() * window.innerHeight * 2,
  size:   Math.random() * 5 + 2,
  speed:  Math.random() * 0.45 + 0.15,
  drift:  (Math.random() - 0.5) * 0.35,
  opacity:Math.random() * 0.35 + 0.08,
  sym:    SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)],
  col:    COLORS [Math.floor(Math.random() * COLORS.length)],
  rot:    Math.random() * 360,
  rotSpd: (Math.random() - 0.5) * 0.6,
}));

(function drawParticles() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  particles.forEach(p => {
    p.y   -= p.speed;
    p.x   += p.drift;
    p.rot += p.rotSpd;
    if (p.y < -60) {
      p.y = canvas.height + 60;
      p.x = Math.random() * canvas.width;
    }
    ctx.save();
    ctx.globalAlpha = p.opacity;
    ctx.fillStyle   = p.col + p.opacity + ')';
    ctx.font        = `${p.size * 3}px serif`;
    ctx.translate(p.x, p.y);
    ctx.rotate(p.rot * Math.PI / 180);
    ctx.fillText(p.sym, 0, 0);
    ctx.restore();
  });
  requestAnimationFrame(drawParticles);
})();

/* ════════════════════════════════════
   3. GSAP HERO ENTRANCE ANIMATIONS
════════════════════════════════════ */
const heroTl = gsap.timeline({ defaults: { ease: 'power3.out' } });

heroTl
  .to('#badge',     { opacity: 1, y: 0, duration: 0.7 }, 0.3)
  .to('#hero-title',{ opacity: 1, x: 0, duration: 0.85 }, 0.5)
  .to('#hero-si',   { opacity: 1, x: 0, duration: 0.7  }, 0.75)
  .to('#hero-sub',  { opacity: 1, y: 0, duration: 0.7  }, 0.95)
  .to('#cta',       { opacity: 1, y: 0, duration: 0.6  }, 1.15)
  .to('#rh',        { opacity: 1, x: 0, duration: 0.85 }, 0.6)
  .to('#stats',     { opacity: 1, y: 0, duration: 0.7  }, 0.9)
  .to('#tech',      { opacity: 1, y: 0, duration: 0.6  }, 1.1);

/* Orb floating stagger on load */
gsap.from(['.food-orb', '.food-orb-r'], {
  scale: 0, opacity: 0,
  duration: 0.8,
  stagger: 0.12,
  ease: 'back.out(1.7)',
  delay: 0.8
});

/* ════════════════════════════════════
   4. PARALLAX MOUSE TRACKING (Hero)
════════════════════════════════════ */
document.addEventListener('mousemove', e => {
  const cx = window.innerWidth  / 2;
  const cy = window.innerHeight / 2;
  const dx = (e.clientX - cx) / cx;
  const dy = (e.clientY - cy) / cy;

  document.querySelectorAll('.food-orb').forEach((orb, i) => {
    const s = (i + 1) * 9;
    gsap.to(orb, { x: dx * s, y: dy * s, duration: 0.5, ease: 'power2.out' });
  });
  document.querySelectorAll('.food-orb-r').forEach((orb, i) => {
    const s = (i + 1) * 7;
    gsap.to(orb, { x: dx * s, y: dy * s, duration: 0.5, ease: 'power2.out' });
  });
});

/* ════════════════════════════════════
   5. SCROLL REVEAL
════════════════════════════════════ */
const revealEls = document.querySelectorAll('.reveal-up, .reveal-left, .reveal-right');
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.12 });
revealEls.forEach(el => revealObs.observe(el));

/* ════════════════════════════════════
   6. COUNTER ANIMATION (Stats)
════════════════════════════════════ */
function animateCounter(el, target, duration = 1800) {
  let start = null;
  const startVal = 0;
  function step(ts) {
    if (!start) start = ts;
    const progress = Math.min((ts - start) / duration, 1);
    el.textContent = Math.floor(progress * target);
    if (progress < 1) requestAnimationFrame(step);
    else el.textContent = target;
  }
  requestAnimationFrame(step);
}

const statObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      const target = +e.target.dataset.target;
      if (target) animateCounter(e.target, target);
      statObs.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });
document.querySelectorAll('.sn[data-target]').forEach(el => statObs.observe(el));

/* ════════════════════════════════════
   7. STEP PLANNER LOGIC
════════════════════════════════════ */
const plannerState = {
  budget: 2000,
  diet: 'non-vegetarian',
  skill: 'beginner',
  store: 'Keells',
};

/* Budget Slider */
const sliderEl  = document.getElementById('budget-slider');
const displayEl = document.getElementById('budget-display');
const tierEl    = document.getElementById('budget-tier');
const coins     = document.querySelectorAll('.coin');

const TIERS = [
  { max: 700,   color: '#dc3545', icon: '🔴', msg: 'Ultra-Budget: Rice, dhal & eggs only. Very tight!' },
  { max: 1500,  color: '#F5C842', icon: '🟡', msg: 'Budget: Rice, eggs, canned fish, basic curries.' },
  { max: 3000,  color: '#28a745', icon: '🟢', msg: 'Moderate: Full variety + occasional chicken!' },
  { max: 99999, color: '#9db8ff', icon: '🎉', msg: 'Comfortable: Full Sri Lankan spread, snacks & more!' },
];

function updateBudget(val) {
  plannerState.budget = +val;
  displayEl.textContent = (+val).toLocaleString();
  sliderEl.value = val;

  const tier = TIERS.find(t => +val <= t.max);
  tierEl.textContent  = `${tier.icon} Budget Tier: ${tier.msg}`;
  tierEl.style.borderColor = tier.color + '44';
  tierEl.style.color = tier.color;

  // Animate coins
  const pct = (+val - 500) / (10000 - 500);
  const litCoins = Math.ceil(pct * coins.length);
  coins.forEach((c, i) => {
    c.textContent = i < litCoins ? '🪙' : '⚪';
    c.style.transform = i < litCoins ? 'scale(1.15)' : 'scale(1)';
  });
}

if (sliderEl) {
  sliderEl.addEventListener('input', e => updateBudget(e.target.value));
  updateBudget(2000);
}

/* Step navigation */
window.goStep = function(stepNum) {
  document.querySelectorAll('.step-panel').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.step-tab').forEach(t => t.classList.remove('active'));
  document.getElementById('step' + stepNum).classList.add('active');
  document.querySelector(`.step-tab[data-step="${stepNum}"]`).classList.add('active');

  // Scroll to planner
  document.getElementById('planner').scrollIntoView({ behavior: 'smooth', block: 'start' });
};

window.selectDiet = function(el, val) {
  document.querySelectorAll('.diet-card').forEach(c => c.classList.remove('selected'));
  el.classList.add('selected');
  plannerState.diet = val;
  gsap.from(el, { scale: 0.9, duration: 0.3, ease: 'back.out(2)' });
};

window.selectSkill = function(el, val) {
  document.querySelectorAll('.skill-card').forEach(c => c.classList.remove('selected'));
  el.classList.add('selected');
  plannerState.skill = val;
};

window.selectStore = function(el, val) {
  document.querySelectorAll('.store-btn').forEach(b => b.classList.remove('selected-store'));
  el.classList.add('selected-store');
  plannerState.store = val;
};

/* ════════════════════════════════════
   8. MEAL PLAN GENERATOR (Frontend Demo)
   NOTE: In production, this calls the Python/FastAPI backend.
   This demo generates a realistic plan locally for demo purposes.
════════════════════════════════════ */
const MEAL_DB = {
  breakfast: [
    { name: 'Pol Roti',          si: 'පොල් රොටී',     cost: 28,  emoji: '🫓', diet: ['vegetarian','vegan','non-vegetarian'] },
    { name: 'String Hoppers',    si: 'ඉඳිඅප්පම්',      cost: 35,  emoji: '🍜', diet: ['vegetarian','vegan','non-vegetarian'] },
    { name: 'Bread + Egg',       si: 'පාන් + බිත්තර',  cost: 42,  emoji: '🍳', diet: ['vegetarian','non-vegetarian'] },
    { name: 'Kiribath',          si: 'කිරිබත්',        cost: 45,  emoji: '🍚', diet: ['vegetarian','non-vegetarian'] },
    { name: 'Roti + Dhal',       si: 'රොටී + පරිප්පු', cost: 38,  emoji: '🫓', diet: ['vegetarian','vegan','non-vegetarian'] },
    { name: 'Hoppers',           si: 'ආප්ප',           cost: 50,  emoji: '🥞', diet: ['vegetarian','non-vegetarian'] },
  ],
  lunch: [
    { name: 'Rice + Dhal Curry', si: 'බත් + පරිප්පු',  cost: 40,  emoji: '🍛', diet: ['vegetarian','vegan','non-vegetarian'] },
    { name: 'Rice + Mackerel',   si: 'බත් + මාළු',     cost: 75,  emoji: '🐟', diet: ['non-vegetarian'] },
    { name: 'Rice & Curry',      si: 'බත් කරිය',       cost: 60,  emoji: '🍲', diet: ['vegetarian','non-vegetarian'] },
    { name: 'Noodles + Veg',     si: 'නූඩල්ස් + එළවළු',cost: 55,  emoji: '🍜', diet: ['vegetarian','vegan','non-vegetarian'] },
    { name: 'Roti + Curry',      si: 'රොටී + කරිය',    cost: 50,  emoji: '🫓', diet: ['vegetarian','non-vegetarian'] },
    { name: 'Rice + Chicken',    si: 'බත් + කුකුළු',   cost: 110, emoji: '🍗', diet: ['non-vegetarian'] },
  ],
  dinner: [
    { name: 'Egg Roti',          si: 'බිත්තර රොටී',   cost: 45,  emoji: '🥚', diet: ['vegetarian','non-vegetarian'] },
    { name: 'Dhal + Rice',       si: 'පරිප්පු + බත්',  cost: 40,  emoji: '🫘', diet: ['vegetarian','vegan','non-vegetarian'] },
    { name: 'SL Spicy Noodles',  si: 'ස්පයිසි නූඩල්ස්',cost: 60,  emoji: '🍜', diet: ['vegetarian','non-vegetarian'] },
    { name: 'Egg Curry + Rice',  si: 'බිත්තර කරිය',   cost: 55,  emoji: '🥚', diet: ['vegetarian','non-vegetarian'] },
    { name: 'Pol Sambol + Rice', si: 'පොල් සම්බෝල',   cost: 35,  emoji: '🥥', diet: ['vegetarian','vegan','non-vegetarian'] },
    { name: 'Fish Curry + Rice', si: 'මාළු කරිය',      cost: 90,  emoji: '🐟', diet: ['non-vegetarian'] },
  ],
};

const GROCERY_LIST = {
  '🥬 Produce': [
    { name: 'Gotukola bunch',  price: 40  },
    { name: 'Onion 1kg',       price: 240 },
    { name: 'Tomato 500g',     price: 120 },
    { name: 'Carrot 500g',     price: 120 },
    { name: 'Green Chilli',    price: 60  },
  ],
  '🌾 Dry Goods': [
    { name: 'Rice Samba 2kg',  price: 470 },
    { name: 'Dhal 500g',       price: 165 },
    { name: 'Wheat Flour 1kg', price: 160 },
    { name: 'Coconut x3',      price: 300 },
  ],
  '🐟 Protein': [
    { name: 'Eggs 10-pack',    price: 300 },
    { name: 'Mackerel Tin x2', price: 400 },
    { name: 'Dried Fish 100g', price: 250 },
  ],
  '🫙 Spices': [
    { name: 'Curry Powder',    price: 165 },
    { name: 'Coconut Oil 500ml',price: 400},
    { name: 'Turmeric 50g',    price: 70  },
    { name: 'Salt 1kg',        price: 70  },
  ],
};

const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

function pickRandom(arr, diet) {
  const filtered = arr.filter(m => m.diet.includes(diet));
  const pool = filtered.length ? filtered : arr;
  return pool[Math.floor(Math.random() * pool.length)];
}

window.generatePlan = function() {
  goStep(4);

  // Profile summary
  const ps = document.getElementById('profile-summary');
  ps.innerHTML = `
    <div class="pm-item"><span class="pm-label">Budget</span><span class="pm-val">LKR ${plannerState.budget.toLocaleString()}/week</span></div>
    <div class="pm-item"><span class="pm-label">Daily</span><span class="pm-val">LKR ${Math.round(plannerState.budget/7)}/day</span></div>
    <div class="pm-item"><span class="pm-label">Diet</span><span class="pm-val">${plannerState.diet}</span></div>
    <div class="pm-item"><span class="pm-label">Skill</span><span class="pm-val">${plannerState.skill}</span></div>
    <div class="pm-item"><span class="pm-label">Store</span><span class="pm-val">${plannerState.store}</span></div>
  `;

  // Generate week grid
  const wg = document.getElementById('week-grid');
  wg.innerHTML = '';
  let totalCost = 0;

  DAYS.forEach((day, i) => {
    const bf = pickRandom(MEAL_DB.breakfast, plannerState.diet);
    const lu = pickRandom(MEAL_DB.lunch,     plannerState.diet);
    const di = pickRandom(MEAL_DB.dinner,    plannerState.diet);
    const dayTotal = bf.cost + lu.cost + di.cost;
    totalCost += dayTotal;

    const col = document.createElement('div');
    col.className = 'day-col';
    col.style.opacity = 0;
    col.innerHTML = `
      <div class="day-header">${day}</div>
      <div class="day-meal">
        <div class="meal-type bf">☀️ BF</div>
        <div class="meal-name-mini">${bf.emoji} ${bf.name}</div>
        <div class="meal-cost-mini">LKR ${bf.cost}</div>
      </div>
      <div class="day-meal">
        <div class="meal-type lu">🌤 LU</div>
        <div class="meal-name-mini">${lu.emoji} ${lu.name}</div>
        <div class="meal-cost-mini">LKR ${lu.cost}</div>
      </div>
      <div class="day-meal">
        <div class="meal-type di">🌙 DI</div>
        <div class="meal-name-mini">${di.emoji} ${di.name}</div>
        <div class="meal-cost-mini">LKR ${di.cost}</div>
      </div>
    `;
    wg.appendChild(col);

    // Stagger animation
    setTimeout(() => {
      gsap.to(col, { opacity: 1, y: 0, duration: 0.4, ease: 'power2.out' });
    }, i * 80);
  });

  // Shopping list
  const ss = document.getElementById('shopping-section');
  const remaining = plannerState.budget - totalCost;
  let listHTML = `<h4 style="color:var(--gold);margin-bottom:1rem">🛒 Shopping List — ${plannerState.store}</h4>`;
  let totalItems = 0;

  Object.entries(GROCERY_LIST).forEach(([cat, items]) => {
    listHTML += `<div class="shop-group"><div class="shop-group-title">${cat}</div>`;
    items.forEach(item => {
      totalItems += item.price;
      listHTML += `
        <div class="shop-item" onclick="toggleCheck(this)">
          <div class="shop-cb"></div>
          <span class="shop-name">${item.name}</span>
          <span class="shop-price">LKR ${item.price}</span>
        </div>`;
    });
    listHTML += `</div>`;
  });

  listHTML += `
    <div class="total-bar">
      <span>Estimated ingredients total:</span>
      <strong>LKR ${totalItems.toLocaleString()}</strong>
    </div>
    <div class="total-bar" style="margin-top:4px">
      <span>Weekly budget remaining:</span>
      <strong style="color:${remaining >= 0 ? 'var(--gold)' : '#dc3545'}">
        ${remaining >= 0 ? '+' : ''}LKR ${remaining.toLocaleString()}
      </strong>
    </div>`;
  ss.innerHTML = listHTML;
  ss.style.display = 'block';

  // Add first AI message
  addAIMessage(`✅ Your 7-day plan is ready! Total estimated meal cost: **LKR ${totalCost.toLocaleString()}**. You have **LKR ${Math.max(0, remaining).toLocaleString()}** left from your budget. Ask me to swap any meal, show a full recipe, or generate your final shopping list! 🍛`);
};

/* Toggle shopping list item */
window.toggleCheck = function(el) {
  el.classList.toggle('checked');
  const cb = el.querySelector('.shop-cb');
  if (el.classList.contains('checked')) {
    cb.textContent = '✓';
    gsap.from(cb, { scale: 0, duration: 0.3, ease: 'back.out(2)' });
  } else {
    cb.textContent = '';
  }
};

/* ════════════════════════════════════
   9. CHAT LOGIC (Frontend Demo)
   In production, this POST to /api/chat on the FastAPI backend
════════════════════════════════════ */
const CHAT_RESPONSES = {
  'shopping': '🛒 Here\'s your optimised shopping list! Head to ' + (plannerState.store || 'Keells') + ' and pick up: Rice (2kg - LKR 470), Dhal 500g (LKR 165), Eggs 10pk (LKR 300), Coconut x3 (LKR 300), Mixed vegetables (LKR 400), Spices bundle (LKR 400). Total ≈ LKR 2,035. Adjust quantities based on your exact plan!',
  'swap': '🔄 Swap suggestion: Instead of your current meal, try **Egg Roti** (LKR 45, 20 mins) or **Dhal + Rice** (LKR 40, 25 mins). Both are filling, cheap, and rasai! Which would you prefer?',
  'recipe': '📝 **Pol Roti Recipe:**\n1. Mix 200g flour + ½ grated coconut + 1 diced onion + 2 chillis + salt\n2. Add water gradually to make firm dough\n3. Divide into 6 balls, flatten to 5mm thick\n4. Cook on medium heat 4 mins each side until golden\n5. Serve with pol sambol or lunu miris 🥥\n\nCost: LKR 28/serving | Time: 20 mins',
  'budget': `💰 Budget Check:\n• Weekly budget: LKR ${plannerState.budget?.toLocaleString() || '2,000'}\n• Daily budget: LKR ${Math.round((plannerState.budget || 2000)/7)}\n• Per meal: LKR ${Math.round((plannerState.budget || 2000)/21)}\n\nYour plan fits within budget! You\'re saving money compared to buying takeaway (avg LKR 350-500/meal). 🎉`,
  'nutrition': '🥗 Nutrition snapshot for today:\n• Breakfast (Pol Roti): ~280 cal, 8g protein\n• Lunch (Rice + Dhal): ~520 cal, 18g protein\n• Dinner (Egg Roti): ~340 cal, 14g protein\n• **Total: ~1,140 cal, 40g protein** ✅ On track for a healthy day!',
  'protein': '💪 To boost protein on your budget:\n• Add an extra egg to breakfast (+LKR 30)\n• Switch to Mackerel Curry for lunch (LKR 75 — great protein!)\n• Evening snack: peanuts or yoghurt (+LKR 40)\nThis adds ~25g more protein for just LKR 145 extra!',
  'default': '🍛 Great question! I can help you with:\n• 📅 Meal swaps (say "swap Monday lunch")\n• 📝 Recipes (say "show me Dhal recipe")\n• 🛒 Shopping list (say "shopping list")\n• 💰 Budget check (say "am I within budget")\n• 🥗 Nutrition info (say "nutrition check")\n\nWhat would you like? Rasai! 😊',
};

function addAIMessage(text) {
  const box = document.getElementById('chat-box');
  const msg = document.createElement('div');
  msg.className = 'chat-msg ai';
  msg.innerHTML = `<span class="ai-label">🍛 RASAPLAN AI</span>${text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/\n/g, '<br>')}`;
  box.appendChild(msg);
  box.scrollTop = box.scrollHeight;
  gsap.from(msg, { opacity: 0, x: -20, duration: 0.4, ease: 'power2.out' });
}

function addUserMessage(text) {
  const box = document.getElementById('chat-box');
  const msg = document.createElement('div');
  msg.className = 'chat-msg user';
  msg.textContent = text;
  box.appendChild(msg);
  box.scrollTop = box.scrollHeight;
  gsap.from(msg, { opacity: 0, x: 20, duration: 0.3, ease: 'power2.out' });
}

function getAIResponse(text) {
  const t = text.toLowerCase();
  if (t.includes('shop') || t.includes('list') || t.includes('buy'))   return CHAT_RESPONSES.shopping;
  if (t.includes('swap') || t.includes('change') || t.includes('alternative')) return CHAT_RESPONSES.swap;
  if (t.includes('recipe') || t.includes('how') || t.includes('pol roti')) return CHAT_RESPONSES.recipe;
  if (t.includes('budget') || t.includes('cost') || t.includes('money')) return CHAT_RESPONSES.budget;
  if (t.includes('nutrition') || t.includes('calorie') || t.includes('healthy')) return CHAT_RESPONSES.nutrition;
  if (t.includes('protein') || t.includes('muscle') || t.includes('more protein')) return CHAT_RESPONSES.protein;
  return CHAT_RESPONSES.default;
}

window.sendChat = function() {
  const input = document.getElementById('chat-input');
  const val   = input.value.trim();
  if (!val) return;
  addUserMessage(val);
  input.value = '';

  // Thinking dots
  const box = document.getElementById('chat-box');
  const thinking = document.createElement('div');
  thinking.className = 'chat-msg ai';
  thinking.innerHTML = `<span class="ai-label">🍛 RASAPLAN AI</span>
    <span class="thinking-dots">
      <span class="dot-anim"></span><span class="dot-anim"></span><span class="dot-anim"></span>
    </span>`;
  box.appendChild(thinking);
  box.scrollTop = box.scrollHeight;

  setTimeout(() => {
    box.removeChild(thinking);
    addAIMessage(getAIResponse(val));
  }, 1000 + Math.random() * 500);
};

window.quickChat = function(text) {
  document.getElementById('chat-input').value = text;
  sendChat();
};

/* ════════════════════════════════════
   10. STEP TAB CLICK
════════════════════════════════════ */
document.querySelectorAll('.step-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    const step = +tab.dataset.step;
    goStep(step);
  });
});

/* ════════════════════════════════════
   11. GSAP SCROLL ANIMATIONS (cards, sections)
════════════════════════════════════ */
gsap.utils.toArray('.meal-card').forEach((card, i) => {
  gsap.fromTo(card,
    { opacity: 0, y: 50 },
    { opacity: 1, y: 0, duration: 0.6, delay: i * 0.1,
      scrollTrigger: { trigger: card, start: 'top 85%', toggleActions: 'play none none reverse' }
    }
  );
});

gsap.utils.toArray('.cat-item').forEach((item, i) => {
  gsap.fromTo(item,
    { opacity: 0, y: 30, scale: 0.8 },
    { opacity: 1, y: 0, scale: 1, duration: 0.5, delay: i * 0.07,
      scrollTrigger: { trigger: item, start: 'top 88%' }
    }
  );
});

/* Fresh bowl parallax */
gsap.to('#bowl', {
  y: -40,
  scrollTrigger: {
    trigger: '.fresh-section',
    start: 'top bottom',
    end: 'bottom top',
    scrub: 1.5,
  }
});

console.log('%c🍛 RasaPlan | රිස බාසි', 'color:#F5C842; font-size:18px; font-weight:bold;');
console.log('%cLB3114 · KDU · Intake 41', 'color:#9db8ff; font-size:12px;');
