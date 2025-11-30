# 🔧 Final Render Build Command Fix

## Problem
Using `python3.11 -m pip` causes "externally-managed-environment" error.

## Solution
Render automatically creates a virtual environment. We just need to use `pip` directly.

### Update Build Command in Render:

**Change from:**
```
backend/ $ python3.11 -m pip install -r requirements.txt
```

**Change to:**
```
pip install -r requirements.txt
```

**OR (if you need to specify Python version):**
```
python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

**BUT the simplest is:**
```
pip install -r requirements.txt
```

Render will automatically:
- Use the Python version from `runtime.txt`
- Create a virtual environment
- Install packages correctly

## Steps:

1. **Go to Render Settings → Build & Deploy**
2. **Click "Edit" on Build Command**
3. **Change to:** `pip install -r requirements.txt`
4. **Save**
5. **Redeploy**

## Why This Works

- Render reads `runtime.txt` and uses Python 3.11
- Render automatically creates a venv
- `pip` command uses the correct Python version
- No need to manually specify Python version in build command

