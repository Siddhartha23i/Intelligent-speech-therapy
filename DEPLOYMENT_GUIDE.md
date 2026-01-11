# Deploying to Hugging Face Spaces 🚀

## 1. Prepare Your Files

### ✅ Essential Files to Upload
You must upload **only** these files and folders:

- `app.py` (Main application)
- `requirements.txt` (Python dependencies - I've updated this for you!)
- `packages.txt` (System dependencies like ffmpeg - I've created this!)
- `modules/` (Folder: contains all your code logic)
- `utils/` (Folder: utility scripts)
- `data/` (Folder: sentence banks)
- `assets/` (Folder: images/styles)

### ❌ Do NOT Upload
- `.venv` (Virtual environment folder)
- `database/` (Or exclude `user_data.db` - let the app create a fresh one)
- `uploads/` (Your test recordings)
- `__pycache__` (Python cache files)
- `.git` (Git history)

---

## 2. Dependencies (Already Fixed!)
I have automatically updated:
- **`requirements.txt`**: Now matches the working "minimal" config.
- **`packages.txt`**: Added `ffmpeg` and `espeak-ng`.

---

## 3. How to Deploy

1. **Create a Space:**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click **"Create new Space"**
   - **Space SDK:** Select `Streamlit`
   - **Hardware:** CPU Basic (Free) is fine

2. **Upload Files:**
   - **Method A (Web Interface):**
     - Go to the "Files" tab of your new Space
     - Click "Add file" -> "Upload files"
     - Drag and drop the folders (`modules`, `utils`, `data`, `assets`) and files (`app.py`, `requirements.txt`, `packages.txt`)
     - Commit changes
   
   - **Method B (Git - Recommended):**
     ```bash
     git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
     cd YOUR_SPACE_NAME
     # Copy your project files here (excluding .venv, .git, etc.)
     git add .
     git commit -m "Initial deploy"
     git push
     ```

3. **Wait for Build:**
   - The "App" tab will show "Building..."
   - Once "Running", your app is live!

---

## 4. Troubleshooting Deployment

- **"Error: ffmpeg not found":** Ensure you uploaded `packages.txt`.
- **"ModuleNotFoundError":** Ensure `requirements.txt` is the one I just updated.
- **"NLTK Error":** The app mimics the self-healing fix we added, so it should auto-download NLTK data.
