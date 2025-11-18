# Dummy Flask backend for `index`(md file for color)

This repository now includes a minimal Flask backend that serves the existing `template/index.html` and a few dummy JSON endpoints, so that is another task complete.

Files added for flask dummy backend:
- `app.py` — minimal Flask app using `template/` as the templates folder and `static/` as static files.
- `requirements.txt` — contains `Flask`.

Terminal run(PowerShell) :

```
python -m venv env
.\env\scripts\activate
pip install -r requirements.txt
python app.py
```

Endpoints:
- `GET /` — serves `index.html` from `template/`
- `GET /api/status` — returns basic status JSON
- `GET /api/dummy` — returns a sample JSON payload with `points` and `rewards`
- `GET /api/profile` — dummy user profile (id, name, email, joined, badges)
- `GET /api/points` — points summary and history
- `GET /api/rewards` — catalog of available rewards
- `GET /api/redeem` — available redemption options and past history
- `GET /api/qr` — temporary QR token / value / expiry placeholder
- `GET /api/street` — nearby drop-off locations
- `GET /api/about` — app metadata (version, description, contact)

Additional Notes:
- The Flask app is configured with `template_folder='template'` to reuse the existing folder name.
