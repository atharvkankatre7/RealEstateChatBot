# 🔧 Render Python Version Fix

## Problem
Render is using Python 3.13.4 by default, but pandas doesn't have pre-built wheels for Python 3.13, causing build failures.

## Solution Options

### Option 1: Set Python Version in Render Dashboard (RECOMMENDED)

1. **Go to Render Dashboard:**
   - Open your service
   - Go to **Settings** tab
   - Scroll to **"Python Version"** section

2. **Set Python Version:**
   - Select **"Python 3.11"** from dropdown
   - Or manually enter: `3.11.0`
   - Click **Save Changes**

3. **Redeploy:**
   - Render will use Python 3.11 for the next build
   - Build should succeed!

### Option 2: Use Build Command with Python Version

In Render dashboard, update **Build Command** to:
```bash
python3.11 -m pip install -r requirements.txt
```

### Option 3: Use Latest Pandas (Alternative)

If you want to use Python 3.13, update `requirements.txt`:
```
pandas>=2.2.3
```

But this may still have issues. **Option 1 is recommended.**

## Current Files

- ✅ `backend/runtime.txt` - Set to `python-3.11.0`
- ✅ `backend/requirements.txt` - Using `pandas==2.1.4` (compatible with Python 3.11)

## Why This Happens

Render sometimes ignores `runtime.txt` if:
- File is in wrong location
- Python version format is incorrect
- Render dashboard has explicit Python version set

## Best Practice

**Always set Python version in Render dashboard** - it's more reliable than `runtime.txt`.

## Next Steps

1. **Set Python 3.11 in Render dashboard** (Settings → Python Version)
2. **Redeploy** - Build should succeed!
3. **Verify** - Check build logs show Python 3.11

