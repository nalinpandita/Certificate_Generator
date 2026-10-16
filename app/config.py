from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG = yaml.safe_load((BASE_DIR / "config.yaml").read_text(encoding="utf-8"))
