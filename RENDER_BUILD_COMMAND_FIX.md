# 🔧 Fix Python Version via Build Command

## Quick Fix

Since Python version setting might not be visible, update the **Build Command** instead.

### Steps:

1. **On the Settings page you're viewing:**
   - Find **"Build Command"** section
   - Click the **"Edit"** button next to it

2. **Update the Build Command:**
   - Current: `backend/ $ pip install -r requirements.txt`
   - Change to: `backend/ $ python3.11 -m pip install -r requirements.txt`
   - Or: `backend/ $ python3.11 -m pip install -r requirements.txt && python3.11 -m gunicorn backend.wsgi --log-file -`

3. **Save Changes**
   - Click "Save" or the checkmark
   - Render will now use Python 3.11 for builds

4. **Redeploy:**
   - Go to "Manual Deploy" (top of page)
   - Click "Deploy latest commit"
   - Build should now succeed!

## Alternative: Check General Settings

1. **Click "General" in the right sidebar** (above "Build & Deploy")
2. **Look for "Python Version"** dropdown
3. **Select Python 3.11** if available

## What This Does

- Forces Render to use Python 3.11 instead of default 3.13
- Ensures pandas installs correctly
- Build should complete successfully

