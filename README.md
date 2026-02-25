# HealthCare Risk Classification — Streamlit app

This repository contains a Streamlit app `app.py` that loads serialized model files and runs a health risk predictor.

Quick prep before pushing to GitHub and deploying to Streamlit Community Cloud:

- Ensure the repo contains `app.py`, `Health_risk_predictor.pkl`, and `label_encoders.pkl` (or host models externally).
- `requirements.txt` is included for dependency installation.
- If your `.pkl` files are large, use Git LFS before committing them.

Deploy to Streamlit Community Cloud:

1. Push this repository to GitHub (example commands below). If you need Git LFS for `.pkl` files, run the Git LFS commands first.
2. Go to: https://share.streamlit.io and sign in with GitHub.
3. Click "New app", select your repo, branch (`main`) and the `app.py` file.
4. Click "Deploy" — Streamlit Cloud will install the packages and run `streamlit run app.py`.

Git commands (run from project folder):

```powershell
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<repo>.git
git push -u origin main
```

If you use Git LFS for `.pkl` files:

```powershell
git lfs install
git lfs track "*.pkl"
git add .gitattributes
git add .
git commit -m "Add files with LFS"
git push origin main
```

If you want, I can run the Git commands here or walk you through pushing to GitHub.