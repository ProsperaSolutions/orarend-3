import streamlit as st
import pandas as pd

st.set_page_config(page_title="📅 Órarend Megjelenítő", layout="wide")
st.title("📅 Órarend Megjelenítő")

uploaded_file = st.file_uploader("📂 Töltsd fel az órarendet CSV formátumban", type=["csv"])
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
        aggfunc=lambda x: "\n".join(x),
    )

    st.dataframe(tabla)
