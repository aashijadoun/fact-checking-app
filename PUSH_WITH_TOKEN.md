# Push Code to GitHub - Authentication Required

Your code is ready to push, but GitHub requires authentication. Here are two options:

## Option 1: Use Personal Access Token (Recommended)

### Step 1: Create Personal Access Token
1. Go to: https://github.com/settings/tokens
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name: "Fact-Checking App"
4. Select scopes: Check **"repo"** (full control of private repositories)
5. Click **"Generate token"**
6. **Copy the token immediately** (you won't see it again!)

### Step 2: Push with Token
Run this command and use your token as the password:

```bash
cd /Users/aashijadoun/Cog_Culture
git push -u origin main
```

When prompted:
- **Username**: `aashijadoun`
- **Password**: Paste your personal access token (NOT your GitHub password)

## Option 2: Use GitHub CLI (if installed)

```bash
gh auth login
git push -u origin main
```

## Option 3: Use Token in URL (One-time)

Replace `YOUR_TOKEN` with your personal access token:

```bash
cd /Users/aashijadoun/Cog_Culture
git remote set-url origin https://YOUR_TOKEN@github.com/aashijadoun/fact-checking-app.git
git push -u origin main
```

Then remove the token from URL for security:
```bash
git remote set-url origin https://github.com/aashijadoun/fact-checking-app.git
```

## Quick Command Reference

Your repository URL: `https://github.com/aashijadoun/fact-checking-app`

After successful push, verify at: https://github.com/aashijadoun/fact-checking-app

