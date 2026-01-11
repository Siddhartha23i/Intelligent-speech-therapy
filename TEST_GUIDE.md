# 🧪 Testing Guide - Speech Therapy Platform

## Quick Start Testing

### 1️⃣ Install & Run

```powershell
# Install dependencies
pip install -r requirements.txt

# Additional package for the test recorder (optional)
pip install sounddevice

# Run the main application
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🎙️ Getting Audio for Testing

### Method 1: Browser Recording (Recommended ✅)
**This is the easiest way!**

1. Run `streamlit run app.py`
2. Go to the Practice page
3. Click the **audio input widget**
4. **Allow microphone permissions** when prompted
5. Speak one of the practice sentences clearly
6. Click "Analyze My Pronunciation"

### Method 2: Using the Test Recorder Script

```powershell
# Run the test recorder
python record_test_audio.py
```

This will:
- Prompt you for recording duration
- Record audio from your microphone
- Save it to the `uploads/` folder
- You can then use these files for testing

### Method 3: Download Sample Audio

Download free speech samples from:
- [Mozilla Common Voice](https://commonvoice.mozilla.org/en/datasets)
- [LibriVox](https://librivox.org/) (audiobooks)
- [Freesound](https://freesound.org/) (search: "speech")

Save them to the `uploads/` folder.

---

## 🧪 Testing Checklist

### Basic Functionality
- [ ] App starts without errors
- [ ] Practice page loads
- [ ] Can select sentences from dropdown
- [ ] "Random Sentence" button works
- [ ] Audio recorder appears
- [ ] Can record audio (browser permissions granted)
- [ ] "Analyze My Pronunciation" button responds
- [ ] Results display with score
- [ ] Feedback text appears
- [ ] Recommendations show up

### Dashboard Tests
- [ ] Dashboard shows welcome message (first time)
- [ ] After practice, statistics appear
- [ ] Score trend chart displays
- [ ] Phoneme heatmap shows
- [ ] Recent sessions table appears

### Settings Tests
- [ ] User ID displays
- [ ] Account statistics show
- [ ] "Reset User ID" button works
- [ ] Data persists across sessions

### Edge Cases
- [ ] Test with very short audio (< 1 second)
- [ ] Test with long audio (> 10 seconds)
- [ ] Test with background noise
- [ ] Test with incorrect sentence (say different words)
- [ ] Test with mumbling/unclear speech

---

## 📊 Sample Test Sentences

Use these sentences for comprehensive testing:

### General Practice
1. **The quick brown fox jumps over the lazy dog.**
2. **She sells seashells by the seashore.**
3. **How much wood would a woodchuck chuck?**

### Phoneme-Specific (TH sound)
4. **The three thieves thought they'd throw the throne.**
5. **I think that this thing is thick.**

### Phoneme-Specific (R sound)
6. **Red lorry, yellow lorry, red lorry, yellow lorry.**
7. **Really rural, really rural.**

### Phoneme-Specific (L sound)
8. **Literally little lollipops lined the lobby.**
9. **Lovely lavender lilacs bloom in April.**

---

## 🐛 Troubleshooting

### Microphone Not Working
**Problem:** Browser can't access microphone

**Solutions:**
1. Check browser permissions (click lock icon in address bar)
2. Allow microphone access for localhost
3. Try a different browser (Chrome/Edge recommended)
4. Check Windows microphone settings

### App Won't Start
**Problem:** `streamlit run app.py` fails

**Solutions:**
1. Verify you're in the correct directory
2. Check Python version (3.8+ required)
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
4. Check error messages for missing packages

### Slow Analysis
**Problem:** "Analyze" button takes forever

**Solutions:**
- First run is always slower (downloads AI models)
- Subsequent runs will be faster
- Check internet connection (for model download)
- Use shorter sentences for testing

### Low Scores Always
**Problem:** Always getting low scores

**Checklist:**
- Are you reading the exact sentence shown?
- Is microphone quality good?
- Is there background noise?
- Are you speaking clearly and at normal pace?

---

## 🎯 Expected Results

### Good Recording
- **Overall Score:** 70-95
- **Fluency Score:** 75-95
- **Feedback:** "Great job!" or "Very good!"
- **Weak Phonemes:** 0-2 phonemes listed

### Poor Recording (expected with bad conditions)
- **Overall Score:** 40-69
- **Fluency Score:** 50-75
- **Feedback:** "Keep practicing" or "Needs improvement"
- **Weak Phonemes:** 3+ phonemes listed

---

## 📁 Test Data Locations

- **Audio Files:** `uploads/` directory
- **Database:** `database/sessions.db`
- **Models Cache:** `models/` directory
- **Sentence Banks:** `data/sentence_banks/`

---

## 🔬 Advanced Testing

### Create Custom Test Cases

Edit sentence banks in `data/sentence_banks/`:
- `general_practice.txt`
- `phoneme_th.txt`
- `phoneme_r.txt`
- `phoneme_l.txt`
- `phoneme_v.txt`

Add your own sentences (one per line).

### Database Inspection

```powershell
# Install SQLite browser
# Or use command line
sqlite3 database/sessions.db
```

```sql
-- View all sessions
SELECT * FROM sessions;

-- View user statistics
SELECT user_id, COUNT(*) as session_count 
FROM sessions 
GROUP BY user_id;
```

---

## ✅ Success Criteria

Your app is working correctly if:
1. ✅ You can record audio without errors
2. ✅ Analysis completes within 30 seconds
3. ✅ You receive a numerical score
4. ✅ Feedback text is displayed
5. ✅ Dashboard updates after practice
6. ✅ Data persists when you restart the app

---

## 💡 Tips for Best Test Results

1. **Use a quiet environment** - Reduces background noise
2. **Speak clearly** - Natural pace, not too fast or slow
3. **Read exactly what's shown** - Word-for-word accuracy matters
4. **Use good microphone** - Built-in laptop mics work, but external is better
5. **Practice multiple times** - See your progress in the dashboard!

---

## 🚀 Next Steps After Testing

1. **Review the code** - Understand how each module works
2. **Customize sentence banks** - Add sentences for specific phonemes
3. **Deploy to Hugging Face** - Share with others
4. **Add features** - Extend functionality
5. **Improve UX** - Enhance the user interface

---

**Happy Testing! 🎉**
