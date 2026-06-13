import json
from pathlib import Path

def fetch(surah : int, ayah : int): # (int chapter & int verse) -> (string full verse)
    if (
        surah < 1 or surah > 114
        or ayah < 1
    ):
        return None
    
    with open(Path(__file__).parent.parent / "db/quran_en_sahih_database_v1.json", "r", encoding="utf-8") as en:
        data = json.load(en)

    with open(Path(__file__).parent.parent / "db/quran_en_sahih_database_v1.json", "r", encoding="utf-8") as verses:
        quran_en = json.load(verses)
    with open(Path(__file__).parent.parent / "db/quran_uthmani_database_v1.json", "r", encoding="utf-8") as verses2:
        quran_ar = json.load(verses2)
        wanted_text = f"**Arabic:** {quran_ar['data']['surahs'][surah - 1]['ayahs'][ayah - 1]['text']} \n \n **English:** {quran_en['data']['surahs'][surah - 1]['ayahs'][ayah - 1]['text']}"
        if len(wanted_text) > 4096:
            return wanted_text[0:4090] + "..."
        else:
            return wanted_text
        
def ranged_fetch(reference: str):
    """
    Example:
        ranged_fetch("4:55-58")
    """

    try:
        surah_part, ayah_part = reference.split(":")
        starting_ayah, ending_ayah = ayah_part.split("-")

        surah = int(surah_part)
        starting_ayah = int(starting_ayah)
        ending_ayah = int(ending_ayah)

    except ValueError:
        return None

    if (
        surah < 1 or surah > 114
        or starting_ayah < 1
        or ending_ayah < 1
        or starting_ayah > ending_ayah
    ):
        return None

    with open(
        Path(__file__).parent.parent / "db/quran_en_sahih_database_v1.json",
        "r",
        encoding="utf-8"
    ) as en_file:
        quran_en = json.load(en_file)

    with open(
        Path(__file__).parent.parent / "db/quran_uthmani_database_v1.json",
        "r",
        encoding="utf-8"
    ) as ar_file:
        quran_ar = json.load(ar_file)

    surah_en = quran_en["data"]["surahs"][surah - 1]
    surah_ar = quran_ar["data"]["surahs"][surah - 1]

    max_ayah = len(surah_en["ayahs"])

    if ending_ayah > max_ayah:
        return None

    arabic_verses = []
    english_verses = []

    for ayah in range(starting_ayah, ending_ayah + 1):
        arabic_text = surah_ar["ayahs"][ayah - 1]["text"]
        english_text = surah_en["ayahs"][ayah - 1]["text"]

        arabic_verses.append(f"{arabic_text} ({ayah})")
        english_verses.append(f"{english_text} ({ayah})")

    arabic_output = " ".join(arabic_verses)
    english_output = " ".join(english_verses)

    final_text = (
        f"**Arabic:**\n{arabic_output}\n\n"
        f"**English:**\n{english_output}"
    )

    if len(final_text) > 4096:
        return final_text[:4090] + "..."

    return final_text

def any_fetch(reference : str):
    """
    This determines what to return based on if the input is ranged or not
    For example:
    user enters 2:4 -> use fetch()
    user enters 2:5-10 -> use ranged_fetch()
    """
    try:
        surah_part, ayah_part = reference.split(":")
        surah = int(surah_part)

        if "-" in ayah_part:
            data = ranged_fetch(reference)
            return data, reference
        else:
            ayah = int(ayah_part)
            data = fetch(surah, ayah)
            return data, reference
    except ValueError:
        return None