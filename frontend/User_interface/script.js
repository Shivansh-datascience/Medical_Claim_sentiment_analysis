
const navDashboard = document.getElementById('navDashboard');
const navReports = document.getElementById('navReports');
const navSettings = document.getElementById('navSettings');

const dashboardSection = document.getElementById('dashboardSection');
const reportsSection = document.getElementById('reportsSection');
const settingsSection = document.getElementById('settingsSection');

navDashboard.addEventListener('click', () => {
  navDashboard.classList.add('active');
  navReports.classList.remove('active');
  navSettings.classList.remove('active');
  dashboardSection.classList.remove('hidden');
  reportsSection.classList.add('hidden');
  settingsSection.classList.add('hidden');
});

navReports.addEventListener('click', () => {
  navReports.classList.add('active');
  navDashboard.classList.remove('active');
  navSettings.classList.remove('active');
  dashboardSection.classList.add('hidden');
  reportsSection.classList.remove('hidden');
  settingsSection.classList.add('hidden');
});

navSettings.addEventListener('click', () => {
  navSettings.classList.add('active');
  navDashboard.classList.remove('active');
  navReports.classList.remove('active');
  dashboardSection.classList.add('hidden');
  reportsSection.classList.add('hidden');
  settingsSection.classList.remove('hidden');
});

// Analysis form submission
const form = document.getElementById('analysisForm');
const textContent = document.getElementById('textContent');
const sentimentEl = document.getElementById('sentiment');
const confidenceEl = document.getElementById('confidence');
const nerList = document.getElementById('nerList');
let lastAnalysis = null;

form.addEventListener('submit', async e => {
  e.preventDefault();
  const text = document.getElementById('medicalText').value;

  try {
    const response = await fetch('http://127.0.0.1:5000/Predict_Sentiment', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ Medical_Claim: text }),
    });

    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    console.log("API returned:", data); // Debugging

    // Parse API response and adapt to UI expectations
    const sentiment = data.Sentiment_Prediction || 'N/A';
    const confidence = data.Sentiment_Score || 0.0;
    const textAnalyzed = data.Sentiment_Text || text;
    const entities = (data.NER_Results || []).map(ent => `${ent.label}: ${ent.text}`);

    // Store for PDF generation
    lastAnalysis = {
      text: textAnalyzed,
      sentiment: sentiment,
      confidence: confidence,
      entities: entities,
    };

    // Update UI
    textContent.textContent = textAnalyzed;
    sentimentEl.textContent = `Sentiment: ${sentiment}`;
    confidenceEl.textContent = `Confidence: ${confidence.toFixed(2)}`;
    nerList.innerHTML = '';
    entities.forEach(entity => {
      const li = document.createElement('li');
      li.textContent = entity;
      nerList.appendChild(li);
    });

  } catch (error) {
    alert('Error during analysis: ' + error.message);
  }
});

// PDF generation
const { jsPDF } = window.jspdf;
const generatePdfBtn = document.getElementById('generatePdfBtn');

generatePdfBtn.addEventListener('click', () => {
  if (!lastAnalysis) {
    alert("Please analyze a medical claim first.");
    return;
  }

  const doc = new jsPDF();

  doc.setFontSize(20);
  doc.text("Medical Sentiment Analysis Report", 20, 20);

  doc.setFontSize(14);
  doc.text("Analyzed Medical Claim:", 20, 35);
  doc.setFontSize(12);
  doc.text(lastAnalysis.text, 20, 45, { maxWidth: 170 });

  doc.setFontSize(14);
  doc.text("Sentiment Analysis:", 20, 70);
  doc.setFontSize(12);
  doc.text(`Sentiment: ${lastAnalysis.sentiment}`, 20, 80);
  doc.text(`Confidence: ${lastAnalysis.confidence.toFixed(2)}`, 20, 90);

  doc.setFontSize(14);
  doc.text("Named Entities:", 20, 110);
  doc.setFontSize(12);

  let y = 120;
  lastAnalysis.entities.forEach((entity) => {
    if (y > 280) {
      doc.addPage();
      y = 20;
    }
    doc.text(`- ${entity}`, 20, y);
    y += 10;
  });

  doc.save("medical_report.pdf");
});

// Settings
const usernameInput = document.getElementById('usernameInput');
const darkModeToggle = document.getElementById('darkModeToggle');
const saveSettingsBtn = document.getElementById('saveSettingsBtn');
const settingsMessage = document.getElementById('settingsMessage');
const userAvatar = document.getElementById('userAvatar');
const usernameDisplay = document.getElementById('usernameDisplay');

window.addEventListener('DOMContentLoaded', () => {
  const savedUsername = localStorage.getItem('username') || 'Shvansh Bajpai';
  const savedDarkMode = localStorage.getItem('darkMode') === 'true';

  usernameInput.value = savedUsername;
  usernameDisplay.textContent = savedUsername;
  userAvatar.textContent = savedUsername.charAt(0).toUpperCase();
  darkModeToggle.checked = savedDarkMode;

  if (savedDarkMode) {
    document.body.classList.add('dark-mode');
  }
});

saveSettingsBtn.addEventListener('click', () => {
  const newUsername = usernameInput.value.trim() || 'Shvansh Bajpai';
  const darkMode = darkModeToggle.checked;

  localStorage.setItem('username', newUsername);
  localStorage.setItem('darkMode', darkMode);

  usernameDisplay.textContent = newUsername;
  userAvatar.textContent = newUsername.charAt(0).toUpperCase();

  if (darkMode) {
    document.body.classList.add('dark-mode');
  } else {
    document.body.classList.remove('dark-mode');
  }

  settingsMessage.textContent = 'Settings saved!';
});

