import streamlit as st
import streamlit.components.v1 as components
import struct
import ctypes
import os
import re
import subprocess

# Настройка страницы
st.set_page_config(
    page_title="S.T.A.L.K.E.R. 2 — Чекер Артефактов",
    page_icon="☢️",
    layout="wide"
)

# Инициализация состояния фильтрации
if "art_filter" not in st.session_state:
    st.session_state.art_filter = "all"  # "all", "missing", "found"

# =========================================================================
# CUSTOM CSS / GAME INVENTORY GRID STYLES + HOVER TOOLTIP
# =========================================================================
st.markdown("""
<style>
    /* Глубокий тёмный фон */
    .stApp {
        background-color: #080A0F;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Ширина контейнера */
    .main .block-container {
        max-width: 1100px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Зона загрузки файлов - РАСТЯНУТА И ОТЦЕНТРИРОВАНА */
    [data-testid="stFileUploader"] {
        background-color: #111520 !important;
        border: 2px dashed #FFB000 !important;
        border-radius: 14px !important;
        padding: 16px !important;
        transition: all 0.3s ease;
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 auto !important;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #FFC107 !important;
        box-shadow: 0 0 20px rgba(255, 176, 0, 0.2);
    }

    [data-testid="stFileUploader"] section {
        padding: 15px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
    }

    [data-testid="stFileUploaderDropzoneInstructions"] {
        text-align: center !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* Замена текста размера файла */
    [data-testid="stFileUploaderDropzoneInstructions"] small {
        font-size: 0 !important;
    }
    [data-testid="stFileUploaderDropzoneInstructions"] small::after {
        content: "Загрузить до 200MB" !important;
        font-size: 0.85rem !important;
        color: #94A3B8 !important;
        display: block !important;
        margin-top: 4px;
    }

    /* СТИЛИ КНОПОК ФИЛЬТРАЦИИ С МЯГКОЙ ОБВОДКОЙ */
    .stButton > button {
        width: 100% !important;
        border-radius: 10px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    /* Активная кнопка (Primary) - Мягкое золотое свечение */
    .stButton > button[kind="primary"] {
        background: linear-gradient(180deg, #1A2234 0%, #111520 100%) !important;
        border: 1px solid #FFB000 !important;
        color: #FFB000 !important;
        box-shadow: 0 0 16px rgba(255, 176, 0, 0.35), inset 0 0 10px rgba(255, 176, 0, 0.1) !important;
    }
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 0 22px rgba(255, 176, 0, 0.5) !important;
        transform: translateY(-1px);
    }

    /* Неактивная кнопка (Secondary) */
    .stButton > button[kind="secondary"] {
        background: #111520 !important;
        border: 1px solid #1E2638 !important;
        color: #94A3B8 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        border-color: #3A4256 !important;
        color: #F8FAFC !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4) !important;
        transform: translateY(-1px);
    }

    /* Иконка кнопки скопировать путь */
    .copy-btn-icon {
        background: #111520;
        border: 1px solid #1E2638;
        border-radius: 6px;
        padding: 5px 8px;
        cursor: pointer;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s ease;
    }
    .copy-btn-icon:hover {
        border-color: #00E676;
        background: rgba(0, 230, 118, 0.12);
        transform: scale(1.05);
    }

    /* СЕТКА ГАЛЕРЕИ (GRID) */
    .art-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 12px;
        padding: 10px 0;
    }

    /* Карточка-плитка артефакта */
    .art-tile {
        position: relative;
        background: #111520;
        border-radius: 12px;
        border: 1px solid #1E2638;
        padding: 10px 6px 8px 6px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        height: 165px;
        cursor: pointer;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        user-select: none;
    }
    .art-tile:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
        border-color: #334155;
        z-index: 100 !important;
    }

    /* ВСПЛЫВАЮЩАЯ ПОДСКАЗКА СТРОГО ПРИ НАВЕДЕНИИ (HOVER TOOLTIP) */
    .art-tile .tooltip-box {
        visibility: hidden;
        opacity: 0;
        width: 220px;
        background-color: #141A26;
        color: #F8FAFC;
        text-align: left;
        border-radius: 8px;
        padding: 10px 12px;
        border: 1px solid #FFB000;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.85);
        position: absolute;
        z-index: 999 !important;
        bottom: 108%;
        left: 50%;
        transform: translateX(-50%) translateY(5px);
        transition: opacity 0.2s ease, visibility 0.2s ease, transform 0.2s ease;
        pointer-events: none;
        font-size: 0.78rem;
        line-height: 1.35;
    }

    .art-tile:hover .tooltip-box {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }

    /* Свечение для НАЙДЕННЫХ артефактов */
    .tile-found {
        border-color: #00E676 !important;
        box-shadow: 0 0 12px rgba(0, 230, 118, 0.3) !important;
        background: radial-gradient(circle at center, rgba(0, 230, 118, 0.08) 0%, #111520 80%);
    }
    .tile-found:hover {
        box-shadow: 0 0 20px rgba(0, 230, 118, 0.5) !important;
    }

    .tile-missing {
        opacity: 0.65;
    }
    .tile-missing:hover {
        opacity: 1;
    }

    .tile-badge {
        position: absolute;
        top: 6px;
        right: 6px;
        z-index: 2;
    }

    .tile-img-container {
        width: 100%;
        height: 95px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 2px;
    }
    .tile-img {
        width: 84px;
        height: 84px;
        background-size: contain;
        background-position: center;
        background-repeat: no-repeat;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.6));
    }

    .tile-label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #F1F5F9;
        text-align: center;
        line-height: 1.15;
        width: 100%;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        padding: 0 4px;
    }

    [data-testid="stMetric"] {
        background-color: #111520;
        border: 1px solid #1E2638;
        border-radius: 12px;
        padding: 16px;
    }

    .stDownloadButton > button {
        background: linear-gradient(135deg, #FFB000 0%, #E69500 100%) !important;
        color: #0A0D14 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 176, 0, 0.25) !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #FFC107 0%, #FFB000 100%) !important;
        box-shadow: 0 0 25px rgba(255, 176, 0, 0.5) !important;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# =========================================================================
# АВТО-КОМПИЛЯЦИЯ КРАКЕН-ДЕКОДЕРА ДЛЯ LINUX (STREAMLIT CLOUD)
# =========================================================================
@st.cache_resource
def get_linux_decompressor():
    so_path = os.path.abspath("libooz.so")
    if os.path.exists(so_path):
        return so_path

    try:
        if os.path.exists("ooz_src") and not os.path.exists(so_path):
            import shutil
            shutil.rmtree("ooz_src", ignore_errors=True)

        if not os.path.exists("ooz_src"):
            res = subprocess.run("git clone https://github.com/powzix/ooz.git ooz_src", shell=True, capture_output=True, text=True)
            if res.returncode != 0:
                st.error(f"Ошибка клонирования репозитория: {res.stderr}")
                return None

        clean_stdafx = """#pragma once
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
#include <sys/stat.h>
#include <immintrin.h>

typedef uint8_t uint8;
typedef uint16_t uint16;
typedef uint32_t uint32;
typedef uint64_t uint64;
typedef int8_t int8;
typedef int16_t int16;
typedef int32_t int32;
typedef int64_t int64;
typedef uint8_t byte;

#define WINAPI
#define HINSTANCE void*
#define HMODULE void*
#define __forceinline inline __attribute__((always_inline))

#undef _rotl
#define _rotl(x, r) (((uint32_t)(x) << (r)) | ((uint32_t)(x) >> (32 - (r))))

#undef _byteswap_ulong
#define _byteswap_ulong __builtin_bswap32

#undef _byteswap_ushort
#define _byteswap_ushort __builtin_bswap16

#undef _byteswap_uint64
#define _byteswap_uint64 __builtin_bswap64

static inline unsigned char _BitScanReverse(unsigned long *Index, uint32_t Mask) {
    if (Mask == 0) return 0;
    *Index = 31 - __builtin_clz(Mask);
    return 1;
}

static inline unsigned char _BitScanForward(unsigned long *Index, uint32_t Mask) {
    if (Mask == 0) return 0;
    *Index = __builtin_ctz(Mask);
    return 1;
}
"""
        with open("ooz_src/stdafx.h", "w") as f:
            f.write(clean_stdafx)

        kraken_cpp = "ooz_src/kraken.cpp"
        with open(kraken_cpp, "r") as f:
            code = f.read()

        if "void LoadLib()" in code:
            code = code.split("void LoadLib()")[0]
        elif "int main(" in code:
            code = code.split("int main(")[0]

        relaxed_fn = """
        #include <stdint.h>
        extern "C" int64_t OozKraken_Decompress(const unsigned char *src, int64_t src_len, unsigned char *dst, int64_t dst_len) {
            KrakenDecoder *dec = Kraken_Create();
            int offset = 0;
            size_t remaining_dst = (size_t)dst_len;
            size_t remaining_src = (size_t)src_len;
            const unsigned char *p = src;
            while (remaining_dst != 0) {
                if (!Kraken_DecodeStep(dec, dst, offset, remaining_dst, p, remaining_src)) { Kraken_Destroy(dec); return offset > 0 ? offset : -1; }
                if (dec->src_used == 0) { Kraken_Destroy(dec); return offset > 0 ? offset : -1; }
                p += dec->src_used;
                remaining_src -= dec->src_used;
                remaining_dst -= dec->dst_used;
                offset += dec->dst_used;
            }
            Kraken_Destroy(dec);
            return offset;
        }
        """
        with open(kraken_cpp, "w") as f:
            f.write(code + "\n" + relaxed_fn)

        compile_cmd = "cd ooz_src && g++ -O3 -shared -fPIC -msse4.1 -w -o ../libooz.so kraken.cpp bitknit.cpp lzna.cpp"
        res = subprocess.run(compile_cmd, shell=True, capture_output=True, text=True)

        if res.returncode != 0:
            st.error(f"Ошибка компиляции декомпрессора:\n{res.stderr}")
            return None

        if os.path.exists(so_path):
            return so_path
    except Exception as e:
        st.error(f"Исключение при сборке: {e}")
    return None

# =========================================================================
# БАЗА ДАННЫХ АРТЕФАКТОВ (SID, Название, Вес, Эффекты)
# =========================================================================
CATEGORIES = [
    {
        "name": "1. 🌌 ГРАВИТАЦИОННЫЕ АРТЕФАКТЫ",
        "items": [
            ("GArtifactGoldFish", "🔘 Золотая рыбка", "0.35 кг", "+10% Радиация, +3 кг Вес"),
            ("GArtifactStoneDrop", "🔘 Каменное сердце", "0.65 кг", "+10% Радиация, +3 кг Вес"),
            ("GArtifactGravy", "🔘 Грави", "0.65 кг", "-10% Радиация, +3 кг Вес"),
            ("GArtifactWrenched", "🔘 Выверт", "0.40 кг", "+10% Физическая защита"),
            ("GArtifactBloodStone", "🔘 Кровь камня", "0.55 кг", "+10% Радиация, +3 кг Вес"),
            ("GArtifactTrunk", "🔘 Канифоль", "0.40 кг", "+1.5 /с Выносливость, +2 кг Вес"),
            ("GArtifactSponge", "🔘 Вихрь", "0.30 кг", "+7% Физическая защита, +1.5 /с Выносливость, -10% Радиация"),
            ("GArtifactPlane", "🔘 Галька", "0.30 кг", "+7% Физическая защита, +1.5 /с Выносливость, +10% Радиация"),
            ("GArtifactLandSlug", "🔘 Медуза", "0.40 кг", "+10% Физическая защита, +10% Радиация"),
            ("GArtifactSpring", "🔵 Пружина", "0.45 кг", "+15% Радиация, +6 кг Вес"),
            ("GArtifactGraphiteBlock", "🔵 Корона", "0.60 кг", "+10% Физическая защита, +2.5 /с Выносливость, +15% Радиация"),
            ("GArtifactHedgehog", "🔵 Мухоловка", "0.35 кг", "-15% Радиация, +6 кг Вес"),
            ("GArtifactNightStar", "🟣 Ночная звезда", "0.60 кг", "+25% Радиация, +9 кг Вес"),
            ("GArtifactSplitStone", "🟣 Битый камень", "0.60 кг", "+25% Физическая защита, +25% Радиация"),
            ("GArtifactBud", "🟣 Бутон", "0.40 кг", "+25% Физическая защита, +5.0 /с Выносливость, +25% Радиация"),
            ("GArtifactCompass", "🟡 Компас", "0.50 кг", "+90% Физическая защита, +50% Радиация"),
            ("GArtifactRubiksCube", "🟡 Кубик-Рубик", "0.40 кг", "+50% Физическая защита, +50% Радиация")
        ]
    },
    {
        "name": "2. 🔥 ТЕРМИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("FArtifactFireBall", "🔘 Огненный шар", "0.50 кг", "+10% Термозащита, -10% Радиация"),
            ("FArtifactSteak", "🔘 Бифштекс", "0.55 кг", "+5% Сопротивление кровотечению, +10% Радиация"),
            ("FArtifactGlass", "🔘 Полость", "0.40 кг", "+3% Сопротивление кровотечению, +2 кг Вес, +10% Радиация"),
            ("FArtifactBurntHunk", "🔘 Вертушка", "0.35 кг", "+5% Сопротивление кровотечению, -10% Радиация"),
            ("FArtifactResin", "🔘 Лира", "0.50 кг", "+3% Сопротивление кровотечению, +2 кг Вес"),
            ("FArtifactDrops", "🔘 Капля", "0.45 кг", "+10% Термозащита, +10% Радиация"),
            ("FArtifactEye", "🔘 Глаз", "0.40 кг", "+10% Термозащита"),
            ("FArtifactCrystal", "🔘 Кристалл", "0.65 кг", "+10% Термозащита, +10% Радиация"),
            ("FArtifactMomsBeads", "🟣 Мамины Бусы", "0.40 кг", "+10% Сопротивление кровотечению, +15% Радиация"),
            ("FArtifactBakedBolts", "🔵 Брак", "0.55 кг", "+5% Сопротивление кровотечению, +3 кг Вес, +15% Радиация"),
            ("FArtifactDeadSponge", "🔵 Мёртвая губка", "0.30 кг", "+10% Сопротивление кровотечению, +15% Радиация"),
            ("FArtifactHellishHedgehog", "🔵 Магма", "0.55 кг", "+10% Термозащита, +3 кг Вес, +15% Радиация"),
            ("FArtifactPlasma", "🔵 Плазма", "0.50 кг", "+15% Термозащита, -15% Радиация"),
            ("FArtifactCandle", "🟣 Лепесток", "0.30 кг", "+20% Сопротивление кровотечению, +25% Радиация"),
            ("FArtifactFireworks", "🟣 Мясная зажигалка", "0.40 кг", "+20% Термозащита, +25% Радиация"),
            ("FArtifactCore", "🟣 Факел", "0.55 кг", "+15% Термозащита, +6 кг Вес, +25% Радиация"),
            ("FArtifactRingOmnipotence", "🟡 Гиперкуб", "0.60 кг", "+35% Термозащита, +40% Кровотечение, +50% Радиация")
        ]
    },
    {
        "name": "3. ⚡ ЭЛЕКТРИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("EArtifactFlash", "🔘 Вспышка", "0.30 кг", "+10% Электрозащита, +10% Радиация"),
            ("EArtifactSnowflake", "🔘 Снежинка", "0.30 кг", "+2.5 /с Выносливость, +10% Радиация"),
            ("EArtifactDummy", "🔘 Пустышка", "0.45 кг", "+2.5 /с Выносливость"),
            ("EArtifactBattery", "🔘 Батарейка", "0.40 кг", "+2.5 /с Выносливость, +10% Радиация"),
            ("EArtifactJellyFish", "🔘 Сапфир", "0.65 кг", "+1.5 /с Выносливость, +3% Кровотечение"),
            ("EArtifactWorm", "🔘 Крысиный король", "0.35 кг", "+7% Электрозащита, +3% Кровотечение, -10% Радиация"),
            ("EArtifactSparkler", "🔘 Бенгальский огонь", "0.40 кг", "+10% Электрозащита, -10% Радиация"),
            ("EArtifactChocolate", "🔘 Шоколадка", "0.40 кг", "+10% Электрозащита, +10% Радиация"),
            ("EArtifactSoul", "🔵 Душа", "0.40 кг", "+5.0 /с Выносливость, +15% Радиация"),
            ("EArtifactMoonlight", "🔵 Лунный свет", "0.55 кг", "+15% Электрозащита, +15% Радиация"),
            ("EArtifactTow", "🔵 Урок труда", "0.40 кг", "+2.5 /с Выносливость, +5% Кровотечение, +15% Радиация"),
            ("EArtifactThunderHedgehog", "🔵 Фонарь", "0.55 кг", "+15% Электрозащита, -15% Радиация"),
            ("EArtifactCloud", "🔵 Арфа", "0.40 кг", "+10% Электрозащита, +5% Кровотечение, +15% Радиация"),
            ("EArtifactAtom", "🟣 Блик", "0.30 кг", "+20% Электрозащита, +25% Радиация"),
            ("EArtifactRazor", "🟣 Морская звезда", "0.55 кг", "+5.0 /с Выносливость, +10% Кровотечение, +25% Радиация"),
            ("EArtifactCrystalGlass", "🟣 Гребень", "0.45 кг", "+7.5 /с Выносливость, +25% Радиация"),
            ("EArtifactDope", "🟡 Грозовая ягода", "0.50 кг", "+12.5 /с Выносливость, +50% Радиация")
        ]
    },
    {
        "name": "4. 🧪 ХИМИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("CArtifactCrystalThorn", "🔘 Кристальная колючка", "0.50 кг", "-10% Радиация"),
            ("CArtifactThorn", "🔘 Колючка", "0.35 кг", "-10% Радиация"),
            ("CArtifactChunkMeat", "🔘 Ломоть мяса", "0.45 кг", "+10% Химзащита, +10% Радиация"),
            ("CArtifactBubble", "🔵 Пузырь", "0.40 кг", "-15% Радиация"),
            ("CArtifactSlug", "🔘 Слизняк", "0.60 кг", "-10% Радиация"),
            ("CArtifactSlime", "🔘 Слизь", "0.65 кг", "+10% Прочность экипировки, -10% Радиация"),
            ("CArtifactKryptonite", "🔘 Плесень", "0.55 кг", "+10% Химзащита, +10% Радиация"),
            ("CArtifactBung", "🔘 Рог", "0.30 кг", "+10% Прочность экипировки, +10% Химзащита, +10% Радиация"),
            ("CArtifactCottonWool", "🔘 Скорлупа", "0.30 кг", "+10% Химзащита, +10% Прочность экипировки, +10% Радиация"),
            ("CArtifactMica", "🔘 Слюда", "0.40 кг", "-10% Радиация"),
            ("CArtifactBun", "🔵 Колобок", "0.45 кг", "+15% Химзащита, +10% Прочность экипировки, +15% Радиация"),
            ("CArtifactEchinus", "🔵 Морской еж", "0.35 кг", "-15% Радиация"),
            ("CArtifactRosin", "🔵 Завтрак туриста", "0.35 кг", "+15% Химзащита, +20% Прочность экипировки, +15% Радиация"),
            ("CArtifactPlasticine", "🔵 Инфузория", "0.35 кг", "+15% Химзащита, +20% Прочность экипировки, +15% Радиация"),
            ("CArtifactPellicle", "🟣 Плёнка", "0.35 кг", "+20% Химзащита, -25% Радиация"),
            ("CArtifactBouncyBall", "🟣 Попрыгунчик", "0.40 кг", "-25% Радиация"),
            ("CArtifactDevilsMushroom", "🟣 Чёртов гриб", "0.45 кг", "+20% Химзащита, +30% Прочность экипировки, +25% Радиация"),
            ("CArtifactLiquidStone", "🟡 Жидкий камень", "0.60 кг", "+35% Химзащита, +40% Прочность экипировки, -50% Радиация")
        ]
    },
    {
        "name": "5. 🌀 СТРАННЫЕ АРТЕФАКТЫ (Ачивка «Все страньше и страньше»)",
        "items": [
            ("AArtifactWeirdWater", "🌀 Странная вода", "0.50 кг", "Аномальный квестовый артефакт"),
            ("AArtifactWeirdBall", "🌀 Странный мяч", "0.50 кг", "Аномальный квестовый артефакт"),
            ("AArtifactWeirdNut", "🌀 Странная гайка", "0.50 кг", "Аномальный квестовый артефакт"),
            ("AArtifactWeirdBolt", "🌀 Странный болт", "0.50 кг", "Аномальный квестовый артефакт"),
            ("AArtifactWeirdKettle", "🌀 Странный котелок", "0.50 кг", "Аномальный квестовый артефакт"),
            ("AArtifactWeirdFlower", "🌀 Странный цветок", "0.50 кг", "Аномальный квестовый артефакт")
        ]
    }
]

# SVG закодированы в Base64
SVG_CHECK_B64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0iIzAwRTY3NiIgZmlsbC1vcGFjaXR5PSIwLjIiIHN0cm9rZT0iIzAwRTY3NiIgc3Ryb2tlLXdpZHRoPSIyIi8+PHBhdGggZD0iTTggMTJMMTEgMTVMMTYgOSIgc3Ryb2tlPSIjMDBFNjc2IiBzdHJva2Utd2lkdGg9IjIuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9zdmc+"
SVG_CROSS_B64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0iIzFFMjYzOCIgZmlsbC1vcGFjaXR5PSIwLjgiIHN0cm9rZT0iIzMzNDE1NSIgc3Ryb2tlLXdpZHRoPSIxLjUiLz48cGF0aCBkPSJNOSA5TDE1IDE1TTE1IDlMOSAxNSIgc3Ryb2tlPSIjNjQ3NDhCIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvc3ZnPg=="

# ФУНКЦИЯ ДЛЯ ГЕНЕРАЦИИ СТРОКИ С ИКОНКОЙ И ЦВЕТОМ ТЕКСТА
def format_stat_with_icon(stat_text):
    stat_clean = stat_text.strip()
    stat_lower = stat_clean.lower()
    icon_name = None
    
    if "вес" in stat_lower:
        icon_name = "Texture_Icon_Weight.png"
    elif "радиация" in stat_lower:
        icon_name = "Texture_Icon_Radiation.png"
    elif "физическая защита" in stat_lower:
        icon_name = "Texture_Icon_PhysicalProtection.png"
    elif "выносливость" in stat_lower:
        icon_name = "Texture_Icon_EnergyRegen.png"
    elif "термозащита" in stat_lower:
        icon_name = "Texture_Icon_ThermalProtection.png"
    elif "кровотечени" in stat_lower:
        icon_name = "Texture_Icon_Bleeding.png"
    elif "электрозащита" in stat_lower:
        icon_name = "Texture_Icon_ElectricalProtection.png"
    elif "химзащита" in stat_lower:
        icon_name = "Texture_Icon_ChemicalProtection.png"
    elif "прочность" in stat_lower:
        icon_name = "T_Icon_Durability_Armor.png"

    if "радиация" in stat_lower:
        is_good = stat_lower.startswith("-")
    else:
        is_good = not stat_lower.startswith("-") if (stat_lower.startswith("+") or stat_lower.startswith("-")) else None

    if is_good is True:
        text_color = "#00E676"  # Салатовый
    elif is_good is False:
        text_color = "#FF5252"  # Красный
    else:
        text_color = "#CBD5E1"  # Нейтральный серый

    if icon_name:
        img_main = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/{icon_name}"
        img_master = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/{icon_name}"
        return f'<div style="display: flex; align-items: center; gap: 6px; margin-bottom: 3px; color: {text_color}; font-weight: 600;"><img src="{img_main}" onerror="this.onerror=null; this.src=\'{img_master}\';" style="width: 15px; height: 15px; object-fit: contain;" /><span>{stat_clean}</span></div>'
    else:
        return f'<div style="margin-bottom: 3px; color: {text_color}; font-weight: 500;">• {stat_clean}</div>'

# =========================================================================
# РАСПАКОВКА И ЧТЕНИЕ В ПАМЯТИ
# =========================================================================
def decompress_sav(bytes_data):
    if len(bytes_data) < 8:
        return None

    uncompressed_size = struct.unpack("<I", bytes_data[:4])[0]
    compressed_data = bytes_data[4:]

    so_path = get_linux_decompressor()
    
    if so_path and os.path.exists(so_path):
        try:
            lib = ctypes.cdll.LoadLibrary(so_path)
            dst_buf = ctypes.create_string_buffer(uncompressed_size)
            
            if hasattr(lib, "OozKraken_Decompress"):
                fn = lib.OozKraken_Decompress
                fn.argtypes = [ctypes.c_char_p, ctypes.c_int64, ctypes.c_char_p, ctypes.c_int64]
                fn.restype = ctypes.c_int64
                res = fn(compressed_data, len(compressed_data), dst_buf, uncompressed_size)
                if res > 0:
                    return dst_buf.raw
        except Exception:
            pass

    try:
        for dll_name in ["./ooz_decompress.dll", "./oo2core_9_win64.dll"]:
            if os.path.exists(dll_name):
                lib = ctypes.cdll.LoadLibrary(dll_name)
                dst_buf = ctypes.create_string_buffer(uncompressed_size)
                fn = lib.OodleLZ_Decompress
                fn.argtypes = [ctypes.c_char_p, ctypes.c_int64, ctypes.c_char_p, ctypes.c_int64, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int64, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int64, ctypes.c_int]
                fn.restype = ctypes.c_int64
                res = fn(compressed_data, len(compressed_data), dst_buf, uncompressed_size, 0,0,0,None,0,None,None,None,0,0)
                if res == uncompressed_size:
                    return dst_buf.raw
    except Exception:
        pass
        
    return None

def find_sids(raw_bytes):
    found = set()
    if not raw_bytes: return found
    for cat in CATEGORIES:
        for item in cat["items"]:
            sid = item[0]
            if sid.encode("ascii") in raw_bytes or sid.encode("utf-16le") in raw_bytes:
                found.add(sid)
    return found

# =========================================================================
# ИНТЕРФЕЙС САЙТА
# =========================================================================
st.markdown("""
<div style="text-align: center; padding: 10px 0 5px 0;">
    <div style="display: inline-block; background: rgba(255, 176, 0, 0.1); border: 1px solid rgba(255, 176, 0, 0.3); border-radius: 20px; padding: 4px 16px; color: #FFB000; font-size: 0.85rem; font-weight: 600; margin-bottom: 12px;">
        ☢️ S.T.A.L.K.E.R. 2 • Patch v1.9
    </div>
    <h1 style="color: #F8FAFC; font-size: 2.8rem; font-weight: 800; margin: 0; display: flex; align-items: center; justify-content: center; gap: 14px; flex-wrap: wrap;">
        <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/Header.png" 
             onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/Header.png';" 
             style="width: 60px; height: 60px; object-fit: contain; filter: drop-shadow(0 4px 8px rgba(255,176,0,0.3));" />
        <span>Чекер Артефактов</span>
    </h1>
    <p style="color: #94A3B8; font-size: 0.98rem; margin-top: 10px; max-width: 850px; margin-left: auto; margin-right: auto; line-height: 1.6;">
        Тут вы легко сможете проверить какие артефакты вы уже собрали а какие еще остались для достижения 
        <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/chud.png" onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/chud.png';" style="width: 22px; height: 22px; vertical-align: sub; margin: 0 2px;" />
        <b style="color: #FFA600;">«Собиратель чудес»</b> (69 артов) а так же для ачивки 
        <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/stran.png" onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/stran.png';" style="width: 22px; height: 22px; vertical-align: sub; margin: 0 2px;" />
        <b style="color: #FFA600;">«Все страньше и страньше»</b> (6 архиартефактов)
    </p>
</div>
""", unsafe_allow_html=True)

# Сворачиваемая инструкция по загрузке С ОТЦЕНТРИРОВАННЫМ ТЕКСТОМ И ИКОНКАМИ КОПИРОВАНИЯ
with st.expander("📁 Инструкция по загрузке файла сохранения", expanded=True):
    st.markdown("""
    <div style="text-align: center; color: #94A3B8; font-size: 0.92rem; line-height: 1.6; padding: 4px 0;">
        <p style="margin-top: 0; font-weight: 600; color: #F1F5F9; font-size: 0.96rem;">
            📁 Перетащите или загрузите по клику ваш файл <b>CampaignsSave.sav</b> в поле ниже.
        </p>
        
        <div style="margin-top: 12px;">
            <div style="color: #FFB000; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.5px; margin-bottom: 4px;">
                STEAM:
            </div>
            <div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; flex-wrap: wrap;">
                <code class="copy-path" data-copy="C:\\Users\\ИМЯ_ПК\\AppData\\Local\\Stalker2\\Saved\\STEAM\\SaveGames" 
                      style="color: #00E676; background: #111520; padding: 6px 12px; border-radius: 6px; border: 1px solid #1E2638; cursor: pointer; font-weight: 600; font-size: 0.85rem;">
                    C:\\Users\\ИМЯ_ПК\\AppData\\Local\\Stalker2\\Saved\\STEAM\\SaveGames
                </code>
                <button class="copy-path copy-btn-icon" data-copy="C:\\Users\\ИМЯ_ПК\\AppData\\Local\\Stalker2\\Saved\\STEAM\\SaveGames" title="Скопировать путь">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#00E676" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                </button>
            </div>
        </div>

        <div style="margin-top: 12px;">
            <div style="color: #FFB000; font-weight: 700; font-size: 0.85rem; letter-spacing: 0.5px; margin-bottom: 4px;">
                GAME PASS / EPIC GAMES:
            </div>
            <div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; flex-wrap: wrap;">
                <code class="copy-path" data-copy="C:\\Users\\ИМЯ_ПК\\AppData\\Local\\Stalker2\\Saved\\SaveGames" 
                      style="color: #00E676; background: #111520; padding: 6px 12px; border-radius: 6px; border: 1px solid #1E2638; cursor: pointer; font-weight: 600; font-size: 0.85rem;">
                    C:\\Users\\ИМЯ_ПК\\AppData\\Local\\Stalker2\\Saved\\SaveGames
                </code>
                <button class="copy-path copy-btn-icon" data-copy="C:\\Users\\ИМЯ_ПК\\AppData\\Local\\Stalker2\\Saved\\SaveGames" title="Скопировать путь">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#00E676" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                        <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                    </svg>
                </button>
            </div>
        </div>

        <div style="color: #64748B; font-size: 0.78rem; margin-top: 10px;">
            (Нажмите на рамку или иконку справа, чтобы скопировать путь)
        </div>
    </div>
    """, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Загрузите ваш файл сохранения (.sav)", type=["sav"])

if uploaded_file is not None:
    bytes_data = uploaded_file.read()
    raw_data = decompress_sav(bytes_data)

    if raw_data is None:
        st.error("❌ Не удалось расшифровать файл сохранения. Убедитесь, что это файл формата S.T.A.L.K.E.R. 2.")
    else:
        found_sids = find_sids(raw_data)

        base_found = 0
        base_total = 69
        weird_found = 0
        weird_total = 6

        for cat in CATEGORIES:
            is_weird = "СТРАННЫЕ" in cat["name"]
            for item in cat["items"]:
                sid = item[0]
                if sid in found_sids:
                    if is_weird: weird_found += 1
                    else: base_found += 1

        base_pct = int(base_found / base_total * 100)
        weird_pct = int(weird_found / weird_total * 100)

        st.markdown("<br/>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div style="background-color: #111520; border: 1px solid #1E2638; border-radius: 12px; padding: 18px 20px; display: flex; align-items: center; gap: 18px;">
                <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/art.png"
                     onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/art.png';"
                     style="width: 65px; height: 65px; object-fit: contain; flex-shrink: 0; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));" />
                <div style="flex-grow: 1;">
                    <div style="color: #94A3B8; font-size: 0.88rem; font-weight: 600; margin-bottom: 4px;">
                        «Собиратель чудес» (69 артов)
                    </div>
                    <div style="display: flex; align-items: baseline; justify-content: space-between;">
                        <span style="color: #F8FAFC; font-size: 1.8rem; font-weight: 800;">{base_found} / {base_total}</span>
                        <span style="color: #00E676; font-size: 0.95rem; font-weight: 700; background: rgba(0, 230, 118, 0.12); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 6px; padding: 2px 10px;">
                            {base_pct}%
                        </span>
                    </div>
                    <div style="width: 100%; background: #1E2638; border-radius: 8px; height: 8px; margin-top: 10px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #FFB000, #00E676); width: {base_pct}%; height: 100%; border-radius: 8px; transition: width 0.5s ease;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background-color: #111520; border: 1px solid #1E2638; border-radius: 12px; padding: 18px 20px; display: flex; align-items: center; gap: 18px;">
                <img src="https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/arch.png"
                     onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/arch.png';"
                     style="width: 65px; height: 65px; object-fit: contain; flex-shrink: 0; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));" />
                <div style="flex-grow: 1;">
                    <div style="color: #94A3B8; font-size: 0.88rem; font-weight: 600; margin-bottom: 4px;">
                        «Все страньше и страньше» (6 архиартефактов)
                    </div>
                    <div style="display: flex; align-items: baseline; justify-content: space-between;">
                        <span style="color: #F8FAFC; font-size: 1.8rem; font-weight: 800;">{weird_found} / {weird_total}</span>
                        <span style="color: #00E676; font-size: 0.95rem; font-weight: 700; background: rgba(0, 230, 118, 0.12); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 6px; padding: 2px 10px;">
                            {weird_pct}%
                        </span>
                    </div>
                    <div style="width: 100%; background: #1E2638; border-radius: 8px; height: 8px; margin-top: 10px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #FFB000, #00E676); width: {weird_pct}%; height: 100%; border-radius: 8px; transition: width 0.5s ease;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # =========================================================================
        # 3 КНОПКИ ФИЛЬТРАЦИИ С МЯГКОЙ СВЕТЯЩЕЙСЯ ОБВОДКОЙ
        # =========================================================================
        f_col1, f_col2, f_col3 = st.columns(3)

        with f_col1:
            if st.button("🌐 Показать все", use_container_width=True, type="primary" if st.session_state.art_filter == "all" else "secondary"):
                st.session_state.art_filter = "all"
                st.rerun()

        with f_col2:
            if st.button("🙈 Скрыть собранные", use_container_width=True, type="primary" if st.session_state.art_filter == "missing" else "secondary"):
                st.session_state.art_filter = "missing"
                st.rerun()

        with f_col3:
            if st.button("👁️ Скрыть не собранные", use_container_width=True, type="primary" if st.session_state.art_filter == "found" else "secondary"):
                st.session_state.art_filter = "found"
                st.rerun()

        st.markdown("<br/>", unsafe_allow_html=True)

        # Вывод категорий в виде СЕТКИ-ГАЛЕРЕИ С УЧЕТОМ ФИЛЬТРА
        for cat in CATEGORIES:
            filtered_items = []
            for item in cat["items"]:
                sid = item[0]
                is_found = sid in found_sids
                
                if st.session_state.art_filter == "missing" and is_found:
                    continue
                if st.session_state.art_filter == "found" and not is_found:
                    continue
                    
                filtered_items.append(item)

            if not filtered_items:
                continue

            with st.expander(cat["name"], expanded=True):
                grid_html = '<div class="art-grid">\n'
                
                for idx, item in enumerate(filtered_items):
                    sid, ru_name, weight, effects = item[0], item[1], item[2], item[3]
                    is_found = sid in found_sids
                    
                    status_svg = f'<img src="{SVG_CHECK_B64}" width="18" height="18" />' if is_found else f'<img src="{SVG_CROSS_B64}" width="18" height="18" />'
                    status_class = "tile-found" if is_found else "tile-missing"
                    
                    clean_name = ru_name[2:] if len(ru_name) > 2 else ru_name
                    
                    img_url_main = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/{sid}.png"
                    img_url_master = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/{sid}.png"
                    
                    img_style = f"background-image: url('{img_url_main}'), url('{img_url_master}');"
                    
                    # Иконка веса
                    weight_icon_url = "https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/Texture_Icon_Weight.png"
                    weight_icon_master = "https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/Texture_Icon_Weight.png"
                    
                    # Генерируем строки эффектов с иконками и цветом
                    effects_formatted = "".join([format_stat_with_icon(eff) for eff in effects.split(",")])
                    
                    tile_code = f'''<div class="art-tile {status_class}" data-copy="XCreateItemInInventoryByID {sid} 0 1 1">
                        <div class="tile-badge">{status_svg}</div>
                        <div class="tile-img-container">
                            <div class="tile-img" style="{img_style}"></div>
                        </div>
                        <div class="tile-label">{clean_name}</div>
                        <div class="tooltip-box">
                            <div style="font-weight: 700; color: #FFB000; font-size: 0.82rem; margin-bottom: 6px; border-bottom: 1px solid rgba(255,176,0,0.25); padding-bottom: 3px;">
                                {clean_name}
                            </div>
                            <div style="display: flex; align-items: center; gap: 6px; color: #CBD5E1; font-size: 0.75rem; margin-bottom: 6px;">
                                <img src="{weight_icon_url}" onerror="this.onerror=null; this.src='{weight_icon_master}';" style="width: 15px; height: 15px; object-fit: contain;" />
                                <span><b>Вес:</b> {weight}</span>
                            </div>
                            <div style="font-size: 0.74rem; line-height: 1.35; margin-bottom: 6px;">
                                {effects_formatted}
                            </div>
                            <div style="color: #64748B; font-size: 0.68rem; border-top: 1px solid #1E2638; padding-top: 4px; text-align: center;">
                                <span>Клик: скопировать ID</span>
                            </div>
                        </div>
                    </div>'''
                    
                    grid_html += tile_code
                
                grid_html += '</div>\n'
                
                if hasattr(st, "html"):
                    st.html(grid_html)
                else:
                    st.markdown(f"<div>{grid_html.replace(chr(10), '')}</div>", unsafe_allow_html=True)

        missing_base = [item[0] for cat in CATEGORIES if "СТРАННЫЕ" not in cat["name"] for item in cat["items"] if item[0] not in found_sids]
        missing_weird = [item[0] for cat in CATEGORIES if "СТРАННЫЕ" in cat["name"] for item in cat["items"] if item[0] not in found_sids]

        txt_content = "=========================================================\n"
        txt_content += "      СПИСОК НЕДОСТАЮЩИХ АРТЕФАКТОВ S.T.A.L.K.E.R. 2\n"
        txt_content += "=========================================================\n\n"

        for cat in CATEGORIES:
            missing_in_cat = [(item[0], item[1]) for item in cat["items"] if item[0] not in found_sids]
            if missing_in_cat:
                txt_content += f"{cat['name']}:\n"
                for sid, ru_name in missing_in_cat:
                    txt_content += f"  {ru_name} ({sid})\n"
                txt_content += "\n"

        txt_content += "=========================================================\n"
        txt_content += "КОМАНДЫ ДЛЯ СПАВНА НЕДОСТАЮЩИХ АРТЕФАКТОВ В ИНВЕНТАРЬ\n"
        txt_content += "=========================================================\n"
        txt_content += "Скопируйте нужный текст ниже (Ctrl+C), откройте консоль в игре и вставьте (Ctrl+V):\n\n"

        if not missing_base and not missing_weird:
            txt_content += "У вас собраны абсолютно все артефакты! Команды не требуются.\n"
        else:
            if missing_base:
                txt_content += "▶ Команда для базовых артефактов («Собиратель чудес»):\n"
                txt_content += "|".join([f"XCreateItemInInventoryByID {s} 0 1 1" for s in missing_base]) + "\n\n"
            if missing_weird:
                txt_content += "▶ Команда для странных артефактов («Все страньше и страньше»):\n"
                txt_content += "|".join([f"XCreateItemInInventoryByID {s} 0 1 1" for s in missing_weird]) + "\n\n"

            txt_content += "*(После ввода команды просто выбросьте заспавненные артефакты на землю и поднимите,\n"
            txt_content += "чтобы они гарантированно зачлись в статистику и ачивки)*\n"

        st.markdown("<br/>", unsafe_allow_html=True)
        st.download_button(
            label="📥 Скачать недостающие артефакты и команды спавна (Missing_Artifacts.txt)",
            data=txt_content,
            file_name="Missing_Artifacts.txt",
            mime="text/plain"
        )

# =========================================================================
# ИНЪЕКЦИЯ СКРИПТА ДЛЯ КОПИРОВАНИЯ КОМАНД И ПУТЕЙ В БУФЕР ОБМЕНА
# =========================================================================
components.html("""
<script>
try {
    const parentDoc = window.parent.document;
    parentDoc.addEventListener('click', function(e) {
        let copyPath = e.target.closest('.copy-path');
        let tile = e.target.closest('.art-tile');
        
        if(copyPath) {
            let pathText = copyPath.getAttribute('data-copy');
            if(pathText && parentDoc.hasFocus()) {
                parentDoc.defaultView.navigator.clipboard.writeText(pathText).then(() => {
                    let codeEl = copyPath.tagName === 'CODE' ? copyPath : copyPath.parentElement.querySelector('code');
                    if(codeEl) {
                        let orig = codeEl.innerText;
                        codeEl.innerText = "✅ Путь скопирован!";
                        setTimeout(() => { codeEl.innerText = orig; }, 1500);
                    }
                });
            }
        } else if(tile) {
            let cmd = tile.getAttribute('data-copy');
            if(cmd && parentDoc.hasFocus()) {
                parentDoc.defaultView.navigator.clipboard.writeText(cmd).then(() => {
                    let tooltip = tile.querySelector('.tooltip-box span');
                    if(tooltip) {
                        let originalText = tooltip.innerText;
                        tooltip.innerText = "✅ Скопировано!";
                        tooltip.style.color = "#00E676";
                        setTimeout(() => { 
                            tooltip.innerText = originalText;
                            tooltip.style.color = "#64748B";
                        }, 1200);
                    }
                }).catch(err => console.error("Clipboard err:", err));
            }
        }
    });
} catch(err) {
    console.log("Iframe cross-origin restriction for clipboard.");
}
</script>
""", height=0, width=0)
