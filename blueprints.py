import streamlit as st
import streamlit.components.v1 as components

# =========================================================================
# БАЗОВЫЕ URL ДЛЯ ЗАГРУЗКИ КАРТИНОК С GITHUB (icons/blueprint)
# =========================================================================
GITHUB_REPO_RAW = "https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/blueprint"
GITHUB_REPO_FALLBACK = "https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/master/icons/blueprint"

def get_icon_url(bp_id):
    return f"{GITHUB_REPO_RAW}/icon_{bp_id}.png"

def get_map_url(bp_id):
    return f"{GITHUB_REPO_RAW}/map_{bp_id}.png"

def get_scr_url(bp_id, index=1):
    if index == 1:
        return f"{GITHUB_REPO_RAW}/scr_{bp_id}.png"
    return f"{GITHUB_REPO_RAW}/scr_{bp_id}_{index}.png"

# =========================================================================
# БАЗА ДАННЫХ ЧЕРТЕЖЕЙ (34 шт.)
# scr_count: количество скриншотов (по умолчанию 1: scr_{id}.png)
# teleport_cmd: координаты телепорта
# =========================================================================
BLUEPRINTS_DATA = [
  # -------------------- ОРУЖИЕ (21 шт.) --------------------
  {
    "id": "Blueprint_M10_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "M10 Gordon", "EN_Short": "M10 Gordon", "UA_Short": "M10 Gordon",
    "RU_Upgrade": "Прорезиненный слой", "EN_Upgrade": "Rubber Layer", "UA_Upgrade": "Гумовий шар",
    "RU_Full": "M10 Gordon: Прорезиненный слой", "EN_Full": "M10 Gordon: Rubber Layer", "UA_Full": "M10 Gordon: Гумовий шар",
    "RU_Desc": "Частично гасит отдачу.", "EN_Desc": "Partially dampens recoil.", "UA_Desc": "Частково гасить віддачу.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Rhino_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "Rhino", "EN_Short": "Rhino", "UA_Short": "Rhino",
    "RU_Upgrade": "Переделка под дробь", "EN_Upgrade": "Buckshot Conversion", "UA_Upgrade": "Перероблення під дріб",
    "RU_Full": "Rhino: Переделка под дробь", "EN_Full": "Rhino: Buckshot Conversion", "UA_Full": "Rhino: Перероблення під дріб",
    "RU_Desc": "Подобную замену можно проделать только один раз, поскольку она связана с рассверливанием ствола и подгонкой деталей под новый тип боеприпаса.",
    "EN_Desc": "This modification can only be done once, since it involves boring out the barrel and adjusting parts to accommodate the new ammunition type.",
    "UA_Desc": "Подібну заміну можна зробити лише один раз, оскільки вона пов'язана з розсвердлюванням ствола та припасуванням деталей під новий тип боєприпасу.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_APB_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "АПБС", "EN_Short": "APSB", "UA_Short": "АПБС",
    "RU_Upgrade": "Установка балансира", "EN_Upgrade": "Counterweight", "UA_Upgrade": "Встановлення балансира",
    "RU_Full": "АПБС: Установка балансира", "EN_Full": "APSB: Counterweight", "UA_Full": "АПБС: Встановлення балансира",
    "RU_Desc": "Балансир увеличивает стабильность оружия, позволяя уменьшить разброс при стрельбе.",
    "EN_Desc": "The addition of the counterweight enhances stability, reducing spread when firing.",
    "UA_Desc": "Балансир збільшує стабільність зброї, що зменшує розкид під час стрільби.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_APB_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "АПБС", "EN_Short": "APSB", "UA_Short": "АПБС",
    "RU_Upgrade": "Индивидуальная подгонка", "EN_Upgrade": "Individual Adjustment", "UA_Upgrade": "Індивідуальне припасування",
    "RU_Full": "АПБС: Индивидуальная подгонка", "EN_Full": "APSB: Individual Adjustment", "UA_Full": "АПБС: Індивідуальне припасування",
    "RU_Desc": "Моделирование рукоятки под стрелка максимально повышает удобство обращения с оружием.",
    "EN_Desc": "Customizing the grip to match the shooter’s hand maximizes comfort when handling the weapon.",
    "UA_Desc": "Моделювання руків'я під стрільця максимально збільшує зручність користування зброєю.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Integral_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "Integral-A", "EN_Short": "Integral-A", "UA_Short": "Integral-A",
    "RU_Upgrade": "Уплотнитель возвр. муфты", "EN_Upgrade": "Return Mechanism Tightener", "UA_Upgrade": "Ущільнювач муфти",
    "RU_Full": "Integral-A: Уплотнитель муфты возвратного механизма", "EN_Full": "Integral-A: Return Mechanism Sleeve Tightener", "UA_Full": "Integral-A: Ущільнювач муфти зворотного механізму",
    "RU_Desc": "Увеличивает давление в стволе, повышая начальную скорость пули.",
    "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.",
    "UA_Desc": "Збільшує тиск у стволі, що підвищує початкову швидкість кулі.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Zubr_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "«Зубр-19»", "EN_Short": "Zubr-19", "UA_Short": "«Зубр-19»",
    "RU_Upgrade": "Доп. нарез ствола", "EN_Upgrade": "Extra Barrel Rifling", "UA_Upgrade": "Додатковий наріз",
    "RU_Full": "«Зубр-19»: Дополнительный нарез в стволе", "EN_Full": "Zubr-19: Extra Barrel Rifling", "UA_Full": "«Зубр-19»: Додатковий наріз у стволі",
    "RU_Desc": "Снижает разрушение пули в стволе, сохраняя её характеристики максимально близкими к расчётным.",
    "EN_Desc": "Reduces bullet deterioration within the barrel to preserve its intended design characteristics.",
    "UA_Desc": "Зменшує руйнування кулі в стволі, що зберігає її характеристики максимально близькими до розрахункових.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Zubr_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "«Зубр-19»", "EN_Short": "Zubr-19", "UA_Short": "«Зубр-19»",
    "RU_Upgrade": "Анатомич. подгонка", "EN_Upgrade": "Anatomical Adjustment", "UA_Upgrade": "Анатомічне припасування",
    "RU_Full": "«Зубр-19»: Анатомическая подгонка", "EN_Full": "Zubr-19: Anatomical Adjustment", "UA_Full": "«Зубр-19»: Анатомічне припасування",
    "RU_Desc": "Более удобная форма цевья повышает ускорение прицеливания.",
    "EN_Desc": "A more comfortable handguard shape contributes to increased aiming speed.",
    "UA_Desc": "Зручніша форма цівки прискорює прицілювання.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Gvintar_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "СВ «Винтарь»", "EN_Short": "VS Vintar", "UA_Short": "СГ «Гвинтар»",
    "RU_Upgrade": "Уплотнитель возвр. муфты", "EN_Upgrade": "Return Mechanism Tightener", "UA_Upgrade": "Ущільнювач муфти",
    "RU_Full": "СВ «Винтарь»: Уплотнитель муфты возвратного механизма", "EN_Full": "VS Vintar: Return Mechanism Sleeve Tightener", "UA_Full": "СГ «Гвинтар»: Ущільнювач муфти зворотного механізму",
    "RU_Desc": "Увеличивает давление в стволе, повышая начальную скорость пули.",
    "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.",
    "UA_Desc": "Збільшує тиск у стволі, що підвищує початкову швидкість кулі.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Gvintar_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "СВ «Винтарь»", "EN_Short": "VS Vintar", "UA_Short": "СГ «Гвинтар»",
    "RU_Upgrade": "Подгонка упоров затвора", "EN_Upgrade": "Adjusted Bolt Lugs", "UA_Upgrade": "Припасування упорів затвора",
    "RU_Full": "СВ «Винтарь»: Подгонка боевых упоров затвора", "EN_Full": "VS Vintar: Adjusted Bolt Locking Lugs", "UA_Full": "СГ «Гвинтар»: Припасування бойових упорів затвора",
    "RU_Desc": "Уменьшает утечку пороховых газов, увеличивая начальную скорость пули.",
    "EN_Desc": "Reducing powder gas leakage leads to increased muzzle velocity.",
    "UA_Desc": "Зменшує витік порохових газів, що підвищує початкову швидкість кулі.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Grim_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "«Гром С-14»", "EN_Short": "Grom S-14", "UA_Short": "«Грім» С-14",
    "RU_Upgrade": "Каучуковый тыльник", "EN_Upgrade": "Rubber Stock Rear", "UA_Upgrade": "Каучуковий тильник",
    "RU_Full": "«Гром С-14»: Каучуковый тыльник приклада", "EN_Full": "Grom S-14: Rubber Stock Rear", "UA_Full": "«Грім» С-14: Каучуковий тильник приклада",
    "RU_Desc": "Делает отдачу от выстрела значительно мягче.",
    "EN_Desc": "Effectively dampens recoil, providing a smoother shooting experience.",
    "UA_Desc": "Робить віддачу пострілу значно м'якшою.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Lavina_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "СА «Лавина»", "EN_Short": "AS Lavina", "UA_Short": "СА «Лавина»",
    "RU_Upgrade": "Подгонка упоров затвора", "EN_Upgrade": "Adjusted Bolt Lugs", "UA_Upgrade": "Припасування упорів затвора",
    "RU_Full": "СА «Лавина»: Подгонка боевых упоров затвора", "EN_Full": "AS Lavina: Adjusted Bolt Locking Lugs", "UA_Full": "СА «Лавина»: Припасування бойових упорів затвора",
    "RU_Desc": "Уменьшает утечку пороховых газов, увеличивая начальную скорость пули.",
    "EN_Desc": "Reducing powder gas leakage leads to increased muzzle velocity.",
    "UA_Desc": "Зменшує витік порохових газів, що підвищує початкову швидкість кулі.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Lavina_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "СА «Лавина»", "EN_Short": "AS Lavina", "UA_Short": "СА «Лавина»",
    "RU_Upgrade": "Прорезиненный слой", "EN_Upgrade": "Rubber Layer", "UA_Upgrade": "Гумовий шар",
    "RU_Full": "СА «Лавина»: Прорезиненный слой", "EN_Full": "AS Lavina: Rubber Layer", "UA_Full": "СА «Лавина»: Гумовий шар",
    "RU_Desc": "Частично гасит отдачу.", "EN_Desc": "Partially dampens recoil.", "UA_Desc": "Частково гасить віддачу.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Kharod_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "Kharod", "EN_Short": "Kharod", "UA_Short": "Kharod",
    "RU_Upgrade": "Установка балансира", "EN_Upgrade": "Counterweight", "UA_Upgrade": "Встановлення балансира",
    "RU_Full": "Kharod: Установка балансира", "EN_Full": "Kharod: Counterweight", "UA_Full": "Kharod: Встановлення балансира",
    "RU_Desc": "Балансир увеличивает стабильность оружия, позволяя уменьшить разброс при стрельбе.",
    "EN_Desc": "The addition of the counterweight enhances stability, reducing spread when firing.",
    "UA_Desc": "Балансир збільшує стабільність зброї, що зменшує розкид під час стрільби.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Kharod_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "Kharod", "EN_Short": "Kharod", "UA_Short": "Kharod",
    "RU_Upgrade": "Прорезиненное покрытие", "EN_Upgrade": "Rubber Coating", "UA_Upgrade": "Гумове покриття",
    "RU_Full": "Kharod: Прорезиненное покрытие", "EN_Full": "Kharod: Rubber Coating", "UA_Full": "Kharod: Гумове покриття",
    "RU_Desc": "Цепкая прорезиненная поверхность амортизирует отдачу и укрепляет хват оружия.",
    "EN_Desc": "The rubberized surface dampens the recoil and enhances the weapon’s grip.",
    "UA_Desc": "Цупка гумова поверхня амортизує віддачу та зміцнює хват зброї.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Dnipro_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "«Днипро»", "EN_Short": "Dnipro", "UA_Short": "«Дніпро»",
    "RU_Upgrade": "Доп. нарез ствола", "EN_Upgrade": "Extra Barrel Rifling", "UA_Upgrade": "Додатковий наріз",
    "RU_Full": "«Днипро»: Дополнительный нарез в стволе", "EN_Full": "Dnipro: Extra Barrel Rifling", "UA_Full": "«Дніпро»: Додатковий наріз у стволі",
    "RU_Desc": "Снижает разрушение пули в стволе, сохраняя её характеристики максимально близкими к расчётным.",
    "EN_Desc": "Reduces bullet deterioration within the barrel to preserve its intended design characteristics.",
    "UA_Desc": "Зменшує руйнування кулі в стволі, що зберігає її характеристики максимально близькими до розрахункових.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Dnipro_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "«Днипро»", "EN_Short": "Dnipro", "UA_Short": "«Дніпро»",
    "RU_Upgrade": "Калибр 7.62", "EN_Upgrade": "Caliber Conversion 7.62", "UA_Upgrade": "Калібр 7.62",
    "RU_Full": "«Днипро»: Переделка под калибр 7.62", "EN_Full": "Dnipro: Caliber Conversion 7.62", "UA_Full": "«Дніпро»: Перероблення під калібр 7.62",
    "RU_Desc": "Подобную замену можно проделать только один раз, поскольку она связана с заменой ствола под новый калибр.",
    "EN_Desc": "This modification can only be done once, since it involves replacing the barrel to accommodate the new caliber.",
    "UA_Desc": "Подібну заміну можна зробити лише один раз, оскільки вона пов'язана із заміною ствола під новий калібр.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_M701_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "M701 Super", "EN_Short": "M701 Super", "UA_Short": "M701 Super",
    "RU_Upgrade": "Уплотнитель возвр. муфты", "EN_Upgrade": "Return Mechanism Tightener", "UA_Upgrade": "Ущільнювач муфти",
    "RU_Full": "M701 Super: Уплотнитель муфты возвратного механизма", "EN_Full": "M701 Super: Return Mechanism Sleeve Tightener", "UA_Full": "M701 Super: Ущільнювач муфти зворотного механізму",
    "RU_Desc": "Увеличивает давление в стволе, повышая начальную скорость пули.",
    "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.",
    "UA_Desc": "Збільшує тиск у стволі, що підвищує початкову швидкість кулі.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_M701_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "M701 Super", "EN_Short": "M701 Super", "UA_Short": "M701 Super",
    "RU_Upgrade": "Полимерная рукоятка", "EN_Upgrade": "Polymer Handle", "UA_Upgrade": "Полімерне руків'я",
    "RU_Full": "M701 Super: Полимерная рукоятка", "EN_Full": "M701 Super: Polymer Handle", "UA_Full": "M701 Super: Полімерне руків'я",
    "RU_Desc": "Применение полимеров снижает вес. Чем легче оружие, тем легче им управлять.",
    "EN_Desc": "Incorporating polymers reduces the overall weight of the weapon, making it easier to use.",
    "UA_Desc": "Застосування полімерів знижує вагу. Чим легша зброя, тим легше з нею обходитися.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_SVU_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "СВУ-МК С-3", "EN_Short": "SVU-MK S-3", "UA_Short": "СВУ-МК С-3",
    "RU_Upgrade": "Индивидуальная подгонка", "EN_Upgrade": "Individual Adjustment", "UA_Upgrade": "Індивідуальне припасування",
    "RU_Full": "СВУ-МК С-3: Индивидуальная подгонка", "EN_Full": "SVU-MK S-3: Individual Adjustment", "UA_Full": "СВУ-МК С-3: Індивідуальне припасування",
    "RU_Desc": "Моделирование рукоятки под стрелка максимально повышает удобство обращения с оружием.",
    "EN_Desc": "Customizing the grip to match the shooter’s hand maximizes comfort when handling the weapon.",
    "UA_Desc": "Моделювання руків'я під стрільця максимально збільшує зручність користування зброєю.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_SVU_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "СВУ-МК С-3", "EN_Short": "SVU-MK S-3", "UA_Short": "СВУ-МК С-3",
    "RU_Upgrade": "Прорезиненный слой", "EN_Upgrade": "Rubber Layer", "UA_Upgrade": "Гумовий шар",
    "RU_Full": "СВУ-МК С-3: Прорезиненный слой", "EN_Full": "SVU-MK S-3: Rubber Layer", "UA_Full": "СВУ-МК С-3: Гумовий шар",
    "RU_Desc": "Частично гасит отдачу.", "EN_Desc": "Partially dampens recoil.", "UA_Desc": "Частково гасить віддачу.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_M860_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "M860 Cracker", "EN_Short": "M860 Cracker", "UA_Short": "M860 Cracker",
    "RU_Upgrade": "Магазинное питание", "EN_Upgrade": "Magazine Feed", "UA_Upgrade": "Магазинна подача",
    "RU_Full": "M860 Cracker: Магазинное питание", "EN_Full": "M860 Cracker: Magazine Feed", "UA_Full": "M860 Cracker: Магазинна подача",
    "RU_Desc": "Установка магазинного питания. Позволяет значительно быстрее перезаряжать оружие.",
    "EN_Desc": "The addition of a magazine feed allows for markedly faster reloading.",
    "UA_Desc": "Встановлення магазинної подачі боєприпасів. Дає змогу значно швидше перезаряджати зброю.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_D12_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "«Сайга Д-12»", "EN_Short": "Saiga D-12", "UA_Short": "«Сайга» Д-12",
    "RU_Upgrade": "Чок", "EN_Upgrade": "Choke", "UA_Upgrade": "Чок",
    "RU_Full": "«Сайга Д-12»: Чок", "EN_Full": "Saiga D-12: Choke", "UA_Full": "«Сайга» Д-12: Чок",
    "RU_Desc": "Насадка на ствол. Уменьшает разлёт, делая пучок дроби более смертоносным.",
    "EN_Desc": "A barrel attachment designed to reduce spread, improving the lethality of buckshot.",
    "UA_Desc": "Насадка на ствол. Зменшує розкид, роблячи пучок дробу більш смертоносним.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_D12_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "«Сайга Д-12»", "EN_Short": "Saiga D-12", "UA_Short": "«Сайга» Д-12",
    "RU_Upgrade": "Ребаланс приклада", "EN_Upgrade": "Rebalanced Stock", "UA_Upgrade": "Ребаланс приклада",
    "RU_Full": "«Сайга Д-12»: Ребаланс приклада", "EN_Full": "Saiga D-12: Rebalanced Stock", "UA_Full": "«Сайга» Д-12: Ребаланс приклада",
    "RU_Desc": "Центр тяжести приклада смещён вперёд для более быстрого прицеливания.",
    "EN_Desc": "The stock’s center of gravity is shifted forward to facilitate quicker, more efficient aiming.",
    "UA_Desc": "Центр ваги приклада зміщений уперед для швидшого прицілювання.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Ram2_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "Ram-2", "EN_Short": "Ram-2", "UA_Short": "Ram-2",
    "RU_Upgrade": "Уплотнитель возвр. муфты", "EN_Upgrade": "Return Mechanism Tightener", "UA_Upgrade": "Ущільнювач муфти",
    "RU_Full": "Ram-2: Уплотнитель муфты возвратного механизма", "EN_Full": "Ram-2: Return Mechanism Sleeve Tightener", "UA_Full": "Ram-2: Ущільнювач муфти зворотного механізму",
    "RU_Desc": "Увеличивает давление в стволе, повышая начальную скорость пули.",
    "EN_Desc": "Increases barrel pressure, resulting in increased muzzle velocity.",
    "UA_Desc": "Збільшує тиск у стволі, що підвищує початкову швидкість кулі.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Ram2_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "Ram-2", "EN_Short": "Ram-2", "UA_Short": "Ram-2",
    "RU_Upgrade": "Газовый регулятор", "EN_Upgrade": "Two-Stage Gas Regulator", "UA_Upgrade": "Газовий регулятор",
    "RU_Full": "Ram-2: Автоматический двухпозиционный газовый регулятор", "EN_Full": "Ram-2: Automatic Two-Stage Gas Regulator", "UA_Full": "Ram-2: Автоматичний двопозиційний газовий регулятор",
    "RU_Desc": "Установка механизма для уменьшения загрязнённости оружия.",
    "EN_Desc": "A mechanism that reduces weapon fouling.",
    "UA_Desc": "Встановлення механізму для зменшення забруднення зброї.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_MG_Upgrade_1", "type": "weapon", "scr_count": 1,
    "RU_Short": "РПМ-74", "EN_Short": "RPM-74", "UA_Short": "РКМ-74",
    "RU_Upgrade": "Прорезиненное покрытие", "EN_Upgrade": "Rubber Coating", "UA_Upgrade": "Гумове покриття",
    "RU_Full": "РПМ-74: Прорезиненное покрытие", "EN_Full": "RPM-74: Rubber Coating", "UA_Full": "РКМ-74: Гумове покриття",
    "RU_Desc": "Цепкая прорезиненная поверхность амортизирует отдачу и укрепляет хват оружия.",
    "EN_Desc": "The rubberized surface dampens the recoil and enhances the weapon’s grip.",
    "UA_Desc": "Цупка гумова поверхня амортизує віддачу та зміцнює хват зброї.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_MG_Upgrade_2", "type": "weapon", "scr_count": 1,
    "RU_Short": "РПМ-74", "EN_Short": "RPM-74", "UA_Short": "РКМ-74",
    "RU_Upgrade": "Каучуковый тыльник", "EN_Upgrade": "Rubber Stock Rear", "UA_Upgrade": "Каучуковий тильник",
    "RU_Full": "РПМ-74: Каучуковый тыльник приклада", "EN_Full": "RPM-74: Rubber Stock Rear", "UA_Full": "РКМ-74: Каучуковий тильник приклада",
    "RU_Desc": "Делает отдачу от выстрела значительно мягче.",
    "EN_Desc": "Effectively dampens recoil, providing a smoother shooting experience.",
    "UA_Desc": "Робить віддачу пострілу значно м'якшою.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },

  # -------------------- БРОНЯ И ШЛЕМЫ (13 шт.) --------------------
  {
    "id": "Blueprint_Heavy2_Military_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«Берилл-5М»", "EN_Short": "Berill-5M", "UA_Short": "«Берил-5М»",
    "RU_Upgrade": "Система «Верблюд»", "EN_Upgrade": "Camel Hydration", "UA_Upgrade": "Система «Верблюд»",
    "RU_Full": "Бронекостюм «Берилл-5М»: Питьевая система «Верблюд»", "EN_Full": "Berill-5M Armored Suit: Camel Hydration System", "UA_Full": "Бронекостюм «Берил-5М»: Система подачі води «Верблюд»",
    "RU_Desc": "Установка в рюкзак гидратора быстро восстановит водный баланс при длительных нагрузках.",
    "EN_Desc": "Incorporating a hydrator in the backpack ensures quick hydration during prolonged physical exertion.",
    "UA_Desc": "Встановлення гідратора в рюкзак швидко відновить водний баланс у разі тривалих навантажень.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Heavy2_Military_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«Берилл-5М»", "EN_Short": "Berill-5M", "UA_Short": "«Берил-5М»",
    "RU_Upgrade": "Свинцовый контейнер", "EN_Upgrade": "Lead Container", "UA_Upgrade": "Свинцевий контейнер",
    "RU_Full": "Бронекостюм «Берилл-5М»: Свинцовый контейнер", "EN_Full": "Berill-5M Armored Suit: Lead Container", "UA_Full": "Бронекостюм «Берил-5М»: Свинцевий контейнер",
    "RU_Desc": "Простой и эффективный способ уберечь себя от радиационного излучения артефактов.",
    "EN_Desc": "A simple and practical way to stay protected from the radiation emitted by artifacts.",
    "UA_Desc": "Простий і ефективний спосіб уберегти себе від радіаційного випромінювання артефактів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyAnomaly_Scientific_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "ССП-100 «Открытие»", "EN_Short": "SSP-100 Discovery", "UA_Short": "ССП-100 «Відкриття»",
    "RU_Upgrade": "Свинцовый контейнер", "EN_Upgrade": "Lead Container", "UA_Upgrade": "Свинцевий контейнер",
    "RU_Full": "ССП-100 «Открытие»: Свинцовый контейнер", "EN_Full": "SSP-100 Discovery: Lead Container", "UA_Full": "ССП-100 «Відкриття»: Свинцевий контейнер",
    "RU_Desc": "Простой и эффективный способ уберечь себя от радиационного излучения артефактов.",
    "EN_Desc": "A simple and practical way to stay protected from the radiation emitted by artifacts.",
    "UA_Desc": "Простий і ефективний спосіб уберегти себе від радіаційного випромінювання артефактів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyAnomaly_Scientific_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "ССП-100 «Открытие»", "EN_Short": "SSP-100 Discovery", "UA_Short": "ССП-100 «Відкриття»",
    "RU_Upgrade": "Арамидная подкладка", "EN_Upgrade": "Aramid Lining", "UA_Upgrade": "Арамідна підкладка",
    "RU_Full": "ССП-100 «Открытие»: Арамидная подкладка", "EN_Full": "SSP-100 Discovery: Aramid Lining", "UA_Full": "ССП-100 «Відкриття»: Арамідна підкладка",
    "RU_Desc": "Арамидная подкладка распределяет импульс от удара, останавливает осколки и пули.",
    "EN_Desc": "The aramid lining efficiently disperses impact force, stopping shrapnel and bullets.",
    "UA_Desc": "Арамідна підкладка розподіляє імпульс від удару, зупиняє осколки та кулі.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Heavy_Svoboda_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "ПСЗ-12В «Булат»", "EN_Short": "PSZ-12V Bulat", "UA_Short": "ПСЗ-12В «Булат»",
    "RU_Upgrade": "Свинцовый контейнер", "EN_Upgrade": "Lead Container", "UA_Upgrade": "Свинцевий контейнер",
    "RU_Full": "ПСЗ-12В «Булат»: Свинцовый контейнер", "EN_Full": "PSZ-12V Bulat: Lead Container", "UA_Full": "ПСЗ-12В «Булат»: Свинцевий контейнер",
    "RU_Desc": "Защита от радиационного излучения артефактов.",
    "EN_Desc": "A simple and practical way to stay protected from artifact radiation.",
    "UA_Desc": "Простий спосіб уберегти себе від радіаційного випромінювання артів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Heavy_Svoboda_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "ПСЗ-12В «Булат»", "EN_Short": "PSZ-12V Bulat", "UA_Short": "ПСЗ-12В «Булат»",
    "RU_Upgrade": "Система «Верблюд»", "EN_Upgrade": "Camel Hydration", "UA_Upgrade": "Система «Верблюд»",
    "RU_Full": "ПСЗ-12В «Булат»: Питьевая система «Верблюд»", "EN_Full": "PSZ-12V Bulat: Camel Hydration System", "UA_Full": "ПСЗ-12В «Булат»: Система подачі води «Верблюд»",
    "RU_Desc": "Установка гидратора для восстановления водного баланса при длительных вылазках.",
    "EN_Desc": "Hydrator setup to stay fresh and hydrated throughout long raids.",
    "UA_Desc": "Встановлення гідратора для швидкого відновлення сил під час ходок.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Heavy_Dolg_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«Броня Долга»", "EN_Short": "Duty Armor", "UA_Short": "«Броня Долгу»",
    "RU_Upgrade": "Система «Верблюд»", "EN_Upgrade": "Camel Hydration", "UA_Upgrade": "Система «Верблюд»",
    "RU_Full": "ПСЗ-9Д «Броня \"Долга\"»: Питьевая система «Верблюд»", "EN_Full": "PSZ-9D Duty Armor: Camel Hydration System", "UA_Full": "ПСЗ-9Д «Броня \"Долгу\"»: Система подачі води «Верблюд»",
    "RU_Desc": "Установка гидратора в рюкзак бойца.", "EN_Desc": "Duty specialized camel hydrator pack.", "UA_Desc": "Встановлення гідратора в рюкзак.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Heavy_Dolg_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«Броня Долга»", "EN_Short": "Duty Armor", "UA_Short": "«Броня Долгу»",
    "RU_Upgrade": "Арамидная подкладка", "EN_Upgrade": "Aramid Lining", "UA_Upgrade": "Арамідна підкладка",
    "RU_Full": "ПСЗ-9Д «Броня \"Долга\"»: Арамидная подкладка", "EN_Full": "PSZ-9D Duty Armor: Aramid Lining", "UA_Full": "ПСЗ-9Д «Броня \"Долгу\"»: Арамідна підкладка",
    "RU_Desc": "Эффективно гасит осколки и пули.", "EN_Desc": "Efficient bullet and shrapnel mitigation.", "UA_Desc": "Ефективно гасить осколки та кулі.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyBattle_Spark_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "ПСЗ-9И «Сокол»", "EN_Short": "PSZ-9I Falcon", "UA_Short": "ПСЗ-9І «Сокіл»",
    "RU_Upgrade": "Плексиглас + свинец", "EN_Upgrade": "Plexiglas + Lead Mesh", "UA_Upgrade": "Плексиглас + свинець",
    "RU_Full": "ПСЗ-9И «Сокол»: Плексигласовый комбинезон со свинцовой сеткой", "EN_Full": "PSZ-9I Falcon: Plexiglas Suit with Lead Mesh", "UA_Full": "ПСЗ-9І «Сокіл»: Плексигласовий комбінезон зі свинцевою сіткою",
    "RU_Desc": "Защищает от излучения без ограничения подвижности.", "EN_Desc": "Shields against radiation without impairing mobility.", "UA_Desc": "Захищає від радіації без сковування рухів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyBattle_Spark_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "ПСЗ-9И «Сокол»", "EN_Short": "PSZ-9I Falcon", "UA_Short": "ПСЗ-9І «Сокіл»",
    "RU_Upgrade": "Свинцовый контейнер", "EN_Upgrade": "Lead Container", "UA_Upgrade": "Свинцевий контейнер",
    "RU_Full": "ПСЗ-9И «Сокол»: Свинцовый контейнер", "EN_Full": "PSZ-9I Falcon: Lead Container", "UA_Full": "ПСЗ-9І «Сокіл»: Свинцевий контейнер",
    "RU_Desc": "Свинцовый отсек для переноски артефактов.", "EN_Desc": "Lead container for radiation resistance.", "UA_Desc": "Свинцевий контейнер для артефактів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_SEVA_Neutral_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«СЕВА»", "EN_Short": "SEVA Suit", "UA_Short": "«СЕВА»",
    "RU_Upgrade": "Кольчужные вставки", "EN_Upgrade": "Chainmail Inserts", "UA_Upgrade": "Кольчужні вставки",
    "RU_Full": "Комбинезон «СЕВА»: Кольчужные вставки", "EN_Full": "SEVA Suit: Chainmail Inserts", "UA_Full": "Комбінезон «СЕВА»: Кольчужні вставки",
    "RU_Desc": "Кольчужное плетение спасает от ножевых и осколочных попаданий.", "EN_Desc": "Reinforced chainmail protective inserts.", "UA_Desc": "Кольчужні вставки рятують від порізів та осколків.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_SEVA_Neutral_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«СЕВА»", "EN_Short": "SEVA Suit", "UA_Short": "«СЕВА»",
    "RU_Upgrade": "Экранирующее покрытие", "EN_Upgrade": "Protective Coating", "UA_Upgrade": "Екранувальне покриття",
    "RU_Full": "Комбинезон «СЕВА»: Экранирующее покрытие", "EN_Full": "SEVA Suit: Protective Coating", "UA_Full": "Комбінезон «СЕВА»: Екранувальне покриття",
    "RU_Desc": "Кратковременная защита по принципу клетки Фарадея.", "EN_Desc": "Electromagnetic shielding (Faraday cage).", "UA_Desc": "Короткочасний захист за принципом клітки Фарадея.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_SEVA_Svoboda_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«СЕВА-В»", "EN_Short": "SEVA-V", "UA_Short": "«СЕВА-В»",
    "RU_Upgrade": "Экранирующее покрытие", "EN_Upgrade": "Protective Coating", "UA_Upgrade": "Екранувальне покриття",
    "RU_Full": "Комбинезон «СЕВА-В»: Экранирующее покрытие", "EN_Full": "SEVA-V Suit: Protective Coating", "UA_Full": "Комбінезон «СЕВА-В»: Екранувальне покриття",
    "RU_Desc": "Экранирование от аномальных воздействий.", "EN_Desc": "Anomalous discharge shielding.", "UA_Desc": "Екранування від аномальних розрядів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_SEVA_Svoboda_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«СЕВА-В»", "EN_Short": "SEVA-V", "UA_Short": "«СЕВА-В»",
    "RU_Upgrade": "Арамидная подкладка", "EN_Upgrade": "Aramid Lining", "UA_Upgrade": "Арамідна підкладка",
    "RU_Full": "Комбинезон «СЕВА-В»: Арамидная подкладка", "EN_Full": "SEVA-V Suit: Aramid Lining", "UA_Full": "Комбінезон «СЕВА-В»: Арамідна підкладка",
    "RU_Desc": "Повышает пулестойкость комбинезона.", "EN_Desc": "Increased ballistic resistance.", "UA_Desc": "Підвищує кульовий захист костюма.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_SEVA_Spark_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«СЕВА-И»", "EN_Short": "SEVA-I", "UA_Short": "«СЕВА-І»",
    "RU_Upgrade": "Накладные карманы", "EN_Upgrade": "Sewn-on Pockets", "UA_Upgrade": "Накладні кишені",
    "RU_Full": "Комбинезон «СЕВА-И»: Накладные карманы", "EN_Full": "SEVA-I Suit: Sewn-on Pockets", "UA_Full": "Комбінезон «СЕВА-І»: Накладні кишені",
    "RU_Desc": "Дополнительные карманы на рукавах и штанах.", "EN_Desc": "Extra pockets on pants and sleeves.", "UA_Desc": "Додаткові кишені для спорядження.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_SEVA_Spark_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«СЕВА-И»", "EN_Short": "SEVA-I", "UA_Short": "«СЕВА-І»",
    "RU_Upgrade": "Свинцовый контейнер", "EN_Upgrade": "Lead Container", "UA_Upgrade": "Свинцевий контейнер",
    "RU_Full": "Комбинезон «СЕВА-И»: Свинцовый контейнер", "EN_Full": "SEVA-I Suit: Lead Container", "UA_Full": "Комбінезон «СЕВА-І»: Свинцевий контейнер",
    "RU_Desc": "Защита от радиационного фона артефактов.", "EN_Desc": "Protects against artifact radiation.", "UA_Desc": "Захист від випромінювання артефактів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_SEVA_Dolg_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«СЕВА-Д»", "EN_Short": "SEVA-D", "UA_Short": "«СЕВА-Д»",
    "RU_Upgrade": "Система «Верблюд»", "EN_Upgrade": "Camel Hydration", "UA_Upgrade": "Система «Верблюд»",
    "RU_Full": "Комбинезон «СЕВА-Д»: Питьевая система «Верблюд»", "EN_Full": "SEVA-D Suit: Camel Hydration System", "UA_Full": "Комбінезон «СЕВА-Д»: Система подачі води «Верблюд»",
    "RU_Desc": "Встроенный в рюкзак гидратор.", "EN_Desc": "Integrated hydration system.", "UA_Desc": "Вбудований у рюкзак гідратор.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_SEVA_Dolg_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«СЕВА-Д»", "EN_Short": "SEVA-D", "UA_Short": "«СЕВА-Д»",
    "RU_Upgrade": "Арамидная подкладка", "EN_Upgrade": "Aramid Lining", "UA_Upgrade": "Арамідна підкладка",
    "RU_Full": "Комбинезон «СЕВА-Д»: Арамидная подкладка", "EN_Full": "SEVA-D Suit: Aramid Lining", "UA_Full": "Комбінезон «СЕВА-Д»: Арамідна підкладка",
    "RU_Desc": "Арамидный баллистический слой.", "EN_Desc": "Aramid ballistic dispersion layer.", "UA_Desc": "Арамідний шар від куль.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»",
    "RU_Upgrade": "Титановые детали", "EN_Upgrade": "Titanium Parts", "UA_Upgrade": "Титанові деталі",
    "RU_Full": "Экзоскелет «Оператор»: Цельнотитановые составляющие", "EN_Full": "Operator Exoskeleton: All-Titanium Components", "UA_Full": "Екзоскелет «Оператор»: Суцільнотитанові складники",
    "RU_Desc": "Сверхпрочный титановый экзокаркас.", "EN_Desc": "Heavy-duty titanium exoskeleton frame.", "UA_Desc": "Надміцний титановий каркас.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»",
    "RU_Upgrade": "Сервомоторы рук", "EN_Upgrade": "Arm Servos", "UA_Upgrade": "Сервомотори рук",
    "RU_Full": "Экзоскелет «Оператор»: Сервомоторы рук", "EN_Full": "Operator Exoskeleton: Arm Servos", "UA_Full": "Екзоскелет «Оператор»: Сервомотори рук",
    "RU_Desc": "Стабилизируют удержание и ведение огня из тяжелого оружия.", "EN_Desc": "Stabilizes heavy weapon recoil and sway.", "UA_Desc": "Стабілізують зброю під час стрільби.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_3", "type": "armor", "scr_count": 1,
    "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»",
    "RU_Upgrade": "Свинцовый контейнер #1", "EN_Upgrade": "Lead Container #1", "UA_Upgrade": "Свинцевий контейнер #1",
    "RU_Full": "Экзоскелет «Оператор»: Свинцовый контейнер", "EN_Full": "Operator Exoskeleton: Lead Container", "UA_Full": "Екзоскелет «Оператор»: Свинцевий контейнер",
    "RU_Desc": "Защита от излучения артефактов.", "EN_Desc": "Artifact radiation containment unit.", "UA_Desc": "Захист від радіації артефактів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_BattleExoskeleton_Varta_Armor_Upgrade_4", "type": "armor", "scr_count": 1,
    "RU_Short": "«Оператор»", "EN_Short": "Operator", "UA_Short": "«Оператор»",
    "RU_Upgrade": "Свинцовый контейнер #2", "EN_Upgrade": "Lead Container #2", "UA_Upgrade": "Свинцевий контейнер #2",
    "RU_Full": "Экзоскелет «Оператор»: Доп. свинцовый контейнер", "EN_Full": "Operator Exoskeleton: Lead Container #2", "UA_Full": "Екзоскелет «Оператор»: Дод. свинцевий контейнер",
    "RU_Desc": "Второй свинцовый контейнер в конструкции экзоскелета.", "EN_Desc": "Secondary lead radiation container.", "UA_Desc": "Другий свинцевий контейнер.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»",
    "RU_Upgrade": "Титановые детали", "EN_Upgrade": "Titanium Parts", "UA_Upgrade": "Титанові деталі",
    "RU_Full": "Экзоскелет «Брумбар»: Цельнотитановые составляющие", "EN_Full": "Brummbar Exoskeleton: All-Titanium Components", "UA_Full": "Екзоскелет «Брумбар»: Суцільнотитанові складники",
    "RU_Desc": "Титановые элементы каркаса наемников.", "EN_Desc": "Mercenary titanium exoskeleton structure.", "UA_Desc": "Титанові елементи каркаса.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»",
    "RU_Upgrade": "Вывод ядовитых веществ", "EN_Upgrade": "Poison Gas Expulsion", "UA_Upgrade": "Виведення отрути",
    "RU_Full": "Экзоскелет «Брумбар»: Система выведения ядовитых веществ", "EN_Full": "Brummbar Exoskeleton: Elimination System for Poisonous Substances", "UA_Full": "Екзоскелет «Брумбар»: Система виведення отруєних речовин",
    "RU_Desc": "Пневматическая очистка полостей респиратора.", "EN_Desc": "Pneumatic hazardous substance flushing.", "UA_Desc": "Пневматичне очищення респіратора.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_3", "type": "armor", "scr_count": 1,
    "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»",
    "RU_Upgrade": "Гидроусилители (Бег)", "EN_Upgrade": "Hydraulic Servos (Run)", "UA_Upgrade": "Гідропідсилювачі (Біг)",
    "RU_Full": "Экзоскелет «Брумбар»: Оснащение сервоприводов гидравлическими усилителям", "EN_Full": "Brummbar Exoskeleton: Hydraulic Amplifiers for Servos", "UA_Full": "Екзоскелет «Брумбар»: Обладнання сервоприводів гідравлічним підсилювачем",
    "RU_Desc": "Позволяет бойцу совершать быстрый спринт в экзоскелете.", "EN_Desc": "Hydraulic tech that enables running/sprinting in full exoskeleton.", "UA_Desc": "Дає змогу швидко бігати в повному екзоскелеті.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Mercenaries_Armor_Upgrade_4", "type": "armor", "scr_count": 1,
    "RU_Short": "«Брумбар»", "EN_Short": "Brummbar", "UA_Short": "«Брумбар»",
    "RU_Upgrade": "Экранирующее покрытие", "EN_Upgrade": "Protective Coating", "UA_Upgrade": "Екранувальне покриття",
    "RU_Full": "Экзоскелет «Брумбар»: Экранирующее покрытие", "EN_Full": "Brummbar Exoskeleton: Protective Coating", "UA_Full": "Екзоскелет «Брумбар»: Екранувальне покриття",
    "RU_Desc": "Защитное экранирование сервоприводов и бойца.", "EN_Desc": "Shielded servo wiring and body protection.", "UA_Desc": "Екранування сервоприводів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет",
    "RU_Upgrade": "Вывод ядовитых веществ", "EN_Upgrade": "Poison Expulsion", "UA_Upgrade": "Виведення отрути",
    "RU_Full": "Экзоскелет: Система выведения ядовитых веществ", "EN_Full": "Exoskeleton: Elimination System for Poisonous Substances", "UA_Full": "Екзоскелет: Система виведення отруєних речовин",
    "RU_Desc": "Очистка респиратора от токсичных газов.", "EN_Desc": "Toxin flushing system.", "UA_Desc": "Очищення респіратора від токсичних газів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет",
    "RU_Upgrade": "Экранирующее покрытие", "EN_Upgrade": "Protective Coating", "UA_Upgrade": "Екранувальне покриття",
    "RU_Full": "Экзоскелет: Экранирующее покрытие", "EN_Full": "Exoskeleton: Protective Coating", "UA_Full": "Екзоскелет: Екранувальне покриття",
    "RU_Desc": "Экранирующий защитный слой.", "EN_Desc": "Protective radiation and electrical coating.", "UA_Desc": "Екранувальний захисний шар.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_3", "type": "armor", "scr_count": 1,
    "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет",
    "RU_Upgrade": "Свинцовый контейнер #1", "EN_Upgrade": "Lead Container #1", "UA_Upgrade": "Свинцевий контейнер #1",
    "RU_Full": "Экзоскелет: Свинцовый контейнер", "EN_Full": "Exoskeleton: Lead Container #1", "UA_Full": "Екзоскелет: Свинцевий контейнер #1",
    "RU_Desc": "Свинцовый контейнер под артефакт.", "EN_Desc": "Artifact lead container slot.", "UA_Desc": "Свинцевий контейнер.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Neutral_Armor_Upgrade_4", "type": "armor", "scr_count": 1,
    "RU_Short": "Экзоскелет", "EN_Short": "Exoskeleton", "UA_Short": "Екзоскелет",
    "RU_Upgrade": "Свинцовый контейнер #2", "EN_Upgrade": "Lead Container #2", "UA_Upgrade": "Свинцевий контейнер #2",
    "RU_Full": "Экзоскелет: Дополнительный свинцовый контейнер", "EN_Full": "Exoskeleton: Lead Container #2", "UA_Full": "Екзоскелет: Свинцевий контейнер #2",
    "RU_Desc": "Второй контейнер.", "EN_Desc": "Second lead container.", "UA_Desc": "Другий контейнер.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»",
    "RU_Upgrade": "Титановые детали", "EN_Upgrade": "Titanium Parts", "UA_Upgrade": "Титанові деталі",
    "RU_Full": "Экзоскелет «Воля»: Цельнотитановые составляющие", "EN_Full": "Liberty Exoskeleton: All-Titanium Components", "UA_Full": "Екзоскелет «Воля»: Суцільнотитанові складники",
    "RU_Desc": "Прочный титановый каркас свободы.", "EN_Desc": "Lightweight high-durability titanium frame.", "UA_Desc": "Міцний титановий каркас.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»",
    "RU_Upgrade": "Вывод ядовитых веществ", "EN_Upgrade": "Poison Expulsion", "UA_Upgrade": "Виведення отрути",
    "RU_Full": "Экзоскелет «Воля»: Система выведения ядовитых веществ", "EN_Full": "Liberty Exoskeleton: Elimination System for Poisonous Substances", "UA_Full": "Екзоскелет «Воля»: Система виведення отруєних речовин",
    "RU_Desc": "Очистка респиратора от токсинов.", "EN_Desc": "Toxin flushing.", "UA_Desc": "Очищення респіратора.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_3", "type": "armor", "scr_count": 1,
    "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»",
    "RU_Upgrade": "Экранирующее покрытие #1", "EN_Upgrade": "Protective Coating #1", "UA_Upgrade": "Екранувальне покриття #1",
    "RU_Full": "Экзоскелет «Воля»: Экранирующее покрытие", "EN_Full": "Liberty Exoskeleton: Protective Coating", "UA_Full": "Екзоскелет «Воля»: Екранувальне покриття",
    "RU_Desc": "Защитное экранирование.", "EN_Desc": "Protective shielding.", "UA_Desc": "Захисне екранування.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Svoboda_Armor_Upgrade_4", "type": "armor", "scr_count": 1,
    "RU_Short": "Экзо «Воля»", "EN_Short": "Liberty Exo", "UA_Short": "Екзо «Воля»",
    "RU_Upgrade": "Экранирующее покрытие #2", "EN_Upgrade": "Protective Coating #2", "UA_Upgrade": "Екранувальне покриття #2",
    "RU_Full": "Экзоскелет «Воля»: Доп. экранирующее покрытие", "EN_Full": "Liberty Exoskeleton: Extra Coating", "UA_Full": "Екзоскелет «Воля»: Дод. екранувальне покриття",
    "RU_Desc": "Второй слой экранирования.", "EN_Desc": "Second layer of protective coating.", "UA_Desc": "Другий шар екранування.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»",
    "RU_Upgrade": "Накладные карманы", "EN_Upgrade": "Sewn-on Pockets", "UA_Upgrade": "Накладні кишені",
    "RU_Full": "Экзокостюм «Оплот»: Накладные карманы", "EN_Full": "Bulwark Exosuit: Sewn-on Pockets", "UA_Full": "Екзокостюм «Оплот»: Накладні кишені",
    "RU_Desc": "Карманы на штанах и рукавах экзокостюма.", "EN_Desc": "Extra capacity pockets.", "UA_Desc": "Додаткові кишені для спорядження.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»",
    "RU_Upgrade": "Герметичная подкладка", "EN_Upgrade": "Airtight Lining", "UA_Upgrade": "Герметична підкладка",
    "RU_Full": "Экзокостюм «Оплот»: Полиэтиленовая герметичная подкладка", "EN_Full": "Bulwark Exosuit: Airtight Polyethylene Lining", "UA_Full": "Екзокостюм «Оплот»: Поліетиленова герметична підкладка",
    "RU_Desc": "Защищает от ядовитых веществ и электрических разрядов.", "EN_Desc": "Airtight chemical and electrical hazard lining.", "UA_Desc": "Захист від токсинів та розрядів струму.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_3", "type": "armor", "scr_count": 1,
    "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»",
    "RU_Upgrade": "Активные фильтры", "EN_Upgrade": "Active Filters", "UA_Upgrade": "Активні фільтри",
    "RU_Full": "Экзокостюм «Оплот»: Активные фильтры", "EN_Full": "Bulwark Exosuit: Active Filters", "UA_Full": "Екзокостюм «Оплот»: Активні фільтри",
    "RU_Desc": "Фильтры оперативно нейтрализуют радионуклиды.", "EN_Desc": "Radionuclide filtration system.", "UA_Desc": "Нейтралізація радіонуклідів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyExoskeleton_Svoboda_Armor_Upgrade_4", "type": "armor", "scr_count": 1,
    "RU_Short": "«Оплот»", "EN_Short": "Bulwark", "UA_Short": "«Оплот»",
    "RU_Upgrade": "Свинцовый контейнер", "EN_Upgrade": "Lead Container", "UA_Upgrade": "Свинцевий контейнер",
    "RU_Full": "Экзокостюм «Оплот»: Свинцовый контейнер", "EN_Full": "Bulwark Exosuit: Lead Container", "UA_Full": "Екзокостюм «Оплот»: Свинцевий контейнер",
    "RU_Desc": "Свинцовый отсек для артефакта.", "EN_Desc": "Lead container unit.", "UA_Desc": "Свинцевий контейнер.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»",
    "RU_Upgrade": "Титановые детали", "EN_Upgrade": "Titanium Parts", "UA_Upgrade": "Титанові деталі",
    "RU_Full": "Экзоскелет «Панцирь»: Цельнотитановые составляющие", "EN_Full": "Cuirass Exoskeleton: All-Titanium Components", "UA_Full": "Екзоскелет «Панцир»: Суцільнотитанові складники",
    "RU_Desc": "Усиленный титановый корпус Долга.", "EN_Desc": "Duty reinforced heavy titanium armor plates.", "UA_Desc": "Посилений титановий корпус Долгу.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»",
    "RU_Upgrade": "Вывод ядовитых веществ", "EN_Upgrade": "Poison Expulsion", "UA_Upgrade": "Виведення отрути",
    "RU_Full": "Экзоскелет «Панцирь»: Система выведения ядовитых веществ", "EN_Full": "Cuirass Exoskeleton: Elimination System for Poisonous Substances", "UA_Full": "Екзоскелет «Панцир»: Система виведення отруєних речовин",
    "RU_Desc": "Пневмосистема продувки респиратора.", "EN_Desc": "Respirator gas purge system.", "UA_Desc": "Пневмосистема очищення респіратора.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_3", "type": "armor", "scr_count": 1,
    "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»",
    "RU_Upgrade": "Экранирующее покрытие", "EN_Upgrade": "Protective Coating", "UA_Upgrade": "Екранувальне покриття",
    "RU_Full": "Экзоскелет «Панцирь»: Экранирующее покрытие", "EN_Full": "Cuirass Exoskeleton: Protective Coating", "UA_Full": "Екзоскелет «Панцир»: Екранувальне покриття",
    "RU_Desc": "Экранирование от аномалий.", "EN_Desc": "Protective shielding.", "UA_Desc": "Захисне екранування.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Exoskeleton_Dolg_Armor_Upgrade_4", "type": "armor", "scr_count": 1,
    "RU_Short": "«Панцирь»", "EN_Short": "Cuirass", "UA_Short": "«Панцир»",
    "RU_Upgrade": "Свинцовый контейнер", "EN_Upgrade": "Lead Container", "UA_Upgrade": "Свинцевий контейнер",
    "RU_Full": "Экзоскелет «Панцирь»: Свинцовый контейнер", "EN_Full": "Cuirass Exoskeleton: Lead Container", "UA_Full": "Екзоскелет «Панцир»: Свинцевий контейнер",
    "RU_Desc": "Контейнер под радиационные арты.", "EN_Desc": "Lead container unit.", "UA_Desc": "Контейнер для артефактів.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»",
    "RU_Upgrade": "Напыленный защитный слой", "EN_Upgrade": "Sprayed Layer", "UA_Upgrade": "Напилений шар",
    "RU_Full": "Экзокостюм «Щит \"Долга\"»: Напыленный защитный слой", "EN_Full": "Shield of Duty Exosuit: Sprayed Protective Layer", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Напилений захисний шар",
    "RU_Desc": "Повышает прочность и износостойкость без утяжеления.", "EN_Desc": "Enhances durability without extra weight.", "UA_Desc": "Підвищує зносостійкість без збільшення ваги.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_2", "type": "armor", "scr_count": 1,
    "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»",
    "RU_Upgrade": "Увеличенный рюкзак", "EN_Upgrade": "Expanded Backpack", "UA_Upgrade": "Збільшений рюкзак",
    "RU_Full": "Экзокостюм «Щит \"Долга\"»: Увеличенный рюкзак", "EN_Full": "Shield of Duty Exosuit: Expanded Backpack", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Збільшений рюкзак",
    "RU_Desc": "Вшитая дополнительная ниша для вещей на молнии.", "EN_Desc": "Expanded zippered backpack section.", "UA_Desc": "Додаткова ніша для речей на блискавці.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_3", "type": "armor", "scr_count": 1,
    "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»",
    "RU_Upgrade": "Экранирующее покрытие", "EN_Upgrade": "Protective Coating", "UA_Upgrade": "Екранувальне покриття",
    "RU_Full": "Экзокостюм «Щит \"Долга\"»: Экранирующее покрытие", "EN_Full": "Shield of Duty Exosuit: Protective Coating", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Екранувальне покриття",
    "RU_Desc": "Защитное экранирование.", "EN_Desc": "Protective coating against anomalies.", "UA_Desc": "Екранувальне покриття.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_HeavyExoskeleton_Dolg_Armor_Upgrade_4", "type": "armor", "scr_count": 1,
    "RU_Short": "«Щит Долга»", "EN_Short": "Shield of Duty", "UA_Short": "«Щит Долгу»",
    "RU_Upgrade": "Свинцовый контейнер", "EN_Upgrade": "Lead Container", "UA_Upgrade": "Свинцевий контейнер",
    "RU_Full": "Экзокостюм «Щит \"Долга\"»: Свинцовый контейнер", "EN_Full": "Shield of Duty Exosuit: Lead Container", "UA_Full": "Екзокостюм «Щит \"Долгу\"»: Свинцевий контейнер",
    "RU_Desc": "Свинцовый отсек под артефакт.", "EN_Desc": "Lead container unit.", "UA_Desc": "Свинцевий контейнер.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Heavy_Duty_Helmet_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«Сфера-М20»", "EN_Short": "Sphere M20", "UA_Short": "«Сфера-М20»",
    "RU_Upgrade": "Арамидная подкладка", "EN_Upgrade": "Aramid Lining", "UA_Upgrade": "Арамідна підкладка",
    "RU_Full": "Шлем «Сфера-М20»: Арамидная подкладка", "EN_Full": "Sphere M20 Helmet: Aramid Lining", "UA_Full": "Шолом «Сфера-М20»: Арамідна підкладка",
    "RU_Desc": "Арамидная подкладка гасит импульс от ударов и пуль.", "EN_Desc": "Aramid lining disperses impact force.", "UA_Desc": "Арамідна підкладка гасить удари та осколки.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Battle_Military_Helmet_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "Баллистический шлем", "EN_Short": "Ballistic Helmet", "UA_Short": "Балістичний шолом",
    "RU_Upgrade": "Арамидная подкладка", "EN_Upgrade": "Aramid Lining", "UA_Upgrade": "Арамідна підкладка",
    "RU_Full": "Баллистический шлем: Арамидная подкладка", "EN_Full": "Ballistic Helmet: Aramid Lining", "UA_Full": "Балістичний шолом: Арамідна підкладка",
    "RU_Desc": "Останавливает осколки и пули.", "EN_Desc": "Stops bullets and shrapnel.", "UA_Desc": "Зупиняє осколки та кулі.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Heavy_Svoboda_Helmet_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "«Маска-1»", "EN_Short": "Mask-1 Helmet", "UA_Short": "«Маска-1»",
    "RU_Upgrade": "Арамидная подкладка", "EN_Upgrade": "Aramid Lining", "UA_Upgrade": "Арамідна підкладка",
    "RU_Full": "Шлем «Маска-1»: Арамидная подкладка", "EN_Full": "Mask-1 Helmet: Aramid Lining", "UA_Full": "Шолом «Маска-1»: Арамідна підкладка",
    "RU_Desc": "Защита головы от осколков.", "EN_Desc": "Head shrapnel protection.", "UA_Desc": "Захист голови від осколків.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  },
  {
    "id": "Blueprint_Heavy_Military_Helmet_Upgrade_1", "type": "armor", "scr_count": 1,
    "RU_Short": "Тактический шлем", "EN_Short": "Tactical Helmet", "UA_Short": "Тактичний шолом",
    "RU_Upgrade": "Плексиглас + экранирование", "EN_Upgrade": "Plexiglas + Shielding", "UA_Upgrade": "Плексиглас + екранування",
    "RU_Full": "Тактический шлем: Плексигласовые накладки с экранирующим покрытием", "EN_Full": "Tactical Helmet: Plexiglas Overlays with Protective Coating", "UA_Full": "Тактичний шолом: Плексигласові накладки з екранувальним покриттям.",
    "RU_Desc": "Защищает не только от бета-, но и от пси-излучения.", "EN_Desc": "Shields against beta- and psi-radiation.", "UA_Desc": "Захищає від бета- й псі-випромінювання.",
    "teleport_cmd": "XTeleportTo 0 0 0"
  }
]

SVG_CHECK_B64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0iIzAwRTY3NiIgZmlsbC1vcGFjaXR5PSIwLjIiIHN0cm9rZT0iIzAwRTY3NiIgc3Ryb2tlLXdpZHRoPSIyIi8+PHBhdGggZD0iTTggMTJMMTEgMTVMMTYgOSIgc3Ryb2tlPSIjMDBFNjc2IiBzdHJva2Utd2lkdGg9IjIuNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+PC9zdmc+"
SVG_CROSS_B64 = "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHZpZXdCb3g9IjAgMCAyNCAyNCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSIxMCIgZmlsbD0iIzFFMjYzOCIgZmlsbC1vcGFjaXR5PSIwLjgiIHN0cm9rZT0iIzMzNDE1NSIgc3Ryb2tlLXdpZHRoPSIxLjUiLz48cGF0aCBkPSJNOSA5TDE1IDE1TTE1IDlMOSAxNSIgc3Ryb2tlPSIjNjQ3NDhCIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvc3ZnPg=="

TEXTS = {
    "ru": {
        "header": "🛠️ Чертёжные схемы (Апгрейды)",
        "desc": "Найденные модификации оружия и экипировки • Нажмите на карточку для подробностей и карты",
        "cat_weapon": "🔫 Оружейные чертежи",
        "cat_armor": "🛡️ Чертежи брони и экипировки",
        "copy_tip": "Кликните для подробностей и карты",
        "summary_btn": "📥 Скачать команды недостающих чертежей",
        "teleport": "📍 Команда телепорта к чертежу:",
        "spawn": "📦 Команда для спавна в инвентарь:",
        "id_label": "🆔 Идентификатор предмета (SID):",
        "slide_map": "🗺️ Карта местности",
        "slide_scr": "📸 Скриншот тайника",
        "found": "НАЙДЕНО",
        "missing": "НЕ НАЙДЕНО"
    },
    "uk": {
        "header": "🛠️ Схеми креслень (Апгрейди)",
        "desc": "Знайдені модифікації зброї та екіпірування • Натисніть на картку для деталей та карти",
        "cat_weapon": "🔫 Збройові креслення",
        "cat_armor": "🛡️ Креслення броні та екіпірування",
        "copy_tip": "Клікніть для деталей та карти",
        "summary_btn": "📥 Завантажити команди відсутніх креслень",
        "teleport": "📍 Команда телепорту до креслення:",
        "spawn": "📦 Команда для спавну в інвентар:",
        "id_label": "🆔 Ідентифікатор предмета (SID):",
        "slide_map": "🗺️ Карта розташування",
        "slide_scr": "📸 Скріншот схованки",
        "found": "ЗНАЙДЕНО",
        "missing": "НЕ ЗНАЙДЕНО"
    },
    "en": {
        "header": "🛠️ Blueprints (Upgrades)",
        "desc": "Discovered weapon & equipment blueprints • Click any card for location map & details",
        "cat_weapon": "🔫 Weapon Blueprints",
        "cat_armor": "🛡️ Armor & Gear Blueprints",
        "copy_tip": "Click for details and map",
        "summary_btn": "📥 Download missing blueprints commands",
        "teleport": "📍 Teleport command to blueprint:",
        "spawn": "📦 Inventory spawn command:",
        "id_label": "🆔 Item Identifier (SID):",
        "slide_map": "🗺️ Location Map",
        "slide_scr": "📸 In-game Screenshot",
        "found": "FOUND",
        "missing": "NOT FOUND"
    }
}

# =========================================================================
# ИНТЕРАКТИВНЫЙ ПОПАП С КАРУСЕЛЬЮ (MAP -> SCREENSHOTS)
# =========================================================================
@st.dialog("🛠️ Карточка схемы", width="large")
def show_blueprint_modal(bp, is_found, lang="ru"):
    txt = TEXTS.get(lang, TEXTS["ru"])
    lp = "RU" if lang == "ru" else ("UA" if lang == "uk" else "EN")
    
    full_name = bp.get(f"{lp}_Full", bp["RU_Full"])
    desc = bp.get(f"{lp}_Desc", bp["RU_Desc"])
    b_id = bp["id"]
    spawn_cmd = f"XCreateItemInInventoryByID {b_id} 0 1 1"
    teleport_cmd = bp.get("teleport_cmd", "XTeleportTo 0 0 0")

    # Формируем список слайдов: Карта ВСЕГДА первая, затем скриншоты
    slides = [
        {"title": txt["slide_map"], "url": get_map_url(b_id)}
    ]
    scr_count = bp.get("scr_count", 1)
    if scr_count == 1:
        slides.append({"title": txt["slide_scr"], "url": get_scr_url(b_id, 1)})
    else:
        for idx in range(1, scr_count + 1):
            slides.append({"title": f"{txt['slide_scr']} #{idx}", "url": get_scr_url(b_id, idx)})

    status_color = "#00E676" if is_found else "#EF4444"
    status_bg = "rgba(0, 230, 118, 0.1)" if is_found else "rgba(239, 68, 68, 0.1)"
    status_text = txt["found"] if is_found else txt["missing"]

    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #1E2638; padding-bottom: 12px; margin-bottom: 15px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <img src="{get_icon_url(b_id)}" onerror="this.style.display='none';" style="width: 32px; height: 32px; object-fit: contain;" />
            <h3 style="color: #FFB000; margin: 0; font-size: 1.25rem; font-weight: 800;">{full_name}</h3>
        </div>
        <span style="color: {status_color}; background: {status_bg}; border: 1px solid {status_color}; border-radius: 6px; padding: 4px 10px; font-size: 0.8rem; font-weight: 700;">{status_text}</span>
    </div>
    """, unsafe_allow_html=True)

    # Карусель картинок (Слайдер)
    session_key = f"bp_slide_{b_id}"
    if session_key not in st.session_state:
        st.session_state[session_key] = 0
        
    cur_idx = st.session_state[session_key]
    if cur_idx >= len(slides):
        cur_idx = 0
        st.session_state[session_key] = 0

    current_slide = slides[cur_idx]

    st.markdown(f"""
    <div style="width: 100%; border-radius: 10px; overflow: hidden; border: 1px solid #1E2638; background: #0A0D14; margin-bottom: 8px; text-align: center; position: relative;">
        <div style="position: absolute; top: 10px; left: 12px; background: rgba(10, 13, 20, 0.85); border: 1px solid #1E2638; padding: 3px 10px; border-radius: 6px; color: #FFB000; font-weight: 700; font-size: 0.8rem; z-index: 2;">
            {current_slide['title']} ({cur_idx + 1}/{len(slides)})
        </div>
        <img src="{current_slide['url']}" onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/coptrhiller-ctrl/stalker2-checker/main/icons/blueprint/placeholder.png';" style="width: 100%; max-height: 400px; object-fit: contain; display: block; margin: 0 auto;" />
    </div>
    """, unsafe_allow_html=True)

    if len(slides) > 1:
        c_prev, c_space, c_next = st.columns([1, 2, 1])
        with c_prev:
            if st.button("◀ Назад", use_container_width=True, key=f"bp_prev_{b_id}"):
                st.session_state[session_key] = (cur_idx - 1) % len(slides)
                st.rerun()
        with c_space:
            st.markdown(f"<div style='text-align: center; color: #64748B; font-size: 0.85rem; margin-top: 8px;'>Используйте кнопки для переключения</div>", unsafe_allow_html=True)
        with c_next:
            if st.button("Вперед ▶", use_container_width=True, key=f"bp_next_{b_id}"):
                st.session_state[session_key] = (cur_idx + 1) % len(slides)
                st.rerun()

    # Описание
    st.markdown(f"""
    <div style="background: #111520; border-left: 3px solid #FFB000; border-radius: 6px; padding: 10px 14px; margin: 12px 0 16px 0; color: #CBD5E1; font-size: 0.9rem; line-height: 1.45;">
        {desc}
    </div>
    """, unsafe_allow_html=True)

    # Интерактивные кликабельные поля для мгновенного копирования
    st.markdown(f"""
    <div style="margin-bottom: 12px;">
        <span style="color: #FFB000; font-size: 0.82rem; font-weight: 700;">{txt['teleport']}</span>
        <div class="stalker-copy-block" data-copy="{teleport_cmd}" title="Нажмите, чтобы скопировать">
            <code style="color: #00E676; font-size: 0.86rem; background: transparent; word-break: break-all;">{teleport_cmd}</code>
            <span class="stalker-copy-badge">📋 Копировать</span>
        </div>
    </div>

    <div style="margin-bottom: 12px;">
        <span style="color: #FFB000; font-size: 0.82rem; font-weight: 700;">{txt['spawn']}</span>
        <div class="stalker-copy-block" data-copy="{spawn_cmd}" title="Нажмите, чтобы скопировать">
            <code style="color: #00E676; font-size: 0.86rem; background: transparent; word-break: break-all;">{spawn_cmd}</code>
            <span class="stalker-copy-badge">📋 Копировать</span>
        </div>
    </div>

    <div>
        <span style="color: #94A3B8; font-size: 0.8rem; font-weight: 600;">{txt['id_label']}</span>
        <div class="stalker-copy-block" data-copy="{b_id}" title="Нажмите, чтобы скопировать">
            <code style="color: #94A3B8; font-size: 0.82rem; background: transparent;">{b_id}</code>
            <span class="stalker-copy-badge">📋 Копировать</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================================
# ГЛАВНАЯ ФУНКЦИЯ ОТРИСОВКИ СЕКЦИИ ЧЕРТЕЖЕЙ
# =========================================================================
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

    weapons = [b for b in BLUEPRINTS_DATA if b["type"] == "weapon"]
    armors = [b for b in BLUEPRINTS_DATA if b["type"] == "armor"]

    found_w = sum(1 for b in weapons if b["id"] in found_bps)
    found_a = sum(1 for b in armors if b["id"] in found_bps)

    pct_w = int(found_w / len(weapons) * 100) if weapons else 0
    pct_a = int(found_a / len(armors) * 100) if armors else 0

    # Стили кликабельных карточек и блоков копирования
    st.markdown("""
    <style>
    .stalker-copy-block {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #0A0D14;
        border: 1px solid #1E2638;
        border-radius: 8px;
        padding: 8px 12px;
        margin-top: 4px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .stalker-copy-block:hover {
        border-color: #00E676;
        background: rgba(0, 230, 118, 0.05);
    }
    .stalker-copy-badge {
        font-size: 0.75rem;
        font-weight: 600;
        color: #94A3B8;
        background: #111520;
        border: 1px solid #1E2638;
        padding: 2px 8px;
        border-radius: 4px;
        transition: all 0.2s ease;
    }
    .stalker-copy-block:hover .stalker-copy-badge {
        color: #00E676;
        border-color: rgba(0, 230, 118, 0.4);
    }

    /* Индивидуальная компактная карточка чертежа */
    .bp-item-tile {
        position: relative;
        background: #111520;
        border-radius: 12px;
        border: 1px solid #1E2638;
        padding: 6px 0 0 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-between;
        height: 135px;
        width: 135px;
        flex: 0 0 135px;
        cursor: pointer;
        transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1);
        user-select: none;
        box-sizing: border-box;
    }
    .bp-item-tile:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.6);
        border-color: #FFB000;
        z-index: 9999 !important;
    }
    .bp-item-tile .bp-tooltip {
        visibility: hidden;
        opacity: 0;
        width: 250px;
        background-color: #141A26;
        color: #F8FAFC;
        text-align: left;
        border-radius: 8px;
        padding: 10px 12px;
        border: 1px solid #FFB000;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.85);
        position: absolute;
        z-index: 99999 !important;
        bottom: 108%;
        left: 50%;
        transform: translateX(-50%) translateY(5px);
        transition: opacity 0.2s ease, visibility 0.2s ease, transform 0.2s ease;
        pointer-events: none;
        font-size: 0.78rem;
        line-height: 1.35;
    }
    .bp-item-tile:hover .bp-tooltip {
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #1E2638; margin: 40px 0 25px 0;'>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 20px;">
        <h2 style="color: #F8FAFC; font-weight: 800; margin-bottom: 4px;">{txt['header']}</h2>
        <span style="color: #94A3B8; font-size: 0.9rem;">{txt['desc']}</span>
    </div>
    """, unsafe_allow_html=True)

    # Дашборд прогресса
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div style="background-color: #111520; border: 1px solid #1E2638; border-radius: 12px; padding: 16px 20px;">
            <div style="color: #94A3B8; font-size: 0.88rem; font-weight: 600; margin-bottom: 4px;">{txt['cat_weapon']}</div>
            <div style="display: flex; align-items: baseline; justify-content: space-between;">
                <span style="color: #F8FAFC; font-size: 1.6rem; font-weight: 800;">{found_w} / {len(weapons)}</span>
                <span style="color: #00E676; font-size: 0.9rem; font-weight: 700; background: rgba(0, 230, 118, 0.12); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 6px; padding: 2px 8px;">{pct_w}%</span>
            </div>
            <div style="width: 100%; background: #1E2638; border-radius: 8px; height: 6px; margin-top: 8px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #FFB000, #00E676); width: {pct_w}%; height: 100%; border-radius: 8px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background-color: #111520; border: 1px solid #1E2638; border-radius: 12px; padding: 16px 20px;">
            <div style="color: #94A3B8; font-size: 0.88rem; font-weight: 600; margin-bottom: 4px;">{txt['cat_armor']}</div>
            <div style="display: flex; align-items: baseline; justify-content: space-between;">
                <span style="color: #F8FAFC; font-size: 1.6rem; font-weight: 800;">{found_a} / {len(armors)}</span>
                <span style="color: #00E676; font-size: 0.9rem; font-weight: 700; background: rgba(0, 230, 118, 0.12); border: 1px solid rgba(0, 230, 118, 0.25); border-radius: 6px; padding: 2px 8px;">{pct_a}%</span>
            </div>
            <div style="width: 100%; background: #1E2638; border-radius: 8px; height: 6px; margin-top: 8px; overflow: hidden;">
                <div style="background: linear-gradient(90deg, #FFB000, #00E676); width: {pct_a}%; height: 100%; border-radius: 8px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Категории
    categories = [
        (txt['cat_weapon'], weapons, found_w),
        (txt['cat_armor'], armors, found_a)
    ]

    for cat_name, items, count in categories:
        filtered = []
        for item in items:
            is_f = item["id"] in found_bps
            if art_filter == "missing" and is_f:
                continue
            if art_filter == "found" and not is_f:
                continue
            filtered.append(item)

        if not filtered:
            continue

        with st.expander(f"{cat_name} [{count}/{len(items)}]", expanded=True):
            # Рендерим интерактивные кнопки-плитки по 6 в ряд
            n_cols = 6
            for row_i in range(0, len(filtered), n_cols):
                cols = st.columns(n_cols)
                row_items = filtered[row_i:row_i + n_cols]
                for col, bp in zip(cols, row_items):
                    with col:
                        b_id = bp["id"]
                        is_f = b_id in found_bps
                        status_icon = "🟢" if is_f else "⚪"
                        
                        short_name = bp.get(f"{lp}_Short", bp["RU_Short"])
                        upgrade_name = bp.get(f"{lp}_Upgrade", bp["RU_Upgrade"])
                        full_name = bp.get(f"{lp}_Full", bp["RU_Full"])
                        desc = bp.get(f"{lp}_Desc", bp["RU_Desc"])

                        # Кнопка открытия карточки
                        btn_label = f"{status_icon} {short_name}\n({upgrade_name})"
                        help_text = f"{full_name}\n\n{desc}\n\n📍 Нажмите, чтобы открыть карту и команды"
                        
                        if st.button(btn_label, key=f"bp_tile_{b_id}", use_container_width=True, help=help_text):
                            show_blueprint_modal(bp, is_f, lang)

    # Скачивание недостающих схем
    missing_bps = [b for b in BLUEPRINTS_DATA if b["id"] not in found_bps]
    if missing_bps:
        txt_content = "=========================================================\n"
        txt_content += "      СПИСОК НЕДОСТАЮЩИХ ЧЕРТЕЖЕЙ S.T.A.L.K.E.R. 2\n"
        txt_content += f"      Недостает схем: {len(missing_bps)} из {len(BLUEPRINTS_DATA)}\n"
        txt_content += "=========================================================\n\n"
        
        txt_content += "▶ Команды спавна недостающих чертежей в инвентарь:\n"
        txt_content += "|".join([f"XCreateItemInInventoryByID {b['id']} 0 1 1" for b in missing_bps]) + "\n\n"
        
        txt_content += "▶ Координаты телепорта к недостающим чертежам:\n"
        for b in missing_bps:
            name = b.get(f"{lp}_Full", b["RU_Full"])
            t_cmd = b.get("teleport_cmd", "XTeleportTo 0 0 0")
            txt_content += f"  • {name}: {t_cmd}\n"

        st.markdown("<br/>", unsafe_allow_html=True)
        st.download_button(
            label=txt['summary_btn'],
            data=txt_content,
            file_name="Missing_Blueprints.txt",
            mime="text/plain",
            key="dl_blueprints"
        )

    # Подключение JavaScript для быстрого копирования
    components.html("""
    <script>
    try {
        const parentDoc = window.parent.document;
        parentDoc.addEventListener('click', function(e) {
            let field = e.target.closest('.stalker-copy-block');
            if(field) {
                let textToCopy = field.getAttribute('data-copy');
                if(textToCopy && parentDoc.hasFocus()) {
                    parentDoc.defaultView.navigator.clipboard.writeText(textToCopy).then(() => {
                        let hint = field.querySelector('.stalker-copy-badge');
                        if(hint) {
                            let old = hint.innerText;
                            hint.innerText = "✅ Скопировано!";
                            hint.style.color = "#00E676";
                            setTimeout(() => {
                                hint.innerText = old;
                                hint.style.color = "";
                            }, 1400);
                        }
                    });
                }
            }
        });
    } catch(err) {
        console.log("Clipboard ready.");
    }
    </script>
    """, height=0, width=0)
