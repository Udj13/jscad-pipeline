# Инструкция по использованию JSCAD Pipeline

## Обзор

Этот проект превращает текстовые описания в 3D-модели (STL-файлы).

**Пайплайн:** Текст → JSCAD-скрипт → STL → Валидация → Готовый файл

---

## Старт новой сессии

Напиши: **«запусти веб-вьюер»**

Я сделаю:
1. Запущу сервер просмотра на порту 8080
2. Открою вьюер в браузере с `box-test.stl`

После этого просто описывай объекты текстом — я буду генерировать STL, а ты увидишь их во вьюере (обнови страницу или нажми «Latest»).

---

## Как запросить модель

Просто опиши объект текстом. Примеры:

```
Сделай кубик 20x20x20 мм
Сделай коробку с открытым верхом: внешние размеры 100x60x40, стенка 3мм
Сделай цилиндр диаметр 30, высота 50 с отверстием 10мм по центру
Сделай шайбу: внешний диаметр 40, внутренний 20, толщина 5
```

---

## Что происходит за кулисами

### Шаг 1 — Генерация JSCAD-скрипта

Я пишу JSCAD-скрипт и сохраняю его в YAML-файл. Пример содержимого:

```yaml
# test-inputs.yaml
script: |
  const main = (params = {}) => {
    return primitives.cuboid({ size: [20, 10, 5] });
  };
outputFormat: stl
```

### Шаг 2 — Рендеринг в STL

```bash
export PATH="$HOME/.deno/bin:$PATH"
swamp model method run box-test run \
  --input-file <имя-файла>.yaml --json
```

Swamp выполняет JSCAD-скрипт и сохраняет STL.

### Шаг 3 — Валидация

```bash
swamp model method run stl-check validate \
  --input cadModelName=box-test --json
```

Проверка: количество треугольников, дегенеративные грани, bounding box.

### Шаг 4 — Копирование STL в проект

```bash
cp .swamp/data/@magistr/jscad-cad/*/output/<версия>/raw <имя>.stl
```

---

## 3D-превью в браузере

После генерации STL можно увидеть модель в 3D-вьюере прямо в браузере.

### Запуск вьюера

```bash
./start-viewer.sh
# или с другим портом:
./start-viewer.sh 9090
```

Откроется `http://localhost:8080/viewer/` — полноценный JSCAD Web UI.

### Как загрузить модель

1. **Через интерфейс** — выпадающий список вверху слева, все `.stl` файлы из проекта обнаруживаются автоматически
2. **Через URL** — `http://localhost:8080/viewer/?model=box-test.stl`
3. **Кнопка «Load Latest»** — загружает последний найденный STL

### Возможности вьюера

- Вращение мышью (ЛКМ — вращение, ПКМ — перемещение, колёсико — зум)
- Редактор JSCAD-скриптов встроен (можно писать и тестировать код прямо в браузере)
- Экспорт в STL, AMF, SVG, DXF
- Настройки отображения: сетка, оси, цвета

---

## Полная последовательность команд с превью

```bash
# 1. Deno в PATH
export PATH="$HOME/.deno/bin:$PATH"

# 2. Рендеринг
swamp model method run box-test run \
  --input-file inputs.yaml --json

# 3. Валидация
swamp model method run stl-check validate \
  --input cadModelName=box-test --json

# 4. Копирование STL
cp .swamp/data/@magistr/jscad-cad/*/output/1/raw my-model.stl

# 5. Просмотр (в отдельном терминале)
./start-viewer.sh
# → открыть http://localhost:8080/viewer/?model=my-model.stl
```

---

## Доступные форматы вывода

В YAML-файле можно указать `outputFormat`:

| Формат | Описание |
|--------|----------|
| `stl` | Binary STL (по умолчанию, для 3D-печати) |
| `stl-ascii` | ASCII STL (читаемый человеком) |
| `dxf` | DXF (2D чертежи) |
| `svg` | SVG (векторная графика) |
| `obj` | Wavefront OBJ |
| `3mf` | 3D Manufacturing Format |

---

## Структура проекта

```
/Users/user/jscad/test/
├── .claude/skills/jscad-codegen/   # Инструкции для генерации кода
│   ├── SKILL.md                     # Основные правила
│   └── references/                  # API, позиционирование, моделирование
├── models/                          # Конфигурации моделей Swamp
│   ├── @magistr/jscad-cad/box-test.yaml       # Рендерер
│   ├── @magistr/jscad-stl-validator/stl-check.yaml  # Валидатор
│   └── @magistr/jscad-stl-slicer/slicer.yaml        # Анализатор
├── viewer/                          # 3D-превью в браузере
│   ├── index.html                   # Страница вьюера
│   ├── dist/jscad-web.min.js        # JSCAD Web UI bundle
│   ├── css/                         # Стили
│   ├── fonts/                       # Шрифты
│   ├── imgs/                        # Иконки
│   └── locales/                     # Переводы
├── workflows/                       # Swamp workflow-ы
├── inputs.yaml                      # Входной YAML со скриптом
├── <имя>.stl                        # Готовые STL-файлы
├── start-viewer.sh                  # Запуск 3D-превью
├── CLAUDE.md                        # Конфиг AI-агента
└── .swamp/                          # Внутренние данные Swamp (не трогать)
```

---

## Модели и их назначение

| Модель | Назначение | Метод |
|--------|-----------|-------|
| `box-test` | Рендер JSCAD → STL/SVG/DXF/OBJ | `run` |
| `stl-check` | Валидация STL файла | `validate` |
| `stl-check` | Валидация STL файла по пути | `validateFile` |
| `slicer` | Анализ: симметрия, сечения, профили | `analyzeSymmetry`, `extractDirectionalProfile`, и др. |

---

## Полезные команды Swamp

```bash
# Показать результат рендеринга (ресурсы)
swamp data get box-test result --version 1 --json

# Получить STL-файл
swamp data get box-test output --version 1 --json

# Получить логи выполнения
swamp data get box-test log --version 1 --json

# Получить отчёт валидации
swamp data get stl-check report --version 1 --json

# Показать все версии
swamp data list box-test output

# Показать статус моделей
swamp model search --json
```
