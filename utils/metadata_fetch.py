import json
from pathlib import Path

# for chapter names
def QuranMetadata(chapter : int):
    if not chapter > 0:
        return "???"
    with open(Path(__file__).parent.parent / "db/quran_meta_data.json", "r", encoding="utf-8") as chapters:
        data = json.load(chapters)
        quran_en = data["data"]["surahs"]["references"][chapter - 1]["englishName"]
        quran_ar = data["data"]["surahs"]["references"][chapter - 1]["name"]
        full_data = f"Surah {quran_en} ({quran_ar})"
        return full_data