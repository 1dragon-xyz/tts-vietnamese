# Budget Monitoring Quick Start

## ✅ What You Have Now

1. **env/ folder** - All secrets centralized and gitignored
2. **Budget monitoring script** - Automated alerts and shutdown
3. **Setup script** - One-command gcloud CLI setup

## 🚀 Quick Setup (5 minutes)

### Step 1: Run the Setup Script

```bash
cd scripts
bash setup-budget.sh
```

This creates:
- Budget with $0.01 limit
- Pub/Sub topic for notifications
- Thresholds at 50%, 70%, 80%

### Step 2: Deploy Auto-Shutdown (Optional but Recommended)

```bash
cd scripts

# Deploy Cloud Function
gcloud functions deploy budget-monitor \
  --runtime python39 \
  --trigger-topic budget-alerts \
  --entry-point pubsub_handler \
  --source . \
  --project lito-tts-app \
  --set-env-vars EMAIL_TO=anhdhnguyen@gmail.com
```

### Step 3: Test It

```bash
# Test the monitoring
python3 budget-monitor.py

# Test Pub/Sub (simulates 80% usage)
gcloud pubsub topics publish budget-alerts \
  --message='{"costAmount": 0.008, "budgetAmount": 0.01}' \
  --project=lito-tts-app
```

## 📊 What Happens

| Usage | Action |
|-------|--------|
| 50% ($0.005) | 📧 Email: "Courtesy notification" |
| 70% ($0.007) | ⚠️ Email: "Warning - approaching limit" |
| 80% ($0.008) | 🛑 **API DISABLED** + Email with re-enable instructions |

## 🔍 Monitoring

Check usage anytime:
```bash
# Via CLI
gcloud billing budgets list --billing-account=013ED6-9913AA-B0942B

# Via Console
https://console.cloud.google.com/billing/budgets?project=lito-tts-app
```

## 🆘 If API Gets Disabled

Don't panic! This means the system is working.

1. Check what caused the spike:
   ```bash
   gcloud logging read "resource.type=api" --project=lito-tts-app --limit=50
   ```

2. Wait for next month (free tier resets) OR increase budget if needed

3. Re-enable when ready:
   ```bash
   gcloud services enable texttospeech.googleapis.com --project=lito-tts-app
   ```

## 📁 File Structure

```
lito/
├── env/                          # ← All secrets here (gitignored)
│   ├── README.md
│   └── lito-key.json
├── scripts/
│   ├── budget-monitor.py         # ← Monitoring logic
│   └── setup-budget.sh           # ← One-command setup
└── project-plan/
    └── google-cloud-budget.md    # ← Full documentation
```

## ⚙️ Configuration

Edit `scripts/budget-monitor.py` to customize:
- Email addresses
- Threshold percentages
- Budget amount
- SMTP settings

## 🔐 Security

- ✅ All secrets in `env/` folder
- ✅ `env/` is gitignored
- ✅ No credentials in code
- ✅ Automated shutdown prevents charges

---

**Next**: Run `bash scripts/setup-budget.sh` to get started!
