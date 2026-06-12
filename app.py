import streamlit as st
import streamlit.components.v1 as components
import json
import pandas as pd

st.set_page_config(
    page_title="Tabel Periodik Kimia",
    page_icon="⚛️",
    layout="wide"
)

# ══════════════════════════════════════════════════════════════════
# DATA ELEMEN (118 unsur)
# ══════════════════════════════════════════════════════════════════
ELEMENTS = [
    dict(n=1,  sym="H",  name="Hidrogen",       cat="nonmetal",   mass="1.008",  period=1, group=1,  config="1s¹",                    phase="Gas",   en="2.20", radius="53",  bp="-252.9°C", mp="-259.1°C"),
    dict(n=2,  sym="He", name="Helium",          cat="noble",      mass="4.003",  period=1, group=18, config="1s²",                    phase="Gas",   en="—",    radius="31",  bp="-268.9°C", mp="—"),
    dict(n=3,  sym="Li", name="Litium",          cat="alkali",     mass="6.941",  period=2, group=1,  config="[He] 2s¹",               phase="Padat", en="0.98", radius="167", bp="1342°C",   mp="180.5°C"),
    dict(n=4,  sym="Be", name="Berilium",        cat="alkaline",   mass="9.012",  period=2, group=2,  config="[He] 2s²",               phase="Padat", en="1.57", radius="112", bp="2470°C",   mp="1287°C"),
    dict(n=5,  sym="B",  name="Boron",           cat="metalloid",  mass="10.81",  period=2, group=13, config="[He] 2s² 2p¹",           phase="Padat", en="2.04", radius="87",  bp="2550°C",   mp="2076°C"),
    dict(n=6,  sym="C",  name="Karbon",          cat="nonmetal",   mass="12.01",  period=2, group=14, config="[He] 2s² 2p²",           phase="Padat", en="2.55", radius="67",  bp="3642°C",   mp="3675°C"),
    dict(n=7,  sym="N",  name="Nitrogen",        cat="nonmetal",   mass="14.01",  period=2, group=15, config="[He] 2s² 2p³",           phase="Gas",   en="3.04", radius="56",  bp="-195.8°C", mp="-210°C"),
    dict(n=8,  sym="O",  name="Oksigen",         cat="nonmetal",   mass="16.00",  period=2, group=16, config="[He] 2s² 2p⁴",           phase="Gas",   en="3.44", radius="48",  bp="-183°C",   mp="-218.8°C"),
    dict(n=9,  sym="F",  name="Fluor",           cat="halogen",    mass="19.00",  period=2, group=17, config="[He] 2s² 2p⁵",           phase="Gas",   en="3.98", radius="42",  bp="-188.1°C", mp="-219.6°C"),
    dict(n=10, sym="Ne", name="Neon",            cat="noble",      mass="20.18",  period=2, group=18, config="[He] 2s² 2p⁶",           phase="Gas",   en="—",    radius="38",  bp="-246.1°C", mp="-248.6°C"),
    dict(n=11, sym="Na", name="Natrium",         cat="alkali",     mass="22.99",  period=3, group=1,  config="[Ne] 3s¹",               phase="Padat", en="0.93", radius="190", bp="882.9°C",  mp="97.8°C"),
    dict(n=12, sym="Mg", name="Magnesium",       cat="alkaline",   mass="24.31",  period=3, group=2,  config="[Ne] 3s²",               phase="Padat", en="1.31", radius="145", bp="1090°C",   mp="650°C"),
    dict(n=13, sym="Al", name="Aluminium",       cat="posttrans",  mass="26.98",  period=3, group=13, config="[Ne] 3s² 3p¹",           phase="Padat", en="1.61", radius="118", bp="2519°C",   mp="660.3°C"),
    dict(n=14, sym="Si", name="Silikon",         cat="metalloid",  mass="28.09",  period=3, group=14, config="[Ne] 3s² 3p²",           phase="Padat", en="1.90", radius="111", bp="3265°C",   mp="1414°C"),
    dict(n=15, sym="P",  name="Fosfor",          cat="nonmetal",   mass="30.97",  period=3, group=15, config="[Ne] 3s² 3p³",           phase="Padat", en="2.19", radius="98",  bp="280.5°C",  mp="44.2°C"),
    dict(n=16, sym="S",  name="Belerang",        cat="nonmetal",   mass="32.06",  period=3, group=16, config="[Ne] 3s² 3p⁴",           phase="Padat", en="2.58", radius="88",  bp="444.6°C",  mp="119.6°C"),
    dict(n=17, sym="Cl", name="Klorin",          cat="halogen",    mass="35.45",  period=3, group=17, config="[Ne] 3s² 3p⁵",           phase="Gas",   en="3.16", radius="79",  bp="-34.1°C",  mp="-101.5°C"),
    dict(n=18, sym="Ar", name="Argon",           cat="noble",      mass="39.95",  period=3, group=18, config="[Ne] 3s² 3p⁶",           phase="Gas",   en="—",    radius="71",  bp="-185.9°C", mp="-189.3°C"),
    dict(n=19, sym="K",  name="Kalium",          cat="alkali",     mass="39.10",  period=4, group=1,  config="[Ar] 4s¹",               phase="Padat", en="0.82", radius="243", bp="759°C",    mp="63.5°C"),
    dict(n=20, sym="Ca", name="Kalsium",         cat="alkaline",   mass="40.08",  period=4, group=2,  config="[Ar] 4s²",               phase="Padat", en="1.00", radius="194", bp="1484°C",   mp="842°C"),
    dict(n=21, sym="Sc", name="Skandium",        cat="transition", mass="44.96",  period=4, group=3,  config="[Ar] 3d¹ 4s²",           phase="Padat", en="1.36", radius="184", bp="2836°C",   mp="1541°C"),
    dict(n=22, sym="Ti", name="Titanium",        cat="transition", mass="47.87",  period=4, group=4,  config="[Ar] 3d² 4s²",           phase="Padat", en="1.54", radius="176", bp="3287°C",   mp="1668°C"),
    dict(n=23, sym="V",  name="Vanadium",        cat="transition", mass="50.94",  period=4, group=5,  config="[Ar] 3d³ 4s²",           phase="Padat", en="1.63", radius="171", bp="3407°C",   mp="1910°C"),
    dict(n=24, sym="Cr", name="Kromium",         cat="transition", mass="52.00",  period=4, group=6,  config="[Ar] 3d⁵ 4s¹",           phase="Padat", en="1.66", radius="166", bp="2671°C",   mp="1907°C"),
    dict(n=25, sym="Mn", name="Mangan",          cat="transition", mass="54.94",  period=4, group=7,  config="[Ar] 3d⁵ 4s²",           phase="Padat", en="1.55", radius="161", bp="2061°C",   mp="1246°C"),
    dict(n=26, sym="Fe", name="Besi",            cat="transition", mass="55.85",  period=4, group=8,  config="[Ar] 3d⁶ 4s²",           phase="Padat", en="1.83", radius="156", bp="2861°C",   mp="1538°C"),
    dict(n=27, sym="Co", name="Kobalt",          cat="transition", mass="58.93",  period=4, group=9,  config="[Ar] 3d⁷ 4s²",           phase="Padat", en="1.88", radius="152", bp="2927°C",   mp="1495°C"),
    dict(n=28, sym="Ni", name="Nikel",           cat="transition", mass="58.69",  period=4, group=10, config="[Ar] 3d⁸ 4s²",           phase="Padat", en="1.91", radius="149", bp="2913°C",   mp="1455°C"),
    dict(n=29, sym="Cu", name="Tembaga",         cat="transition", mass="63.55",  period=4, group=11, config="[Ar] 3d¹⁰ 4s¹",          phase="Padat", en="1.90", radius="145", bp="2562°C",   mp="1084.6°C"),
    dict(n=30, sym="Zn", name="Seng",            cat="transition", mass="65.38",  period=4, group=12, config="[Ar] 3d¹⁰ 4s²",          phase="Padat", en="1.65", radius="142", bp="907°C",    mp="419.5°C"),
    dict(n=31, sym="Ga", name="Galium",          cat="posttrans",  mass="69.72",  period=4, group=13, config="[Ar] 3d¹⁰ 4s² 4p¹",      phase="Padat", en="1.81", radius="136", bp="2229°C",   mp="29.8°C"),
    dict(n=32, sym="Ge", name="Germanium",       cat="metalloid",  mass="72.63",  period=4, group=14, config="[Ar] 3d¹⁰ 4s² 4p²",      phase="Padat", en="2.01", radius="125", bp="2820°C",   mp="938.3°C"),
    dict(n=33, sym="As", name="Arsen",           cat="metalloid",  mass="74.92",  period=4, group=15, config="[Ar] 3d¹⁰ 4s² 4p³",      phase="Padat", en="2.18", radius="114", bp="887°C",    mp="817°C"),
    dict(n=34, sym="Se", name="Selenium",        cat="nonmetal",   mass="78.97",  period=4, group=16, config="[Ar] 3d¹⁰ 4s² 4p⁴",      phase="Padat", en="2.55", radius="103", bp="685°C",    mp="220.8°C"),
    dict(n=35, sym="Br", name="Brom",            cat="halogen",    mass="79.90",  period=4, group=17, config="[Ar] 3d¹⁰ 4s² 4p⁵",      phase="Cair",  en="2.96", radius="94",  bp="58.8°C",   mp="-7.3°C"),
    dict(n=36, sym="Kr", name="Kripton",         cat="noble",      mass="83.80",  period=4, group=18, config="[Ar] 3d¹⁰ 4s² 4p⁶",      phase="Gas",   en="3.00", radius="88",  bp="-153.4°C", mp="-157.4°C"),
    dict(n=37, sym="Rb", name="Rubidium",        cat="alkali",     mass="85.47",  period=5, group=1,  config="[Kr] 5s¹",               phase="Padat", en="0.82", radius="265", bp="688°C",    mp="39.3°C"),
    dict(n=38, sym="Sr", name="Stronsium",       cat="alkaline",   mass="87.62",  period=5, group=2,  config="[Kr] 5s²",               phase="Padat", en="0.95", radius="219", bp="1377°C",   mp="777°C"),
    dict(n=39, sym="Y",  name="Itrium",          cat="transition", mass="88.91",  period=5, group=3,  config="[Kr] 4d¹ 5s²",           phase="Padat", en="1.22", radius="212", bp="3345°C",   mp="1526°C"),
    dict(n=40, sym="Zr", name="Zirkonium",       cat="transition", mass="91.22",  period=5, group=4,  config="[Kr] 4d² 5s²",           phase="Padat", en="1.33", radius="206", bp="4409°C",   mp="1855°C"),
    dict(n=41, sym="Nb", name="Niobium",         cat="transition", mass="92.91",  period=5, group=5,  config="[Kr] 4d⁴ 5s¹",           phase="Padat", en="1.60", radius="198", bp="4744°C",   mp="2477°C"),
    dict(n=42, sym="Mo", name="Molibden",        cat="transition", mass="95.96",  period=5, group=6,  config="[Kr] 4d⁵ 5s¹",           phase="Padat", en="2.16", radius="190", bp="4639°C",   mp="2623°C"),
    dict(n=43, sym="Tc", name="Teknesium",       cat="transition", mass="(98)",   period=5, group=7,  config="[Kr] 4d⁵ 5s²",           phase="Padat", en="1.90", radius="183", bp="4265°C",   mp="2157°C"),
    dict(n=44, sym="Ru", name="Ruthenium",       cat="transition", mass="101.1",  period=5, group=8,  config="[Kr] 4d⁷ 5s¹",           phase="Padat", en="2.20", radius="178", bp="3900°C",   mp="2334°C"),
    dict(n=45, sym="Rh", name="Rhodium",         cat="transition", mass="102.9",  period=5, group=9,  config="[Kr] 4d⁸ 5s¹",           phase="Padat", en="2.28", radius="173", bp="3695°C",   mp="1964°C"),
    dict(n=46, sym="Pd", name="Paladium",        cat="transition", mass="106.4",  period=5, group=10, config="[Kr] 4d¹⁰",              phase="Padat", en="2.20", radius="169", bp="2963°C",   mp="1554.9°C"),
    dict(n=47, sym="Ag", name="Perak",           cat="transition", mass="107.9",  period=5, group=11, config="[Kr] 4d¹⁰ 5s¹",          phase="Padat", en="1.93", radius="165", bp="2162°C",   mp="961.8°C"),
    dict(n=48, sym="Cd", name="Kadmium",         cat="transition", mass="112.4",  period=5, group=12, config="[Kr] 4d¹⁰ 5s²",          phase="Padat", en="1.69", radius="161", bp="767°C",    mp="321.1°C"),
    dict(n=49, sym="In", name="Indium",          cat="posttrans",  mass="114.8",  period=5, group=13, config="[Kr] 4d¹⁰ 5s² 5p¹",      phase="Padat", en="1.78", radius="156", bp="2072°C",   mp="156.6°C"),
    dict(n=50, sym="Sn", name="Timah",           cat="posttrans",  mass="118.7",  period=5, group=14, config="[Kr] 4d¹⁰ 5s² 5p²",      phase="Padat", en="1.96", radius="145", bp="2602°C",   mp="231.9°C"),
    dict(n=51, sym="Sb", name="Antimon",         cat="metalloid",  mass="121.8",  period=5, group=15, config="[Kr] 4d¹⁰ 5s² 5p³",      phase="Padat", en="2.05", radius="133", bp="1587°C",   mp="630.6°C"),
    dict(n=52, sym="Te", name="Telurium",        cat="metalloid",  mass="127.6",  period=5, group=16, config="[Kr] 4d¹⁰ 5s² 5p⁴",      phase="Padat", en="2.10", radius="123", bp="988°C",    mp="449.5°C"),
    dict(n=53, sym="I",  name="Iodium",          cat="halogen",    mass="126.9",  period=5, group=17, config="[Kr] 4d¹⁰ 5s² 5p⁵",      phase="Padat", en="2.66", radius="115", bp="184.3°C",  mp="113.7°C"),
    dict(n=54, sym="Xe", name="Xenon",           cat="noble",      mass="131.3",  period=5, group=18, config="[Kr] 4d¹⁰ 5s² 5p⁶",      phase="Gas",   en="2.60", radius="108", bp="-108.1°C", mp="-111.8°C"),
    dict(n=55, sym="Cs", name="Sesium",          cat="alkali",     mass="132.9",  period=6, group=1,  config="[Xe] 6s¹",               phase="Padat", en="0.79", radius="298", bp="671°C",    mp="28.5°C"),
    dict(n=56, sym="Ba", name="Barium",          cat="alkaline",   mass="137.3",  period=6, group=2,  config="[Xe] 6s²",               phase="Padat", en="0.89", radius="253", bp="1870°C",   mp="727°C"),
    dict(n=57, sym="La", name="Lantanum",        cat="lanthanide", mass="138.9",  period=6, group=3,  config="[Xe] 5d¹ 6s²",           phase="Padat", en="1.10", radius="250", bp="3464°C",   mp="918°C"),
    dict(n=72, sym="Hf", name="Hafnium",         cat="transition", mass="178.5",  period=6, group=4,  config="[Xe] 4f¹⁴ 5d² 6s²",      phase="Padat", en="1.30", radius="208", bp="4600°C",   mp="2233°C"),
    dict(n=73, sym="Ta", name="Tantalum",        cat="transition", mass="180.9",  period=6, group=5,  config="[Xe] 4f¹⁴ 5d³ 6s²",      phase="Padat", en="1.50", radius="200", bp="5458°C",   mp="3017°C"),
    dict(n=74, sym="W",  name="Wolfram",         cat="transition", mass="183.8",  period=6, group=6,  config="[Xe] 4f¹⁴ 5d⁴ 6s²",      phase="Padat", en="2.36", radius="193", bp="5555°C",   mp="3422°C"),
    dict(n=75, sym="Re", name="Renium",          cat="transition", mass="186.2",  period=6, group=7,  config="[Xe] 4f¹⁴ 5d⁵ 6s²",      phase="Padat", en="1.90", radius="188", bp="5596°C",   mp="3186°C"),
    dict(n=76, sym="Os", name="Osmium",          cat="transition", mass="190.2",  period=6, group=8,  config="[Xe] 4f¹⁴ 5d⁶ 6s²",      phase="Padat", en="2.20", radius="185", bp="5012°C",   mp="3033°C"),
    dict(n=77, sym="Ir", name="Iridium",         cat="transition", mass="192.2",  period=6, group=9,  config="[Xe] 4f¹⁴ 5d⁷ 6s²",      phase="Padat", en="2.20", radius="180", bp="4428°C",   mp="2446°C"),
    dict(n=78, sym="Pt", name="Platinum",        cat="transition", mass="195.1",  period=6, group=10, config="[Xe] 4f¹⁴ 5d⁹ 6s¹",      phase="Padat", en="2.28", radius="177", bp="3825°C",   mp="1768.3°C"),
    dict(n=79, sym="Au", name="Emas",            cat="transition", mass="197.0",  period=6, group=11, config="[Xe] 4f¹⁴ 5d¹⁰ 6s¹",     phase="Padat", en="2.54", radius="174", bp="2856°C",   mp="1064.2°C"),
    dict(n=80, sym="Hg", name="Raksa",           cat="transition", mass="200.6",  period=6, group=12, config="[Xe] 4f¹⁴ 5d¹⁰ 6s²",     phase="Cair",  en="2.00", radius="171", bp="356.7°C",  mp="-38.8°C"),
    dict(n=81, sym="Tl", name="Talium",          cat="posttrans",  mass="204.4",  period=6, group=13, config="[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹", phase="Padat", en="1.62", radius="156", bp="1473°C",   mp="304°C"),
    dict(n=82, sym="Pb", name="Timbal",          cat="posttrans",  mass="207.2",  period=6, group=14, config="[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p²", phase="Padat", en="2.33", radius="154", bp="1749°C",   mp="327.5°C"),
    dict(n=83, sym="Bi", name="Bismut",          cat="posttrans",  mass="209.0",  period=6, group=15, config="[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p³", phase="Padat", en="2.02", radius="143", bp="1564°C",   mp="271.4°C"),
    dict(n=84, sym="Po", name="Polonium",        cat="posttrans",  mass="(209)",  period=6, group=16, config="[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁴", phase="Padat", en="2.00", radius="135", bp="962°C",    mp="254°C"),
    dict(n=85, sym="At", name="Astatin",         cat="halogen",    mass="(210)",  period=6, group=17, config="[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁵", phase="Padat", en="2.20", radius="127", bp="337°C",    mp="302°C"),
    dict(n=86, sym="Rn", name="Radon",           cat="noble",      mass="(222)",  period=6, group=18, config="[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁶", phase="Gas",   en="—",    radius="120", bp="-61.7°C",  mp="-71°C"),
    dict(n=87, sym="Fr", name="Fransium",        cat="alkali",     mass="(223)",  period=7, group=1,  config="[Rn] 7s¹",               phase="Padat", en="0.70", radius="348", bp="677°C",    mp="27°C"),
    dict(n=88, sym="Ra", name="Radium",          cat="alkaline",   mass="(226)",  period=7, group=2,  config="[Rn] 7s²",               phase="Padat", en="0.90", radius="283", bp="1737°C",   mp="700°C"),
    dict(n=89, sym="Ac", name="Aktinium",        cat="actinide",   mass="(227)",  period=7, group=3,  config="[Rn] 6d¹ 7s²",           phase="Padat", en="1.10", radius="260", bp="3198°C",   mp="1051°C"),
    dict(n=104,sym="Rf", name="Rutherfordium",   cat="transition", mass="(267)",  period=7, group=4,  config="[Rn] 5f¹⁴ 6d² 7s²",      phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=105,sym="Db", name="Dubnium",         cat="transition", mass="(268)",  period=7, group=5,  config="[Rn] 5f¹⁴ 6d³ 7s²",      phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=106,sym="Sg", name="Seaborgium",      cat="transition", mass="(271)",  period=7, group=6,  config="[Rn] 5f¹⁴ 6d⁴ 7s²",      phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=107,sym="Bh", name="Bohrium",         cat="transition", mass="(272)",  period=7, group=7,  config="[Rn] 5f¹⁴ 6d⁵ 7s²",      phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=108,sym="Hs", name="Hassium",         cat="transition", mass="(277)",  period=7, group=8,  config="[Rn] 5f¹⁴ 6d⁶ 7s²",      phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=109,sym="Mt", name="Meitnerium",      cat="transition", mass="(276)",  period=7, group=9,  config="[Rn] 5f¹⁴ 6d⁷ 7s²",      phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=110,sym="Ds", name="Darmstadtium",    cat="transition", mass="(281)",  period=7, group=10, config="[Rn] 5f¹⁴ 6d⁸ 7s²",      phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=111,sym="Rg", name="Roentgenium",     cat="transition", mass="(280)",  period=7, group=11, config="[Rn] 5f¹⁴ 6d¹⁰ 7s¹",     phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=112,sym="Cn", name="Kopernikum",      cat="transition", mass="(285)",  period=7, group=12, config="[Rn] 5f¹⁴ 6d¹⁰ 7s²",     phase="Gas",   en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=113,sym="Nh", name="Nihonium",        cat="posttrans",  mass="(284)",  period=7, group=13, config="[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p¹", phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=114,sym="Fl", name="Flerovium",       cat="posttrans",  mass="(289)",  period=7, group=14, config="[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p²", phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=115,sym="Mc", name="Moskovium",       cat="posttrans",  mass="(288)",  period=7, group=15, config="[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p³", phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=116,sym="Lv", name="Livermorium",     cat="posttrans",  mass="(293)",  period=7, group=16, config="[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁴", phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=117,sym="Ts", name="Tennesin",        cat="halogen",    mass="(294)",  period=7, group=17, config="[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁵", phase="Padat", en="—",    radius="—",   bp="—",        mp="—"),
    dict(n=118,sym="Og", name="Oganesson",       cat="noble",      mass="(294)",  period=7, group=18, config="[Rn] 5f¹⁴ 6d¹⁰ 7s² 7p⁶", phase="Gas",   en="—",    radius="—",   bp="—",        mp="—"),
    # Lanthanida
    dict(n=58, sym="Ce", name="Serium",          cat="lanthanide", mass="140.1",  period=8, group=4,  config="[Xe] 4f¹ 5d¹ 6s²",       phase="Padat", en="1.12", radius="247", bp="3433°C",   mp="798°C"),
    dict(n=59, sym="Pr", name="Praseodimium",    cat="lanthanide", mass="140.9",  period=8, group=5,  config="[Xe] 4f³ 6s²",            phase="Padat", en="1.13", radius="243", bp="3520°C",   mp="931°C"),
    dict(n=60, sym="Nd", name="Neodimium",       cat="lanthanide", mass="144.2",  period=8, group=6,  config="[Xe] 4f⁴ 6s²",            phase="Padat", en="1.14", radius="242", bp="3074°C",   mp="1021°C"),
    dict(n=61, sym="Pm", name="Prometium",       cat="lanthanide", mass="(145)",  period=8, group=7,  config="[Xe] 4f⁵ 6s²",            phase="Padat", en="1.13", radius="241", bp="3000°C",   mp="1042°C"),
    dict(n=62, sym="Sm", name="Samarium",        cat="lanthanide", mass="150.4",  period=8, group=8,  config="[Xe] 4f⁶ 6s²",            phase="Padat", en="1.17", radius="238", bp="1794°C",   mp="1072°C"),
    dict(n=63, sym="Eu", name="Europium",        cat="lanthanide", mass="152.0",  period=8, group=9,  config="[Xe] 4f⁷ 6s²",            phase="Padat", en="1.20", radius="231", bp="1529°C",   mp="822°C"),
    dict(n=64, sym="Gd", name="Gadolinium",      cat="lanthanide", mass="157.3",  period=8, group=10, config="[Xe] 4f⁷ 5d¹ 6s²",        phase="Padat", en="1.20", radius="233", bp="3273°C",   mp="1313°C"),
    dict(n=65, sym="Tb", name="Terbium",         cat="lanthanide", mass="158.9",  period=8, group=11, config="[Xe] 4f⁹ 6s²",            phase="Padat", en="1.10", radius="225", bp="3230°C",   mp="1356°C"),
    dict(n=66, sym="Dy", name="Disprosium",      cat="lanthanide", mass="162.5",  period=8, group=12, config="[Xe] 4f¹⁰ 6s²",           phase="Padat", en="1.22", radius="228", bp="2567°C",   mp="1412°C"),
    dict(n=67, sym="Ho", name="Holmium",         cat="lanthanide", mass="164.9",  period=8, group=13, config="[Xe] 4f¹¹ 6s²",           phase="Padat", en="1.23", radius="226", bp="2720°C",   mp="1474°C"),
    dict(n=68, sym="Er", name="Erbium",          cat="lanthanide", mass="167.3",  period=8, group=14, config="[Xe] 4f¹² 6s²",           phase="Padat", en="1.24", radius="226", bp="2868°C",   mp="1529°C"),
    dict(n=69, sym="Tm", name="Tulium",          cat="lanthanide", mass="168.9",  period=8, group=15, config="[Xe] 4f¹³ 6s²",           phase="Padat", en="1.25", radius="222", bp="1950°C",   mp="1545°C"),
    dict(n=70, sym="Yb", name="Iterbium",        cat="lanthanide", mass="173.0",  period=8, group=16, config="[Xe] 4f¹⁴ 6s²",           phase="Padat", en="1.10", radius="222", bp="1196°C",   mp="824°C"),
    dict(n=71, sym="Lu", name="Lutesium",        cat="lanthanide", mass="175.0",  period=8, group=17, config="[Xe] 4f¹⁴ 5d¹ 6s²",       phase="Padat", en="1.27", radius="217", bp="3402°C",   mp="1663°C"),
    # Aktinida
    dict(n=90, sym="Th", name="Thorium",         cat="actinide",   mass="232.0",  period=9, group=4,  config="[Rn] 6d² 7s²",            phase="Padat", en="1.30", radius="237", bp="4788°C",   mp="1750°C"),
    dict(n=91, sym="Pa", name="Protaktinium",    cat="actinide",   mass="231.0",  period=9, group=5,  config="[Rn] 5f² 6d¹ 7s²",        phase="Padat", en="1.50", radius="—",   bp="4027°C",   mp="1572°C"),
    dict(n=92, sym="U",  name="Uranium",         cat="actinide",   mass="238.0",  period=9, group=6,  config="[Rn] 5f³ 6d¹ 7s²",        phase="Padat", en="1.38", radius="175", bp="4131°C",   mp="1135°C"),
    dict(n=93, sym="Np", name="Neptunium",       cat="actinide",   mass="(237)",  period=9, group=7,  config="[Rn] 5f⁴ 6d¹ 7s²",        phase="Padat", en="1.36", radius="—",   bp="4000°C",   mp="644°C"),
    dict(n=94, sym="Pu", name="Plutonium",       cat="actinide",   mass="(244)",  period=9, group=8,  config="[Rn] 5f⁶ 7s²",            phase="Padat", en="1.28", radius="—",   bp="3228°C",   mp="640°C"),
    dict(n=95, sym="Am", name="Amerisium",       cat="actinide",   mass="(243)",  period=9, group=9,  config="[Rn] 5f⁷ 7s²",            phase="Padat", en="1.30", radius="—",   bp="2011°C",   mp="1176°C"),
    dict(n=96, sym="Cm", name="Kurium",          cat="actinide",   mass="(247)",  period=9, group=10, config="[Rn] 5f⁷ 6d¹ 7s²",        phase="Padat", en="1.30", radius="—",   bp="3110°C",   mp="1345°C"),
    dict(n=97, sym="Bk", name="Berkelium",       cat="actinide",   mass="(247)",  period=9, group=11, config="[Rn] 5f⁹ 7s²",            phase="Padat", en="1.30", radius="—",   bp="—",        mp="986°C"),
    dict(n=98, sym="Cf", name="Kalifornium",     cat="actinide",   mass="(251)",  period=9, group=12, config="[Rn] 5f¹⁰ 7s²",           phase="Padat", en="1.30", radius="—",   bp="—",        mp="900°C"),
    dict(n=99, sym="Es", name="Einsteinium",     cat="actinide",   mass="(252)",  period=9, group=13, config="[Rn] 5f¹¹ 7s²",           phase="Padat", en="1.30", radius="—",   bp="—",        mp="860°C"),
    dict(n=100,sym="Fm", name="Fermium",         cat="actinide",   mass="(257)",  period=9, group=14, config="[Rn] 5f¹² 7s²",           phase="Padat", en="1.30", radius="—",   bp="—",        mp="1527°C"),
    dict(n=101,sym="Md", name="Mendelevium",     cat="actinide",   mass="(258)",  period=9, group=15, config="[Rn] 5f¹³ 7s²",           phase="Padat", en="1.30", radius="—",   bp="—",        mp="827°C"),
    dict(n=102,sym="No", name="Nobelium",        cat="actinide",   mass="(259)",  period=9, group=16, config="[Rn] 5f¹⁴ 7s²",           phase="Padat", en="1.30", radius="—",   bp="—",        mp="827°C"),
    dict(n=103,sym="Lr", name="Lawrensium",      cat="actinide",   mass="(262)",  period=9, group=17, config="[Rn] 5f¹⁴ 7s² 7p¹",       phase="Padat", en="1.30", radius="—",   bp="—",        mp="1627°C"),
]

CAT_INFO = {
    "alkali":     {"label": "Logam Alkali",         "bg": "#FAEEDA", "color": "#633806", "border": "#EF9F27"},
    "alkaline":   {"label": "Logam Alkali Tanah",   "bg": "#FAC775", "color": "#633806", "border": "#EF9F27"},
    "transition": {"label": "Logam Transisi",       "bg": "#E6F1FB", "color": "#0C447C", "border": "#85B7EB"},
    "posttrans":  {"label": "Logam Pasca-Transisi", "bg": "#EEEDFE", "color": "#3C3489", "border": "#AFA9EC"},
    "metalloid":  {"label": "Metaloid",             "bg": "#EAF3DE", "color": "#3B6D11", "border": "#97C459"},
    "nonmetal":   {"label": "Non-Logam",            "bg": "#E1F5EE", "color": "#0F6E56", "border": "#5DCAA5"},
    "halogen":    {"label": "Halogen",              "bg": "#FBEAF0", "color": "#72243E", "border": "#ED93B1"},
    "noble":      {"label": "Gas Mulia",            "bg": "#FAECE7", "color": "#712B13", "border": "#F0997B"},
    "lanthanide": {"label": "Lantanida",            "bg": "#FCEBEB", "color": "#791F1F", "border": "#F09595"},
    "actinide":   {"label": "Aktinida",             "bg": "#F1EFE8", "color": "#444441", "border": "#B4B2A9"},
}

ELEMENT_INFO = {
    "O":  {"nama": "Oksigen",    "nomor": 8,  "massa": 15.999, "golongan": "Non-Logam"},
    "C":  {"nama": "Karbon",     "nomor": 6,  "massa": 12.011, "golongan": "Non-Logam"},
    "H":  {"nama": "Hidrogen",   "nomor": 1,  "massa": 1.008,  "golongan": "Non-Logam"},
    "N":  {"nama": "Nitrogen",   "nomor": 7,  "massa": 14.007, "golongan": "Non-Logam"},
    "Ca": {"nama": "Kalsium",    "nomor": 20, "massa": 40.078, "golongan": "Logam Alkali Tanah"},
    "P":  {"nama": "Fosfor",     "nomor": 15, "massa": 30.974, "golongan": "Non-Logam"},
    "K":  {"nama": "Kalium",     "nomor": 19, "massa": 39.098, "golongan": "Logam Alkali"},
    "S":  {"nama": "Sulfur",     "nomor": 16, "massa": 32.06,  "golongan": "Non-Logam"},
    "Na": {"nama": "Natrium",    "nomor": 11, "massa": 22.990, "golongan": "Logam Alkali"},
    "Cl": {"nama": "Klorin",     "nomor": 17, "massa": 35.45,  "golongan": "Halogen"},
    "Mg": {"nama": "Magnesium",  "nomor": 12, "massa": 24.305, "golongan": "Logam Alkali Tanah"},
    "Fe": {"nama": "Besi",       "nomor": 26, "massa": 55.845, "golongan": "Logam Transisi"},
    "Zn": {"nama": "Seng",       "nomor": 30, "massa": 65.38,  "golongan": "Logam Transisi"},
    "I":  {"nama": "Iodin",      "nomor": 53, "massa": 126.90, "golongan": "Halogen"},
    "F":  {"nama": "Fluor",      "nomor": 9,  "massa": 18.998, "golongan": "Halogen"},
    "Si": {"nama": "Silikon",    "nomor": 14, "massa": 28.085, "golongan": "Metaloid"},
    "Al": {"nama": "Aluminium",  "nomor": 13, "massa": 26.982, "golongan": "Logam Pasca-Transisi"},
    "Cr": {"nama": "Kromium",    "nomor": 24, "massa": 51.996, "golongan": "Logam Transisi"},
    "Ni": {"nama": "Nikel",      "nomor": 28, "massa": 58.693, "golongan": "Logam Transisi"},
    "Cu": {"nama": "Tembaga",    "nomor": 29, "massa": 63.546, "golongan": "Logam Transisi"},
    "Sn": {"nama": "Timah",      "nomor": 50, "massa": 118.71, "golongan": "Logam Pasca-Transisi"},
}

WARNA_GOLONGAN = {
    "Logam Alkali":           "#FFA07A",
    "Logam Alkali Tanah":     "#FFD700",
    "Logam Transisi":         "#87CEEB",
    "Logam Pasca-Transisi":   "#90EE90",
    "Metaloid":               "#DDA0DD",
    "Non-Logam":              "#98FB98",
    "Halogen":                "#FFB6C1",
    "Gas Mulia":              "#E6E6FA",
}

BAGIAN_TUBUH = {
    "🦴 Tulang & Gigi": {
        "deskripsi": "Tulang dan gigi adalah jaringan keras utama dalam tubuh manusia yang berfungsi sebagai penyangga, pelindung organ vital, dan tempat produksi sel darah.",
        "unsur": [
            {"simbol": "Ca", "persen": 39.0,  "fungsi": "Komponen utama hidroksiapatit — mineral penyusun tulang dan gigi, menjaga kepadatan dan kekuatan struktur tulang."},
            {"simbol": "O",  "persen": 28.0,  "fungsi": "Terdapat dalam gugus fosfat dan hidroksil pada hidroksiapatit, serta dalam matriks organik kolagen."},
            {"simbol": "P",  "persen": 17.0,  "fungsi": "Bergabung dengan kalsium membentuk kalsium fosfat, menyusun sekitar 85% cadangan fosfor tubuh ada di tulang."},
            {"simbol": "C",  "persen": 15.0,  "fungsi": "Menyusun kolagen — protein organik utama yang memberi elastisitas dan ketahanan tulang terhadap benturan."},
            {"simbol": "H",  "persen": 1.0,   "fungsi": "Terdapat dalam gugus hidroksil (-OH) pada mineral hidroksiapatit dan dalam struktur kolagen."},
        ]
    },
    "🩸 Darah": {
        "deskripsi": "Darah adalah jaringan cair yang beredar dalam sistem peredaran darah, bertugas mengangkut oksigen, nutrisi, hormon, dan membuang sisa metabolisme.",
        "unsur": [
            {"simbol": "O",  "persen": 65.0,  "fungsi": "Diangkut oleh hemoglobin dari paru-paru ke seluruh sel tubuh."},
            {"simbol": "C",  "persen": 18.0,  "fungsi": "Menyusun protein plasma (albumin, globulin, fibrinogen) dan glukosa."},
            {"simbol": "H",  "persen": 10.0,  "fungsi": "Komponen utama molekul air (H₂O) yang mendominasi plasma darah."},
            {"simbol": "N",  "persen": 3.0,   "fungsi": "Menyusun asam amino dan protein darah seperti hemoglobin dan antibodi."},
            {"simbol": "Na", "persen": 0.3,   "fungsi": "Ion utama ekstraseluler yang menjaga tekanan osmotik darah."},
            {"simbol": "Cl", "persen": 0.3,   "fungsi": "Anion utama dalam plasma darah yang menjaga keseimbangan elektrolit."},
            {"simbol": "K",  "persen": 0.2,   "fungsi": "Ion utama intraseluler yang berperan dalam transmisi impuls saraf."},
            {"simbol": "Fe", "persen": 0.006, "fungsi": "Inti atom pusat hemoglobin yang mengikat dan melepas oksigen."},
        ]
    },
    "💪 Otot": {
        "deskripsi": "Jaringan otot adalah jaringan yang mampu berkontraksi dan relaksasi untuk menghasilkan gerakan tubuh.",
        "unsur": [
            {"simbol": "O",  "persen": 65.0,  "fungsi": "Diperlukan untuk respirasi aerobik dalam mitokondria sel otot."},
            {"simbol": "C",  "persen": 18.0,  "fungsi": "Menyusun protein struktural otot seperti aktin dan miosin."},
            {"simbol": "H",  "persen": 10.0,  "fungsi": "Komponen air intraseluler dan menyusun seluruh rantai protein otot."},
            {"simbol": "N",  "persen": 3.0,   "fungsi": "Menyusun asam amino pembentuk protein otot."},
            {"simbol": "K",  "persen": 0.35,  "fungsi": "Menjaga potensial membran sel otot dan berperan dalam depolarisasi."},
            {"simbol": "P",  "persen": 0.2,   "fungsi": "Terdapat dalam ATP — sumber energi langsung untuk kontraksi otot."},
            {"simbol": "Ca", "persen": 0.1,   "fungsi": "Ion kalsium memicu kontraksi otot dengan berikatan pada troponin C."},
            {"simbol": "Mg", "persen": 0.05,  "fungsi": "Kofaktor enzim ATPase miosin untuk hidrolisis ATP."},
        ]
    },
    "🧠 Otak & Saraf": {
        "deskripsi": "Sistem saraf terdiri dari otak, sumsum tulang belakang, dan jaringan saraf yang mengatur seluruh fungsi tubuh.",
        "unsur": [
            {"simbol": "O",  "persen": 65.0,    "fungsi": "Otak mengonsumsi ~20% oksigen tubuh untuk metabolisme glukosa neuron."},
            {"simbol": "C",  "persen": 18.0,    "fungsi": "Menyusun lipid mielin yang melapisi akson saraf."},
            {"simbol": "H",  "persen": 10.0,    "fungsi": "Komponen utama air dan fosfolipid membran sel saraf."},
            {"simbol": "N",  "persen": 3.0,     "fungsi": "Menyusun neurotransmiter seperti dopamin, serotonin, dan GABA."},
            {"simbol": "P",  "persen": 1.1,     "fungsi": "Komponen fosfolipid pada membran sel saraf (mielin)."},
            {"simbol": "K",  "persen": 0.35,    "fungsi": "Ion kalium keluar saat repolarisasi, mengembalikan potensial membran."},
            {"simbol": "Na", "persen": 0.15,    "fungsi": "Ion natrium masuk ke dalam sel saraf saat depolarisasi."},
            {"simbol": "I",  "persen": 0.00002, "fungsi": "Hormon tiroid mengandung iodin, krusial dalam perkembangan otak."},
        ]
    },
    "🫁 Paru-paru": {
        "deskripsi": "Paru-paru adalah organ pernapasan yang memfasilitasi pertukaran gas antara udara dan darah.",
        "unsur": [
            {"simbol": "O",  "persen": 65.0, "fungsi": "Gas oksigen diserap dari udara melalui alveolus masuk ke kapiler darah."},
            {"simbol": "C",  "persen": 18.0, "fungsi": "Menyusun surfaktan paru (fosfolipid) yang melapisi alveolus."},
            {"simbol": "H",  "persen": 10.0, "fungsi": "Komponen air dalam lapisan cairan tipis alveolus."},
            {"simbol": "N",  "persen": 3.0,  "fungsi": "Menyusun protein elastin dan kolagen pada jaringan paru."},
            {"simbol": "Ca", "persen": 0.1,  "fungsi": "Berperan dalam regulasi tonus otot polos bronkus."},
        ]
    },
    "🫀 Jantung": {
        "deskripsi": "Jantung adalah organ otot berongga yang memompa darah ke seluruh tubuh secara terus-menerus.",
        "unsur": [
            {"simbol": "O",  "persen": 65.0,  "fungsi": "Jantung membutuhkan pasokan oksigen konstan melalui arteri koroner."},
            {"simbol": "C",  "persen": 18.0,  "fungsi": "Menyusun protein kontraktil (aktin, miosin) kardiomiosit."},
            {"simbol": "H",  "persen": 10.0,  "fungsi": "Komponen air intraseluler kardiomiosit."},
            {"simbol": "N",  "persen": 3.0,   "fungsi": "Menyusun protein struktural termasuk troponin."},
            {"simbol": "K",  "persen": 0.35,  "fungsi": "Mengatur ritme jantung — ketidakseimbangan kalium dapat menyebabkan aritmia."},
            {"simbol": "Ca", "persen": 0.1,   "fungsi": "Ion kalsium memicu setiap kontraksi jantung."},
            {"simbol": "Fe", "persen": 0.004, "fungsi": "Komponen mioglobin otot jantung yang menyimpan oksigen lokal."},
        ]
    },
    "🦷 Kulit": {
        "deskripsi": "Kulit adalah organ terbesar tubuh manusia yang berfungsi sebagai pelindung fisik, termoregulasi, dan sensoris.",
        "unsur": [
            {"simbol": "O",  "persen": 65.0,  "fungsi": "Terdapat dalam semua biomolekul kulit termasuk kolagen dan elastin."},
            {"simbol": "C",  "persen": 18.0,  "fungsi": "Menyusun keratin, kolagen, dan elastin dalam kulit."},
            {"simbol": "H",  "persen": 10.0,  "fungsi": "Komponen air yang menjaga kelembapan dan turgor kulit."},
            {"simbol": "N",  "persen": 3.0,   "fungsi": "Menyusun asam amino dalam keratin, kolagen, dan elastin."},
            {"simbol": "S",  "persen": 0.3,   "fungsi": "Membentuk ikatan disulfida yang mengunci struktur keratin."},
            {"simbol": "Zn", "persen": 0.002, "fungsi": "Kofaktor enzim yang melindungi kulit dan mendukung penyembuhan luka."},
        ]
    },
}

BENDA_SEHARI = {
    "💧 Air (H₂O)": {
        "rumus": "H₂O",
        "deskripsi": "Air adalah senyawa paling melimpah di bumi dan pelarut universal yang menopang seluruh kehidupan.",
        "unsur": [{"simbol": "H", "jumlah": 2}, {"simbol": "O", "jumlah": 1}],
        "fakta": "Air memiliki tegangan permukaan tinggi akibat ikatan hidrogen antar molekulnya.",
    },
    "🧂 Garam Dapur (NaCl)": {
        "rumus": "NaCl",
        "deskripsi": "Natrium klorida adalah senyawa ionik yang digunakan sebagai bumbu dan pengawet makanan sejak ribuan tahun lalu.",
        "unsur": [{"simbol": "Na", "jumlah": 1}, {"simbol": "Cl", "jumlah": 1}],
        "fakta": "Garam laut mengandung lebih dari 80 jenis mineral selain NaCl murni.",
    },
    "🪟 Kaca (SiO₂)": {
        "rumus": "SiO₂",
        "deskripsi": "Silikon dioksida adalah bahan utama pembuatan kaca yang terbentuk dari SiO₂ yang dicairkan pada suhu ~1700°C.",
        "unsur": [{"simbol": "Si", "jumlah": 1}, {"simbol": "O", "jumlah": 2}],
        "fakta": "Pasir pantai sebagian besar adalah SiO₂. Kaca bersifat amorf sehingga dianggap cairan super-dingin.",
    },
    "🔩 Baja (Fe + C)": {
        "rumus": "Fe-C",
        "deskripsi": "Baja adalah paduan logam antara besi dan karbon dengan tambahan Cr dan Ni untuk ketahanan korosi.",
        "unsur": [
            {"simbol": "Fe", "jumlah": 1},
            {"simbol": "C",  "jumlah": None},
            {"simbol": "Cr", "jumlah": None},
            {"simbol": "Ni", "jumlah": None},
        ],
        "fakta": "Baja nirkarat mengandung minimal 10,5% kromium yang membentuk lapisan oksida pelindung.",
    },
    "🥄 Aluminium Foil (Al)": {
        "rumus": "Al",
        "deskripsi": "Aluminium adalah logam ringan yang secara alami terlindungi lapisan oksida tipis (Al₂O₃).",
        "unsur": [{"simbol": "Al", "jumlah": 1}],
        "fakta": "Daur ulang aluminium hanya membutuhkan 5% energi dibanding produksi dari bijih bauksit.",
    },
    "🪥 Pasta Gigi (NaF / CaF₂)": {
        "rumus": "NaF / CaF₂",
        "deskripsi": "Pasta gigi mengandung fluorida yang memperkuat enamel gigi dengan membentuk fluorapatit yang tahan asam.",
        "unsur": [
            {"simbol": "Ca", "jumlah": 1},
            {"simbol": "F",  "jumlah": 2},
            {"simbol": "Na", "jumlah": 1},
        ],
        "fakta": "Fluorapatit 10 kali lebih tahan terhadap asam dibanding enamel gigi biasa.",
    },
    "🧪 Baking Soda (NaHCO₃)": {
        "rumus": "NaHCO₃",
        "deskripsi": "Natrium bikarbonat digunakan sebagai pengembang kue, penghilang bau, dan antasida.",
        "unsur": [
            {"simbol": "Na", "jumlah": 1},
            {"simbol": "H",  "jumlah": 1},
            {"simbol": "C",  "jumlah": 1},
            {"simbol": "O",  "jumlah": 3},
        ],
        "fakta": "Reaksi NaHCO₃ + asam asetat menghasilkan CO₂ — efek yang dipakai dalam percobaan gunung berapi mainan.",
    },
    "🥫 Kaleng Minuman (Al + Sn)": {
        "rumus": "Al / Sn",
        "deskripsi": "Kaleng minuman modern terbuat dari aluminium. Kaleng makanan tradisional menggunakan baja berlapis timah.",
        "unsur": [
            {"simbol": "Al", "jumlah": 1},
            {"simbol": "Sn", "jumlah": None},
            {"simbol": "Fe", "jumlah": None},
        ],
        "fakta": "Lapisan timah pada kaleng makanan hanya setebal 0,0003 mm namun cukup mencegah korosi bertahun-tahun.",
    },
}



  const info=CAT_INFO[e.cat];
  const badge=document.getElementById('p-badge');
  badge.style.background=info.bg;badge.style.borderColor=info.border;
  document.getElementById('p-sym').textContent=e.sym;
  document.getElementById('p-sym').style.color=info.color;
  document.getElementById('p-num').textContent=e.n;
  document.getElementById('p-num').style.color=info.color;
  document.getElementById('p-name').textContent=e.name;
  document.getElementById('p-cat').textContent=info.label+' · Fase: '+e.phase;
  document.getElementById('p-stats').innerHTML=`
    <div class="sbox"><div class="slabel">⚖️ Massa Atom</div><div class="sval">${{e.mass}} u</div></div>
    <div class="sbox"><div class="slabel">⚡ Elektronegativitas</div><div class="sval">${{e.en}}</div></div>
    <div class="sbox"><div class="slabel">🔴 Jari-jari Atom</div><div class="sval">${{e.radius}} pm</div></div>
    <div class="sbox"><div class="slabel">🔥 Titik Lebur</div><div class="sval">${{e.mp}}</div></div>
    <div class="sbox"><div class="slabel">💧 Titik Didih</div><div class="sval">${{e.bp}}</div></div>
    <div class="sbox"><div class="slabel">📌 Periode / Golongan</div><div class="sval">${{e.period}} / ${{e.group}}</div></div>`;
  document.getElementById('p-config').innerHTML='🧬 Konfigurasi Elektron: <code>'+e.config+'</code>';
  const panel=document.getElementById('panel');
  panel.classList.add('visible');
  panel.scrollIntoView({{behavior:'smooth',block:'nearest'}});
}}
function closePanel(){{
  document.getElementById('panel').classList.remove('visible');
  document.querySelectorAll('.el.active').forEach(d=>d.classList.remove('active'));
}}
window.addEventListener('message',function(event){{
  if(event.data&&event.data.type==='selectEl')selectEl(event.data.sym);
}});
</script></body></html>"""


def kartu_unsur_html(simbol, fungsi="", persen=None):
    if simbol not in ELEMENT_INFO:
        return ""
    el = ELEMENT_INFO[simbol]
    nama   = el["nama"]
    nomor  = el["nomor"]
    massa  = el["massa"]
    gol    = el["golongan"]
    warna  = WARNA_GOLONGAN.get(gol, "#EEEEEE")

    if persen is not None:
        if persen < 0.001:
            p_fmt = f"{persen:.5f}%"
        elif persen < 0.1:
            p_fmt = f"{persen:.3f}%"
        else:
            p_fmt = f"{persen:.1f}%"
        persen_badge = (
            f'<span style="font-size:11px;color:#555;margin-left:4px;">{p_fmt}</span>'
        )
    else:
        persen_badge = ""

    fungsi_div = (
        f'<div style="font-size:12px;color:#333;margin-top:5px;line-height:1.5;">{fungsi}</div>'
        if fungsi else ""
    )

    return (
        f'<div style="background:{warna}33;border:1.5px solid {warna};border-radius:10px;'
        f'padding:10px 14px;margin-bottom:8px;">'
        f'<div style="display:flex;align-items:center;justify-content:space-between;">'
        f'<div style="display:flex;align-items:center;gap:8px;">'
        f'<span style="font-size:20px;font-weight:700;">{simbol}</span>'
        f'<span style="font-size:13px;color:#444;">{nama}</span>'
        f'{persen_badge}'
        f'</div>'
        f'<span style="font-size:11px;background:{warna};padding:2px 8px;border-radius:10px;color:#333;">{gol}</span>'
        f'</div>'
        f'<div style="font-size:11px;color:#666;margin-top:4px;">No. Atom: <b>{nomor}</b> &nbsp;|&nbsp; Massa: <b>{massa} u</b></div>'
        f'{fungsi_div}'
        f'</div>'
    )


def hitung_bobot_molekul(unsur_list):
    total = 0.0
    rincian = []
    for item in unsur_list:
        s = item["simbol"]
        n = item.get("jumlah")
        if n is None or s not in ELEMENT_INFO:
            continue
        massa = ELEMENT_INFO[s]["massa"]
        kontribusi = massa * n
        total += kontribusi
        rincian.append((s, ELEMENT_INFO[s]["nama"], massa, n, round(kontribusi, 4)))
    return total, rincian


# ══════════════════════════════════════════════════════════════════
# HALAMAN: TABEL PERIODIK
# ══════════════════════════════════════════════════════════════════
def page_tabel_periodik():
    # ── Sidebar: hanya navigasi + search ──
    with st.sidebar:
        st.markdown("## ⚛️ Tabel Periodik")
        st.markdown("---")
        query = st.text_input("🔍 Cari Elemen", placeholder="Contoh: Emas / Au", key="search_el")
        st.markdown("---")

    # ── Main area: tabel periodik ──
    st.title("⚛️ Tabel Periodik Kimia")
    st.caption("Klik elemen di tabel untuk melihat informasi lengkapnya.")

    # Render tombol hasil search di sidebar SETELAH definisi area utama
    candidates = sorted(ELEMENTS, key=lambda x: x["n"])
    if query:
        candidates = [e for e in candidates
                      if query.lower() in e["name"].lower() or query.lower() in e["sym"].lower()]

    with st.sidebar:
        st.markdown(f"**{len(candidates)} elemen**")
        buttons_html = ""
        for e in candidates:
            info = CAT_INFO[e["cat"]]
            buttons_html += (
                f'<div class="sb-el" '
                f'style="background:{info["bg"]};border:1px solid {info["border"]};color:{info["color"]};" '
                f'onclick="triggerEl(\'{e["sym"]}\')">'
                f'<b>{e["sym"]}</b> — {e["name"]}'
                f'</div>'
            )

        sidebar_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{font-family:system-ui,sans-serif;background:transparent;}}
.sb-el{{border-radius:6px;padding:6px 10px;margin-bottom:5px;font-size:13px;cursor:pointer;transition:opacity .15s,transform .1s;user-select:none;}}
.sb-el:hover{{opacity:.8;transform:translateX(2px);}}
</style></head><body>
{buttons_html}
<script>
function triggerEl(sym){{
  const iframes=window.parent.document.querySelectorAll('iframe');
  iframes.forEach(function(iframe){{
    try{{iframe.contentWindow.postMessage({{type:'selectEl',sym:sym}},'*');}}catch(e){{}}
  }});
}}
</script></body></html>"""

        sidebar_height = max(50, len(candidates) * 37)
        components.html(sidebar_html, height=min(sidebar_height, 500), scrolling=True)

    # Render tabel periodik di area UTAMA
    html_content = build_full_html(ELEMENTS, CAT_INFO)
    components.html(html_content, height=900, scrolling=True)


# ══════════════════════════════════════════════════════════════════
# HALAMAN: UNSUR KEHIDUPAN
# ══════════════════════════════════════════════════════════════════
def page_unsur_kehidupan():
    st.title("🌍 Unsur di Sekitar & Dalam Dirimu")
    st.markdown("Jelajahi unsur-unsur kimia yang menyusun **tubuh manusia** dan **benda-benda sehari-hari** di sekitarmu.")

    tab1, tab2 = st.tabs(["🫀 Tubuh Manusia", "🏠 Benda Sehari-hari"])

    with tab1:
        st.subheader("Unsur Penyusun Tubuh Manusia")
        st.markdown("Pilih bagian tubuh untuk melihat unsur-unsur kimia penyusunnya beserta fungsi biologisnya.")

        pilihan_bagian = st.selectbox("Pilih bagian tubuh:", list(BAGIAN_TUBUH.keys()), key="bagian_tubuh")
        data = BAGIAN_TUBUH[pilihan_bagian]

        st.info(data["deskripsi"])
        st.markdown("#### 🔬 Unsur Penyusun")

        html_cards = "".join(
            kartu_unsur_html(item["simbol"], fungsi=item["fungsi"], persen=item["persen"])
            for item in data["unsur"]
        )
        card_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui,sans-serif;}}</style>
</head><body style="background:transparent;padding:4px 0;">{html_cards}</body></html>"""
        components.html(card_html, height=len(data["unsur"]) * 115, scrolling=False)

        st.markdown("#### 📊 Komposisi Persentase")
        df_chart = pd.DataFrame([
            {
                "Unsur": f"{ELEMENT_INFO[i['simbol']]['nama']} ({i['simbol']})",
                "Persentase (%)": i["persen"]
            }
            for i in data["unsur"] if i["simbol"] in ELEMENT_INFO
        ]).sort_values("Persentase (%)", ascending=False)
        st.bar_chart(df_chart.set_index("Unsur"), use_container_width=True)

    with tab2:
        st.subheader("Unsur dalam Benda Sehari-hari")
        st.markdown("Pilih benda untuk melihat unsur-unsur penyusunnya dan menghitung bobot molekulnya.")

        pilihan_benda = st.selectbox("Pilih benda:", list(BENDA_SEHARI.keys()), key="benda_sehari")
        benda = BENDA_SEHARI[pilihan_benda]

        col_info, col_rumus = st.columns([3, 1])
        with col_info:
            st.info(benda["deskripsi"])
        with col_rumus:
            st.markdown(f"""
            <div style="text-align:center;background:#f0f4ff;border:2px solid #4A90D9;
                        border-radius:12px;padding:18px 10px;margin-top:4px;">
                <div style="font-size:12px;color:#555;">Rumus Kimia</div>
                <div style="font-size:26px;font-weight:700;color:#1a1a2e;">{benda['rumus']}</div>
            </div>""", unsafe_allow_html=True)

        bm, rincian = hitung_bobot_molekul(benda["unsur"])
        if bm > 0:
            st.markdown("#### ⚖️ Perhitungan Bobot Molekul")
            df_bm = pd.DataFrame([
                {"Simbol": r[0], "Nama Unsur": r[1], "Massa Atom (u)": r[2],
                 "Jumlah Atom": int(r[3]), "Kontribusi (u)": r[4]}
                for r in rincian
            ])
            st.dataframe(df_bm, use_container_width=True, hide_index=True)
            st.markdown(f"""
            <div style="background:#e8f5e9;border:2px solid #43A047;border-radius:10px;
                        padding:14px 20px;font-size:16px;font-weight:700;color:#1B5E20;margin-top:8px;">
                ⚖️ Bobot Molekul {benda['rumus']} = <span style="font-size:22px;">{bm:.4f} g/mol</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("#### 🔬 Detail Unsur Penyusun")
        html_detail = "".join(kartu_unsur_html(item["simbol"]) for item in benda["unsur"])
        detail_html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>*{{box-sizing:border-box;margin:0;padding:0;font-family:system-ui,sans-serif;}}</style>
</head><body style="background:transparent;padding:4px 0;">{html_detail}</body></html>"""
        components.html(detail_html, height=len(benda["unsur"]) * 80, scrolling=False)

        st.markdown("#### 💡 Fakta Menarik")
        st.success(f"**{pilihan_benda}** — {benda['fakta']}")


# ══════════════════════════════════════════════════════════════════
# HALAMAN: BERANDA
# ══════════════════════════════════════════════════════════════════
def page_beranda():
    st.markdown("""
    <style>
    .beranda-wrap {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 40px 20px 20px;
        text-align: center;
    }
    .beranda-label {
        font-size: 12px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #888;
        margin-bottom: 6px;
    }
    .beranda-title {
        font-size: 36px;
        font-weight: 700;
        color: #1a1a2e;
        margin: 0 0 4px;
    }
    .beranda-underline {
        width: 48px;
        height: 4px;
        background: #185FA5;
        border-radius: 2px;
        margin: 0 auto 28px;
    }
    .beranda-logo-circle {
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: #E6F1FB;
        border: 3px solid #B5D4F4;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 10px;
        font-size: 60px;
    }
    .beranda-logo-label {
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #185FA5;
        margin-bottom: 24px;
    }
    .beranda-desc {
        font-size: 14px;
        color: #555;
        max-width: 480px;
        line-height: 1.8;
        margin: 0 auto 36px;
    }
    </style>
    <div class="beranda-wrap">
        <div class="beranda-label">Aplikasi Kimia Interaktif</div>
        <div class="beranda-title">Selamat Datang!</div>
        <div class="beranda-underline"></div>
        <div class="beranda-logo-circle">⚛️</div>
        <div class="beranda-logo-label">Tabel Periodik Kimia</div>
        <div class="beranda-desc">
            Tabel Periodik Kimia Interatif  dirancang untuk memudahkan pengguna dalam mengeksplorasi 118 unsur kimia, komposisi unsur dalam tubuh manusia,
            dan benda-benda sehari-hari. Silakan pilih menu di sebelah kiri untuk mulai menjelajah.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#E6F1FB;border:1px solid #B5D4F4;border-radius:12px;padding:20px;text-align:center;">
            <div style="font-size:32px;margin-bottom:8px;">🔬</div>
            <div style="font-size:14px;font-weight:600;color:#0C447C;">Tabel Periodik</div>
            <div style="font-size:12px;color:#555;margin-top:4px;">118 elemen interaktif</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#E1F5EE;border:1px solid #9FE1CB;border-radius:12px;padding:20px;text-align:center;">
            <div style="font-size:32px;margin-bottom:8px;">🌍</div>
            <div style="font-size:14px;font-weight:600;color:#085041;">Unsur Kehidupan</div>
            <div style="font-size:12px;color:#555;margin-top:4px;">Tubuh & benda sehari-hari</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#FAEEDA;border:1px solid #FAC775;border-radius:12px;padding:20px;text-align:center;">
            <div style="font-size:32px;margin-bottom:8px;">ℹ️</div>
            <div style="font-size:14px;font-weight:600;color:#633806;">Tentang Aplikasi</div>
            <div style="font-size:12px;color:#555;margin-top:4px;">Info & cara penggunaan</div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
# HALAMAN: TENTANG
# ══════════════════════════════════════════════════════════════════
def page_tentang():
    st.title("ℹ️ Tentang Aplikasi")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        ### 📌 Deskripsi
        **Tabel Periodik Kimia Interaktif** adalah aplikasi edukasi berbasis web yang dirancang
        untuk memudahkan eksplorasi unsur-unsur kimia secara interaktif.

        Aplikasi ini cocok digunakan oleh:
        - Pelajar SMA/sederajat yang sedang mempelajari kimia dasar
        - Mahasiswa yang membutuhkan referensi unsur cepat
        - Siapapun yang penasaran dengan dunia kimia
        """)
    with col2:
        st.markdown("""
        <div style="background:#f0f4ff;border:2px solid #4A90D9;border-radius:14px;padding:20px;text-align:center;">
            <div style="font-size:48px;margin-bottom:8px;">⚛️</div>
            <div style="font-size:15px;font-weight:700;color:#1a1a2e;">Tabel Periodik</div>
            <div style="font-size:12px;color:#555;margin-top:4px;">Kimia Interaktif</div>
            <hr style="margin:12px 0;border-color:#cce;">
            <div style="font-size:12px;color:#666;">118 Elemen · 10 Kategori</div>
            <div style="font-size:12px;color:#666;">7 Periode · 18 Golongan</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    col_a, col_b, col_c, col_d = st.columns(4)
    with col_a:
        st.metric("Total Elemen", "118")
    with col_b:
        st.metric("Kategori", "10")
    with col_c:
        st.metric("Periode", "7")
    with col_d:
        st.metric("Golongan", "18")


# ══════════════════════════════════════════════════════════════════
# NAVIGASI UTAMA
# ══════════════════════════════════════════════════════════════════
def main():
    with st.sidebar:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:8px;padding:4px 0 8px;">
            <span style="font-size:22px;">⚛️</span>
            <span style="font-size:16px;font-weight:700;color:#1a1a2e;">Tabel Periodik</span>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("**Menu**")
        halaman = st.radio(
            "Navigasi",
            ["🏠 Beranda", "🔬 Tabel Periodik", "🌍 Unsur Kehidupan", "ℹ️ Tentang Aplikasi"],
            label_visibility="collapsed"
        )
        st.markdown("---")

    if halaman == "🏠 Beranda":
        page_beranda()
    elif halaman == "🔬 Tabel Periodik":
        page_tabel_periodik()
    elif halaman == "🌍 Unsur Kehidupan":
        page_unsur_kehidupan()
    else:
        page_tentang()

if __name__ == "__main__":
    main()
