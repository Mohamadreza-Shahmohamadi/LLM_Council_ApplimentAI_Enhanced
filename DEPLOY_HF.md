# Deploying to Hugging Face Spaces (The "One Docker Space" Method)

This guide will help you deploy the full stack (FastAPI + React) to a single Hugging Face Docker Space.

## Prerequisites
1. A Hugging Face account (Free)
2. Git installed locally
3. Your OpenRouter API Key

## Deployment Steps

### 1. Create a New Space
1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. **Space Name**: `llm-council`
3. **License**: MIT
4. **SDK**: Docker
5. **Space Hardware**: CPU Basic (Free - 2 vCPU · 16 GB RAM) - *More than enough!*
6. Click **Create Space**

### 2. Push Your Code
Hugging Face Spaces are git repositories. You need to push this code to your space.

```bash
# Initialize git if you haven't (just in case)
git init

# Add your files
git add .
git commit -m "Initial commit for HF Spaces"

# Add the HF remote (get the URL from your Space page)
# Format: https://huggingface.co/spaces/YOUR_USERNAME/SPACE_NAME
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/llm-council

# Push to deploy (this triggers the build)
git push space main
```

### 3. Configure Environment Variables
Your app needs API keys to work.

1. Go to your Space's **Settings** tab.
2. Scroll to **Variables and secrets**.
3. Click **New Secret** for sensitive keys:
   - `OPENROUTER_API_KEY`: Your key (sk-or-...)
   - `OPENAI_API_KEY`: (Optional)
4. Click **New Variable** for public config:
   - `ENABLE_TOOLS`: `true`
   - `DB_TYPE`: `json` (simplest for Spaces)

### 4. Watch It Build
1. Go to the **App** tab.
2. You'll see "Building". Click **Logs** to watch the Docker build.
3. Once valid, it will say "Running" and show your app!

---

## Domain Configuration (The "Council.Appliment.io" Part)

### Option A: True Custom Domain (Requires HF Pro @ $9/mo)
This enables `https://council.appliment.io` directly.

1. **In Hugging Face Space**: Settings -> Custom Domain -> Enter `council.appliment.io`.
2. **In Hostinger DNS Zone Editor**:
   - **Type**: `CNAME`
   - **Name**: `council`
   - **Target**: `spaces.huggingface.tech`
   - **TTL**: `3600`
3. Wait ~30 mins for propagation.

### Option B: The "Iframe" Workaround ($0 Cost)
This runs the app on HF but displays it on your WordPress site at `appliment.io/council`.

1. **In WordPress**: Install "Blank Slate" or similar plugin to allow full-width, headerless pages.
2. **Create New Page**: Name it "Council". Permalink should be `appliment.io/council`.
3. **Add Custom HTML Block**:
   ```html
   <style>
     body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; }
     iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: none; }
   </style>
   <iframe src="https://YOUR_USERNAME-llm-council.hf.space"></iframe>
   ```
4. **Publish**. 
5. (Optional) In Hostinger, redirect `council.appliment.io` to `appliment.io/council` if you want that URL to work (it will redirect, not mask).

