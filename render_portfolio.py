import os
import json
from jinja2 import Environment, FileSystemLoader

# Path settings
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "portfolio_server", "templates")
DATA_FILE = os.path.join(BASE_DIR, "portfolio_server", "data.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "index.html")

def render_static():
    # Load data
    if not os.path.exists(DATA_FILE):
        print(f"Data file {DATA_FILE} not found.")
        return
        
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
        if "content" in data:
            c = data["content"]
            if "careers" in c: c["careers"] = sorted(c["careers"], key=lambda x: str(x.get("period", "")).replace(" ", ""), reverse=True)
            if "educations" in c: c["educations"] = sorted(c["educations"], key=lambda x: str(x.get("period", "")).replace(" ", ""), reverse=True)
            if "trainings" in c: c["trainings"] = sorted(c["trainings"], key=lambda x: str(x.get("period", "")).replace(" ", ""), reverse=True)
            if "activities" in c: c["activities"] = sorted(c["activities"], key=lambda x: str(x.get("period", "")).replace(" ", ""), reverse=True)
            if "awards" in c: c["awards"] = sorted(c["awards"], key=lambda x: str(x.get("date", "")).replace(" ", ""), reverse=True)

    # Setup Jinja2
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("index.html")

    # Render
    html_content = template.render(data=data)

    # Save to root index.html
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"Successfully rendered static portfolio to {OUTPUT_FILE}")

if __name__ == "__main__":
    render_static()
