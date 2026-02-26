# Tailscale Setup — Windows PC

**What this does:** Connects your Windows PC to your Mac Studio over a private encrypted network. Once done, you can access VoiceClaw and other services running on the Mac Studio directly from your browser.

**Time:** ~5 minutes

---

## Step 1: Create a Tailscale Account

1. Go to **https://login.tailscale.com**
2. Click **Sign up** — use Google, Microsoft, or GitHub (whichever you prefer)
3. You'll land on the Tailscale admin dashboard — you're done with this step

> **Important:** Remember which account you used to sign up. The Mac Studio needs to log into the **same account**.

---

## Step 2: Install Tailscale on Windows

1. Go to **https://tailscale.com/download/windows**
2. Download and run the installer
3. When it finishes, you'll see a **Tailscale icon in your system tray** (bottom-right, near the clock — you may need to click the `^` arrow to find it)
4. Click the Tailscale icon → **Log in**
5. Sign in with the **same account** from Step 1
6. If Windows Defender asks about firewall access → **Allow**

---

## Step 3: Verify It's Working

Open **PowerShell** or **Command Prompt** and run:

```
tailscale status
```

You should see your PC listed with a `100.x.x.x` IP address. That's your Tailscale IP.

> **Screenshot this output and send it to Cnid** — they'll need the info to connect the Mac Studio to the same network.

---

## Step 4: Enable HTTPS (Admin Console)

1. Go to **https://login.tailscale.com/admin/dns**
2. Toggle **MagicDNS** to **ON** (if not already)
3. Go to **https://login.tailscale.com/admin/settings/features**
4. Toggle **HTTPS** to **ON**

These settings let you access the Mac Studio with a real HTTPS address (needed for microphone access in the browser).

---

## That's It! 🎉

Once Cnid connects the Mac Studio to the same Tailscale account, you'll be able to:

- **Open VoiceClaw** in your browser at `https://[mac-studio-name].[your-tailnet].ts.net`
- **Talk to your OpenClaw agent** with voice
- **Access any other services** running on the Mac Studio

Cnid will handle the Mac Studio side and send you the URL when it's ready.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Can't find Tailscale icon | Check the hidden system tray icons (click `^` near the clock) |
| "Not connected" after login | Right-click the Tailscale tray icon → **Connect** |
| Firewall popup | Always **Allow** — Tailscale needs network access |
| `tailscale status` not recognized | Close and reopen your terminal, or try `tailscale.exe status` |
| Need to switch accounts | Right-click tray icon → **Log out**, then log in with the right account |
