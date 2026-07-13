# Autonomous Human-Like Browser Automation Framework

An enterprise-grade, stateful browser automation core built using Python and Playwright. This framework is designed to bypass standard anti-bot protection layers by seamlessly integrating dynamic human interaction models, adaptive DOM analysis, and isolated profile session tracking.

## 🚀 Key Architectural Features

* **Multi-Engine Foundation (Module 1):** Centrally configured and abstract browser lifecycle management supporting Chromium, Firefox, and WebKit binaries via unified configuration paradigms.
* **Mechanical Interaction Subsystem (Module 2):** Complete implementation of low-level web interactions including native tab manipulation, input manipulation, keyboard stroke controls, and runtime screenshot generation.
* **Intelligent DOM Synchronization (Module 3):** Defensive element locating using robust CSS Selectors and XPath queries, utilizing strict asynchronous auto-waiting states to eliminate locator race conditions.
* **Human Behavior Simulation (Module 4):** Sophisticated behavior obfuscation engine that randomizes typing speeds (WPM strings), introduces organic typing mistakes with real-time backspace self-corrections, calculates varied scrolling trajectories, and triggers realistic attention-span reading delays.
* **Stateful Profile Memory Layer (Module 5):** Multi-user execution isolation utilizing persistent user data directories to preserve local storage, browser cache matrices, and session cookies across separate run profiles.

## 📁 Repository Structure

```text
├── src/
│   ├── config.py              # Environment configuration loader
│   ├── browser_engine.py       # Core browser lifecycle & actions layer
│   └── human_behavior.py      # Behavioral obfuscation & typing simulator
├── .env                       # Local environment variables (Config)
├── main.py                    # Principal automation orchestration pipeline
└── requirements.txt           # Project software dependencies
