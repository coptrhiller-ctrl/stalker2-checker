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
# CUSTOM CSS / GAME INVENTORY GRID STYLES
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

    /* СЕТКА ГАЛЕРЕИ (GRID) */
    .art-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(135px, 1fr));
        gap: 12px;
        padding: 10px 0;
    }

    /* Карточка-плитка артефакта */
    .art-tile {
        position: relative;
        background: #111520;
        border-radius: 12px;
        padding: 10px 6px 8px 6px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        height: 145px;
        cursor: pointer;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        user-select: none;
    }
    .art-tile:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
    }

    /* Цветовые рамки редкости */
    .rarity-common { border: 2px solid #3A4256; }
    .rarity-uncommon { border: 2px solid #00B4D8; }
    .rarity-rare { border: 2px solid #9D4EDD; }
    .rarity-epic { border: 2px solid #FF9E00; }
    .rarity-weird { border: 2px solid #E024A5; }

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

    /* Значок галочки/крестика в правом верхнем углу */
    .tile-badge {
        position: absolute;
        top: 6px;
        right: 6px;
        z-index: 2;
    }

    /* Контейнер картинки */
    .tile-img-container {
        width: 100%;
        height: 75px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-top: 4px;
    }
    .tile-img {
        max-width: 62px;
        max-height: 62px;
        object-fit: contain;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.6));
    }

    /* Подпись названия снизу */
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

    /* Легенда редкостей снизу */
    .legend-bar {
        display: flex;
        justify-content: center;
        gap: 12px;
        margin-top: 15px;
        flex-wrap: wrap;
    }
    .legend-item {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
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

# SVG Галочка и Крестик
SVG_CHECK = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" fill="#00E676" fill-opacity="0.2" stroke="#00E676" stroke-width="2"/><path d="M8 12L11 15L16 9" stroke="#00E676" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
SVG_CROSS = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" fill="#1E2638" fill-opacity="0.8" stroke="#334155" stroke-width="1.5"/><path d="M9 9L15 15M15 9L9 15" stroke="#64748B" stroke-width="2" stroke-linecap="round"/></svg>"""

def get_rarity_class(ru_name):
    if ru_name.startswith("🔘"): return "rarity-common"
    if ru_name.startswith("🔵"): return "rarity-uncommon"
    if ru_name.startswith("🟣"): return "rarity-rare"
    if ru_name.startswith("🟡"): return "rarity-epic"
    return "rarity-weird"

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
        Проверка достижений «Собиратель чудес» (69 артов) и «Все страньше и страньше» (6 артов) онлайн
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style='background: #111520; border: 1px solid #1E2638; border-left: 4px solid #FFB000; border-radius: 10px; padding: 14px 20px; margin: 15px 0 22px 0; box-shadow: 0 4px 15px rgba(0,0,0,0.3);'>
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
        st.markdown("<h3 style='color: #FFB000;'>📋 Подробная витрина артефактов:</h3>", unsafe_allow_html=True)

        # Вывод категорий в виде СЕТКИ-ГАЛЕРЕИ (как в игре)
        for cat in CATEGORIES:
            with st.expander(cat["name"], expanded=True):
                grid_html = '<div class="art-grid">'
                
                for idx, (sid, ru_name) in enumerate(cat["items"]):
                    is_found = sid in found_sids
                    status_svg = SVG_CHECK if is_found else SVG_CROSS
                    status_class = "tile-found" if is_found else "tile-missing"
                    rarity_cls = get_rarity_class(ru_name)
                    
                    clean_name = ru_name[2:] if len(ru_name) > 2 else ru_name
                    
                    img_url_main = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/{sid}.png"
                    img_url_master = f"https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/{sid}.png"
                    
                    grid_html += f"""
                    <div class="art-tile {rarity_cls} {status_class}" 
                         title="ID: {sid}&#10;Кликните, чтобы скопировать команду спавна!" 
                         onclick="navigator.clipboard.writeText('XCreateItemInInventoryByID {sid} 0 1 1');">
                        <div class="tile-badge">{status_svg}</div>
                        <div class="tile-img-container">
                            <img src="{img_url_main}" 
                                 onerror="this.onerror=null; this.src='{img_url_master}'; this.onerror=function(){{this.style.opacity='0';}};" 
                                 class="tile-img" />
                        </div>
                        <div class="tile-label">{clean_name}</div>
                    </div>
                    """
                
                grid_html += '</div>'
                
                # Легенда редкостей снизу под каждой категорией
                grid_html += """
                <div class="legend-bar">
                    <span class="legend-item" style="background: rgba(58, 66, 86, 0.25); border: 1px solid #3A4256; color: #E2E8F0;">🔘 Обычный</span>
                    <span class="legend-item" style="background: rgba(0, 180, 216, 0.12); border: 1px solid #00B4D8; color: #00B4D8;">🔵 Необычный</span>
                    <span class="legend-item" style="background: rgba(157, 78, 221, 0.12); border: 1px solid #9D4EDD; color: #9D4EDD;">🟣 Редкий</span>
                    <span class="legend-item" style="background: rgba(255, 158, 0, 0.12); border: 1px solid #FF9E00; color: #FF9E00;">🟡 Эпический</span>
                </div>
                """
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
