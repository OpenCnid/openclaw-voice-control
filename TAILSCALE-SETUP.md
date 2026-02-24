# Tailscale Setup — VoiceClaw for Hans

**Goal:** Hans's PC browser → HTTPS → Mac Studio voice server (with mic access)

---

## Phase 1: Tailscale Accounts & Install (~10 min)

### 1.1 Create Tailscale Account

1. Go to https://login.tailscale.com
2. Sign up with Google, Microsoft, or GitHub (whichever Hans prefers)
3. This creates a **tailnet** (private network) — note the tailnet name (e.g., `tail1234.ts.net`)

### 1.2 Install on Mac Studio

```bash
# Option A: Homebrew (recommended)
brew install --cask tailscale

# Option B: Download from https://tailscale.com/download/mac
```

After install:
1. Open **Tailscale** from Applications
2. Click **"Log in"** in the menu bar icon
3. Sign in with the same account from step 1.1
4. **macOS will prompt:** "Tailscale wants to add VPN configurations" → **Allow**
5. Mac Studio should now appear in the Tailscale admin console

**Verify:**
```bash
tailscale status
# Should show the Mac Studio with a 100.x.x.x IP and hostname
```

**Note the hostname** — it'll be something like `hans-mac-studio`. The full FQDN will be `hans-mac-studio.tail1234.ts.net`.

### 1.3 Install on PC

**Windows:**
1. Download from https://tailscale.com/download/windows
2. Run installer
3. Click the Tailscale icon in system tray → **Log in**
4. Sign in with the **same account**
5. If Windows Defender prompts about firewall → **Allow**

**Verify both machines see each other:**
```bash
# On either machine
tailscale status
# Should list both devices with 100.x.x.x IPs
```

**Quick test:**
```bash
# From PC, ping Mac Studio
ping hans-mac-studio  # or whatever the hostname is
```

---

## Phase 2: Enable HTTPS (~2 min)

### 2.1 Tailscale Admin Console

1. Go to https://login.tailscale.com/admin/dns
2. **Enable MagicDNS** (toggle ON if not already)
3. Go to https://login.tailscale.com/admin/settings/features
4. **Enable HTTPS** (toggle ON)

That's it — Tailscale can now provision TLS certs for `*.tail1234.ts.net`.

---

## Phase 3: Expose Voice Server via `tailscale serve` (~2 min)

On the **Mac Studio**, run:

```bash
# Expose the voice server (port 8765) as HTTPS on port 443
tailscale serve --bg --https=443 http://localhost:8765
```

**What this does:**
- Creates a reverse proxy: `https://hans-mac-studio.tail1234.ts.net` → `http://localhost:8765`
- Auto-provisions a real TLS certificate
- Handles WebSocket upgrade (required for voice streaming)
- Runs in background (`--bg`)
- Persists across reboots

**Verify it's running:**
```bash
tailscale serve status
```

---

## Phase 4: Test from PC (~5 min)

### 4.1 Open Voice Dashboard

On Hans's PC, open Chrome/Edge/Firefox:

```
https://hans-mac-studio.tail1234.ts.net
```

(Replace `hans-mac-studio.tail1234.ts.net` with the actual FQDN from `tailscale status`)

### 4.2 Test Checklist

- [ ] Page loads with VoiceClaw UI
- [ ] Connection dot shows green "Connected"
- [ ] Browser prompts for **mic permission** → Allow
- [ ] Tap the orb or press Space → waveform shows, "Listening…"
- [ ] Speak → transcript appears → AI responds
- [ ] Audio plays back (TTS)
- [ ] Text input works (type message, hit Enter)
- [ ] Space to pause/resume works

### 4.3 If WebSocket Fails

Symptom: Page loads but dot stays red "Offline" or "Connecting"

**Fix — use TCP port forwarding instead of serve:**
```bash
# On Mac Studio, stop the serve
tailscale serve --bg --https=443 off

# Use funnel or direct cert approach instead:
tailscale cert hans-mac-studio.tail1234.ts.net

# This creates:
#   hans-mac-studio.tail1234.ts.net.crt  (certificate)
#   hans-mac-studio.tail1234.ts.net.key  (private key)

# Then start uvicorn with TLS directly:
cd /path/to/openclaw-voice-control
PYTHONPATH=. .venv/bin/python3 -m uvicorn src.server.main:app \
  --host 0.0.0.0 --port 8765 \
  --ssl-certfile hans-mac-studio.tail1234.ts.net.crt \
  --ssl-keyfile hans-mac-studio.tail1234.ts.net.key
```

Then access: `https://hans-mac-studio.tail1234.ts.net:8765`

---

## Phase 5: (Optional) Expose OpenClaw Control UI Too

If Hans also wants the OpenClaw dashboard from his PC:

```bash
# On Mac Studio — serve OpenClaw gateway on a different HTTPS port
tailscale serve --bg --https=8443 http://localhost:18789
```

Access: `https://hans-mac-studio.tail1234.ts.net:8443`

---

## Keeping It Running

### Mac Studio Must Stay Awake

```bash
# Prevent sleep (Mac Studio should be always-on as a server)
sudo pmset -a sleep 0 displaysleep 0 disksleep 0
```

### Auto-Start on Boot

- **Tailscale:** Starts automatically after install (Launch Agent)
- **Voice server:** Should already be in a tmux session or systemd service
- **`tailscale serve`:** Persists across reboots (stored in tailscaled config)

### If Tailscale Cert Expires

Certs auto-renew. If they don't:
```bash
# On Mac Studio
tailscale serve --bg --https=443 http://localhost:8765
# Re-run to refresh
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Page loads, mic prompt doesn't appear | Check URL is `https://` not `http://` |
| "Not secure" warning in browser | MagicDNS or HTTPS not enabled in admin console |
| Devices can't see each other | Both logged into same Tailscale account? Firewall blocking UDP 41641? |
| Mac asks for VPN permission again | Approve in System Settings → Privacy & Security → VPN |
| WebSocket won't connect through serve | Use direct cert approach (Phase 4.3 fallback) |
| Slow/laggy audio | Check `tailscale ping hans-mac-studio` — should be <5ms on LAN |
| Voice server not running after reboot | Re-launch from tmux: `tmux -S /tmp/sock new -s voice "cd /path && python -m src.server.main"` |

---

## Summary

```
Hans's PC (browser + mic)
    │
    │  HTTPS + WebSocket (encrypted, real TLS cert)
    │
    ▼
Tailscale mesh (WireGuard, ~1ms LAN)
    │
    │  tailscale serve (reverse proxy)
    │
    ▼
Mac Studio localhost:8765 (voice server)
    │
    ├── Whisper (STT)
    ├── OpenClaw Gateway (AI)
    └── Chatterbox (TTS)
```

**Total setup time: ~20 minutes**
