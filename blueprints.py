import streamlit as st
import streamlit.components.v1 as components
import json
import base64

# =========================================================================
# ИКОНКИ И ССЫЛКИ GITHUB
# =========================================================================
GITHUB_RAW = "https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main"
GITHUB_FALLBACK = "https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master"

HEADER_ICON_MAIN = f"{GITHUB_RAW}/icons/flesh_icon.png"
HEADER_ICON_FALLBACK = f"{GITHUB_FALLBACK}/icons/flesh_icon.png"

DEF_CARD_ICON_MAIN = f"{GITHUB_RAW}/icons/blueprint/icon_def_blue.png"
DEF_CARD_ICON_FALLBACK = f"{GITHUB_FALLBACK}/icons/blueprint/icon_def_blue.png"

def get_bp_icon_url(bp_id):
    return f"{GITHUB_RAW}/icons/blueprint/icon_{bp_id}.png"

def get_def_icon_url(bp_id):
    idx = (sum(ord(c) for c in bp_id) % 11) + 1
    return f"{GITHUB_RAW}/icons/blueprint/icon_def_{idx}.png"

def get_def_icon_fallback_url(bp_id):
    idx = (sum(ord(c) for c in bp_id) % 11) + 1
    return f"{GITHUB_FALLBACK}/icons/blueprint/icon_def_{idx}.png"

def get_map_url(bp_id):
    return f"{GITHUB_RAW}/icons/blueprint/map_{bp_id}.png"

def get_scr_url(bp_id, index=1):
    if index == 1:
        return f"{GITHUB_RAW}/icons/blueprint/scr_{bp_id}.png"
    return f"{GITHUB_RAW}/icons/blueprint/scr_{bp_id}_{index}.png"

# =========================================================================
# БАЗА ДАННЫХ ЧЕРТЕЖЕЙ (77 ШТ.)
# =========================================================================
BLUEPRINTS_DATA = [
  # --- ОРУЖИЕ (27 шт.) ---
  {"id": "Blueprint_M10_Upgrade_1", "type": "weapon", "RU_Short": "M10 Gordon", "EN_Short": "M10 Gordon", "UA_Short": "M10 Gordon", "RU_Full": "M10 Gordon: Прорезиненный слой", "EN_Full": "M10 Gordon: Rubber Layer", "UA_Full": "M10 Gordon: Гумовий шар", "RU_Desc": "Частично гасит отдачу.", "EN_Desc": "Partially dampens recoil.", "UA_Desc": "Частково гасить віддачу.", "teleport_cmd": "XTeleportTo 412334.406885 357791.667238 985.7941", "map_url": "https://joric.github.io/stalker/#D6F7FCF342C3FDF1720FBA96E658A4B0"},
  {"id": "Blueprint_Rhino_Upgrade_1", "type": "weapon", "RU_Short": "Rhino", "EN_Short": "Rhino", "UA_Short": "Rhino", "RU_Full": "Rhino: Переделка под дробь", "EN_Full": "Rhino: Buckshot Conversion", "UA_Full": "Rhino: Перероблення під дріб", "RU_Desc": "Связана с рассверливанием ствола и подгонкой деталей под новый тип боеприпаса.", "EN_Desc": "Boring out the barrel and adjusting parts to accommodate new ammunition.", "UA_Desc": "Розсвердлювання ствола та припасування деталей під новий тип боєприпасу.", "teleport_cmd": "XTeleportTo 263410.590723 589963.614277 1120.966385", "map_url": "https://joric.github.io/stalker/#FEEFD9914436AF2F7032088C3AF8A11E"},
  {
    "id": "Blueprint_APB_Upgrade_1", "type": "weapon", "RU_Short": "АПБС", "EN_Short": "APSB", "UA_Short": "АПБС",
    "RU_Full": "АПБС: Установка балансира", "EN_Full": "APSB: Counterweight", "UA_Full": "АПБС: Встановлення балансира",
    "RU_Desc": "Балансир увеличивает стабильность оружия, уменьшая разброс при стрельбе.", "EN_Desc": "Enhances stability, reducing spread when firing.", "UA_Desc": "Збільшує стабільність зброї, що зменшує розкид під час стрільби.",
    "RU_Warn": "Флешка с чертежом появляется только после завершения сюжетного квеста «Поиски былой славы». До этого времени сейф отсутствует. Придется вернуться в подземелье «Агропром» во второй раз после завершения квеста.",
    "UA_Warn": "Флешка з кресленням з'являється лише після завершення сюжетного квесту «Пошуки колишньої слави». До цього часу сейф відсутній. Доведеться повернутися в підземелля «Агропрому» вдруге після завершення квесту.",
    "EN_Warn": "This flash drive only appears after completing the story quest 'In Search of Past Glory'. The safe is absent before that. You must return to the Agroprom Underground a second time after finishing the quest.",
    "teleport_cmd": "XTeleportTo 239788.204227 464708.50443 -1259.095031", "map_url": "https://joric.github.io/stalker/#C290D85847B442E3514EA58DF407ED4F"
  },
  {"id": "Blueprint_APB_Upgrade_2", "type": "weapon", "RU_Short": "АПБС", "EN_Short": "APSB", "UA_Short": "АПБС", "RU_Full": "АПБС: Индивидуальная подгонка", "EN_Full": "APSB: Individual Adjustment", "UA_Full": "АПБС: Індивідуальне припасування", "RU_Desc": "Моделирование рукоятки под стрелка повышает удобство обращения.", "EN_Desc": "Customizing the grip to match shooter's hand.", "UA_Desc": "Моделювання руків'я під стрільця підвищує зручність.", "teleport_cmd": "XTeleportTo 128163.000455 514183.159424 1403.812164", "map_url": "https://joric.github.io/stalker/#098E76F14ADD5CFF9C62508DB31013E3"},
  {
    "id": "Blueprint_Integral_Upgrade_1", "type": "weapon", "RU_Short": "Integral-A", "EN_Short": "Integral-A", "UA_Short": "Integral-A",
    "RU_Full": "Integral-A: Уплотнитель муфты возвратного механизма", "EN_Full": "Integral-A: Return Mechanism Sleeve Tightener", "UA_Full": "Integral-A: Ущільнювач муфти зворотного механізму",
    "RU_Desc": "Увеличивает давление в стволе, повышая начальную скорость пули.", "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.", "UA_Desc": "Збільшує тиск у стволі, що підвищує початкову швидкість кулі.",
    "RU_Warn": "Забрать эту флешку с чертежом можно только во время выполнения сюжетного квеста «До последней капли крови», после чего путь в «НИИЧАЗ» будет закрыт навсегда. Дубликата этого чертежа нет. Если вы его пропустили, получить его можно только путём загрузки ранних сохранений.",
    "UA_Warn": "Забрати цю флешку з кресленням можна тільки під час виконання сюжетного квесту «До останньої краплі крові», після чого шлях до «НДІЧАЗ» буде закрито назавжди. Дубліката цього креслення немає. Якщо ви його пропустили, отримати його можна лише шляхом завантаження ранніх збережень.",
    "EN_Warn": "This flash drive can ONLY be collected during the story quest 'To the Last Drop of Blood', after which access to SIRCAA will be locked forever. There is no duplicate. If missed, it can only be obtained by reloading an earlier save.",
    "teleport_cmd": "XTeleportTo 666996.209939 456129.806797 1393.600021", "map_url": "https://joric.github.io/stalker/#F5C45E2941CD2B53C196DC8B80C50500"
  },
  {"id": "Blueprint_Zubr_Upgrade_1", "type": "weapon", "RU_Short": "«Зубр-19»", "EN_Short": "Zubr-19", "UA_Short": "«Зубр-19»", "RU_Full": "«Зубр-19»: Дополнительный нарез в стволе", "EN_Full": "Zubr-19: Extra Barrel Rifling", "UA_Full": "«Зубр-19»: Додатковий наріз у стволі", "RU_Desc": "Снижает разрушение пули в стволе, сохраняя её характеристики.", "EN_Desc": "Reduces bullet deterioration within the barrel.", "UA_Desc": "Зменшує руйнування кулі в стволі.", "teleport_cmd": "XTeleportTo 168691.43198 278738.273426 858.817567", "map_url": "https://joric.github.io/stalker/#B7DBD42047E7047AD5C4989FCF76290F"},
  {"id": "Blueprint_Zubr_Upgrade_2", "type": "weapon", "RU_Short": "«Зубр-19»", "EN_Short": "Zubr-19", "UA_Short": "«Зубр-19»", "RU_Full": "«Зубр-19»: Анатомическая подгонка", "EN_Full": "Zubr-19: Anatomical Adjustment", "UA_Full": "«Зубр-19»: Анатомічне припасування", "RU_Desc": "Более удобная форма цевья повышает ускорение прицеливания.", "EN_Desc": "A more comfortable handguard shape contributes to increased aiming speed.", "UA_Desc": "Зручніша форма цівки прискорює прицілювання.", "teleport_cmd": "XTeleportTo 161276.943341 650322.048641 653.375015", "map_url": "https://joric.github.io/stalker/#193A0C674EC31AD853462698819AED75"},
  {"id": "Blueprint_Gvintar_Upgrade_1", "type": "weapon", "RU_Short": "СВ «Винтарь»", "EN_Short": "VS Vintar", "UA_Short": "СГ «Гвинтар»", "RU_Full": "СВ «Винтарь»: Уплотнитель муфты возвратного механизма", "EN_Full": "VS Vintar: Return Mechanism Sleeve Tightener", "UA_Full": "СГ «Гвинтар»: Ущільнювач муфти зворотного механізму", "RU_Desc": "Увеличивает давление в стволе, повышая скорость пули.", "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.", "UA_Desc": "Збільшує тиск у стволі, підвищуючи швидкість кулі.", "teleport_cmd": "XTeleportTo 681204.736397 640613.011916 2104.772779", "map_url": "https://joric.github.io/stalker/#EC5B93A14AE1E80F274534A82959CEDB"},
  {
    "id": "Blueprint_Gvintar_Upgrade_2", "type": "weapon", "RU_Short": "СВ «Винтарь»", "EN_Short": "VS Vintar", "UA_Short": "СГ «Гвинтар»",
    "RU_Full": "СВ «Винтарь»: Подгонка боевых упоров затвора", "EN_Full": "VS Vintar: Adjusted Bolt Locking Lugs", "UA_Full": "СГ «Гвинтар»: Припасування бойових упорів затвора",
    "RU_Desc": "Уменьшает утечку пороховых газов, увеличивая скорость пули.", "EN_Desc": "Reducing powder gas leakage leads to increased muzzle velocity.", "UA_Desc": "Зменшує витік порохових газів, підвищуючи швидкість кулі.",
    "RU_Warn": "Он находится на базе «Чистого Неба». Вход на базу будет недоступен раньше получения квеста «Через тернии к звёздам», до этого момента флешку получить нельзя.",
    "UA_Warn": "Він знаходиться на базі «Чистого Неба». Вхід на базу буде недоступний раніше отримання квесту «Крізь терни до зірок», до цього моменту флешку отримати не можна.",
    "EN_Warn": "Located at the Clear Sky Base. Access to the base is locked prior to receiving the quest 'Per Aspera Ad Astra'; the flash drive cannot be obtained before then.",
    "teleport_cmd": "XTeleportTo 791474.540296 771386.183028 238.401869", "map_url": "https://joric.github.io/stalker/#202244494AA5864C0803E08AE76F9F86"
  },
  {"id": "Blueprint_Grim_Upgrade_1", "type": "weapon", "RU_Short": "«Гром С-14»", "EN_Short": "Grom S-14", "UA_Short": "«Грім» С-14", "RU_Full": "«Гром С-14»: Каучуковый тыльник приклада", "EN_Full": "Grom S-14: Rubber Stock Rear", "UA_Full": "«Грім» С-14: Каучуковий тильник приклада", "RU_Desc": "Делает отдачу от выстрела значительно мягче.", "EN_Desc": "Effectively dampens recoil, providing a smoother shooting experience.", "UA_Desc": "Робить віддачу пострілу значно м'якшою.", "teleport_cmd": "XTeleportTo 542223.865608 359050.291472 446.646803", "map_url": "https://joric.github.io/stalker/#D348EBCF4D9A4F08BB0D23B313E28C1D"},
  {"id": "Blueprint_Lavina_Upgrade_1", "type": "weapon", "RU_Short": "СА «Лавина»", "EN_Short": "AS Lavina", "UA_Short": "СА «Лавина»", "RU_Full": "СА «Лавина»: Подгонка боевых упоров затвора", "EN_Full": "AS Lavina: Adjusted Bolt Locking Lugs", "UA_Full": "СА «Лавина»: Припасування бойових упорів затвора", "RU_Desc": "Уменьшает утечку пороховых газов, увеличивая скорость пули.", "EN_Desc": "Reducing powder gas leakage leads to increased muzzle velocity.", "UA_Desc": "Зменшує витік порохових газів, підвищуючи швидкість кулі.", "teleport_cmd": "XTeleportTo 336678.768043 584444.330903 900.496425", "map_url": "https://joric.github.io/stalker/#F1506A494724DE80C2FE038FB7374170"},
  {"id": "Blueprint_Lavina_Upgrade_2", "type": "weapon", "RU_Short": "СА «Лавина»", "EN_Short": "AS Lavina", "UA_Short": "СА «Лавина»", "RU_Full": "СА «Лавина»: Прорезиненный слой", "EN_Full": "AS Lavina: Rubber Layer", "UA_Full": "СА «Лавина»: Гумовий шар", "RU_Desc": "Частично гасит отдачу.", "EN_Desc": "Partially dampens recoil.", "UA_Desc": "Частково гасить віддачу.", "teleport_cmd": "XTeleportTo 253827.796239 462334.523247 1177.413838", "map_url": "https://joric.github.io/stalker/#8A9621A640A8CD0A4827E49AF3CE5F06"},
  {"id": "Blueprint_Kharod_Upgrade_1", "type": "weapon", "RU_Short": "Kharod", "EN_Short": "Kharod", "UA_Short": "Kharod", "RU_Full": "Kharod: Установка балансира", "EN_Full": "Kharod: Counterweight", "UA_Full": "Kharod: Встановлення балансира", "RU_Desc": "Балансир увеличивает стабильность оружия, снижая разброс.", "EN_Desc": "Counterweight enhances stability, reducing spread.", "UA_Desc": "Балансир збільшує стабільність зброї, зменшуючи розкид.", "teleport_cmd": "XTeleportTo 471793.8108 572758.432735 201.003234", "map_url": "https://joric.github.io/stalker/#E31FEB0046B50CFA7E31E3819325FE5F"},
  {"id": "Blueprint_Kharod_Upgrade_2", "type": "weapon", "RU_Short": "Kharod", "EN_Short": "Kharod", "UA_Short": "Kharod", "RU_Full": "Kharod: Прорезиненное покрытие", "EN_Full": "Kharod: Rubber Coating", "UA_Full": "Kharod: Гумове покриття", "RU_Desc": "Прорезиненная поверхность амортизирует отдачу и укрепляет хват.", "EN_Desc": "Rubberized surface dampens recoil and enhances grip.", "UA_Desc": "Гумова поверхня амортизує віддачу та зміцнює хват.", "teleport_cmd": "XTeleportTo 227091.922544 379005.810809 -28.200402", "map_url": "https://joric.github.io/stalker/#45725B8D4EC7EF61033FF6ABFA242C43"},
  {"id": "Blueprint_Dnipro_Upgrade_1", "type": "weapon", "RU_Short": "«Днипро»", "EN_Short": "Dnipro", "UA_Short": "«Дніпро»", "RU_Full": "«Днипро»: Дополнительный нарез в стволе", "EN_Full": "Dnipro: Extra Barrel Rifling", "UA_Full": "«Дніпро»: Додатковий наріз у стволі", "RU_Desc": "Снижает разрушение пули в стволе.", "EN_Desc": "Reduces bullet deterioration within the barrel.", "UA_Desc": "Зменшує руйнування кулі в стволі.", "teleport_cmd": "XTeleportTo 171227.557801 299667.824163 878.478752", "map_url": "https://joric.github.io/stalker/#A0B73D5B4B8FC09CB823D58318FD7154"},
  {"id": "Blueprint_Dnipro_Upgrade_2", "type": "weapon", "RU_Short": "«Днипро»", "EN_Short": "Dnipro", "UA_Short": "«Дніпро»", "RU_Full": "«Днипро»: Переделка под калибр 7.62", "EN_Full": "Dnipro: Caliber Conversion 7.62", "UA_Full": "«Дніпро»: Перероблення під калібр 7.62", "RU_Desc": "Замена ствола под новый мощный калибр 7.62.", "EN_Desc": "Replaces the barrel to accommodate the 7.62 caliber.", "UA_Desc": "Заміна ствола під новий калібр 7.62.", "teleport_cmd": "XTeleportTo 250620.034125 167902.77634 245.435965", "map_url": "https://joric.github.io/stalker/#A967B24D4326428E7B141994FF90A0B3"},
  {"id": "Blueprint_M701_Upgrade_1", "type": "weapon", "RU_Short": "M701 Super", "EN_Short": "M701 Super", "UA_Short": "M701 Super", "RU_Full": "M701 Super: Уплотнитель муфты возвратного механизма", "EN_Full": "M701 Super: Return Mechanism Sleeve Tightener", "UA_Full": "M701 Super: Ущільнювач муфти зворотного механізму", "RU_Desc": "Увеличивает давление в стволе, повышая скорость пули.", "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.", "UA_Desc": "Збільшує тиск у стволі, підвищуючи швидкість кулі.", "teleport_cmd": "XTeleportTo 193393.985448 644364.853802 822.171043", "map_url": "https://joric.github.io/stalker/#C8D423994ACEE1A20BF8ECA549DD1537"},
  {"id": "Blueprint_M701_Upgrade_2", "type": "weapon", "RU_Short": "M701 Super", "EN_Short": "M701 Super", "UA_Short": "M701 Super", "RU_Full": "M701 Super: Полимерная рукоятка", "EN_Full": "M701 Super: Polymer Handle", "UA_Full": "M701 Super: Полімерне руків'я", "RU_Desc": "Применение полимеров значительно снижает вес оружия.", "EN_Desc": "Polymers reduce overall weapon weight.", "UA_Desc": "Полімери значно знижують вагу зброї.", "teleport_cmd": "XTeleportTo 288885.087574 174460.644818 27.907521", "map_url": "https://joric.github.io/stalker/#F095D09A48FDB402BF104DBE3547C544"},
  {"id": "Blueprint_SVU_Upgrade_1", "type": "weapon", "RU_Short": "СВУ-МК С-3", "EN_Short": "SVU-MK S-3", "UA_Short": "СВУ-МК С-3", "RU_Full": "СВУ-МК С-3: Индивидуальная подгонка", "EN_Full": "SVU-MK S-3: Individual Adjustment", "UA_Full": "СВУ-МК С-3: Індивідуальне припасування", "RU_Desc": "Моделирование рукоятки под стрелка максимально повышает удобство.", "EN_Desc": "Customizing grip to match shooter's hand.", "UA_Desc": "Моделювання руків'я під стрільця підвищує зручність.", "teleport_cmd": "XTeleportTo 142882.770471 346168.860114 711.551835", "map_url": "https://joric.github.io/stalker/#C538F0094D6CD0FE7DF6ED80C8CA4489"},
  {"id": "Blueprint_SVU_Upgrade_2", "type": "weapon", "RU_Short": "СВУ-МК С-3", "EN_Short": "SVU-MK S-3", "UA_Short": "СВУ-МК С-3", "RU_Full": "СВУ-МК С-3: Прорезиненный слой", "EN_Full": "SVU-MK S-3: Rubber Layer", "UA_Full": "СВУ-МК С-3: Гумовий шар", "RU_Desc": "Частично гасит отдачу при стрельбе.", "EN_Desc": "Partially dampens recoil.", "UA_Desc": "Частково гасить віддачу під час стрільби.", "teleport_cmd": "XTeleportTo 263081.335047 189245.162572 385.436147", "map_url": "https://joric.github.io/stalker/#705CA46C459D171FB0ED2AB94C757D6D"},
  {"id": "Blueprint_M860_Upgrade_1", "type": "weapon", "RU_Short": "M860 Cracker", "EN_Short": "M860 Cracker", "UA_Short": "M860 Cracker", "RU_Full": "M860 Cracker: Магазинное питание", "EN_Full": "M860 Cracker: Magazine Feed", "UA_Full": "M860 Cracker: Магазинна подача", "RU_Desc": "Позволяет значительно быстрее перезаряжать дробовик.", "EN_Desc": "Allows for markedly faster reloading.", "UA_Desc": "Дає змогу значно швидше перезаряджати зброю.", "teleport_cmd": "XTeleportTo 300592.926209 484635.334838 1445.368942", "map_url": "https://joric.github.io/stalker/#F43F41734811F641B676EEA8F9D91BB7"},
  {"id": "Blueprint_D12_Upgrade_1", "type": "weapon", "RU_Short": "«Сайга Д-12»", "EN_Short": "Saiga D-12", "UA_Short": "«Сайга» Д-12", "RU_Full": "«Сайга Д-12»: Чок", "EN_Full": "Saiga D-12: Choke", "UA_Full": "«Сайга» Д-12: Чок", "RU_Desc": "Насадка на ствол. Уменьшает разлёт дроби.", "EN_Desc": "A barrel attachment designed to reduce spread.", "UA_Desc": "Насадка на ствол. Зменшує розкид дробу.", "teleport_cmd": "XTeleportTo 220432.573787 425700.480116 366.631657", "map_url": "https://joric.github.io/stalker/#9B54AC8D4EE96AEC918368A894CDF62F"},
  {"id": "Blueprint_D12_Upgrade_2", "type": "weapon", "RU_Short": "«Сайга Д-12»", "EN_Short": "Saiga D-12", "UA_Short": "«Сайга» Д-12", "RU_Full": "«Сайга Д-12»: Ребаланс приклада", "EN_Full": "Saiga D-12: Rebalanced Stock", "UA_Full": "«Сайга» Д-12: Ребаланс приклада", "RU_Desc": "Центр тяжести смещён вперёд для более быстрого прицеливания.", "EN_Desc": "Center of gravity shifted forward to facilitate quicker aiming.", "UA_Desc": "Центр ваги зміщений уперед для швидшого прицілювання.", "teleport_cmd": "XTeleportTo 250337.157676 154860.192597 100.000224", "map_url": "https://joric.github.io/stalker/#11A944244FC593510E44C5973455168A"},
  {"id": "Blueprint_Ram2_Upgrade_1", "type": "weapon", "RU_Short": "Ram-2", "EN_Short": "Ram-2", "UA_Short": "Ram-2", "RU_Full": "Ram-2: Уплотнитель муфты возвратного механизма", "EN_Full": "Ram-2: Return Mechanism Sleeve Tightener", "UA_Full": "Ram-2: Ущільнювач муфти зворотного механізму", "RU_Desc": "Увеличивает давление в стволе, повышая скорость пули.", "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.", "UA_Desc": "Збільшує тиск у стволі, підвищуючи швидкість кулі.", "teleport_cmd": "XTeleportTo 116971.001567 431348.798135 2616", "map_url": "https://joric.github.io/stalker/#464E8FB14AEEC7B154602AB22BEA1EBC"},
  {"id": "Blueprint_Ram2_Upgrade_2", "type": "weapon", "RU_Short": "Ram-2", "EN_Short": "Ram-2", "UA_Short": "Ram-2", "RU_Full": "Ram-2: Автоматический двухпозиционный газовый регулятор", "EN_Full": "Ram-2: Automatic Two-Stage Gas Regulator", "UA_Full": "Ram-2: Автоматичний двопозиційний газовый регулятор", "RU_Desc": "Механизм для значительного уменьшения загрязнённости оружия.", "EN_Desc": "A mechanism that reduces weapon fouling.", "UA_Desc": "Механізм для зменшення забруднення зброї.", "teleport_cmd": "XTeleportTo 238122.976198 157174.420213 621.009847", "map_url": "https://joric.github.io/stalker/#7D1E219B4D21A2DB94E7CCA214E6E143"},
  {"id": "Blueprint_MG_Upgrade_1", "type": "weapon", "RU_Short": "РПМ-74", "EN_Short": "RPM-74", "UA_Short": "РКМ-74", "RU_Full": "РПМ-74: Прорезиненное покрытие", "EN_Full": "RPM-74: Rubber Coating", "UA_Full": "РКМ-74: Гумове покриття", "RU_Desc": "Цепкая прорезиненная поверхность амортизирует отдачу пулемета.", "EN_Desc": "Rubberized surface dampens recoil and enhances grip.", "UA_Desc": "Гумова поверхня амортизує віддачу та зміцнює хват.", "teleport_cmd": "XTeleportTo 299004 366529.769907 1095.343278", "map_url": "https://joric.github.io/stalker/#FE40604641CA7604446AEB88904CC649"},
  {"id": "Blueprint_MG_Upgrade_2", "type": "weapon", "RU_Short": "РПМ-74", "EN_Short": "RPM-74", "UA_Short": "РКМ-74", "RU_Full": "РПМ-74: Каучуковый тыльник приклада", "EN_Full": "RPM-74: Rubber Stock Rear", "UA_Full": "РКМ-74: Каучуковий тильник приклада", "RU_Desc": "Делает отдачу от выстрела значительно мягче.", "EN_Desc": "Effectively dampens recoil, providing a smoother shooting experience.", "UA_Desc": "Робить віддачу пострілу значно м'якшою.", "teleport_cmd": "XTeleportTo 279031.030272 276195.948979 456.701442", "map_url": "https://joric.github.io/stalker/#E8F2346A4D52FB990278DDBC9A5C9D7A"},

  # --- БРОНЯ И ШЛЕМЫ (50 шт.) ---
  {"id": "Blueprint_Heavy2_Military_Armor_Upgrade_1", "type": "armor", "RU_Short": "«Берилл-5М»", "EN_Short": "Berill-5M", "UA_Short": "«Берил-5М»", "RU_Full": "Бронекостюм «Берилл-5М»: Питьевая система «Верблюд»", "EN_Full": "Berill-5M: Camel Hydration System", "UA_Full": "Бронекостюм «Берил-5М»: Система «Верблюд»", "RU_Desc": "Быстро восстановит водный баланс при длительных нагрузках.", "EN_Desc": "Ensures quick hydration during prolonged exertion.", "UA_Desc": "Швидко відновить водний баланс.", "teleport_cmd": "XTeleportTo 265963.427494 345327.579072 -246.116907", "map_url": "https://joric.github.io/stalker/#4ACB98FA4CF3BB010F3F349375DDC399"},
  {"id": "Blueprint_Heavy2_Military_Armor_Upgrade_2", "type": "armor", "RU_Short": "«Берилл-5М»", "EN_Short": "Berill-5M", "UA_Short": "«Берил-5М»", "RU_Full": "Бронекостюм «Берилл-5М»: Свинцовый контейнер", "EN_Full": "Berill-5M: Lead Container", "UA_Full": "Бронекостюм «Берил-5М»: Свинцевий контейнер", "RU_Desc": "Способ уберечь себя от радиационного излучения артефактов.", "EN_Desc": "Protected from the radiation emitted by artifacts.", "UA_Desc": "Захист від радіаційного випромінювання артефактів.", "teleport_cmd": "XTeleportTo 265549.57714 161209.304218 2808.968189", "map_url": "https://joric.github.io/stalker/#D83BE49E4084BE8326EE21BC968992E8"},
  {"id": "Blueprint_HeavyAnomaly_Scientific_Armor_Upgrade_1", "type": "armor", "RU_Short": "ССП-100", "EN_Short": "SSP-100", "UA_Short": "ССП-100", "RU_Full": "ССП-100 «Открытие»: Свинцовый контейнер", "EN_Full": "SSP-100: Lead Container", "UA_Full": "ССП-100 «Відкриття»: Свинцевий контейнер", "RU_Desc": "Защита от радиационного излучения артефактов.", "EN_Desc": "Protected from artifact radiation.", "UA_Desc": "Захист від радіації артефактів.", "teleport_cmd": "XTeleportTo 188185.344469 220116.346245 285.520178", "map_url": "https://joric.github.io/stalker/#ADAD30144343A959D1308EA8484DBC2A"},
  {"id": "Blueprint_HeavyAnomaly_Scientific_Armor_Upgrade_2", "type": "armor", "RU_Short": "ССП-100", "EN_Short": "SSP-100", "UA_Short": "ССП-100", "RU_Full": "ССП-100 «Открытие»: Арамидная подкладка", "EN_Full": "SSP-100: Aramid Lining", "UA_Full": "ССП-100 «Відкриття»: Арамідна підкладка", "RU_Desc": "Распределяет импульс от удара, останавливает осколки и пули.", "EN_Desc": "Disperses impact force, stopping shrapnel and bullets.", "UA_Desc": "Розподіляє імпульс від удару, зупиняє осколки та кулі.", "teleport_cmd": "XTeleportTo 278958.722232 199448.413508 384.595248", "map_url": "https://joric.github.io/stalker/#1EB51B454F44CB8E8EC86CBE2CBCFD17"},
  {"id": "Blueprint_Heavy_Svoboda_Armor_Upgrade_1", "type": "armor", "RU_Short": "ПСЗ-12В «Булат»", "EN_Short": "PSZ-12V Bulat", "UA_Short": "ПСЗ-12В «Булат»", "RU_Full": "ПСЗ-12В «Булат»: Свинцовый контейнер", "EN_Full": "PSZ-12V Bulat: Lead Container", "UA_Full": "ПСЗ-12В «Булат»: Свинцевий контейнер", "RU_Desc": "Свинцовый отсек под артефакты.", "EN_Desc": "Lead container for artifacts.", "UA_Desc": "Свинцевий відсік під артефакти.", "teleport_cmd": "XTeleportTo 337826.850911 444685.415198 652.802269", "map_url": "https://joric.github.io/stalker/#2FDAD8BA4B275ED25300E3A80191122E"},
  {"id": "Blueprint_Heavy_Svoboda_Armor_Upgrade_2", "type": "armor", "RU_Short": "ПСЗ-12В «Булат»", "EN_Short": "PSZ-12V Bulat", "UA_Short": "ПСЗ-12В «Булат»", "RU_Full": "ПСЗ-12В «Булат»: Питьевая система «Верблюд»", "EN_Full": "PSZ-12V Bulat: Camel Hydration System", "UA_Full": "ПСЗ-12В «Булат»: Система «Верблюд»", "RU_Desc": "Гидратор в рюкзак для выносливости.", "EN_Desc": "Hydrator in backpack for stamina.", "UA_Desc": "Гідратор у рюкзак для витривалості.", "teleport_cmd": "XTeleportTo 526969.44479 326897.107815 4169.575005", "map_url": "https://joric.github.io/stalker/#159079454CE67BF3A4DE8E84D2658E2B"},
  {"id": "Blueprint_Heavy_Dolg_Armor_Upgrade_1", "type": "armor", "RU_Short": "«Броня Долга»", "EN_Short": "Duty Armor", "UA_Short": "«Броня Долгу»", "RU_Full": "ПСЗ-9Д «Броня \"Долга\"»: Питьевая система «Верблюд»", "EN_Full": "PSZ-9D Duty Armor: Camel Hydration", "UA_Full": "ПСЗ-9Д «Броня \"Долгу\"»: Система «Верблюд»", "RU_Desc": "Гидратор быстро восстановит водный баланс.", "EN_Desc": "Quick hydration during long raids.", "UA_Desc": "Швидке відновлення сил у ході вилазок.", "teleport_cmd": "XTeleportTo 189437.221496 389348.111805 592.512881", "map_url": "https://joric.github.io/stalker/#09C24B874DB635E17354BDB04EFEF1AD"},
  {"id": "Blueprint_Heavy_Dolg_Armor_Upgrade_2", "type": "armor", "RU_Short": "«Броня Долга»", "EN_Short": "Duty Armor", "UA_Short": "«Броня Долгу»", "RU_Full": "ПСЗ-9Д «Броня \"Долга\"»: Арамидная подкладка", "EN_Full": "PSZ-9D Duty Armor: Aramid Lining", "UA_Full": "ПСЗ-9Д «Броня \"Долгу\"»: Арамідна підкладка", "RU_Desc": "Арамидная подкладка распределяет импульс от удара.", "EN_Desc": "Aramid lining disperses impact force.", "UA_Desc": "Арамідна підкладка зупиняє осколки.", "teleport_cmd": "XTeleportTo 191362.995846 665420.604118 874.674716", "map_url": "https://joric.github.io/stalker/#3EA329FA45F1ABA29E714BA9DC4A3CE3"},
  {"id": "Blueprint_HeavyBattle_Spark_Armor_Upgrade_1", "type": "armor", "RU_Short": "ПСЗ-9И «Сокол»", "EN_Short": "PSZ-9I Falcon", "UA_Short": "ПСЗ-9І «Сокіл»", "RU_Full": "ПСЗ-9И «Сокол»: Плексигласовый комбинезон со свинцовой сеткой", "EN_Full": "PSZ-9I Falcon: Plexiglas Suit with Lead Mesh", "UA_Full": "ПСЗ-9І «Сокіл»: Плексигласовий комбінезон", "RU_Desc": "Защищает от излучения и вредных веществ без потери подвижности.", "EN_Desc": "Protects against radiation without impeding mobility.", "UA_Desc": "Захищає від радіації та не сковує рухів.", "teleport_cmd": "XTeleportTo 94572.913765 491796.773937 1204.852445", "map_url": "https://joric.github.io/stalker/#A0D5E16D402FD5FDCE684795CAAA13FA"},
  {"id": "Blueprint_HeavyBattle_Spark_Armor_Upgrade_2", "type": "armor", "RU_Short": "ПСЗ-9И «Сокол»", "EN_Short": "PSZ-9I Falcon", "UA_Short": "ПСЗ-9І «Сокіл»", "RU_Full": "ПСЗ-9И «Сокол»: Свинцовый контейнер", "EN_Full": "PSZ-9I Falcon: Lead Container", "UA_Full": "ПСЗ-9І «Сокіл»: Свинцевий контейнер", "RU_Desc": "Защита от излучения артефактов.", "EN_Desc": "Lead container for radiation resistance.", "UA_Desc": "Захист від випромінювання артефактів.", "teleport_cmd": "XTeleportTo 182313.535537 323931.760897 2552.342677", "map_url": "https://joric.github.io/stalker/#1021AC464E8A74F689435091FF67609F"},
  {
    "id": "Blueprint_SEVA_Neutral_Armor_Upgrade_1", "type": "armor", "RU_Short": "«СЕВА»", "EN_Short": "SEVA Suit", "UA_Short": "«СЕВА»",
    "RU_Full": "Комбинезон «СЕВА»: Кольчужные вставки", "EN_Full": "SEVA Suit: Chainmail Inserts", "UA_Full": "Комбінезон «СЕВА»: Кольчужні вставки",
    "RU_Desc": "Кольчужное плетение спасает от ножевых и осколочных попаданий.", "EN_Desc": "Reinforced chainmail protective inserts.", "UA_Desc": "Кольчужні вставки рятують від порізів та осколків.",
    "RU_Warn": "Металлическая дверь в «Крытый склад» будет закрыта до начала сюжетного квеста «Поиски былой славы». До получения этого квеста флешку с чертежом получить нельзя.",
    "UA_Warn": "Металеві двері до «Критого складу» будуть зачинені до початку сюжетного квесту «Пошуки колишньої слави». До отримання цього квесту флешку з кресленням отримати не можна.",
    "EN_Warn": "The metal door to the 'Covered Warehouse' remains locked until starting the story quest 'In Search of Past Glory'. The flash drive cannot be obtained before this quest.",
    "teleport_cmd": "XTeleportTo 264735.752117 507333.286217 452.579329", "map_url": "https://joric.github.io/stalker/#2225A2914D5A514223BDDAB5EFB4CB19"
  },
  {"id": "Blueprint_SEVA_Neutral_Armor_Upgrade_2", "type": "armor", "RU_Short": "«СЕВА»", "EN_Short": "SEVA Suit", "UA_Short": "«СЕВА»", "RU_Full": "Комбинезон «СЕВА»: Экранирующее покрытие", "EN_Full": "SEVA Suit: Protective Coating", "UA_Full": "Комбінезон «СЕВА»: Екранувальне покриття", "RU_Desc": "Работает по принципу клетки Фарадея.", "EN_Desc": "Operates akin to a Faraday cage.", "UA_Desc": "Працює за принципом клітки Фарадея.", "teleport_cmd": "XTeleportTo 473610.087612 661142.140441 -1716.914603", "map_url": "https://joric.github.io/stalker/#1A0D31C743BF4E30832946A66FB9DAB8"},
  {"id": "Blueprint_SEVA_Svoboda_Armor_Upgrade_1", "type": "armor", "RU_Short": "«СЕВА-В»", "EN_Short": "SEVA-V", "UA_Short": "«СЕВА-В»", "RU_Full": "Комбинезон «СЕВА-В»: Экранирующее покрытие", "EN_Full": "SEVA-V Suit: Protective Coating", "UA_Full": "Комбінезон «СЕВА-В»: Екранувальне покриття", "RU_Desc": "Защитное экранирование от аномальных полей.", "EN_Desc": "Anomalous discharge shielding.", "UA_Desc": "Екранування від аномальних розрядів.", "teleport_cmd": "XTeleportTo 564518.359445 599451.038532 2175.49219", "map_url": "https://joric.github.io/stalker/#A73D798C49677A0370C0248C1FE1AD44"},
  {"id": "Blueprint_SEVA_Svoboda_Armor_Upgrade_2", "type": "armor", "RU_Short": "«СЕВА-В»", "EN_Short": "SEVA-V", "UA_Short": "«СЕВА-В»", "RU_Full": "Комбинезон «СЕВА-В»: Арамидная подкладка", "EN_Full": "SEVA-V Suit: Aramid Lining", "UA_Full": "Комбінезон «СЕВА-В»: Арамідна подкладка", "RU_Desc": "Повышает пулестойкость комбинезона.", "EN_Desc": "Increased ballistic resistance.", "UA_Desc": "Підвищує кульовий захист костюма.", "teleport_cmd": "XTeleportTo 733334.372147 749553.207578 96.037023", "map_url": "https://joric.github.io/stalker/#D988E3A54E2F6A1054D2C89E4E85EACE"},
  {"id": "Blueprint_SEVA_Spark_Armor_Upgrade_1", "type": "armor", "RU_Short": "«СЕВА-И»", "EN_Short": "SEVA-I", "UA_Short": "«СЕВА-І»", "RU_Full": "Комбинезон «СЕВА-И»: Накладные карманы", "EN_Full": "SEVA-I Suit: Sewn-on Pockets", "UA_Full": "Комбінезон «СЕВА-І»: Накладні кишені", "RU_Desc": "Дополнительные карманы на рукавах и штанах.", "EN_Desc": "Extra pockets on pants and sleeves.", "UA_Desc": "Додаткові кишені для спорядження.", "teleport_cmd": "XTeleportTo 199038 402663.329061 1120", "map_url": "https://joric.github.io/stalker/#E287E3924CD60A0310D9EEB1407C784B"},
  {"id": "Blueprint_SEVA_Spark_Armor_Upgrade_2", "type": "armor", "RU_Short": "«СЕВА-И»", "EN_Short": "SEVA-I", "UA_Short": "«СЕВА-І»", "RU_Full": "Комбинезон «СЕВА-И»: Свинцовый контейнер", "EN_Full": "SEVA-I Suit: Lead Container", "UA_Full": "Комбінезон «СЕВА-І»: Свинцевий контейнер", "RU_Desc": "Защита от радиационного фона артефактов.", "EN_Desc": "Protects against artifact radiation.", "UA_Desc": "Захист від випромінювання артефактів.", "teleport_cmd": "XTeleportTo 106980.534768 581899.527631 2757.893668", "map_url": "https://joric.github.io/stalker/#8EFA75F548409DF2E98329A3689E2CBE"},
  {"id": "Blueprint_SEVA_Dolg_Armor_Upgrade_1", "type": "armor", "RU_Short": "«СЕВА-Д»", "EN_Short": "SEVA-D", "UA_Short": "«СЕВА-Д»", "RU_Full": "Комбинезон «СЕВА-Д»: Питьевая система «Верблюд»", "EN_Full": "SEVA-D Suit: Camel Hydration", "UA_Full": "Комбінезон «СЕВА-Д»: Система «Верблюд»", "RU_Desc": "Встроенный в рюкзак гидратор.", "EN_Desc": "Integrated hydration system.", "UA_Desc": "Вбудований у рюкзак гідратор.", "teleport_cmd": "XTeleportTo 512228.632686 390665.471154 -910.397823", "map_url": "https://joric.github.io/stalker/#ADCF0C6748A56A60EC00F39FD0A88ED3"},
  {"id": "Blueprint_SEVA_Dolg_Armor_Upgrade_2", "type": "armor", "RU_Short": "«СЕВА-Д»", "EN_Short": "SEVA-D", "UA_Short": "«СЕВА-Д»", "RU_Full": "Комбинезон «СЕВА-Д»: Арамидная подкладка", "EN_Full": "SEVA-D Suit: Aramid Lining", "UA_Full": "Комбінезон «СЕВА-Д»: Арамідна подкладка", "RU_Desc": "Арамидный баллистический слой.", "EN_Desc": "Aramid ballistic layer.", "UA_Desc": "Арамідний шар від куль.", "teleport_cmd": "XTeleportTo 490223.64648 507859.053194 319.359764", "map_url": "https://joric.github.io/stalker/#5D6585714DBEF4C1749136AF8499F7E4"},
  {
    "id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_1", "type": "armor", "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»",
    "RU_Full": "Экзоскелет «Оператор»: Цельнотитановые составляющие", "EN_Full": "Operator: All-Titanium Components", "UA_Full": "Екзоскелет «Оператор»: Суцільнотитанові складники",
    "RU_Desc": "Сверхпрочный титановый экзокаркас.", "EN_Desc": "Titanium exoskeleton structure.", "UA_Desc": "Надміцний титановий каркас.",
    "RU_Warn": "Двери в «Лабораторию X15» будут закрыты до начала сюжетного квеста «Тонкая материя». Раньше получения квеста флешку с чертежом не получить.",
    "UA_Warn": "Двері до «Лабораторії X15» будуть зачинені до початку сюжетного квесту «Тонка матерія». Раніше отримання квесту флешку з кресленням не отримати.",
    "EN_Warn": "The doors to 'Laboratory X15' remain locked until starting the story quest 'Subtle Matter'. The flash drive cannot be obtained prior to this quest.",
    "teleport_cmd": "XTeleportTo 294030.396308 612656.781151 1014.992922", "map_url": "https://joric.github.io/stalker/#DFC954CB47D34D8634CA6597D0C00D0F"
  },
  {"id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_2", "type": "armor", "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»", "RU_Full": "Экзоскелет «Оператор»: Сервомоторы рук", "EN_Full": "Operator: Arm Servos", "UA_Full": "Екзоскелет «Оператор»: Сервомотори рук", "RU_Desc": "Стабилизируют удержание оружия в руках.", "EN_Desc": "Counteract inertia and stabilize weapon handling.", "UA_Desc": "Стабілізують положення зброї в руках.", "teleport_cmd": "XTeleportTo 63833.877176 459587.185551 3048.490956", "map_url": "https://joric.github.io/stalker/#28DE00F14537B51CBA3FBB8F32141267"},
  {"id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_3", "type": "armor", "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»", "RU_Full": "Экзоскелет «Оператор»: Свинцовый контейнер", "EN_Full": "Operator: Lead Container", "UA_Full": "Екзоскелет «Оператор»: Свинцевий контейнер", "RU_Desc": "Защита от излучения артефактов.", "EN_Desc": "Artifact radiation container.", "UA_Desc": "Захист від радіації артефактів.", "teleport_cmd": "XTeleportTo 268662.033353 156832.843927 30.999993", "map_url": "https://joric.github.io/stalker/#0B3C1AC54E81E76539977992E73A5EF6"},
  {"id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_4", "type": "armor", "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»", "RU_Full": "Экзоскелет «Оператор»: Доп. свинцовый контейнер", "EN_Full": "Operator: Lead Container #2", "UA_Full": "Екзоскелет «Оператор»: Дод. свинцевий контейнер", "RU_Desc": "Второй свинцовый контейнер.", "EN_Desc": "Second lead container.", "UA_Desc": "Другий свинцевий контейнер.", "teleport_cmd": "XTeleportTo 295625.434324 189338.233724 291.000016", "map_url": "https://joric.github.io/stalker/#1B214AEF4FE374D7239435BFDF09983F"},
  {"id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_1", "type": "armor", "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»", "RU_Full": "Экзоскелет «Брумбар»: Цельнотитановые составляющие", "EN_Full": "Brummbar: All-Titanium Components", "UA_Full": "Екзоскелет «Брумбар»: Суцільнотитанові складники", "RU_Desc": "Титановые элементы каркаса наемников.", "EN_Desc": "Titanium exoskeleton construction.", "UA_Desc": "Титанові елементи каркаса наємників.", "teleport_cmd": "XTeleportTo 268635.611048 264308.343203 989.8561", "map_url": "https://joric.github.io/stalker/#87DD088547E72190C6318D8BAA2A8AED"},
  {"id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_2", "type": "armor", "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»", "RU_Full": "Экзоскелет «Брумбар»: Система выведения ядовитых веществ", "EN_Full": "Brummbar: Poison Expulsion System", "UA_Full": "Екзоскелет «Брумбар»: Система виведення отрути", "RU_Desc": "Пневматическая очистка полостей респиратора.", "EN_Desc": "Pneumatic expulsion system for hazardous substances.", "UA_Desc": "Пневматичне очищення респіратора.", "teleport_cmd": "XTeleportTo 220574.917159 247487.999623 586.720357", "map_url": "https://joric.github.io/stalker/#776B7DA54560A6F5012E3E90A231C855"},
  {"id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_3", "type": "armor", "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»", "RU_Full": "Экзоскелет «Брумбар»: Оснащение сервоприводов гидравлическими усилителям", "EN_Full": "Brummbar: Hydraulic Servos (Sprint)", "UA_Full": "Екзоскелет «Брумбар»: Гідравлічні підсилювачі", "RU_Desc": "Позволяет переходить на бег в тяжелом экзоскелете.", "EN_Desc": "Hydraulic amplifiers that enable running.", "UA_Desc": "Гідравлічні підсилювачі для швидкого бігу.", "teleport_cmd": "XTeleportTo 275519.003432 144654.297935 447.087518", "map_url": "https://joric.github.io/stalker/#91054D1742F732C13F77269B85FCE8B0"},
  {"id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_4", "type": "armor", "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»", "RU_Full": "Экзоскелет «Брумбар»: Экранирующее покрытие", "EN_Full": "Brummbar: Protective Coating", "UA_Full": "Екзоскелет «Брумбар»: Екранувальне покриття", "RU_Desc": "Защитное экранирование сервоприводов.", "EN_Desc": "Protective shielding layer.", "UA_Desc": "Екранувальне покриття.", "teleport_cmd": "XTeleportTo 253179.758425 144787.567248 414.997434", "map_url": "https://joric.github.io/stalker/#3612452147E4E0C44DED9B84F755461F"},
  {"id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_1", "type": "armor", "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет", "RU_Full": "Экзоскелет: Система выведения ядовитых веществ", "EN_Full": "Exoskeleton: Poison Expulsion", "UA_Full": "Екзоскелет: Система виведення отрути", "RU_Desc": "Очистка респиратора от токсичных газов.", "EN_Desc": "Hazardous substance removal.", "UA_Desc": "Виведення небезпечних речовин.", "teleport_cmd": "XTeleportTo 455931.738492 680523.449508 -3343.771225", "map_url": "https://joric.github.io/stalker/#F55360FA473ED5225B0690958C656441"},
  {"id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_2", "type": "armor", "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет", "RU_Full": "Экзоскелет: Экранирующее покрытие", "EN_Full": "Exoskeleton: Protective Coating", "UA_Full": "Екзоскелет: Екранувальне покриття", "RU_Desc": "Экранирующий защитный слой.", "EN_Desc": "Faraday cage shielding.", "UA_Desc": "Екранувальне покриття.", "teleport_cmd": "XTeleportTo 263532.806655 542539.535022 223.632601", "map_url": "https://joric.github.io/stalker/#1033F0A94E6BDC49F9C89AB6D0431905"},
  {"id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_3", "type": "armor", "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет", "RU_Full": "Экзоскелет: Свинцовый контейнер", "EN_Full": "Exoskeleton: Lead Container", "UA_Full": "Екзоскелет: Свинцевий контейнер", "RU_Desc": "Свинцовый отсек для артефакта.", "EN_Desc": "Lead container for artifacts.", "UA_Desc": "Свинцевий контейнер для артефакту.", "teleport_cmd": "XTeleportTo 231825.807453 140417.054158 381.456424", "map_url": "https://joric.github.io/stalker/#2ECAF9D34744025FC1E9BA8358B7BC3B"},
  {"id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_4", "type": "armor", "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет", "RU_Full": "Экзоскелет: Дополнительный свинцовый контейнер", "EN_Full": "Exoskeleton: Lead Container #2", "UA_Full": "Екзоскелет: Дод. свинцевий контейнер", "RU_Desc": "Второй контейнер под артефакт.", "EN_Desc": "Second lead container.", "UA_Desc": "Другий свинцевий контейнер.", "teleport_cmd": "XTeleportTo 304491.171573 176947.89898 319", "map_url": "https://joric.github.io/stalker/#7A018E83491538019702E28FF562A81F"},
  {"id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_1", "type": "armor", "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»", "RU_Full": "Экзоскелет «Воля»: Цельнотитановые составляющие", "EN_Full": "Liberty Exoskeleton: Titanium Components", "UA_Full": "Екзоскелет «Воля»: Суцільнотитанові складники", "RU_Desc": "Легкий и прочный титановый каркас.", "EN_Desc": "Titanium exoskeleton construction.", "UA_Desc": "Титанові деталі конструкції.", "teleport_cmd": "XTeleportTo 279207.539293 184354.82284 625.763835", "map_url": "https://joric.github.io/stalker/#A99DC48C413277DF106C55A6CEA8F9CE"},
  {"id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_2", "type": "armor", "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»", "RU_Full": "Экзоскелет «Воля»: Система выведения ядовитых веществ", "EN_Full": "Liberty Exoskeleton: Poison Expulsion", "UA_Full": "Екзоскелет «Воля»: Система виведення отрути", "RU_Desc": "Пневматическая очистка респиратора.", "EN_Desc": "Respirator gas purge system.", "UA_Desc": "Очищення порожнин респіратора.", "teleport_cmd": "XTeleportTo 230052.80646 169996.994646 -68.626778", "map_url": "https://joric.github.io/stalker/#9558BABF4F4953634C33A387A8EC5E1E"},
  {"id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_3", "type": "armor", "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»", "RU_Full": "Экзоскелет «Воля»: Экранирующее покрытие", "EN_Full": "Liberty Exoskeleton: Protective Coating", "UA_Full": "Екзоскелет «Воля»: Екранувальне покриття", "RU_Desc": "Экранирующее защитное покрытие.", "EN_Desc": "Protective coating.", "UA_Desc": "Екранувальне покриття.", "teleport_cmd": "XTeleportTo 264945.925445 180705.229297 403.520772", "map_url": "https://joric.github.io/stalker/#C5148B904E3E4A92D9DFCF9B50A4E1E7"},
  {"id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_4", "type": "armor", "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»", "RU_Full": "Экзоскелет «Воля»: Доп. экранирующее покрытие", "EN_Full": "Liberty Exoskeleton: Extra Coating", "UA_Full": "Екзоскелет «Воля»: Дод. екранувальне покриття", "RU_Desc": "Второй слой экранирования.", "EN_Desc": "Second layer of protective coating.", "UA_Desc": "Другий шар екранування.", "teleport_cmd": "XTeleportTo 225491.458437 181592.245422 413.032971", "map_url": "https://joric.github.io/stalker/#825B8CE5425899CDB7549A943890CFD1"},
  {"id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_1", "type": "armor", "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»", "RU_Full": "Экзокостюм «Оплот»: Накладные карманы", "EN_Full": "Bulwark: Sewn-on Pockets", "UA_Full": "Екзокостюм «Оплот»: Накладні кишені", "RU_Desc": "Карманы на штанах и рукавах.", "EN_Desc": "Extra pockets on pants and sleeves.", "UA_Desc": "Додаткові кишені на рукавах.", "teleport_cmd": "XTeleportTo 248251.4317 132025.755218 534.833938", "map_url": "https://joric.github.io/stalker/#36D5B00E46AA8F291DB7EBBF6DBF9068"},
  {
    "id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_2", "type": "armor", "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»",
    "RU_Full": "Экзокостюм «Оплот»: Полиэтиленовая герметичная подкладка", "EN_Full": "Bulwark: Airtight Polyethylene Lining", "UA_Full": "Екзокостюм «Оплот»: Герметична підкладка",
    "RU_Desc": "Защита от ядовитых веществ и электрического тока.", "EN_Desc": "Airtight chemical and shock protection.", "UA_Desc": "Захист від токсинів та розрядів струму.",
    "RU_Warn": "Двери в «Кабельный коллектор» будут закрыты до начала сюжетного квеста «Жест милосердия». Раньше получения квеста флешку с чертежом не получить.",
    "UA_Warn": "Двері до «Кабельного колектора» будуть зачинені до початку сюжетного квесту «Жест милосердя». Раніше отримання квесту флешку з кресленням не отримати.",
    "EN_Warn": "The doors to the 'Cable Collector' remain locked until starting the story quest 'A Gesture of Mercy'. The flash drive cannot be obtained prior to this quest.",
    "teleport_cmd": "XTeleportTo 289722.943941 295516.298683 667.892073", "map_url": "https://joric.github.io/stalker/#DEE23B5842C92BEC5C62A9B7C1542242"
  },
  {"id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_3", "type": "armor", "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»", "RU_Full": "Экзокостюм «Оплот»: Активные фильтры", "EN_Full": "Bulwark: Active Filters", "UA_Full": "Екзокостюм «Оплот»: Активні фільтри", "RU_Desc": "Активные фильтры нейтрализуют радионуклиды.", "EN_Desc": "Active filters neutralize radionuclides.", "UA_Desc": "Активні фільтри нейтралізують радіонукліди.", "teleport_cmd": "XTeleportTo 254234.256671 155317.899642 3342.954194", "map_url": "https://joric.github.io/stalker/#B5F415A945245E975C51A181D099D8B1"},
  {"id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_4", "type": "armor", "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»", "RU_Full": "Экзокостюм «Оплот»: Свинцовый контейнер", "EN_Full": "Bulwark: Lead Container", "UA_Full": "Екзокостюм «Оплот»: Свинцевий контейнер", "RU_Desc": "Свинцовый отсек для артефакта.", "EN_Desc": "Lead container unit.", "UA_Desc": "Свинцевий контейнер.", "teleport_cmd": "XTeleportTo 288664.840419 161297.480689 390.596556", "map_url": "https://joric.github.io/stalker/#8AF83ADE437B04847E7A69A028B73577"},
  {"id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_1", "type": "armor", "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»", "RU_Full": "Экзоскелет «Панцирь»: Цельнотитановые составляющие", "EN_Full": "Cuirass: All-Titanium Components", "UA_Full": "Екзоскелет «Панцир»: Суцільнотитанові складники", "RU_Desc": "Усиленный титановый корпус Долга.", "EN_Desc": "Duty reinforced heavy titanium armor.", "UA_Desc": "Посилений титановий корпус Долгу.", "teleport_cmd": "XTeleportTo 192904.019747 575669.538755 972.162833", "map_url": "https://joric.github.io/stalker/#C8FF4FAA493FBEA86B7F54A0AF485ADC"},
  {"id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_2", "type": "armor", "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»", "RU_Full": "Экзоскелет «Панцирь»: Система выведения ядовитых веществ", "EN_Full": "Cuirass: Poison Expulsion System", "UA_Full": "Екзоскелет «Панцир»: Система виведення отрути", "RU_Desc": "Пневмосистема продувки респиратора.", "EN_Desc": "Hazardous gas expulsion.", "UA_Desc": "Очищення респіратора від газів.", "teleport_cmd": "XTeleportTo 221592.477201 589577.547569 1286.013323", "map_url": "https://joric.github.io/stalker/#6F3B78A440FA4379634827A94B63A4A0"},
  {"id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_3", "type": "armor", "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»", "RU_Full": "Экзоскелет «Панцирь»: Экранирующее покрытие", "EN_Full": "Cuirass: Protective Coating", "UA_Full": "Екзоскелет «Панцир»: Екранувальне покриття", "RU_Desc": "Защитное экранирование.", "EN_Desc": "Protective shielding.", "UA_Desc": "Захисне екранування.", "teleport_cmd": "XTeleportTo 280251.2722 162539.07598 1548.101954", "map_url": "https://joric.github.io/stalker/#B2C90F934AB1E5172FD3DDB5DB524F74"},
  {"id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_4", "type": "armor", "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»", "RU_Full": "Экзоскелет «Панцирь»: Свинцовый контейнер", "EN_Full": "Cuirass: Lead Container", "UA_Full": "Екзоскелет «Панцир»: Свинцевий контейнер", "RU_Desc": "Контейнер под радиационные арты.", "EN_Desc": "Lead container unit.", "UA_Desc": "Свинцевий контейнер.", "teleport_cmd": "XTeleportTo 281786.874011 196160.401915 861.519577", "map_url": "https://joric.github.io/stalker/#F967C371408C3D5D00E819B397E6234B"},
  {"id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_1", "type": "armor", "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»", "RU_Full": "Экзокостюм «Щит \"Долга\"»: Напыленный защитный слой", "EN_Full": "Shield of Duty: Sprayed Layer", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Напилений шар", "RU_Desc": "Повышает износостойкость без увеличения веса.", "EN_Desc": "Enhances durability without extra weight.", "UA_Desc": "Підвищує зносостійкість без збільшення ваги.", "teleport_cmd": "XTeleportTo 173701.120796 343466.208552 777.900961", "map_url": "https://joric.github.io/stalker/#BABD19F648417F1ACA026896FB62E568"},
  {"id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_2", "type": "armor", "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»", "RU_Full": "Экзокостюм «Щит \"Долга\"»: Увеличенный рюкзак", "EN_Full": "Shield of Duty: Expanded Backpack", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Збільшений рюкзак", "RU_Desc": "Дополнительная ниша для вещей на молнии.", "EN_Desc": "Expanded zippered backpack section.", "UA_Desc": "Додаткова ніша для речей на блискавці.", "teleport_cmd": "XTeleportTo 253237.893898 248674.42941 544.440989", "map_url": "https://joric.github.io/stalker/#4ED7E9B04AA21765098A6092275D27DA"},
  {"id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_3", "type": "armor", "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»", "RU_Full": "Экзокостюм «Щит \"Долга\"»: Экранирующее покрытие", "EN_Full": "Shield of Duty: Protective Coating", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Екранувальне покриття", "RU_Desc": "Защитное экранирование от аномалий.", "EN_Desc": "Protective shielding.", "UA_Desc": "Захисне екранування.", "teleport_cmd": "XTeleportTo 259287.319476 136344.666202 373.167733", "map_url": "https://joric.github.io/stalker/#B277FF074902A4E3F839C6B8CE7D46D3"},
  {"id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_4", "type": "armor", "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»", "RU_Full": "Экзокостюм «Щит \"Долга\"»: Свинцовый контейнер", "EN_Full": "Shield of Duty: Lead Container", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Свинцевий контейнер", "RU_Desc": "Свинцовый отсек под артефакт.", "EN_Desc": "Lead container unit.", "UA_Desc": "Свинцевий контейнер.", "teleport_cmd": "XTeleportTo 284244.991853 140250.882582 448.661072", "map_url": "https://joric.github.io/stalker/#D3C0DF90460AB8B177615C864F4B5E7E"},
  {"id": "Blueprint_Heavy_Duty_Helmet_Upgrade_1", "type": "armor", "RU_Short": "«Сфера-М20»", "EN_Short": "Sphere M20", "UA_Short": "«Сфера-М20»", "RU_Full": "Шлем «Сфера-М20»: Арамидная подкладка", "EN_Full": "Sphere M20: Aramid Lining", "UA_Full": "Шолом «Сфера-М20»: Арамідна підкладка", "RU_Desc": "Арамидная подкладка гасит импульс от ударов и пуль.", "EN_Desc": "Aramid lining disperses impact force.", "UA_Desc": "Арамідна підкладка зупиняє осколки.", "teleport_cmd": "XTeleportTo 396745.809836 469864.372106 1136.214677", "map_url": "https://joric.github.io/stalker/#B83225D1406F30EB34632BBF0515A6C4"},
  {"id": "Blueprint_Battle_Military_Helmet_Upgrade_1", "type": "armor", "RU_Short": "Баллистический шлем", "EN_Short": "Ballistic Helmet", "UA_Short": "Балістичний шолом", "RU_Full": "Баллистический шлем: Арамидная подкладка", "EN_Full": "Ballistic Helmet: Aramid Lining", "UA_Full": "Балістичний шолом: Арамідна підкладка", "RU_Desc": "Останавливает осколки и пули.", "EN_Desc": "Stops bullets and shrapnel.", "UA_Desc": "Зупиняє осколки та кулі.", "teleport_cmd": "XTeleportTo 242066.021474 512782.983368 100", "map_url": "https://joric.github.io/stalker/#15EAEDC34C1C7752CDE8A29188CCC7BA"},
  {"id": "Blueprint_Heavy_Svoboda_Helmet_Upgrade_1", "type": "armor", "RU_Short": "«Маска-1»", "EN_Short": "Mask-1 Helmet", "UA_Short": "«Маска-1»", "RU_Full": "Шлем «Маска-1»: Арамидная подкладка", "EN_Full": "Mask-1 Helmet: Aramid Lining", "UA_Full": "Шолом «Маска-1»: Арамідна підкладка", "RU_Desc": "Защита головы от осколков.", "EN_Desc": "Head protection against shrapnel.", "UA_Desc": "Захист голови від осколків.", "teleport_cmd": "XTeleportTo 261996.440624 413491.402897 775.903058", "map_url": "https://joric.github.io/stalker/#91DEEFFE4A9AD3ECD153FB8082E103FE"},
  {"id": "Blueprint_Heavy_Military_Helmet_Upgrade_1", "type": "armor", "RU_Short": "Тактический шлем", "EN_Short": "Tactical Helmet", "UA_Short": "Тактичний шолом", "RU_Full": "Тактический шлем: Плексигласовые накладки с экранирующим покрытием", "EN_Full": "Tactical Helmet: Plexiglas Overlays", "UA_Full": "Тактичний шолом: Плексигласові накладки", "RU_Desc": "Защищает не только от бета-, но и от пси-излучения.", "EN_Desc": "Shields against beta- and psi-radiation.", "UA_Desc": "Захищає від бета- й псі-випромінювання.", "teleport_cmd": "XTeleportTo 304591.148623 325688.061712 418.343824", "map_url": "https://joric.github.io/stalker/#3D6B45A24FD0071DE0CCC4B54C6F1690"}
]

SVG_CHECK_B64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0iIzAwRTY3NiIgZmlsbC1vcGFjaXR5PSIwLjIiIHN0cm9rZT0iIzAwRTY3NiIgc3Ryb2tlLXdpZHRoPSIyIi8+PHBhdGggZD0iTTggMTJMMTEgMTVMMTYgOSIgc3Ryb2tlPSIjMDBFNjc2IiBzdHJva2Utd2lkdGg9IjIuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9zdmc+"
SVG_CROSS_B64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0iIzFFMjYzOCIgZmlsbC1vcGFjaXR5PSIwLjgiIHN0cm9rZT0iIzMzNDE1NSIgc3Ryb2tlLXdpZHRoPSIxLjUiLz48cGF0aCBkPSJNOSA5TDE1IDE1TTE1IDlMOSAxNSIgc3Ryb2tlPSIjNjQ3NDhCIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvc3ZnPg=="

TEXTS = {
    "ru": {
        "header": "«Флешка-рояль» (77)",
        "desc_bar": "Найдено флешек",
        "cat_weapon": "Оружейные чертежи",
        "cat_armor": "Чертежи брони и экипировки",
        "copy_tip": "Кликните для подробностей",
        "summary_btn": "Скачать команды недостающих чертежей",
        "teleport": "Телепорт к чертежу:",
        "spawn": "Спавн в инвентарь:",
        "open_map_btn": "Открыть на интерактивной карте",
        "copy_btn": "Копировать",
        "copied": "Скопировано!",
        "found": "НАЙДЕНО",
        "missing": "НЕ НАЙДЕНО"
    },
    "uk": {
        "header": "«Флешка-рояль» (77)",
        "desc_bar": "Знайдено флешок",
        "cat_weapon": "Збройові креслення",
        "cat_armor": "Креслення броні та екіпірування",
        "copy_tip": "Клікніть для деталей",
        "summary_btn": "Завантажити команди відсутніх креслень",
        "teleport": "Телепорт до креслення:",
        "spawn": "Спавн в інвентар:",
        "open_map_btn": "Відкрити на інтерактивній карті",
        "copy_btn": "Копіювати",
        "copied": "Скопійовано!",
        "found": "ЗНАЙДЕНО",
        "missing": "НЕ ЗНАЙДЕНО"
    },
    "en": {
        "header": "\"Flash Royal\" (77)",
        "desc_bar": "Found Flash Drives",
        "cat_weapon": "Weapon Blueprints",
        "cat_armor": "Armor & Gear Blueprints",
        "copy_tip": "Click for details",
        "summary_btn": "Download missing blueprints commands",
        "teleport": "Teleport to blueprint:",
        "spawn": "Spawn into inventory:",
        "open_map_btn": "Open on Interactive Map",
        "copy_btn": "Copy",
        "copied": "Copied!",
        "found": "FOUND",
        "missing": "NOT FOUND"
    }
}

def find_blueprints(raw_bytes):
    found = set()
    if not raw_bytes:
        return found
    for bp in BLUEPRINTS_DATA:
        b_id = bp["id"]
        if b_id.encode("ascii") in raw_bytes or b_id.encode("utf-16le") in raw_bytes:
            found.add(b_id)
    return found

def render_blueprints_section(raw_bytes, lang="ru", art_filter="all"):
    if not raw_bytes:
        return

    txt = TEXTS.get(lang, TEXTS["ru"])
    lp = "RU" if lang == "ru" else ("UA" if lang == "uk" else "EN")
    
    found_bps = find_blueprints(raw_bytes)

    total_count = len(BLUEPRINTS_DATA)
    total_found = sum(1 for b in BLUEPRINTS_DATA if b["id"] in found_bps)
    total_pct = int(total_found / total_count * 100) if total_count > 0 else 0

    weapons = [b for b in BLUEPRINTS_DATA if b["type"] == "weapon"]
    armors = [b for b in BLUEPRINTS_DATA if b["type"] == "armor"]

    st.markdown(f"""
    <style>
    .bp-modal-overlay {{
        display: none;
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(4, 6, 10, 0.88);
        backdrop-filter: blur(6px);
        z-index: 99999999 !important;
        align-items: center;
        justify-content: center;
        padding: 16px;
        box-sizing: border-box;
    }}
    .bp-modal-box {{
        background: #0F131D;
        border: 1px solid #1E2638;
        border-radius: 14px;
        max-width: 620px;
        width: 100%;
        max-height: 90vh;
        overflow-y: auto;
        padding: 20px 22px;
        box-shadow: 0 16px 40px rgba(0,0,0,0.9);
        position: relative;
        color: #F8FAFC;
        box-sizing: border-box;
    }}
    .bp-modal-header {{
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 12px;
        border-bottom: 1px solid #1E2638;
        padding-bottom: 12px;
        margin-bottom: 14px;
    }}
    .bp-modal-title {{
        color: #FFB000;
        margin: 0;
        font-size: 1.15rem;
        font-weight: 700;
        line-height: 1.35;
        flex: 1;
    }}
    .bp-modal-actions {{
        display: flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
    }}
    .bp-modal-close-btn {{
        background: #182030;
        border: 1px solid #28334A;
        border-radius: 6px;
        width: 28px;
        height: 28px;
        color: #94A3B8;
        font-size: 1.2rem;
        line-height: 1;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.15s ease;
        padding: 0;
    }}
    .bp-modal-close-btn:hover {{
        background: #EF4444;
        border-color: #EF4444;
        color: #FFF;
    }}
    
    .bp-image-frame {{
        width: 100%;
        height: 310px;
        border-radius: 10px;
        overflow: hidden;
        border: 1px solid #1E2638;
        background: #080A0F;
        margin-bottom: 14px;
        position: relative;
    }}
    .bp-image-frame img {{
        width: 100% !important;
        height: 100% !important;
        object-fit: cover !important;
        object-position: center !important;
        transform: scale(1.05) !important;
        display: block !important;
    }}

    .tile-warn-badge {{
        position: absolute;
        top: 6px;
        left: 6px;
        z-index: 2;
        background: rgba(255, 176, 0, 0.18);
        border: 1px solid rgba(255, 176, 0, 0.5);
        border-radius: 6px;
        padding: 1px 4px;
        font-size: 0.72rem;
        line-height: 1.1;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 8px rgba(255, 176, 0, 0.15);
    }}

    .bp-copy-row {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        background: #080A0F;
        border: 1px solid #1E2638;
        border-radius: 6px;
        padding: 6px 10px;
        margin-top: 4px;
        cursor: pointer;
        transition: border-color 0.2s ease, background-color 0.2s ease;
    }}
    .bp-copy-row:hover {{
        border-color: #00E676;
        background: rgba(0, 230, 118, 0.04);
    }}
    .bp-copy-code {{
        color: #00E676;
        font-size: 0.76rem !important;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        white-space: nowrap;
        overflow-x: auto;
        scrollbar-width: none;
    }}
    .bp-copy-code::-webkit-scrollbar {{
        display: none;
    }}
    .bp-copy-btn {{
        font-size: 0.72rem;
        font-weight: 600;
        color: #94A3B8;
        background: #141A26;
        border: 1px solid #1E2638;
        padding: 3px 8px;
        border-radius: 4px;
        flex-shrink: 0;
        white-space: nowrap;
        user-select: none;
    }}
    .bp-copy-row:hover .bp-copy-btn {{
        color: #00E676;
        border-color: rgba(0, 230, 118, 0.4);
    }}
    
    .bp-map-link-btn {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        width: 100%;
        background: #121824;
        border: 1px solid #222E44;
        color: #38BDF8 !important;
        text-decoration: none !important;
        font-size: 0.8rem;
        font-weight: 600;
        padding: 8px 14px;
        border-radius: 6px;
        transition: all 0.2s ease;
        box-sizing: border-box;
        margin-top: 14px;
    }}
    .bp-map-link-btn:hover {{
        background: #1A2234;
        border-color: #38BDF8;
        color: #FFF !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.2);
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #1E2638; margin: 40px 0 25px 0;'>", unsafe_allow_html=True)

    # ОБЩИЙ ПРОГРЕСС-БАР («Флешка-рояль» с иконкой flesh_icon.png)
    st.markdown(f"""
    <div style="background-color: #111520; border: 1px solid #1E2638; border-radius: 12px; padding: 18px 22px; margin-bottom: 25px; display: flex; align-items: center; gap: 20px;">
        <img src="{HEADER_ICON_MAIN}" onerror="this.onerror=null; this.src='{HEADER_ICON_FALLBACK}';" style="width: 54px; height: 54px; object-fit: contain; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.5));" />
        <div style="flex-grow: 1;">
            <div style="display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 6px;">
                <span style="color: #F8FAFC; font-size: 1.25rem; font-weight: 700;">{txt['header']}</span>
                <span style="color: #00E676; font-size: 0.92rem; font-weight: 700; background: rgba(0, 230, 118, 0.12); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 6px; padding: 2px 10px;">{total_pct}%</span>
            </div>
            <div style="display: flex; justify-content: space-between; color: #94A3B8; font-size: 0.84rem; font-weight: 500; margin-bottom: 6px;">
                <span>{txt['desc_bar']}: <b style="color: #F8FAFC;">{total_found} / {total_count}</b></span>
            </div>
            <div style="width: 100%; background: #1E2638; border-radius: 8px; height: 7px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #FFB000, #00E676); width: {total_pct}%; height: 100%; border-radius: 8px; transition: width 0.5s ease;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    categories = [
        (txt['cat_weapon'], weapons),
        (txt['cat_armor'], armors)
    ]

    # СЕТКА КАРТОЧЕК ЧЕРТЕЖЕЙ
    for cat_name, items in categories:
        found_in_cat = sum(1 for item in items if item["id"] in found_bps)
        cat_title = f"{cat_name} [{found_in_cat}/{len(items)}]"

        filtered_items = []
        for item in items:
            is_f = item["id"] in found_bps
            if art_filter == "missing" and is_f:
                continue
            if art_filter == "found" and not is_f:
                continue
            filtered_items.append(item)

        if not filtered_items:
            continue

        with st.expander(cat_title, expanded=True):
            grid_html = '<div class="art-grid">\n'
            for bp in filtered_items:
                b_id = bp["id"]
                is_f = b_id in found_bps
                status_svg = f'<img src="{SVG_CHECK_B64}" width="18" height="18" />' if is_f else f'<img src="{SVG_CROSS_B64}" width="18" height="18" />'
                status_class = "tile-found" if is_f else "tile-missing"

                short_name = bp.get(f"{lp}_Short", bp["RU_Short"])
                full_name = bp.get(f"{lp}_Full", bp["RU_Full"])
                desc = bp.get(f"{lp}_Desc", bp["RU_Desc"])
                warn_note = bp.get(f"{lp}_Warn", "")

                icon_url = get_bp_icon_url(b_id)
                def_icon_url = get_def_icon_url(b_id)
                def_icon_fb = get_def_icon_fallback_url(b_id)

                map_url = get_map_url(b_id)
                scr_url = get_scr_url(b_id, 1)
                teleport_cmd = bp.get("teleport_cmd", "XTeleportTo 0 0 0")
                map_link = bp.get("map_url", "")
                spawn_cmd = f"XCreateItemInInventoryByID {b_id} 0 1 1"

                img_css_bg = f"background-image: url('{icon_url}'), url('{def_icon_url}'), url('{def_icon_fb}');"

                warn_badge_html = '<div class="tile-warn-badge">⚠️</div>' if warn_note else ''
                warn_tooltip_html = f'<div style="background: rgba(255, 176, 0, 0.1); border: 1px solid rgba(255, 176, 0, 0.35); border-radius: 5px; padding: 5px 8px; margin-bottom: 6px; color: #FFB000; font-size: 0.71rem; line-height: 1.3;">⚠️ {warn_note}</div>' if warn_note else ''

                payload_dict = {
                    "id": b_id,
                    "title": full_name,
                    "desc": desc,
                    "warn": warn_note,
                    "found": is_f,
                    "map": map_url,
                    "scr": scr_url,
                    "teleport": teleport_cmd,
                    "spawn": spawn_cmd,
                    "map_link": map_link
                }
                b64_payload = base64.b64encode(json.dumps(payload_dict).encode("utf-8")).decode("utf-8")

                grid_html += f'''
<div class="art-tile bp-clickable-tile {status_class}" data-bp-b64="{b64_payload}">
    <div class="tile-badge">{status_svg}</div>
    {warn_badge_html}
    <div class="tile-img-container">
        <div class="tile-img" style="{img_css_bg}"></div>
    </div>
    <div class="tile-label-container">
        <div class="tile-label" title="{short_name}">{short_name}</div>
    </div>
    <div class="tooltip-box">
        <div style="font-weight: 700; color: #FFB000; font-size: 0.82rem; margin-bottom: 6px; border-bottom: 1px solid rgba(255,176,0,0.25); padding-bottom: 3px;">
            {full_name}
        </div>
        <div style="width: 100%; height: 95px; border-radius: 6px; overflow: hidden; margin-bottom: 6px; background: #0A0D14; border: 1px solid #1E2638;">
            <img src="{map_url}" onerror="this.parentElement.style.display='none';" style="width: 100% !important; height: 100% !important; object-fit: cover !important; object-position: center !important; transform: scale(1.05) !important; display: block !important;" />
        </div>
        {warn_tooltip_html}
        <div style="color: #CBD5E1; font-size: 0.74rem; line-height: 1.35; margin-bottom: 6px;">
            {desc}
        </div>
        <div style="color: #64748B; font-size: 0.68rem; border-top: 1px solid #1E2638; padding-top: 4px; text-align: center;">
            <span>{txt['copy_tip']}</span>
        </div>
    </div>
</div>'''
            grid_html += '</div>\n'
            st.markdown(f"<div>{grid_html.replace(chr(10), '')}</div>", unsafe_allow_html=True)

    # Скачивание файла со списком недостающих чертежей
    missing_bps = [b for b in BLUEPRINTS_DATA if b["id"] not in found_bps]
    if missing_bps:
        txt_content = "=========================================================\n"
        txt_content += "      СПИСОК НЕДОСТАЮЩИХ ЧЕРТЕЖЕЙ S.T.A.L.K.E.R. 2\n"
        txt_content += f"      Недостает схем: {len(missing_bps)} из {total_count}\n"
        txt_content += "=========================================================\n\n"
        
        txt_content += "▶ Команды спавна недостающих чертежей в инвентарь:\n"
        txt_content += "|".join([f"XCreateItemInInventoryByID {b['id']} 0 1 1" for b in missing_bps]) + "\n\n"
        
        txt_content += "▶ Координаты телепорта к недостающим чертежам:\n"
        for b in missing_bps:
            name = b.get(f"{lp}_Full", b["RU_Full"])
            t_cmd = b.get("teleport_cmd", "XTeleportTo 0 0 0")
            warn = b.get(f"{lp}_Warn", "")
            warn_txt = f"    [!] Примечание: {warn}\n" if warn else ""
            txt_content += f"  • {name}:\n    {t_cmd}\n{warn_txt}"

        st.markdown("<br/>", unsafe_allow_html=True)
        st.download_button(
            label=txt['summary_btn'],
            data=txt_content,
            file_name="Missing_Blueprints.txt",
            mime="text/plain",
            key="dl_blueprints"
        )

    # JS: МОДАЛЬНОЕ ОКНО
    components.html(f"""
    <script>
    try {{
        const pDoc = window.parent.document;

        let modalEl = pDoc.getElementById('bp-dynamic-modal');
        if(!modalEl) {{
            modalEl = pDoc.createElement('div');
            modalEl.id = 'bp-dynamic-modal';
            modalEl.className = 'bp-modal-overlay';
            modalEl.innerHTML = `
                <div class="bp-modal-box">
                    <div id="bp-modal-content"></div>
                </div>
            `;
            pDoc.body.appendChild(modalEl);

            modalEl.addEventListener('click', function(e) {{
                if(e.target === modalEl) {{
                    modalEl.style.display = 'none';
                }}
            }});

            pDoc.addEventListener('keydown', function(e) {{
                if(e.key === 'Escape' && modalEl.style.display === 'flex') {{
                    modalEl.style.display = 'none';
                }}
            }});
        }}

        pDoc.addEventListener('click', function(e) {{
            let closeBtn = e.target.closest('.bp-modal-close-btn');
            if(closeBtn) {{
                modalEl.style.display = 'none';
                return;
            }}

            let tile = e.target.closest('.bp-clickable-tile');
            if(tile) {{
                let b64 = tile.getAttribute('data-bp-b64');
                if(b64) {{
                    let rawStr = decodeURIComponent(escape(atob(b64)));
                    let data = JSON.parse(rawStr);

                    let statusColor = data.found ? '#00E676' : '#EF4444';
                    let statusBg = data.found ? 'rgba(0, 230, 118, 0.12)' : 'rgba(239, 68, 68, 0.12)';
                    let statusBorder = data.found ? 'rgba(0, 230, 118, 0.3)' : 'rgba(239, 68, 68, 0.3)';
                    let statusText = data.found ? '{txt["found"]}' : '{txt["missing"]}';

                    let warnHtml = '';
                    if (data.warn) {{
                        warnHtml = `
                            <div style="background: rgba(255, 176, 0, 0.1); border-left: 3px solid #FFB000; border-radius: 6px; padding: 8px 12px; margin-bottom: 14px; color: #FFB000; font-size: 0.83rem; line-height: 1.42;">
                                ⚠️ <b>${{data.warn}}</b>
                            </div>
                        `;
                    }}

                    let mapBtnHtml = '';
                    if (data.map_link) {{
                        mapBtnHtml = `
                            <a href="${{data.map_link}}" target="_blank" rel="noopener noreferrer" class="bp-map-link-btn">
                                <span>{txt['open_map_btn']}</span> <span>↗</span>
                            </a>
                        `;
                    }}

                    let contentHtml = `
                        <div class="bp-modal-header">
                            <h3 class="bp-modal-title">${{data.title}}</h3>
                            <div class="bp-modal-actions">
                                <span style="color: ${{statusColor}}; background: ${{statusBg}}; border: 1px solid ${{statusBorder}}; border-radius: 6px; padding: 4px 8px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px;">${{statusText}}</span>
                                <button class="bp-modal-close-btn" title="Закрыть (Esc)">&times;</button>
                            </div>
                        </div>

                        <!-- КАРТИНКА БЕЗ ПОЛОС ПО БОКАМ -->
                        <div class="bp-image-frame">
                            <img src="${{data.map}}" onerror="this.onerror=null; this.src='${{data.scr}}'; this.onerror=function(){{this.parentElement.style.display='none';}};" />
                        </div>

                        <!-- СЮЖЕТНОЕ ПРЕДУПРЕЖДЕНИЕ -->
                        ${{warnHtml}}

                        <!-- ОПИСАНИЕ -->
                        <div style="background: #080A0F; border-left: 3px solid #FFB000; border-radius: 6px; padding: 10px 12px; margin-bottom: 14px; color: #CBD5E1; font-size: 0.86rem; line-height: 1.45;">
                            ${{data.desc}}
                        </div>

                        <!-- ТЕЛЕПОРТ -->
                        <div style="margin-bottom: 10px;">
                            <span style="color: #94A3B8; font-size: 0.78rem; font-weight: 600;">{txt['teleport']}</span>
                            <div class="bp-copy-row bp-btn-copy" data-copy="${{data.teleport}}">
                                <code class="bp-copy-code">${{data.teleport}}</code>
                                <span class="bp-copy-btn">{txt['copy_btn']}</span>
                            </div>
                        </div>

                        <!-- СПАВН -->
                        <div>
                            <span style="color: #94A3B8; font-size: 0.78rem; font-weight: 600;">{txt['spawn']}</span>
                            <div class="bp-copy-row bp-btn-copy" data-copy="${{data.spawn}}">
                                <code class="bp-copy-code">${{data.spawn}}</code>
                                <span class="bp-copy-btn">{txt['copy_btn']}</span>
                            </div>
                        </div>

                        <!-- КНОПКА ПЕРЕХОДА НА ИНТЕРАКТИВНУЮ КАРТУ -->
                        ${{mapBtnHtml}}
                    `;

                    pDoc.getElementById('bp-modal-content').innerHTML = contentHtml;
                    modalEl.style.display = 'flex';
                }}
            }}

            let copyBtn = e.target.closest('.bp-btn-copy');
            if(copyBtn) {{
                let text = copyBtn.getAttribute('data-copy');
                if(text) {{
                    pDoc.defaultView.navigator.clipboard.writeText(text).then(() => {{
                        let btn = copyBtn.querySelector('.bp-copy-btn');
                        if(btn) {{
                            let prev = btn.innerText;
                            btn.innerText = "{txt['copied']}";
                            btn.style.color = "#00E676";
                            setTimeout(() => {{ btn.innerText = prev; btn.style.color = ""; }}, 1400);
                        }}
                    }});
                }}
            }}
        }});
    }} catch(e) {{
        console.error(e);
    }}
    </script>
    """, height=0, width=0)
