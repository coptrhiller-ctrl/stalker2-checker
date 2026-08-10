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
    layout="centered"
)

# =========================================================================
# CUSTOM CSS / UI/UX СТИЛИЗАЦИЯ (ТЕМНАЯ ТЕМА S.T.A.L.K.E.R.)
# =========================================================================
st.markdown("""
<style>
    /* Базовый тёмный фон приложения */
    .stApp {
        background-color: #0B0E14;
        color: #E0E6ED;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }

    /* Скрытие стандартного футера Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Кастомная зона загрузки файла */
    [data-testid="stFileUploader"] {
        background-color: #151922 !important;
        border: 2px dashed #FFB000 !important;
        border-radius: 12px !important;
        padding: 15px !important;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover {
        border-color: #FFC107 !important;
        box-shadow: 0 0 15px rgba(255, 176, 0, 0.2);
    }

    /* Стили плашек найденных и ненайденных артефактов */
    .art-found {
        background: rgba(0, 230, 118, 0.07);
        border: 1px solid rgba(0, 230, 118, 0.3);
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        color: #00E676;
        font-weight: 600;
        font-size: 0.95rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .art-missing {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid #232A3B;
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
        color: #6C7A89;
        font-size: 0.95rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Карточки дашбордов */
    [data-testid="stMetric"] {
        background-color: #151922;
        border: 1px solid #232A3B;
        border-radius: 12px;
        padding: 15px;
    }

    /* Кнопка скачивания файла */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #FFB000 0%, #E69500 100%) !important;
        color: #0B0E14 !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 14px 28px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(255, 176, 0, 0.3) !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #FFC107 0%, #FFB000 100%) !important;
        box-shadow: 0 0 25px rgba(255, 176, 0, 0.6) !important;
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
st.markdown("<h1 style='text-align: center; color: #FFB000;'>☢️ S.T.A.L.K.E.R. 2 — ЧЕКЕР АРТЕФАКТОВ</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #8C9BAE;'>Проверка прогресса достижений <b>«Собиратель чудес»</b> (69 артов) и <b>«Все страньше и страньше»</b> (6 артов) онлайн</p>", unsafe_allow_html=True)

st.markdown("""
<div style='background: #151922; border: 1px solid #232A3B; border-radius: 10px; padding: 12px 18px; margin-bottom: 20px;'>
    <span style='color: #FFB000; font-weight: bold;'>💡 Как узнать свой прогресс:</span><br/>
    <span style='color: #A0AEC0; font-size: 0.9em;'>Загрузите ваш файл <b>CampaignsSave.sav</b> (обычно лежит в <code>AppData/Local/Stalker2/Saved/STEAM/SaveGames/</code>)</span>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Перетащите сюда файл сохранения (.sav)", type=["sav"])

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

        # Вывод категорий в двухколоночной сетке
        for cat in CATEGORIES:
            with st.expander(cat["name"], expanded=True):
                col_a, col_b = st.columns(2)
                for idx, (sid, ru_name) in enumerate(cat["items"]):
                    is_found = sid in found_sids
                    status_icon = "✅" if is_found else "❌"
                    card_class = "art-found" if is_found else "art-missing"
                    
                    item_html = f"""
                    <div class="{card_class}">
                        <span>{ru_name}</span>
                        <span>{status_icon}</span>
                    </div>
                    """
                    
                    if idx % 2 == 0:
                        with col_a:
                            st.markdown(item_html, unsafe_allow_html=True)
                    else:
                        with col_b:
                            st.markdown(item_html, unsafe_allow_html=True)

        # Подготовка файла для скачивания
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
