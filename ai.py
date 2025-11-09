#!/usr/bin/env python3
import os, sys, json, re, requests, threading, itertools, time
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax

console = Console()

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
API_KEY_FILE = Path.home() / "Single-Session-CLI-Chatbot-AI/.geminikey"
HISTORY_FILE = Path.home() / "Single-Session-CLI-Chatbot-AI/.session"
ROLE_FILE = Path.home() / "Single-Session-CLI-Chatbot-AI/.role"
MAX_HISTORY_CHARS = 25000

# ========== Util dasar ==========

def load_api_key():
    if not API_KEY_FILE.exists():
        console.print(f"[red]Error:[/red] File API key {API_KEY_FILE} tidak ditemukan.")
        sys.exit(1)
    key = API_KEY_FILE.read_text().strip()
    if not key:
        console.print(f"[red]Error:[/red] File {API_KEY_FILE} kosong.")
        sys.exit(1)
    return key

def ensure_role_file():
    if not ROLE_FILE.exists():
        try:
            ROLE_FILE.write_text("")
        except Exception as e:
            console.print(f"[red]Gagal membuat file .role:[/red] {e}")

def load_history():
    if HISTORY_FILE.exists():
        try:
            return json.loads(HISTORY_FILE.read_text())
        except json.JSONDecodeError:
            console.print("[yellow]Warning:[/yellow] History rusak, mulai baru.")
    return []

def save_history(history):
    try:
        HISTORY_FILE.write_text(json.dumps(history, indent=2))
    except Exception as e:
        console.print(f"[red]Gagal simpan history:[/red] {e}")

def prune_history(history):
    new_history, current_chars = [], 0
    for msg in reversed(history):
        msg_text_len = sum(len(p.get("text", "")) for p in msg.get("parts", []) if isinstance(p, dict))
        if current_chars + msg_text_len > MAX_HISTORY_CHARS and new_history:
            break
        new_history.insert(0, msg)
        current_chars += msg_text_len
    return new_history

def safe_extract_text(resp_json):
    try:
        parts = resp_json["candidates"][0]["content"]["parts"]
        return "\n".join(p.get("text", "") for p in parts if "text" in p)
    except Exception:
        return ""

# ========== Spinner UI ==========

def spinner_task(stop_event):
    import time
    from rich.console import Console

    console = Console()
    colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]

    total_slots = 15  # panjang baris
    color_idx = 0
    direction = 1  # 1 = nambah ke kanan, -1 = ngurang ke kiri
    visible = 0    # jumlah bola yang kelihatan

    while not stop_event.is_set():
        row = [" " for _ in range(total_slots)]

        # bikin bola sesuai jumlah visible
        for i in range(visible):
            color = colors[(color_idx + i) % len(colors)]
            row[i * 2] = f"[bold {color}]●[/bold {color}]"

        frame = "".join(row)
        console.print(f"[bold green]Thinking[/bold green] {frame}", end="\r", highlight=False)

        # update jumlah bola & arah
        visible += direction
        if visible * 2 >= total_slots:  # mentok kanan (penuh)
            direction = -1
            color_idx += 1
        elif visible <= 0:  # hilang semua (mentok kiri)
            direction = 1
            color_idx += 1

        time.sleep(0.08)

    console.print(" " * 80, end="\r")

# ========== Rendering pintar ==========

def _render_gemini_response(console, text_content):
    if not text_content.strip():
        console.print("[yellow]Warning:[/yellow] Respons kosong.")
        return

    code_match = re.match(r"^```(\w+)\n(.*?)\n```$", text_content.strip(), re.DOTALL)
    if code_match:
        lang = code_match.group(1).lower()
        code = code_match.group(2).strip()
        console.print(Syntax(code, lang, theme="solarized-dark", line_numbers=True, word_wrap=True))
        return
    try:
        console.print(Markdown(text_content, code_theme="monokai"))
    except Exception:
        console.print(text_content)

# ========== Fungsi panggil API ==========

def call_gemini(api_key, history):
    clean_history = []
    for msg in history:
        role = msg.get("role", "user")
        if role not in ("user", "model"):
            role = "user"
        parts = msg.get("parts", [])
        safe_parts = []
        for p in parts:
            if isinstance(p, dict) and "text" in p:
                safe_parts.append({"text": str(p["text"])})
            elif isinstance(p, str):
                safe_parts.append({"text": p})
        if safe_parts:
            clean_history.append({"role": role, "parts": safe_parts})

    payload = {"contents": clean_history}
    headers = {"Content-Type": "application/json"}

    stop_event = threading.Event()
    spinner = threading.Thread(target=spinner_task, args=(stop_event,))
    spinner.start()

    try:
        r = requests.post(f"{API_URL}?key={api_key}", headers=headers, json=payload, timeout=45)
        r.raise_for_status()
        resp_json = r.json()
    except requests.exceptions.RequestException as e:
        console.print(f"\n[red]API Error:[/red] {e}")
        if getattr(e, "response", None):
            console.print(f"[dim]{e.response.text}[/dim]")
        resp_json = None
    finally:
        stop_event.set()
        spinner.join()

    return resp_json

# ========== CLI utama ==========

def repl():
    console.print("[bold cyan]===[/bold cyan] Gemini CLI (gemini-2.5-flash) [bold cyan]===[/bold cyan]")
    console.print("Type [bold]q/exit/Ctrl+C/D[/bold] to quit. Use [bold]::[/bold] for multiline input.")
    api_key = load_api_key()
    ensure_role_file()
    history = load_history()

    while True:
        try:
            user_input = console.input("[bold bright_yellow]User >>>:[/bold bright_yellow] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bold yellow]Keluar...[/bold yellow]")
            save_history(history)
            break

        if not user_input:
            continue
        if user_input.lower() in ("q", "quit", "exit"):
            console.print("[bold yellow]Keluar...[/bold yellow]")
            save_history(history)
            break

        # Multiline input
        if user_input == "::":
            console.print("[dim]Masuk mode multiline. Ketik '::' lagi untuk kirim.[/dim]")
            lines = []
            while True:
                line = input()
                if line.strip() == "::":
                    break
                lines.append(line)
            user_input = "\n".join(lines)

        # Help
        if user_input == ".help":
            console.print("""
[bold cyan]Perintah khusus:[/bold cyan]
  .help               - Tampilkan bantuan
  .file <path> [desc] - Kirim isi file ke model
  q / exit / Ctrl+C/D - Keluar dan simpan sesi
  ::                  - Mode multiline input
""")
            continue

        # File handler
        if user_input.startswith(".file"):
            parts = user_input.split(" ", 2)
            if len(parts) < 2:
                console.print("[yellow]Usage:[/yellow] .file <path> [desc]")
                continue
            filepath = Path(parts[1]).expanduser()
            desc = parts[2] if len(parts) > 2 else ""
            if not filepath.exists():
                console.print(f"[red]File tidak ditemukan:[/red] {filepath}")
                continue
            try:
                file_content = filepath.read_text()
                file_msg = f"{desc}\n\nIsi file {filepath.name}:\n```\n{file_content}\n```"
                history.append({"role": "user", "parts": [{"text": file_msg}]})
            except Exception as e:
                console.print(f"[red]Gagal baca file:[/red] {e}")
                continue
        else:
            history.append({"role": "user", "parts": [{"text": user_input}]})

        history = prune_history(history)
        resp = call_gemini(api_key, history)
        if not resp:
            continue

        text = safe_extract_text(resp)
        history.append({"role": "model", "parts": [{"text": text}]})

        console.print("\n[bold blue]AI >>>:[/bold blue]")
        _render_gemini_response(console, text)
        console.print()

        save_history(history)

# ========== Entry point ==========
if __name__ == "__main__":
    repl()
