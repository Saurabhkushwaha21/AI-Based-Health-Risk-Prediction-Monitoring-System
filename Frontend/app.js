'use strict';
const BASE_URL = "https://your-backend-url.onrender.com";
function initApp() {
  console.log("App loaded ✅");
}

/* ════════════════════════════════════════════════
   HEALTH RISK PREDICTION SYSTEM — app.js
════════════════════════════════════════════════ */
/* ── In-memory user store (simulates backend) ── */
let currentUser = null;
let testCount   = 0;
let lastResult  = null;

/* ═══════════════════════════
   NAVIGATION
═══════════════════════════ */
function showPage(id) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  const pg = document.getElementById(id);
  if (pg) { pg.classList.add('active'); window.scrollTo({ top:0, behavior:'smooth' }); }
}

function goToLogin() { showPage('login-page'); }
function goToDashboard() { closeSidebar(); showPage('dashboard-page'); }

/* ═══════════════════════════
   AUTH — LOGIN
═══════════════════════════ */
function doLogin() {
  const email = document.getElementById('login-email').value.trim().toLowerCase();
  const pass  = document.getElementById('login-pass').value.trim();

  let users = JSON.parse(localStorage.getItem("users")) || [];

  const user = users.find(u => u.email === email && u.password === pass);
  console.log("Entered:", email, pass);
  console.log("Stored users:", users);

  if (user) {
    currentUser = user;
    applyUserToUI();
    showPage('dashboard-page');
    loadHistory();// 🔥 important
  } else {
    alert("Invalid email or password ❌");
  }
}

/* ═══════════════════════════
   AUTH — REGISTER
═══════════════════════════ */
function doRegister() {
  const email = document.getElementById('reg-email').value.trim().toLowerCase();
  const pass = document.getElementById('reg-pass').value.trim();
  const fname = document.getElementById('reg-fname').value;
  const lname = document.getElementById('reg-lname').value;
  const phone = document.getElementById('reg-phone').value;
  const gender = document.getElementById('reg-gender').value;
  const dob = document.getElementById('reg-dob').value;
  const blood = document.getElementById('reg-blood').value;


  if (!email || !pass) {
    alert("Fill all fields");
    return;
  }

  let users = JSON.parse(localStorage.getItem("users")) || [];

  // ✅ check duplicate email
  const exists = users.find(u => u.email === email);
  if (exists) {
    alert("User already exists ❌");
    return;
  }

  /*check password match */

  const cpass = document.getElementById('reg-cpass').value;

  if (pass !== cpass) {
  alert("Passwords do not match ❌");
  return;
  }

  // ✅ save clean data
  users.push({ email, password: pass ,fname, lname,phone,
  gender,
  dob,
  blood});

  localStorage.setItem("users", JSON.stringify(users));

  alert("Registered successfully ✅");

  // 👉 optional: login page pe le jao
  showPage('login-page');
}


/* ═══════════════════════════
   APPLY USER TO UI
═══════════════════════════ */
function applyUserToUI() {
  if (!currentUser) return;
  const fullName = `${currentUser.fname} ${currentUser.lname}`;
  const initials = `${currentUser.fname[0]}${currentUser.lname[0]}`.toUpperCase();

  setText('welcome-name',    currentUser.fname);
  setText('topbar-username', fullName);
  setText('sb-username',     fullName);
  setText('sb-avatar',       initials);

  // Profile section
  setText('prof-name',    fullName);
  setText('prof-email',   currentUser.email);
  setText('prof-phone',   currentUser.phone   || '—');
  setText('prof-gender',  currentUser.gender  || '—');
  setText('prof-blood',   currentUser.blood   || '—');
  setText('prof-dob',     currentUser.dob     || '—');
  setText('prof-avatar',  initials);
  setText('prof-tests',   testCount);
}

function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}

/* ═══════════════════════════
   SIDEBAR TOGGLE (mobile)
═══════════════════════════ */
function toggleSidebar() {
  const sidebar   = document.getElementById('sidebar');
  const overlay   = document.getElementById('sidebar-overlay');
  const hamburger = document.getElementById('hamburger');
  const isOpen    = sidebar.classList.toggle('open');
  overlay.classList.toggle('visible', isOpen);
  if (hamburger) hamburger.classList.toggle('open', isOpen);
  document.body.style.overflow = isOpen ? 'hidden' : '';
}

function closeSidebar() {
  const sidebar   = document.getElementById('sidebar');
  const overlay   = document.getElementById('sidebar-overlay');
  const hamburger = document.getElementById('hamburger');
  sidebar.classList.remove('open');
  overlay.classList.remove('visible');
  if (hamburger) hamburger.classList.remove('open');
  document.body.style.overflow = '';
}

window.addEventListener('resize', () => { if (window.innerWidth >= 768) closeSidebar(); });

/* ═══════════════════════════
   SECTION SWITCHING
═══════════════════════════ */
async function switchSection(sectionId, navEl) {
  // Sections
  if (sectionId === 'section-history') {
    await loadHistory();
  }
  if (sectionId === 'section-reports') {
    await loadHistory();
     loadReports();
   }
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  const sec = document.getElementById(sectionId);
  if (sec) sec.classList.add('active');

  // Nav items
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
  if (navEl) navEl.classList.add('active');

  // Topbar title
  const titles = {
    'section-home':    'Health Dashboard',
    'section-input':   'Input Data',
    'section-history': 'History',
    'section-reports': 'Reports',
    'section-profile': 'My Profile',
  };
  setText('topbar-title', titles[sectionId] || 'Dashboard');

  closeSidebar();
  window.scrollTo({ top:0, behavior:'smooth' });
}

/* ═══════════════════════════
   TAB SWITCHING
═══════════════════════════ */
function switchTab(tabId, btnEl) {
  document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  const pane = document.getElementById(tabId);
  if (pane) pane.classList.add('active');
  if (btnEl) btnEl.classList.add('active');
}

/* ═══════════════════════════
   RISK PREDICTION
═══════════════════════════ */
  // ── Diabetes inputs ──
async function predictRisk() {

  // ── Diabetes inputs ──
  const preg = parseFloat(document.getElementById('pregnancies').value) || 0;
  const glucose = parseFloat(document.getElementById('glucose').value) || 0;
  const bpVal = parseFloat(document.getElementById('bp').value) || 0;
  const skin = parseFloat(document.getElementById('skin').value) || 0;
  const insulin = parseFloat(document.getElementById('insulin').value) || 0;
  const dBmi = parseFloat(document.getElementById('d-bmi').value) || 0;
  const dpf = parseFloat(document.getElementById('dpf').value) || 0;
  const dAge = parseFloat(document.getElementById('d-age').value) || 0;

  // ── Heart inputs ──
  const hAge = parseFloat(document.getElementById('h-age').value) || 0;
  const sex = parseInt(document.getElementById('sex').value) || 0;
  const cp = parseInt(document.getElementById('cp').value) || 0;
  const rbp = parseFloat(document.getElementById('rbp').value) || 0;
  const chol = parseFloat(document.getElementById('chol').value) || 0;
  const fbs = parseInt(document.getElementById('fbs').value) || 0;
  const ecg = parseInt(document.getElementById('ecg').value) || 0;
  const maxHr = parseFloat(document.getElementById('max-hr').value) || 0;
  const angina = parseInt(document.getElementById('angina').value) || 0;
  const oldpeak = parseFloat(document.getElementById('oldpeak').value) || 0;
  const slope = parseInt(document.getElementById('slope').value) || 0;
  const vessels = parseInt(document.getElementById('vessels').value) || 0;
  const thal = parseInt(document.getElementById('thal').value) || 1;

    // inputs (same as yours)...

    const data = {
  diabetes_features: [
    preg, glucose, bpVal, skin, insulin, dBmi, dpf, dAge
  ],
  heart_features: {
    age: hAge,
    sex: sex === 1 ? "Male" : "Female",

    chest_pain_type:
      cp == 0 ? "Typical Angina" :
      cp == 1 ? "Atypical Angina" :
      cp == 2 ? "Non-anginal Pain" : "Asymptomatic",

    resting_blood_pressure: rbp,

    // 🔥 FIX 1 (spelling change)
    cholestoral: chol,
    fasting_blood_sugar:
      fbs == 1 ? "Greater than 120 mg/ml" : "Lower than 120 mg/ml",

    rest_ecg:
      ecg == 0 ? "Normal" :
      ecg == 1 ? "ST-T wave abnormality" :
      "Left ventricular hypertrophy",

    // 🔥 FIX 2 (capital M)
    Max_heart_rate: maxHr,

    exercise_induced_angina: angina == 1 ? "Yes" : "No",

    oldpeak: oldpeak,

    slope:
      slope == 0 ? "Upsloping" :
      slope == 1 ? "Flat" : "Downsloping",

    vessels_colored_by_flourosopy:
    vessels == 0 ? "Zero" :
    vessels == 1 ? "One" :
    vessels == 2 ? "Two" : "Three",

    thalassemia:
      thal == 1 ? "Normal" :
      thal == 2 ? "Fixed Defect" : "Reversible Defect"
  }
};

  // API call//https://127.0.1:8001/predict
  let result;
console.log("Sending data:", data);
try {
  const response = await fetch("BASE_URL/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });

  if (!response.ok) {
    throw new Error("API failed");
  }

  result = await response.json(); // ✅ only once

  console.log("API result:", result);

} catch (err) {
  console.error("Error:", err);
  alert("Backend not working ❌");
  return; // ✅ IMPORTANT (stop further execution)
}

    const diabetesRisk = result["Diabetes_Risk (%)"] || 0;
    const heartRisk = result["Heart_Risk (%)"] || 0;
    const overall = result["Overall_Risk (%)"] || 0;
    // ✅ features calculation (YAHI shift karo)
    const features = [
      { name: 'Glucose', val: clamp(Math.round((glucose - 70) * 0.3), 0, 100) },
      { name: 'Age', val: clamp(Math.round((Math.max(dAge, hAge) - 20) * 1.1), 0, 100) },
      { name: 'BMI', val: clamp(Math.round((dBmi - 18.5) * 3.5), 0, 100) },
      { name: 'Cholesterol', val: clamp(Math.round((chol - 150) * 0.25), 0, 100) },
    ];

  lastResult = { overall, heartRisk, diabetesRisk, features, date: new Date() };
  testCount++;
  setText('stat-tests', testCount);
  setText('prof-tests', testCount);

    renderResults(overall, heartRisk, diabetesRisk, features);
    updateDashboardStats(heartRisk, diabetesRisk);
     
    await loadHistory();
    showPage('results-page');
  }
/* forget password */

  function resetPassword() {
  const email = document.getElementById("fp-email").value.trim().toLowerCase();
  const newPass = document.getElementById("fp-newpass").value.trim();
  const confirmPass = document.getElementById("fp-confirmpass").value.trim();

  if (!email || !newPass || !confirmPass) {
    alert("Fill all fields ❌");
    return;
  }

  if (newPass !== confirmPass) {
    alert("Passwords do not match ❌");
    return;
  }

  let users = JSON.parse(localStorage.getItem("users")) || [];

  // 🔍 find user
  const userIndex = users.findIndex(u => u.email === email);

  if (userIndex === -1) {
    alert("Email not registered ❌");
    return;
  }

  // ✅ update password
  users[userIndex].password = newPass;

  localStorage.setItem("users", JSON.stringify(users));

  alert("Password reset successful ✅");

  goToLogin(); // login page pe redirect
  }

/* ═══════════════════════════
   RENDER RESULTS
═══════════════════════════ */
function renderResults(overall, heart, diabetes, features) {
  // Gauge
  const fill = document.getElementById('gauge-fill');
  const offset = 238 - (overall / 100) * 238;
  setTimeout(() => { if (fill) fill.style.strokeDashoffset = offset; }, 80);

  // Score label
  const oC = riskClass(overall);
  setClass('score-pct',   `gauge-score ${oC.color}`);
  setText('score-pct',    overall + '%');
  setClass('score-label', `gauge-label ${oC.color}`);
  setText('score-label',  oC.label + ' Risk');

  // Pills
  applyPill('heart-pill',   'heart-pct',   'heart-tag',   heart);
  applyPill('diabetes-pill','diabetes-pct','diabetes-tag', diabetes);

  // Feature bars
  const barsEl = document.getElementById('feat-bars');
  if (barsEl) {
    barsEl.innerHTML = features.map(f => `
      <div class="feat-bar">
        <div class="feat-bar-top"><span>${f.name}</span><span>${f.val}%</span></div>
        <div class="feat-track"><div class="feat-fill" data-target="${f.val}%"></div></div>
      </div>`).join('');
    requestAnimationFrame(() => {
      setTimeout(() => {
        barsEl.querySelectorAll('.feat-fill').forEach(el => { el.style.width = el.dataset.target; });
      }, 120);
    });
  }

  // Recommendations
  const allRecs = [
    { icon:'🏃', text:'Exercise at least 30 minutes daily',              cond: overall > 40 },
    { icon:'🥗', text:'Adopt a low-sugar, low-fat balanced diet',        cond: true },
    { icon:'🩸', text:'Monitor blood glucose weekly',                    cond: diabetes > 45 },
    { icon:'❤️', text:'Schedule a cardiac evaluation with your doctor',  cond: heart > 60 },
    { icon:'⚖️', text:'Work toward a healthy BMI (18.5 – 24.9)',         cond: true },
    { icon:'🚭', text:'Avoid smoking and limit alcohol',                 cond: overall > 50 },
    { icon:'😴', text:'Get 7–8 hours of quality sleep nightly',          cond: true },
    { icon:'💊', text:'Consult your doctor about medication review',     cond: overall > 65 },
    { icon:'🧘', text:'Practice stress management and mindfulness',      cond: overall > 45 },
    { icon:'💧', text:'Stay well hydrated — 8+ glasses of water/day',   cond: true },
  ];
  const recs = allRecs.filter(r => r.cond).slice(0, 6);
  const recEl = document.getElementById('rec-list');
  if (recEl) {
    recEl.innerHTML = recs.map(r =>
      `<li><span class="rec-icon">${r.icon}</span>${r.text}</li>`
    ).join('');
  }
}

function applyPill(pillId, pctId, tagId, pct) {
  const c = riskClass(pct);
  setClass(pillId, `risk-pill ${c.bg}`);
  setClass(pctId,  `rp-pct ${c.color}`);
  setText(pctId,   pct + '%');
  setClass(tagId,  `rp-tag ${c.tag}`);
  setText(tagId,   c.label);
}

function setClass(id, cls) {
  const el = document.getElementById(id);
  if (el) el.className = cls;
}

function riskClass(pct) {
  if (pct >= 70) return { color:'c-danger',  bg:'bg-danger',  tag:'tag-danger',  label:'High'   };
  if (pct >= 40) return { color:'c-warning', bg:'bg-warning', tag:'tag-warning', label:'Medium' };
  return             { color:'c-success', bg:'bg-success', tag:'tag-success', label:'Low'    };
}


/* ═══════════════════════════
   HISTORY LOAD FUNCTION
═══════════════════════════ */
async function loadHistory() {
  try {
    const res = await fetch("BASE_URL/history")
    const data = await res.json();
    window.historyData = data;
    console.log("History:", data);

    const container = document.getElementById("history-list");
    const emptyState = document.getElementById("history-empty");

    if (!data || data.length === 0) {
      emptyState.style.display = "block";
      container.innerHTML = "";
      return;
    }

    emptyState.style.display = "none";

    container.innerHTML = data.map(item => `
    <div class="history-card">
      <div class="hc-top">📅 ${item.date}</div>

      <div class="hc-body">
        <div>🩸 ${item.diabetes_risk}%</div>
        <div>❤️ ${item.heart_risk}%</div>
        <div>⚡ ${item.overall_risk}%</div>
      </div>

      <div class="hc-actions">
        <button onclick='viewHistory(${item.id})'>View</button>
        <button onclick='deleteHistory("${item.id}")'>Delete</button>
      </div>
    </div>
  `).join("");
  } catch (err) {
    console.error("History load error:",err)
  }
}
 
/*view history*/
function viewHistory(id) {
  const item = window.historyData.find(i => i.id === id);

  renderResults(
    item.overall_risk,
    item.heart_risk,
    item.diabetes_risk,
    item.input_data?.features || []   // future use
  );
  showPage('results-page');
}
/*delete history*/
async function deleteHistory(id) {
  await fetch(`BASE_URL/${id}`, {
    method: "DELETE"
  });

  loadHistory();
}

/* ═══════════════════════════
   DASHBOARD STAT CARDS
═══════════════════════════ */
function updateDashboardStats(heart, diabetes) {
  const hC = riskClass(heart);
  const dC = riskClass(diabetes);
  const hEl = document.getElementById('stat-heart');
  const dEl = document.getElementById('stat-diab');
  const dtEl= document.getElementById('stat-date');

  if (hEl) { hEl.textContent = heart + '%'; hEl.className = `stat-val ${hC.color}`; }
  if (dEl) { dEl.textContent = diabetes + '%'; dEl.className = `stat-val ${dC.color}`; }
  if (dtEl) {
    dtEl.textContent = new Date().toLocaleDateString('en-IN',{day:'numeric',month:'short'});
  }
}

/* ═══════════════════════════
   KEYBOARD ACCESSIBILITY
═══════════════════════════ */
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeSidebar();
});
document.querySelectorAll('.nav-item').forEach(item => {
  item.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); item.click(); }
  });
});

document.addEventListener("DOMContentLoaded", initApp);
function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}


/* load reports */
function loadReports() {
  const container = document.getElementById("report-data");

  if (!window.historyData || window.historyData.length === 0) {
    container.innerHTML = "No data available";
    return;
  }

  const last = window.historyData[0];

  container.innerHTML = `
    <div>
      <h3>Last Report</h3>
      <p>❤️ Heart Risk: ${last.heart_risk}%</p>
      <p>🩸 Diabetes Risk: ${last.diabetes_risk}%</p>
      <p>⚡ Overall Risk: ${last.overall_risk}%</p>
    </div>
  `;
}