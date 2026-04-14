from flask import Flask, request, jsonify, render_template_string
import re
import string
from collections import Counter

app = Flask(__name__)

def analyze_text(text):
    if not text.strip():
        return {"error": "No text provided"}

    # Basic counts
    char_count = len(text)
    char_no_spaces = len(text.replace(" ", "").replace("\n", ""))
    words = re.findall(r'\b\w+\b', text.lower())
    word_count = len(words)
    sentences = re.split(r'[.!?]+', text)
    sentence_count = len([s for s in sentences if s.strip()])
    lines = text.split("\n")
    line_count = len(lines)
    paragraph_count = len([p for p in re.split(r'\n\s*\n', text.strip()) if p.strip()])

    # Word frequency
    word_freq = Counter(words)
    stop_words = {"the","a","an","and","or","but","in","on","at","to","for",
                  "of","with","by","from","is","are","was","were","be","been",
                  "have","has","had","do","does","did","will","would","could",
                  "should","may","might","it","its","this","that","these","those",
                  "i","you","he","she","we","they","my","your","his","her","our"}
    meaningful_words = {w: c for w, c in word_freq.items() if w not in stop_words and len(w) > 2}
    top_words = sorted(meaningful_words.items(), key=lambda x: x[1], reverse=True)[:10]

    # Readability
    avg_word_len = sum(len(w) for w in words) / max(word_count, 1)
    avg_sentence_len = word_count / max(sentence_count, 1)

    # Character breakdown
    letters = sum(1 for c in text if c.isalpha())
    digits = sum(1 for c in text if c.isdigit())
    spaces = sum(1 for c in text if c == ' ')
    punctuation = sum(1 for c in text if c in string.punctuation)

    # Unique words
    unique_words = len(set(words))
    lexical_diversity = round(unique_words / max(word_count, 1) * 100, 1)

    # Longest word
    longest_word = max(words, key=len) if words else ""

    # Reading time (avg 200 wpm)
    reading_time_sec = int(word_count / 200 * 60)
    reading_time = f"{reading_time_sec // 60}m {reading_time_sec % 60}s" if reading_time_sec >= 60 else f"{reading_time_sec}s"

    return {
        "char_count": char_count,
        "char_no_spaces": char_no_spaces,
        "word_count": word_count,
        "unique_words": unique_words,
        "sentence_count": sentence_count,
        "line_count": line_count,
        "paragraph_count": paragraph_count,
        "avg_word_length": round(avg_word_len, 1),
        "avg_sentence_length": round(avg_sentence_len, 1),
        "lexical_diversity": lexical_diversity,
        "longest_word": longest_word,
        "reading_time": reading_time,
        "letters": letters,
        "digits": digits,
        "spaces": spaces,
        "punctuation": punctuation,
        "top_words": top_words,
    }

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TextLens — File Analyzer</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --ink: #0f0e0c;
    --paper: #f4f0e8;
    --cream: #e6e0d0;
    --sepia: #8a7055;
    --rust: #a04828;
    --gold: #b07c20;
    --shadow: rgba(15,14,12,0.12);
  }
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  html { font-size: 16px; }
  body {
    background: var(--paper);
    color: var(--ink);
    font-family: 'DM Mono', monospace;
    min-height: 100vh;
    background-image: 
      repeating-linear-gradient(0deg, transparent, transparent 27px, rgba(200,184,154,0.18) 28px);
    position: relative;
  }
  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background: radial-gradient(ellipse at 20% 10%, rgba(201,152,58,0.06) 0%, transparent 60%),
                radial-gradient(ellipse at 80% 90%, rgba(184,92,56,0.06) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
  }

  header {
    border-bottom: 2px solid var(--ink);
    padding: 2rem 3rem;
    display: flex;
    align-items: baseline;
    gap: 1.5rem;
    position: relative;
    z-index: 1;
    background: var(--paper);
  }
  header h1 {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1;
  }
  header span {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 400;
    color: var(--sepia);
    text-transform: uppercase;
    letter-spacing: 0.18em;
  }
  header .edition {
    margin-left: auto;
    font-size: 0.65rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--sepia);
    border: 1.5px solid var(--sepia);
    padding: 0.3rem 0.7rem;
  }

  main {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    min-height: calc(100vh - 90px);
    position: relative;
    z-index: 1;
  }

  .input-panel {
    border-right: 2px solid var(--ink);
    padding: 2.5rem 3rem;
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
  }
  .panel-label {
    font-size: 0.65rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.22em;
    color: var(--sepia);
    border-bottom: 1px solid var(--cream);
    padding-bottom: 0.6rem;
    margin-bottom: 0.3rem;
  }

  .drop-zone {
    border: 2px dashed var(--sepia);
    padding: 1.8rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s;
    background: var(--cream);
    font-size: 0.78rem;
    font-weight: 400;
    letter-spacing: 0.05em;
    color: #6a5540;
  }
  .drop-zone:hover, .drop-zone.drag-over {
    border-color: var(--rust);
    color: var(--rust);
    background: #f9f5ed;
  }
  .drop-zone input { display: none; }

  textarea {
    width: 100%;
    flex: 1;
    min-height: 320px;
    background: transparent;
    border: 1.5px solid var(--sepia);
    border-radius: 0;
    padding: 1.2rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.85rem;
    font-weight: 400;
    color: var(--ink);
    resize: vertical;
    line-height: 1.75;
    outline: none;
    transition: border-color 0.2s;
  }
  textarea::placeholder { color: #9a8060; opacity: 1; }
  textarea:focus { border-color: var(--rust); }

  .btn-analyze {
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    background: var(--ink);
    color: var(--paper);
    border: none;
    padding: 1rem 2rem;
    cursor: pointer;
    transition: all 0.2s;
    width: 100%;
  }
  .btn-analyze:hover {
    background: var(--rust);
    color: #fff;
  }
  .btn-analyze:active { transform: scale(0.99); }

  .results-panel {
    padding: 2.5rem 3rem;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    opacity: 0;
    transform: translateY(8px);
    transition: opacity 0.4s, transform 0.4s;
  }
  .results-panel.visible {
    opacity: 1;
    transform: translateY(0);
  }

  .stats-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    border: 1px solid var(--ink);
  }
  .stat-cell {
    padding: 1rem 1.2rem;
    border-right: 1px solid var(--ink);
    border-bottom: 1px solid var(--ink);
    animation: fadeIn 0.3s ease both;
  }
  .stat-cell:nth-child(even) { border-right: none; }
  .stat-cell:nth-last-child(-n+2) { border-bottom: none; }
  .stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--rust);
    display: block;
    line-height: 1.1;
  }
  .stat-label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--sepia);
    margin-top: 0.2rem;
    display: block;
  }

  .section-title {
    font-size: 0.62rem;
    text-transform: uppercase;
    letter-spacing: 0.22em;
    color: var(--sepia);
    border-bottom: 1px solid var(--cream);
    padding-bottom: 0.5rem;
  }

  .composition-row {
    display: flex;
    gap: 0.5rem;
    align-items: stretch;
    height: 6px;
    border-radius: 0;
    overflow: hidden;
    margin-top: 0.5rem;
  }
  .comp-bar { height: 100%; transition: width 0.5s; }
  .bar-letters { background: var(--rust); }
  .bar-spaces  { background: var(--sepia); }
  .bar-digits  { background: var(--gold); }
  .bar-punct   { background: var(--ink); }
  .comp-legend {
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem;
    margin-top: 0.8rem;
  }
  .legend-item {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.65rem;
    letter-spacing: 0.08em;
    color: var(--ink);
  }
  .legend-dot { width: 8px; height: 8px; border-radius: 50%; }

  .top-words { display: flex; flex-direction: column; gap: 0.4rem; }
  .word-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    animation: slideIn 0.3s ease both;
  }
  .word-text {
    font-size: 0.75rem;
    font-weight: 500;
    min-width: 90px;
    color: var(--ink);
  }
  .word-bar-wrap {
    flex: 1;
    height: 4px;
    background: var(--cream);
  }
  .word-bar {
    height: 100%;
    background: var(--gold);
    transition: width 0.5s;
  }
  .word-count {
    font-size: 0.65rem;
    color: var(--sepia);
    min-width: 24px;
    text-align: right;
  }

  .meta-row {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
  }
  .meta-item { font-size: 0.72rem; }
  .meta-item strong {
    font-weight: 500;
    color: var(--rust);
    display: block;
    font-family: 'Playfair Display', serif;
    font-size: 0.95rem;
  }

  .placeholder-msg {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    gap: 0.6rem;
    color: var(--sepia);
    text-align: center;
  }
  .placeholder-msg p { font-size: 0.7rem; letter-spacing: 0.1em; opacity: 0.7; }
  .placeholder-msg .big { font-family: 'Playfair Display', serif; font-style: italic; font-size: 1.6rem; opacity: 0.3; }

  @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes slideIn { from { opacity: 0; transform: translateX(-6px); } to { opacity: 1; transform: translateX(0); } }

  @media (max-width: 768px) {
    main { grid-template-columns: 1fr; }
    .input-panel { border-right: none; border-bottom: 2px solid var(--ink); }
    header { padding: 1.2rem 1.5rem; }
    .input-panel, .results-panel { padding: 1.5rem; }
  }
</style>
</head>
<body>
<header>
  <h1>TextLens</h1>
  <span>Text File Analyzer</span>
  <span class="edition">v1.0 · Python + Flask</span>
</header>
<main>
  <div class="input-panel">
    <div class="panel-label">Input</div>

    <div class="drop-zone" id="dropZone">
      <input type="file" id="fileInput" accept=".txt,.md,.csv,.log,.py,.js,.html,.css">
      <p>Drop a file here or <strong style="color:var(--rust);cursor:pointer" onclick="document.getElementById('fileInput').click()">browse</strong></p>
      <p style="margin-top:0.3rem;font-size:0.65rem;opacity:0.7">.txt .md .csv .log .py .js and more</p>
    </div>

    <div class="panel-label" style="margin-top:0.5rem">— or paste text —</div>
    <textarea id="textInput" placeholder="Paste your text here…"></textarea>

    <button class="btn-analyze" onclick="analyze()">Analyze Text →</button>
  </div>

  <div class="results-panel" id="results">
    <div class="placeholder-msg" id="placeholder">
      <div class="big">Awaiting text…</div>
      <p>Upload a file or paste text, then click Analyze</p>
    </div>
  </div>
</main>

<script>
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');
  const textInput = document.getElementById('textInput');

  dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('drag-over'); });
  dropZone.addEventListener('dragleave', () => dropZone.classList.remove('drag-over'));
  dropZone.addEventListener('drop', e => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    const file = e.dataTransfer.files[0];
    if (file) readFile(file);
  });
  fileInput.addEventListener('change', () => { if (fileInput.files[0]) readFile(fileInput.files[0]); });

  function readFile(file) {
    const reader = new FileReader();
    reader.onload = e => { textInput.value = e.target.result; };
    reader.readAsText(file);
  }

  async function analyze() {
    const text = textInput.value;
    if (!text.trim()) { textInput.focus(); return; }

    const btn = document.querySelector('.btn-analyze');
    btn.textContent = 'Analyzing…';
    btn.disabled = true;

    try {
      const res = await fetch('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const data = await res.json();
      renderResults(data);
    } finally {
      btn.textContent = 'Analyze Text →';
      btn.disabled = false;
    }
  }

  function renderResults(d) {
    if (d.error) { alert(d.error); return; }

    const total = d.letters + d.digits + d.spaces + d.punctuation || 1;
    const pct = v => ((v / total) * 100).toFixed(1);

    const maxWord = d.top_words.length ? d.top_words[0][1] : 1;

    const panel = document.getElementById('results');
    panel.innerHTML = `
      <div>
        <div class="section-title">Overview</div>
        <div class="stats-grid" style="margin-top:0.8rem">
          <div class="stat-cell"><span class="stat-value">${d.word_count.toLocaleString()}</span><span class="stat-label">Words</span></div>
          <div class="stat-cell"><span class="stat-value">${d.char_count.toLocaleString()}</span><span class="stat-label">Characters</span></div>
          <div class="stat-cell"><span class="stat-value">${d.sentence_count.toLocaleString()}</span><span class="stat-label">Sentences</span></div>
          <div class="stat-cell"><span class="stat-value">${d.paragraph_count.toLocaleString()}</span><span class="stat-label">Paragraphs</span></div>
        </div>
      </div>

      <div>
        <div class="section-title">Metrics</div>
        <div class="meta-row" style="margin-top:0.8rem">
          <div class="meta-item"><strong>${d.unique_words.toLocaleString()}</strong>Unique words</div>
          <div class="meta-item"><strong>${d.lexical_diversity}%</strong>Lexical diversity</div>
          <div class="meta-item"><strong>${d.avg_word_length}</strong>Avg word length</div>
          <div class="meta-item"><strong>${d.avg_sentence_length}</strong>Words / sentence</div>
          <div class="meta-item"><strong>${d.reading_time}</strong>Reading time</div>
          <div class="meta-item"><strong>${d.longest_word}</strong>Longest word</div>
        </div>
      </div>

      <div>
        <div class="section-title">Character Composition</div>
        <div class="composition-row" style="margin-top:0.8rem">
          <div class="comp-bar bar-letters" style="width:${pct(d.letters)}%"></div>
          <div class="comp-bar bar-spaces"  style="width:${pct(d.spaces)}%"></div>
          <div class="comp-bar bar-digits"  style="width:${pct(d.digits)}%"></div>
          <div class="comp-bar bar-punct"   style="width:${pct(d.punctuation)}%"></div>
        </div>
        <div class="comp-legend">
          <div class="legend-item"><div class="legend-dot" style="background:var(--rust)"></div>Letters (${pct(d.letters)}%)</div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--sepia)"></div>Spaces (${pct(d.spaces)}%)</div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--gold)"></div>Digits (${pct(d.digits)}%)</div>
          <div class="legend-item"><div class="legend-dot" style="background:var(--ink)"></div>Punctuation (${pct(d.punctuation)}%)</div>
        </div>
      </div>

      <div>
        <div class="section-title">Top Words (filtered stop words)</div>
        <div class="top-words" style="margin-top:0.8rem">
          ${d.top_words.map(([w, c], i) => `
            <div class="word-row" style="animation-delay:${i * 0.04}s">
              <span class="word-text">${w}</span>
              <div class="word-bar-wrap"><div class="word-bar" style="width:${(c/maxWord*100).toFixed(0)}%"></div></div>
              <span class="word-count">${c}</span>
            </div>
          `).join('')}
        </div>
      </div>
    `;

    panel.classList.add('visible');
  }
</script>
</body>
</html>"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    text = data.get("text", "")
    return jsonify(analyze_text(text))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
