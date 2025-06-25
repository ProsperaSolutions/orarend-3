import streamlit as st
import json
import datetime
from logic import generate_schedule_for_all

st.set_page_config(page_title="📘 Órarend Adatszerkesztő", layout="wide")
st.title("📘 Órarend Adatszerkesztő GUI")

if "data" not in st.session_state:
    st.session_state.data = []
    st.session_state.data = {
        "csoportok": [],
        "oktatok": [],
        "termek": [],
        "idosavok": [],
    }

st.markdown("### 📦 JSON betöltése")
uploaded = st.file_uploader("Tölts fel egy bemeneti JSON fájlt", type=["json"])
if uploaded:
    st.session_state.data = json.load(uploaded)
    st.success("✅ JSON sikeresen betöltve")
    # Streamlit's uploader returns a BytesIO-like object.  Read its contents
    # explicitly to avoid issues with file position or binary mode on different
    # platforms.
    try:
        content = uploaded.getvalue().decode("utf-8")
        loaded = json.loads(content)
    except Exception as e:
        st.error(f"❌ JSON beolvasási hiba: {e}")
        loaded = None
    if loaded is not None:
        if isinstance(loaded, list):
            st.session_state.data = {
                "csoportok": loaded,
                "oktatok": [],
                "termek": [],
                "idosavok": [],
            }
        elif isinstance(loaded, dict):
            # Normalize structure so missing keys become empty lists
            st.session_state.data = {
                "csoportok": loaded.get("csoportok", []),
                "oktatok": loaded.get("oktatok", []),
                "termek": loaded.get("termek", []),
                "idosavok": loaded.get("idosavok", []),
            }
        else:
            st.error("❌ A JSON szerkezete érvénytelen")
        st.success("✅ JSON sikeresen betöltve")

if st.button("➕ Új tanulócsoport hozzáadása"):
    uj_id = f"C{len(st.session_state.data)+1:02d}"
    st.session_state.data.append({
        "csoport": {"id": uj_id, "nev": f"Új csoport {uj_id}", "letszam": 30},
        "tantargyak": [],
        "oktatok": [],
        "termek": [],
        "idosavok": [
            {"id": "H1", "nap": "Hetfo", "ido": "08:00"},
            {"id": "H2", "nap": "Hetfo", "ido": "10:00"},
            {"id": "K1", "nap": "Kedd", "ido": "08:00"},
            {"id": "K2", "nap": "Kedd", "ido": "10:00"},
            {"id": "S1", "nap": "Szerda", "ido": "08:00"},
            {"id": "S2", "nap": "Szerda", "ido": "10:00"}
        ],
        "beallitasok": {"hetek_szama": 2, "kezdo_datum": "2025-09-01"}
    })

for idx, group in enumerate(st.session_state.data):
    uj_id = f"C{len(st.session_state.data['csoportok'])+1:02d}"
    st.session_state.data["csoportok"].append(
        {
            "csoport": {"id": uj_id, "nev": f"Új csoport {uj_id}", "letszam": 30},
            "tantargyak": [],
            "beallitasok": {"hetek_szama": 2, "kezdo_datum": "2025-09-01"},
        }
    )

for idx, group in enumerate(st.session_state.data["csoportok"]):
    with st.expander(f"👥 {group['csoport']['nev']} ({group['csoport']['id']})"):
        col1, col2 = st.columns(2)
        group['csoport']['nev'] = col1.text_input("📛 Csoport neve", value=group['csoport']['nev'], key=f"nev_{idx}")
        group['csoport']['letszam'] = col2.number_input("👥 Létszám", min_value=1, step=1, value=group['csoport']['letszam'], key=f"letszam_{idx}")
        group["csoport"]["nev"] = col1.text_input(
            "📛 Csoport neve", value=group["csoport"]["nev"], key=f"nev_{idx}"
        )
        group["csoport"]["letszam"] = col2.number_input(
            "👥 Létszám",
            min_value=1,
            step=1,
            value=group["csoport"]["letszam"],
            key=f"letszam_{idx}",
        )

        col3, col4 = st.columns(2)
        group['beallitasok']['kezdo_datum'] = col3.date_input("📅 Kezdő dátum", value=datetime.datetime.strptime(group['beallitasok']['kezdo_datum'], "%Y-%m-%d"), key=f"datum_{idx}").strftime("%Y-%m-%d")
        group['beallitasok']['hetek_szama'] = col4.number_input("📆 Hetek száma", min_value=1, max_value=52, value=group['beallitasok']['hetek_szama'], key=f"hetek_{idx}")
        group["beallitasok"]["kezdo_datum"] = col3.date_input(
            "📅 Kezdő dátum",
            value=datetime.datetime.strptime(
                group["beallitasok"]["kezdo_datum"], "%Y-%m-%d"
            ),
            key=f"datum_{idx}",
        ).strftime("%Y-%m-%d")
        group["beallitasok"]["hetek_szama"] = col4.number_input(
            "📆 Hetek száma",
            min_value=1,
            max_value=52,
            value=group["beallitasok"]["hetek_szama"],
            key=f"hetek_{idx}",
        )

        st.markdown("#### 📚 Tantárgyak")
        for t_idx, tantargy in enumerate(group['tantargyak']):
        for t_idx, tantargy in enumerate(group["tantargyak"]):
            st.markdown(f"**Tantárgy {t_idx+1}**")
            tantargy['nev'] = st.text_input("Név", tantargy['nev'], key=f"tnev_{idx}_{t_idx}")
            tantargy['oraszam'] = st.number_input("Óraszám", min_value=1, value=tantargy['oraszam'], key=f"ora_{idx}_{t_idx}")
            tantargy['tipus'] = st.selectbox("Típus", ["elmelet", "gyakorlat"], index=0 if tantargy['tipus']=="elmelet" else 1, key=f"ttip_{idx}_{t_idx}")
            tantargy['teremtipus'] = st.text_input("Terem típusa", tantargy['teremtipus'], key=f"tt_{idx}_{t_idx}")
            tantargy["nev"] = st.text_input(
                "Név", tantargy["nev"], key=f"tnev_{idx}_{t_idx}"
            )
            tantargy["oraszam"] = st.number_input(
                "Óraszám",
                min_value=1,
                value=tantargy["oraszam"],
                key=f"ora_{idx}_{t_idx}",
            )
            tantargy["tipus"] = st.selectbox(
                "Típus",
                ["elmelet", "gyakorlat"],
                index=0 if tantargy["tipus"] == "elmelet" else 1,
                key=f"ttip_{idx}_{t_idx}",
            )
            tantargy["teremtipus"] = st.text_input(
                "Terem típusa", tantargy["teremtipus"], key=f"tt_{idx}_{t_idx}"
            )
            st.markdown("---")

        if st.button("➕ Új tantárgy", key=f"new_tantargy_{idx}"):
            group['tantargyak'].append({
                "id": f"T{len(group['tantargyak']) + 1}",
                "nev": "Új tantárgy",
                "tipus": "elmelet",
                "oraszam": 30,
                "teremtipus": "elmeleti"
            })

        st.markdown("#### 🧑‍🏫 Oktatók")
        for o_idx, oktato in enumerate(group['oktatok']):
            st.markdown(f"**Oktató {o_idx+1}**")
            oktato['nev'] = st.text_input("Név", oktato['nev'], key=f"oknev_{idx}_{o_idx}")
            oktato['kompetenciak'] = st.multiselect("Kompetenciák", [t['id'] for t in group['tantargyak']], default=oktato['kompetenciak'], key=f"okkomp_{idx}_{o_idx}")
            oktato['elerhetoseg'] = st.multiselect("Elérhetőségi idősávok", [s['id'] for s in group['idosavok']], default=oktato['elerhetoseg'], key=f"okeler_{idx}_{o_idx}")
            st.markdown("---")

        if st.button("➕ Új oktató", key=f"new_oktato_{idx}"):
            group['oktatok'].append({
                "id": f"O{len(group['oktatok']) + 1}",
                "nev": "Új oktató",
                "kompetenciak": [],
                "elerhetoseg": []
            })

        st.markdown("#### 🏫 Termek")
        for r_idx, terem in enumerate(group['termek']):
            st.markdown(f"**Terem {r_idx+1}**")
            terem['nev'] = st.text_input("Név", terem['nev'], key=f"rnev_{idx}_{r_idx}")
            terem['tipus'] = st.text_input("Típus", terem['tipus'], key=f"rtip_{idx}_{r_idx}")
            terem['kapacitas'] = st.number_input("Kapacitás", min_value=1, value=terem['kapacitas'], key=f"rkap_{idx}_{r_idx}")
            st.markdown("---")
            group["tantargyak"].append(
                {
                    "id": f"T{len(group['tantargyak']) + 1}",
                    "nev": "Új tantárgy",
                    "tipus": "elmelet",
                    "oraszam": 30,
                    "teremtipus": "elmeleti",
                }
            )

        if st.button("➕ Új terem", key=f"new_terem_{idx}"):
            group['termek'].append({
                "id": f"R{len(group['termek']) + 1}",
                "nev": "Új terem",
                "tipus": "elmeleti",
                "kapacitas": 30
            })

st.markdown("---")
st.download_button("⬇️ JSON exportálása", json.dumps(st.session_state.data, indent=2, ensure_ascii=False), file_name="orarend_adatbazis.json", mime="application/json")

st.markdown("### 🧑‍🏫 Oktatók")
all_targyak = [
    t["id"] for g in st.session_state.data["csoportok"] for t in g["tantargyak"]
]
for o_idx, oktato in enumerate(st.session_state.data["oktatok"]):
    with st.expander(f"Oktató {o_idx+1} ({oktato['id']})"):
        oktato["nev"] = st.text_input(
            "Név", oktato.get("nev", ""), key=f"oknev_g_{o_idx}"
        )
        oktato["kompetenciak"] = st.multiselect(
            "Kompetenciák",
            all_targyak,
            default=oktato.get("kompetenciak", []),
            key=f"okcomp_g_{o_idx}",
        )
        oktato["elerhetoseg"] = st.multiselect(
            "Elérhetőségi idősávok",
            [s["id"] for s in st.session_state.data["idosavok"]],
            default=oktato.get("elerhetoseg", []),
            key=f"okeler_g_{o_idx}",
        )

if st.button("➕ Új oktató", key="add_global_oktato"):
    st.session_state.data["oktatok"].append(
        {
            "id": f"O{len(st.session_state.data['oktatok']) + 1}",
            "nev": "Új oktató",
            "kompetenciak": [],
            "elerhetoseg": [],
        }
    )

st.markdown("### 🏫 Termek")
for r_idx, terem in enumerate(st.session_state.data["termek"]):
    with st.expander(f"Terem {r_idx+1} ({terem['id']})"):
        terem["nev"] = st.text_input("Név", terem.get("nev", ""), key=f"rnev_g_{r_idx}")
        terem["tipus"] = st.text_input(
            "Típus", terem.get("tipus", ""), key=f"rtip_g_{r_idx}"
        )
        terem["kapacitas"] = st.number_input(
            "Kapacitás",
            min_value=1,
            value=terem.get("kapacitas", 1),
            key=f"rkap_g_{r_idx}",
        )

if st.button("➕ Új terem", key="add_global_terem"):
    st.session_state.data["termek"].append(
        {
            "id": f"R{len(st.session_state.data['termek']) + 1}",
            "nev": "Új terem",
            "tipus": "elmeleti",
            "kapacitas": 30,
        }
    )

st.markdown("### ⌚ Idősávok")
for s_idx, sav in enumerate(st.session_state.data["idosavok"]):
    with st.expander(f"Idősáv {s_idx+1} ({sav['id']})"):
        sav["nap"] = st.text_input("Nap", sav.get("nap", ""), key=f"savnap_{s_idx}")
        sav["ido"] = st.text_input("Idő", sav.get("ido", ""), key=f"savido_{s_idx}")

if st.button("➕ Új idősáv", key="add_global_idosav"):
    st.session_state.data["idosavok"].append(
        {
            "id": f"SAV{len(st.session_state.data['idosavok']) + 1}",
            "nap": "Hetfo",
            "ido": "08:00",
        }
    )

st.download_button(
    "⬇️ JSON exportálása",
    json.dumps(st.session_state.data, indent=2, ensure_ascii=False),
    file_name="orarend_adatbazis.json",
    mime="application/json",
    key="download_json",
)

if st.button("🧠 Órarend generálása"):
    result = generate_schedule_for_all(st.session_state.data)
    groups_for_gen = []
    for grp in st.session_state.data["csoportok"]:
        g = grp.copy()
        g["oktatok"] = st.session_state.data["oktatok"]
        g["termek"] = st.session_state.data["termek"]
        g["idosavok"] = st.session_state.data["idosavok"]
        groups_for_gen.append(g)
    result = generate_schedule_for_all(groups_for_gen)
    st.success("✅ Órarend generálva")
    st.dataframe(result)
logic.py
+75
-32


from datetime import datetime, timedelta
from collections import defaultdict
import random
import pandas as pd


def generate_schedule_for_all(csoportok):
    global_orarend = []
    global_oktatok_foglalt = defaultdict(set)
    global_termek_foglalt = defaultdict(set)
    global_csoport_foglalt = defaultdict(set)

    idopontok = {
        "H1": "08:00-10:00", "H2": "10:00-12:00", "H3": "12:00-14:00", "H4": "14:00-16:00", "H5": "16:00-18:00", "H6": "18:00-20:00",
        "K1": "08:00-10:00", "K2": "10:00-12:00", "K3": "12:00-14:00", "K4": "14:00-16:00", "K5": "16:00-18:00", "K6": "18:00-20:00",
        "S1": "08:00-10:00", "S2": "10:00-12:00", "S3": "12:00-14:00", "S4": "14:00-16:00", "S5": "16:00-18:00", "S6": "18:00-20:00",
        "CS1": "08:00-10:00", "CS2": "10:00-12:00", "CS3": "12:00-14:00", "CS4": "14:00-16:00", "CS5": "16:00-18:00", "CS6": "18:00-20:00",
        "P1": "08:00-10:00", "P2": "10:00-12:00", "P3": "12:00-14:00", "P4": "14:00-16:00", "P5": "16:00-18:00", "P6": "18:00-20:00"
        "H1": "08:00-10:00",
        "H2": "10:00-12:00",
        "H3": "12:00-14:00",
        "H4": "14:00-16:00",
        "H5": "16:00-18:00",
        "H6": "18:00-20:00",
        "K1": "08:00-10:00",
        "K2": "10:00-12:00",
        "K3": "12:00-14:00",
        "K4": "14:00-16:00",
        "K5": "16:00-18:00",
        "K6": "18:00-20:00",
        "S1": "08:00-10:00",
        "S2": "10:00-12:00",
        "S3": "12:00-14:00",
        "S4": "14:00-16:00",
        "S5": "16:00-18:00",
        "S6": "18:00-20:00",
        "CS1": "08:00-10:00",
        "CS2": "10:00-12:00",
        "CS3": "12:00-14:00",
        "CS4": "14:00-16:00",
        "CS5": "16:00-18:00",
        "CS6": "18:00-20:00",
        "P1": "08:00-10:00",
        "P2": "10:00-12:00",
        "P3": "12:00-14:00",
        "P4": "14:00-16:00",
        "P5": "16:00-18:00",
        "P6": "18:00-20:00",
    }

    for input_data in csoportok:
        csoport = input_data['csoport']
        tantargyak = input_data['tantargyak']
        oktatok = input_data['oktatok']
        termek = input_data['termek']
        idosavok = input_data['idosavok']
        beallitasok = input_data['beallitasok']
        csoport = input_data["csoport"]
        tantargyak = input_data["tantargyak"]
        oktatok = input_data["oktatok"]
        termek = input_data["termek"]
        idosavok = input_data["idosavok"]
        beallitasok = input_data["beallitasok"]

        kezdo_datum = datetime.strptime(beallitasok["kezdo_datum"], "%Y-%m-%d")
        hetek_szama = beallitasok["hetek_szama"]
        ora_hossz = 2

        nap_map = {"Hetfo": 0, "Kedd": 1, "Szerda": 2, "Csütörtök": 3, "Péntek": 4}
        idosavok_kiterjesztve = []
        for het in range(hetek_szama):
            het_kezdete = kezdo_datum + timedelta(weeks=het)
            for sav in idosavok:
                if sav["nap"] not in nap_map:
                    continue
                datum = het_kezdete + timedelta(days=nap_map[sav["nap"]])
                idopont = datetime.strptime(sav["ido"], "%H:%M").time()
                teljes_datum = datetime.combine(datum.date(), idopont)
                idosavok_kiterjesztve.append({
                    "het": het,
                    "nap": sav["nap"],
                    "idosav_id": sav["id"],
                    "datum": teljes_datum
                })
                idosavok_kiterjesztve.append(
                    {
                        "het": het,
                        "nap": sav["nap"],
                        "idosav_id": sav["id"],
                        "datum": teljes_datum,
                    }
                )

        foglalt_tantargyak = defaultdict(lambda: defaultdict(set))
        foglalt_tantargy_savok = defaultdict(lambda: defaultdict(list))

        for tantargy in tantargyak:
            max_kap = max((r["kapacitas"] for r in termek if r["tipus"] == tantargy["teremtipus"]), default=1)
            orablokkok = ((csoport["letszam"] + max_kap - 1) // max_kap) * (tantargy["oraszam"] // ora_hossz)
            max_kap = max(
                (
                    r["kapacitas"]
                    for r in termek
                    if r["tipus"] == tantargy["teremtipus"]
                ),
                default=1,
            )
            orablokkok = ((csoport["letszam"] + max_kap - 1) // max_kap) * (
                tantargy["oraszam"] // ora_hossz
            )
            alkalmak = 0

            for ido in idosavok_kiterjesztve:
                if alkalmak >= orablokkok:
                    break

                napok = foglalt_tantargyak[tantargy["id"]][ido["het"]]
                if len(napok) >= 2 and ido["nap"] not in napok:
                    continue
                nap_savok = foglalt_tantargy_savok[tantargy["id"]][ido["het"]]
                if len([x for x in nap_savok if x[0] == ido["nap"]]) >= 2:
                    continue

                random.shuffle(oktatok)
                oktato_found = None
                for oktato in oktatok:
                    if tantargy["id"] in oktato["kompetenciak"] and ido["idosav_id"] in oktato["elerhetoseg"]:
                    if (
                        tantargy["id"] in oktato["kompetenciak"]
                        and ido["idosav_id"] in oktato["elerhetoseg"]
                    ):
                        if ido["datum"] not in global_oktatok_foglalt[oktato["id"]]:
                            oktato_found = oktato
                            break

                if not oktato_found:
                    continue

                random.shuffle(termek)
                terem_found = None
                for terem in termek:
                    if terem["tipus"] == tantargy["teremtipus"]:
                        if ido["datum"] not in global_termek_foglalt[terem["id"]]:
                            terem_found = terem
                            break

                if not terem_found:
                    continue

                if ido["datum"] in global_csoport_foglalt[csoport["id"]]:
                    continue

                global_orarend.append({
                    "csoport": csoport["nev"],
                    "tantargy": tantargy["nev"],
                    "oktato": oktato_found["nev"],
                    "terem": terem_found["nev"],
                    "idosav": ido["idosav_id"],
                    "datum": ido["datum"].strftime("%Y-%m-%d %H:%M"),
                    "datum_csak_nap": ido["datum"].strftime("%Y-%m-%d"),
                    "idointervallum": idopontok.get(ido["idosav_id"], "")
                })
                global_orarend.append(
                    {
                        "csoport": csoport["nev"],
                        "tantargy": tantargy["nev"],
                        "oktato": oktato_found["nev"],
                        "terem": terem_found["nev"],
                        "idosav": ido["idosav_id"],
                        "datum": ido["datum"].strftime("%Y-%m-%d %H:%M"),
                        "datum_csak_nap": ido["datum"].strftime("%Y-%m-%d"),
                        "idointervallum": idopontok.get(ido["idosav_id"], ""),
                    }
                )

                global_oktatok_foglalt[oktato_found["id"]].add(ido["datum"])
                global_termek_foglalt[terem_found["id"]].add(ido["datum"])
                global_csoport_foglalt[csoport["id"]].add(ido["datum"])
                foglalt_tantargyak[tantargy["id"]][ido["het"]].add(ido["nap"])
                foglalt_tantargy_savok[tantargy["id"]][ido["het"]].append((ido["nap"], ido["idosav_id"]))
                foglalt_tantargy_savok[tantargy["id"]][ido["het"]].append(
                    (ido["nap"], ido["idosav_id"])
                )
                alkalmak += 1

    return pd.DataFrame(global_orarend)
orarend_megjelenito.py
+12
-5


import streamlit as st
import pandas as pd

st.set_page_config(page_title="📅 Órarend Megjelenítő", layout="wide")
st.title("📅 Órarend Megjelenítő")

uploaded_file = st.file_uploader("📂 Töltsd fel az órarendet CSV formátumban", type=["csv"])
uploaded_file = st.file_uploader(
    "📂 Töltsd fel az órarendet CSV formátumban", type=["csv"]
)
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df["datum"] = pd.to_datetime(df["datum"])
    df["het"] = df["datum"].dt.isocalendar().week
    df["nap"] = df["datum"].dt.strftime("%A")
    df["datum_str"] = df["datum"].dt.strftime("%Y-%m-%d")

    csoportok = df["csoport"].unique()
    csoport = st.selectbox("👥 Csoport kiválasztása", csoportok)

    het_val = st.selectbox("📆 Hét kiválasztása", sorted(df["het"].unique()))

    szurt_df = df[(df["csoport"] == csoport) & (df["het"] == het_val)]

    szurt_df["nap_rendezes"] = pd.Categorical(szurt_df["nap"], categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], ordered=True)
    szurt_df["nap_rendezes"] = pd.Categorical(
        szurt_df["nap"],
        categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        ordered=True,
    )
    szurt_df = szurt_df.sort_values("nap_rendezes")

    szurt_df["info"] = szurt_df["tantargy"] + "\n" + szurt_df["oktato"] + "\n" + szurt_df["terem"]
    szurt_df["info"] = (
        szurt_df["tantargy"] + "\n" + szurt_df["oktato"] + "\n" + szurt_df["terem"]
    )

    tabla = szurt_df.pivot_table(
        index="idointervallum",
        columns="datum_str",
        values="info",
        aggfunc=lambda x: "\n".join(x)
        aggfunc=lambda x: "\n".join(x),
    )

    st.dataframe(tabla)
