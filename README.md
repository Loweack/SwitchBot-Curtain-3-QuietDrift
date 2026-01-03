# SwitchBot Curtain 3 QuietDrift for Home Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Custom%20Component-orange)

A native Home Assistant custom component to enable **QuietDrift** mode on SwitchBot Curtain 3 devices.

This component exposes a custom service that allows you to control the position of your curtains with a specific speed parameter, unlocking the silent "QuietDrift" feature that is otherwise unavailable in standard Home Assistant cover calls. It wraps the native Bluetooth library to send precise commands directly to your device.

## ✨ Features

*   **🤫 QuietDrift Support**: Move your curtains slowly and silently by setting the speed to `1` (or low values).
*   **⚡ Native Integration**: Works directly with your existing SwitchBot Curtain entities via the native Home Assistant Bluetooth stack.
*   **🛠️ Zero Dependencies**: Does not require external gateways or cloud APIs; operates entirely locally via Bluetooth.
*   **⚙️ UI Installation**: Install easily via HACS and configure via the Home Assistant interface.

## 📥 Installation

### Option 1: HACS (Recommended)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Loweack&repository=SwitchBot-Curtain-3-QuietDrift&category=integration)

1.  Open **HACS** in Home Assistant.
2.  Go to the **Integrations** section.
3.  Click the menu (three dots) in the top right corner and select **Custom repositories**.
4.  Paste the URL of your GitHub repository.
5.  Select **Integration** as the category and click **Add**.
6.  Click **Download** on the new "SwitchBot Curtain 3 QuietDrift" card.
7.  **Restart Home Assistant**.

### Option 2: Manual Installation

1.  Download the repository.
2.  Copy the `custom_components/switchbot_curtain_3_quietdrift` folder into your Home Assistant's `homeassistant/custom_components/` directory.
3.  **Restart Home Assistant**.

---

## ⚙️ Configuration

1.  Navigate to **Settings** > **Devices & Services**.
2.  Click **+ Add Integration**.
3.  Search for **SwitchBot QuietDrift Service**.
4.  Confirm the installation. No additional configuration is needed; it simply registers the global service.

---

## 🚀 Usage

You can control your curtains using the `switchbot_curtain_3_quietdrift.set_switchbot_curtain_position` service in Automations, Scripts, or Developer Tools.

### Service: `switchbot_curtain_3_quietdrift.set_switchbot_curtain_position`

**Parameters:**
*   `entity_id` (Required): The SwitchBot Curtain cover entity (e.g., `cover.bedroom_curtain`).
*   `position` (Required): The target position, from `0` (Closed) to `100` (Open).
*   `speed` (Optional): The movement speed (1-255).
    *   **255**: Fast (Default)
    *   **1**: Slowest (QuietDrift mode)

### Example: Automation (YAML)

Open the curtains silently at sunrise so you wake up naturally:

```yaml
alias: "[Curtain] Sunrise QuietDrift"
description: >-
  Slowly opens the bedroom curtains at sunrise using QuietDrift mode
  to minimize noise.
triggers:
  - trigger: sun
    event: sunrise
    offset: 0
actions:
  - action: switchbot_curtain_3_quietdrift.set_switchbot_curtain_position
    data:
      entity_id: cover.bedroom_curtain
      position: 100
      speed: 1
mode: single
