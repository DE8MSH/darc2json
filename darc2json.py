import csv
import json

def parse_frequency(freq_str):
    """
    Wandle z.B. '438,87500' in int-Hz und formatiere auf 8/9/10 Stellen je nach MHz-Bereich.
    """
    try:
        freq_mhz = float(freq_str.replace(',', '.'))
        freq_hz = freq_mhz * 1_000_000
        hz_int = int(freq_hz)

        if freq_mhz < 100:
            hz_str = str(hz_int).ljust(8, '0')[:8]
        elif freq_mhz < 1000:
            hz_str = str(hz_int).ljust(9, '0')[:9]
        else:
            hz_str = str(hz_int).ljust(10, '0')[:10]

        return int(hz_str)
    except ValueError:
        return None

def clean_name(name):
    """Entferne 'DB' am Anfang, wenn vorhanden."""
    name = name.strip()
    if name.upper().startswith("DB"):
        return name[2:]
    return name

def csv_to_bookmark_json(csv_filename, json_filename):
    bookmarks = []

    with open(csv_filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            if not row or len(row) < 10:
                continue  # überspringe unvollständige Zeilen

            name_raw = row[0].strip().upper()

            # Ignoriere Calls mit -R oder -L
            if "-R" in name_raw or "-L" in name_raw:
                continue

            frequency_str = row[1].strip()
            frequency = parse_frequency(frequency_str)
            if frequency is None:
                continue

            name = clean_name(name_raw)

            info = row[4].strip()
            distance = row[9].strip()
            description = f"{info} {distance}".strip()

            bookmark = {
                "name": name,
                "frequency": frequency,
                "modulation": "nfm",
                "underlying": "",
                "description": description,
                "scannable": True
            }
            bookmarks.append(bookmark)

    with open(json_filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(bookmarks, jsonfile, indent=4, ensure_ascii=False)

# Beispiel-Aufruf
if __name__ == "__main__":
    csv_to_bookmark_json("relais.csv", "bookmarks.json")

