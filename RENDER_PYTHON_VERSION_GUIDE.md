# 📍 Where to Find Python Version in Render

## Step-by-Step Guide

### Method 1: Settings Tab (Recommended)

1. **Go to Render Dashboard:**
   - Visit [https://dashboard.render.com](https://dashboard.render.com)
   - Log in to your account

2. **Select Your Service:**
   - Click on your backend service name (e.g., "real-estate-backend")
   - This opens the service details page

3. **Open Settings Tab:**
   - Look at the top of the page for tabs: **"Logs"**, **"Metrics"**, **"Settings"**, etc.
   - Click on **"Settings"** tab

4. **Find Python Version:**
   - Scroll down in the Settings page
   - Look for a section called:
     - **"Python Version"** OR
     - **"Environment"** OR
     - **"Build & Deploy"**
   - You'll see a dropdown or input field for Python version

5. **Set Python Version:**
   - If it's a dropdown: Select **"Python 3.11"** or **"3.11.0"**
   - If it's an input field: Type `python-3.11.0` or `3.11.0`
   - Click **"Save Changes"** button

### Method 2: Environment Tab

1. **Go to Your Service**
2. **Click "Environment" tab** (instead of Settings)
3. **Look for Python-related environment variables:**
   - Sometimes Python version is set via environment variable
   - Look for `PYTHON_VERSION` or similar

### Method 3: Build & Deploy Settings

1. **Go to Your Service**
2. **Click "Settings" tab**
3. **Scroll to "Build & Deploy" section**
4. **Look for "Python Version"** in this section

## Visual Guide

```
Render Dashboard
├── Your Service Name (click here)
    ├── Logs (tab)
    ├── Metrics (tab)
    ├── Settings (tab) ← CLICK HERE
    │   ├── General Settings
    │   ├── Environment Variables
    │   ├── Build & Deploy
    │   │   └── Python Version ← FOUND HERE
    │   └── Danger Zone
    └── Environment (tab)
```

## What to Look For

The Python version setting might appear as:
- **Dropdown menu** with options like:
  - Python 3.13 (default)
  - Python 3.12
  - Python 3.11 ← **SELECT THIS**
  - Python 3.10

- **Text input field** where you can type:
  - `python-3.11.0`
  - `3.11.0`
  - `3.11`

## If You Can't Find It

### Option A: Update Build Command Instead

1. **Go to Settings → Build & Deploy**
2. **Find "Build Command"**
3. **Change it to:**
   ```
   python3.11 -m pip install -r requirements.txt
   ```
4. **Save Changes**

### Option B: Add Environment Variable

1. **Go to Settings → Environment**
2. **Click "Add Environment Variable"**
3. **Add:**
   - Key: `PYTHON_VERSION`
   - Value: `3.11.0`
4. **Save**

### Option C: Check Service Type

- Make sure your service is a **"Web Service"** (not Static Site)
- Python version option only appears for Web Services

## After Setting Python Version

1. **Save Changes**
2. **Go to "Manual Deploy"** (top right)
3. **Click "Deploy latest commit"**
4. **Wait for build** - should now use Python 3.11!

## Verification

After deployment, check build logs:
- Should see: `Using Python version 3.11.0`
- NOT: `Using Python version 3.13.4`

## Quick Checklist

- [ ] Logged into Render dashboard
- [ ] Selected your backend service
- [ ] Clicked "Settings" tab
- [ ] Found "Python Version" setting
- [ ] Changed to Python 3.11
- [ ] Saved changes
- [ ] Redeployed service

## Still Can't Find It?

**Alternative Solution:**
Update your `Procfile` to explicitly use Python 3.11:

```
web: python3.11 -m gunicorn backend.wsgi --log-file -
```

But the **Settings tab method is preferred** and more reliable.

---

**Need Help?**
- Render Docs: https://render.com/docs/python-version
- Render Support: Check their help center

