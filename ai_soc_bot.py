import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import openai
import json
import pandas as pd
import os

# --- Set your OpenAI API Key ---
openai.api_key = "your-api-key-here"  # Replace with your real key

# --- Function to Analyze Alert ---
def analyze_alert(alert_text):
    prompt = f"""
You are a cybersecurity analyst. Given the alert below, summarize the threat, classify the incident, recommend actions, and map it to a MITRE ATT&CK technique.

Alert:
{alert_text}

Respond in this format:
- Summary:
- Incident Type:
- Recommended Response:
- MITRE ATT&CK Mapping (Tactic + Technique ID + Name):
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- Function to Load File ---
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("JSON or CSV", "*.json *.csv")])
    if file_path:
        try:
            if file_path.endswith(".json"):
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    return json.dumps(data, indent=2)
            elif file_path.endswith(".csv"):
                df = pd.read_csv(file_path)
                return df.to_string(index=False)
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to load file: {e}")
    return ""

# --- GUI App ---
class SOCApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AI SOC Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#1e1e2f")

        # Heading
        title = tk.Label(root, text="AI SOC Assistant Bot", font=("Segoe UI", 20, "bold"), fg="white", bg="#1e1e2f")
        title.pack(pady=10)

        # Text input for alerts
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=110, height=12, font=("Consolas", 10))
        self.text_area.pack(padx=15, pady=5)

        # Buttons
        btn_frame = tk.Frame(root, bg="#1e1e2f")
        btn_frame.pack(pady=10)

        load_btn = tk.Button(btn_frame, text="📂 Load Alert File", command=self.load_file, bg="#44475a", fg="white", font=("Segoe UI", 10, "bold"), padx=10, pady=5)
        load_btn.pack(side=tk.LEFT, padx=10)

        analyze_btn = tk.Button(btn_frame, text="⚙️ Analyze Alert", command=self.analyze, bg="#50fa7b", fg="black", font=("Segoe UI", 10, "bold"), padx=10, pady=5)
        analyze_btn.pack(side=tk.LEFT, padx=10)

        # Output label
        output_label = tk.Label(root, text="Analysis Output", font=("Segoe UI", 12, "bold"), fg="#8be9fd", bg="#1e1e2f")
        output_label.pack(pady=(15, 5))

        # Output area
        self.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=110, height=15, font=("Consolas", 10), bg="#282a36", fg="#f8f8f2")
        self.output_area.pack(padx=15, pady=5)
        self.output_area.config(state='disabled')

    def load_file(self):
        content = load_file()
        if content:
            self.text_area.insert(tk.END, content + "\n")

    def analyze(self):
        alert_text = self.text_area.get("1.0", tk.END).strip()
        if not alert_text:
            messagebox.showwarning("Input Required", "Please paste or load alert text.")
            return

        self.output_area.config(state='normal')
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, "Analyzing alert...\n")
        self.output_area.update()

        result = analyze_alert(alert_text)
        self.output_area.delete("1.0", tk.END)
        self.output_area.insert(tk.END, result)
        self.output_area.config(state='disabled')

        with open("incident_log.txt", "a") as log:
            log.write(result + "\n\n")

# --- Run the GUI App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SOCApp(root)
    root.mainloop()
