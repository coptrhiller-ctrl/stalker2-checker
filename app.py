import streamlit as st
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

# =========================================================================
# CUSTOM CSS / СТИЛИЗАЦИЯ КАРТОЧЕК С КАК НА СКРИНШОТЕ
# =========================================================================
st.markdown("""
<style>
    .stApp {
        background-color: #080A0F;
        color: #E2E8F0;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    .main .block-container {
        max-width: 1200px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Зона загрузки файлов */
    [data-testid="stFileUploader"] {
        background-color: #111520 !important;
        border: 2px dashed #FFB000 !important;
        border-radius: 14px !important;
        padding: 16px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #FFC107 !important;
        box-shadow: 0 0 20px rgba(255, 176, 0, 0.2);
    }

    /* Аккордеоны */
    div[data-baseweb="accordion"] > div {
        background-color: #111520 !important;
        border: 1px solid #1E2638 !important;
        border-radius: 12px !important;
        margin-bottom: 12px !important;
    }

    /* ===================================================================
       СЕТКА ПЛИТОК (GRID) И КАРТОЧКИ КАК НА СКРИНШОТЕ
       =================================================================== */
    .artifact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
        gap: 14px;
        padding: 10px 0;
    }

    .art-tile {
        position: relative;
        background: #111520;
        border-radius: 14px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        cursor: pointer;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        user-select: none;
        height: 160px;
    }

    /* Найденные карточки */
    .art-tile-found {
        border: 2px solid #00E676 !important;
        box-shadow: 0 0 14px rgba(0, 230, 118, 0.25);
    }
    .art-tile-found:hover {
        transform: translateY(-4px);
        box-shadow: 0 0 22px rgba(0, 230, 118, 0.45);
    }

    /* Ненайденные карточки */
    .art-tile-missing {
        border: 2px solid var(--rarity-color);
        opacity: 0.6;
    }
    .art-tile-missing:hover {
        opacity: 1;
        transform: translateY(-4px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
    }

    /* Бейдж в верхнем правом углу */
    .art-badge-pos {
        position: absolute;
        top: 8px;
        right: 8px;
        z-index: 2;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
    }

    /* Контейнер иконки */
    .art-tile-img-box {
        width: 100%;
        height: 115px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 10px;
    }
    .art-tile-img {
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
        filter: drop-shadow(0 4px 10px rgba(0,0,0,0.7));
    }

    /* Нижняя цветная плашка с названием */
    .art-tile-footer {
        width: 100%;
        padding: 8px 4px;
        text-align: center;
        font-size: 0.82rem;
        font-weight: 700;
        color: #FFFFFF;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.15);
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
# БАЗА ДАННЫХ АРТЕФАКТОВ
# =========================================================================
CATEGORIES = [
    {
        "name": "1. 🌌 ГРАВИТАЦИОННЫЕ АРТЕФАКТЫ",
        "items": [
            ("GArtifactGoldFish", "🔘 Золотая рыбка"),
            ("GArtifactStoneDrop", "🔘 Каменное сердце"),
            ("GArtifactGravy", "🔘 Грави"),
            ("GArtifactWrenched", "🔘 Выверт"),
            ("GArtifactBloodStone", "🔘 Кровь камня"),
            ("GArtifactTrunk", "🔘 Канифоль"),
            ("GArtifactSponge", "🔘 Вихрь"),
            ("GArtifactPlane", "🔘 Галька"),
            ("GArtifactLandSlug", "🔘 Медуза"),
            ("GArtifactSpring", "🔵 Пружина"),
            ("GArtifactGraphiteBlock", "🔵 Корона"),
            ("GArtifactHedgehog", "🔵 Мухоловка"),
            ("GArtifactNightStar", "🟣 Ночная звезда"),
            ("GArtifactSplitStone", "🟣 Битый камень"),
            ("GArtifactBud", "🟣 Бутон"),
            ("GArtifactCompass", "🟡 Компас"),
            ("GArtifactRubiksCube", "🟡 Кубик-Рубик")
        ]
    },
    {
        "name": "2. 🔥 ТЕРМИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("FArtifactFireBall", "🔘 Огненный шар"),
            ("FArtifactSteak", "🔘 Бифштекс"),
            ("FArtifactGlass", "🔘 Полость"),
            ("FArtifactBurntHunk", "🔘 Вертушка"),
            ("FArtifactResin", "🔘 Лира"),
            ("FArtifactDrops", "🔘 Капли"),
            ("FArtifactEye", "🔘 Глаз"),
            ("FArtifactCrystal", "🔘 Кристалл"),
            ("FArtifactMomsBeads", "🟣 Мамины Бусы"),
            ("FArtifactBakedBolts", "🔵 Брак"),
            ("FArtifactDeadSponge", "🔵 Мёртвая губка"),
            ("FArtifactHellishHedgehog", "🔵 Магма"),
            ("FArtifactPlasma", "🔵 Плазма"),
            ("FArtifactCandle", "🟣 Лепесток"),
            ("FArtifactFireworks", "🟣 Мясная зажигалка"),
            ("FArtifactCore", "🟣 Факел"),
            ("FArtifactRingOmnipotence", "🟡 Гиперкуб")
        ]
    },
    {
        "name": "3. ⚡ ЭЛЕКТРИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("EArtifactFlash", "🔘 Вспышка"),
            ("EArtifactSnowflake", "🔘 Снежинка"),
            ("EArtifactDummy", "🔘 Пустышка"),
            ("EArtifactBattery", "🔘 Батарейка"),
            ("EArtifactJellyFish", "🔘 Сапфир"),
            ("EArtifactWorm", "🔘 Крысиный король"),
            ("EArtifactSparkler", "🔘 Бенгальский огонь"),
            ("EArtifactChocolate", "🔘 Шоколадка"),
            ("EArtifactSoul", "🔵 Душа"),
            ("EArtifactMoonlight", "🔵 Лунный свет"),
            ("EArtifactTow", "🔵 Урок труда"),
            ("EArtifactThunderHedgehog", "🔵 Фонарь"),
            ("EArtifactCloud", "🔵 Арфа"),
            ("EArtifactAtom", "🟣 Блик"),
            ("EArtifactRazor", "🟣 Морская звезда"),
            ("EArtifactCrystalGlass", "🟣 Гребень"),
            ("EArtifactDope", "🟡 Грозовая ягода")
        ]
    },
    {
        "name": "4. 🧪 ХИМИЧЕСКИЕ АРТЕФАКТЫ",
        "items": [
            ("CArtifactCrystalThorn", "🔘 Кристальная колючка"),
            ("CArtifactThorn", "🔘 Колючка"),
            ("CArtifactChunkMeat", "🔘 Ломоть мяса"),
            ("CArtifactBubble", "🔵 Пузырь"),
            ("CArtifactSlug", "🔘 Слизняк"),
            ("CArtifactSlime", "🔘 Слизь"),
            ("CArtifactKryptonite", "🔘 Плесень"),
            ("CArtifactBung", "🔘 Рог"),
            ("CArtifactCottonWool", "🔘 Скорлупа"),
            ("CArtifactMica", "🔘 Слюда"),
            ("CArtifactBun", "🔵 Колобок"),
            ("CArtifactEchinus", "🔵 Морской еж"),
            ("CArtifactRosin", "🔵 Завтрак туриста"),
            ("CArtifactPlasticine", "🔵 Инфузория"),
            ("CArtifactPellicle", "🟣 Плёнка"),
            ("CArtifactBouncyBall", "🟣 Попрыгунчик"),
            ("CArtifactDevilsMushroom", "🟣 Чёртов гриб"),
            ("CArtifactLiquidStone", "🟡 Жидкий камень")
        ]
    },
    {
        "name": "5. 🌀 СТРАННЫЕ АРТЕФАКТЫ (Ачивка «Все страньше и страньше»)",
        "items": [
            ("AArtifactWeirdWater", "🌀 Странная вода"),
            ("AArtifactWeirdBall", "🌀 Странный мяч"),
            ("AArtifactWeirdNut", "🌀 Странная гайка"),
            ("AArtifactWeirdBolt", "🌀 Странный болт"),
            ("AArtifactWeirdKettle", "🌀 Странный котелок"),
            ("AArtifactWeirdFlower", "🌀 Странный цветок")
        ]
    }
]

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
        for sid, _ in cat["items"]:
            if sid.encode("ascii") in raw_bytes or sid.encode("utf-16le") in raw_bytes:
                found.add(sid)
    return found

# =========================================================================
# ИНТЕРФЕЙС САЙТА
# =========================================================================
st.markdown("""
<div style="text-align: center; padding: 10px 0 5px 0;">
    <div style="display: inline-block; background: rgba(255, 176, 0, 0.1); border: 1px solid rgba(255, 176, 0, 0.3); border-radius: 20px; padding: 4px 16px; color: #FFB000; font-size: 0.85rem; font-weight: 600; margin-bottom: 12px;">
        ☢️ S.T.A.L.K.E.R. 2 • SAVE INSPECTOR v1.0
    </div>
    <h1 style="color: #F8FAFC; font-size: 2.1rem; font-weight: 800; margin: 0;">
        Чекер Артефактов
    </h1>
    <p style="color: #94A3B8; font-size: 0.98rem; margin-top: 8px;">
        Мгновенная онлайн-проверка достижений «Собиратель чудес» (69 артов) и «Все страньше и страньше» (6 артов)
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background: #111520; border: 1px solid #1E2638; border-left: 4px solid #FFB000; border-radius: 10px; padding: 16px 20px; margin: 15px 0 22px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.3);'>
    <div style='display: flex; align-items: center; gap: 10px; margin-bottom: 6px;'>
        <span style='font-size: 1.2rem;'>📁</span>
        <span style='color: #FFB000; font-weight: 700; font-size: 1rem; text-transform: uppercase; letter-spacing: 0.5px;'>Инструкция по загрузке:</span>
    </div>
    <div style='color: #94A3B8; font-size: 0.92rem; line-height: 1.5; padding-left: 28px;'>
        Перетащите ваш файл <b>CampaignsSave.sav</b> в поле ниже.<br/>
        <span style='font-size: 0.82rem; opacity: 0.8;'>Путь к файлу: <code>AppData/Local/Stalker2/Saved/STEAM/SaveGames/</code></span>
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
            for sid, _ in cat["items"]:
                if sid in found_sids:
                    if is_weird: weird_found += 1
                    else: base_found += 1

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #FFB000;'>🏆 Прогресс по достижениям:</h3>", unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="«Собиратель чудес» (69 артов)", value=f"{base_found} / {base_total}", delta=f"{int(base_found/base_total*100)}%")
            st.progress(base_found / base_total)
        with col2:
            st.metric(label="«Все страньше и страньше» (6 артов)", value=f"{weird_found} / {weird_total}", delta=f"{int(weird_found/weird_total*100)}%")
            st.progress(weird_found / weird_total)

        st.markdown("<br/>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #FFB000;'>📋 Подробный чек-лист по категориям:</h3>", unsafe_allow_html=True)

        # РЕНДЕРИНГ ПЛИТОК КАК НА СКРИНШОТЕ ПО КАТЕГОРИЯМ
        # SVG ГАЛКА И КРЕСТИК
        svg_verified = """<svg width="22" height="22" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" fill="#00E676"/><path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z" fill="#0A0D14"/></svg>"""
        svg_cross = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" fill="#1E2638" stroke="#3A4256" stroke-width="1.5"/><path d="M15 9L9 15M9 9l6 6" stroke="#6C7A89" stroke-width="2" stroke-linecap="round"/></svg>"""

        for cat in CATEGORIES:
            with st.expander(cat["name"], expanded=True):
                cards_html = []
                for sid, ru_name in cat["items"]:
                    is_found = sid in found_sids
                    icon_type = ru_name[0]
                    clean_name = ru_name[2:] if len(ru_name) > 2 else ru_name

                    # Цвета подложки плашки по редким видам
                    r_color, footer_bg = {
                        "🔘": ("#3A4256", "#232A3B"),
                        "🔵": ("#00A8E8", "#0077B6"),
                        "🟣": ("#9D4EDD", "#7B2CBF"),
                        "🟡": ("#FFB000", "#D48800"),
                        "🌀": ("#00E5FF", "#0091EA")
                    }.get(icon_type, ("#3A4256", "#232A3B"))

                    tile_class = "art-tile-found" if is_found else "art-tile-missing"
                    badge_svg = svg_verified if is_found else svg_cross

                    img_url_main = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/{sid}.png"
                    img_url_master = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/{sid}.png"

                    cmd = f"XCreateItemInInventoryByID {sid} 0 1 1"
                    tooltip_text = f"Название: {clean_name}&#10;ID: {sid}&#10;Нажмите, чтобы скопировать команду спавна"

                    card_html = f"""
                    <div class="art-tile {tile_class}" style="--rarity-color: {r_color};" title="{tooltip_text}" onclick="navigator.clipboard.writeText('{cmd}');">
                        <div class="art-badge-pos">{badge_svg}</div>
                        <div class="art-tile-img-box">
                            <img src="{img_url_main}" onerror="this.onerror=null; this.src='{img_url_master}'; this.onerror=function(){{this.style.opacity='0';}};" class="art-tile-img" />
                        </div>
                        <div class="art-tile-footer" style="background-color: {footer_bg};">
                            {clean_name}
                        </div>
                    </div>
                    """
                    cards_html.append(card_html)

                grid_html = f'<div class="artifact-grid">{"".join(cards_html)}</div>'
                st.markdown(grid_html, unsafe_allow_html=True)

        missing_base = [sid for cat in CATEGORIES if "СТРАННЫЕ" not in cat["name"] for sid, _ in cat["items"] if sid not in found_sids]
        missing_weird = [sid for cat in CATEGORIES if "СТРАННЫЕ" in cat["name"] for sid, _ in cat["items"] if sid not in found_sids]

        txt_content = "=========================================================\n"
        txt_content += "      СПИСОК НЕДОСТАЮЩИХ АРТЕФАКТОВ S.T.A.L.K.E.R. 2\n"
        txt_content += "=========================================================\n\n"

        for cat in CATEGORIES:
            is_weird_cat = "СТРАННЫЕ" in cat["name"]
            missing_in_cat = [(sid, ru_name) for sid, ru_name in cat["items"] if sid not in found_sids]
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
