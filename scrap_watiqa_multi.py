import requests
from bs4 import BeautifulSoup
import json
import time
import sys
import os

BASE_URL = "https://www.watiqa.ma/index.php5?page=citoyen.FormulaireCommande"

session = requests.Session()
headers = {
    "User-Agent": "Mozilla/5.0"
}

def get_initial_form(lang="fr"):
    resp = session.get(BASE_URL, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    prado_pagestate_tag = soup.find("input", {"name": "PRADO_PAGESTATE"})
    if not prado_pagestate_tag:
        raise Exception("Impossible de trouver PRADO_PAGESTATE dans la page.")
    prado_pagestate = prado_pagestate_tag["value"]

    if lang == "ar":
        data = {
            "PRADO_PAGESTATE": prado_pagestate,
            "PRADO_POSTBACK_TARGET": "ctl0$toAr",
            "PRADO_POSTBACK_PARAMETER": "",
        }
        resp = session.post(BASE_URL, data=data, headers=headers)
        soup = BeautifulSoup(resp.text, "lxml")
        prado_pagestate_tag = soup.find("input", {"name": "PRADO_PAGESTATE"})
        if not prado_pagestate_tag:
            raise Exception("Impossible de trouver PRADO_PAGESTATE après passage en arabe.")
        prado_pagestate = prado_pagestate_tag["value"]
    return soup, prado_pagestate

def get_regions(soup):
    select = soup.find("select", {"id": "ctl0_CONTENU_PAGE_etatCivil_ListeRegion"})
    regions = []
    for opt in select.find_all("option"):
        if opt["value"] != "0":
            regions.append({"id": opt["value"], "name": opt.text.strip()})
    return regions

def get_provinces(region_id, prado_pagestate):
    data = {
        "PRADO_PAGESTATE": prado_pagestate,
        "ctl0$CONTENU_PAGE$etatCivil$panelEtatCivil": "ctl0$CONTENU_PAGE$etatCivil$naissanceMaroc",
        "ctl0$CONTENU_PAGE$etatCivil$ListeRegion": region_id,
        "ctl0$CONTENU_PAGE$etatCivil$ListeProvince": "0",
        "ctl0$CONTENU_PAGE$etatCivil$ListeCommune": "0",
        "ctl0$CONTENU_PAGE$etatCivil$ListePrefectureArondissement": "0",
        "ctl0$CONTENU_PAGE$etatCivil$ListeArondissement": "0",
        "ctl0$CONTENU_PAGE$etatCivil$ListeBec": "0",
        "PRADO_POSTBACK_TARGET": "ctl0$CONTENU_PAGE$etatCivil$ListeRegion",
        "PRADO_POSTBACK_PARAMETER": "",
    }
    resp = session.post(BASE_URL, data=data, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    select = soup.find("select", {"id": "ctl0_CONTENU_PAGE_etatCivil_ListeProvince"})
    provinces = []
    for opt in select.find_all("option"):
        if opt["value"] != "0":
            provinces.append({"id": opt["value"], "name": opt.text.strip()})
    prado_pagestate_tag = soup.find("input", {"name": "PRADO_PAGESTATE"})
    if not prado_pagestate_tag:
        raise Exception("Impossible de trouver PRADO_PAGESTATE après sélection de la région.")
    prado_pagestate = prado_pagestate_tag["value"]
    return provinces, prado_pagestate

def get_communes(region_id, province_id, prado_pagestate):
    data = {
        "PRADO_PAGESTATE": prado_pagestate,
        "ctl0$CONTENU_PAGE$etatCivil$panelEtatCivil": "ctl0$CONTENU_PAGE$etatCivil$naissanceMaroc",
        "ctl0$CONTENU_PAGE$etatCivil$ListeRegion": region_id,
        "ctl0$CONTENU_PAGE$etatCivil$ListeProvince": province_id,
        "ctl0$CONTENU_PAGE$etatCivil$ListeCommune": "0",
        "ctl0$CONTENU_PAGE$etatCivil$ListePrefectureArondissement": "0",
        "ctl0$CONTENU_PAGE$etatCivil$ListeArondissement": "0",
        "ctl0$CONTENU_PAGE$etatCivil$ListeBec": "0",
        "PRADO_POSTBACK_TARGET": "ctl0$CONTENU_PAGE$etatCivil$ListeProvince",
        "PRADO_POSTBACK_PARAMETER": "",
    }
    resp = session.post(BASE_URL, data=data, headers=headers)
    soup = BeautifulSoup(resp.text, "lxml")
    select = soup.find("select", {"id": "ctl0_CONTENU_PAGE_etatCivil_ListeCommune"})
    communes = []
    for opt in select.find_all("option"):
        if opt["value"] != "0":
            communes.append(opt.text.strip())
    return communes

def main():
    lang = "fr"
    if len(sys.argv) > 1 and sys.argv[1] in ("fr", "ar"):
        lang = sys.argv[1]
    else:
        print("Usage: python scrap_watiqa_multi.py [fr|ar]")
        print("Par défaut : français")
    os.makedirs("data", exist_ok=True)
    output_file = "data/regions_prefectures_communes.json" if lang == "fr" else "data/regions_prefectures_communes_ar.json"

    soup, prado_pagestate = get_initial_form(lang)
    regions = get_regions(soup)
    result = {}
    for region in regions:
        print(f"Région: {region['name']}")
        provinces, prado_pagestate = get_provinces(region["id"], prado_pagestate)
        result[region["name"]] = {}
        for province in provinces:
            print(f"  Préfecture: {province['name']}")
            communes = get_communes(region["id"], province["id"], prado_pagestate)
            result[region["name"]][province["name"]] = communes
            time.sleep(0.5)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
