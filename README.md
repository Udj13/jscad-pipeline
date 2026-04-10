# JSCAD 3D Modeling Pipeline

Проект для генерации 3D-моделей из текстовых описаний с использованием JSCAD v2, Swamp и AI.

**Пайплайн:** Текст → JSCAD-скрипт → STL → Валидация → Готовый файл

---

## Требования

- **macOS/Linux** (Windows через WSL)
- **Python 3.7+** (для веб-сервера просмотра)
- **Deno** (JavaScript/TypeScript runtime)
- **Swamp CLI** (оркестратор pipeline)

---

## Установка

### 1. Установка Deno

Deno — это безопасная среда выполнения для JavaScript/TypeScript, необходимая для запуска JSCAD-скриптов.

```bash
# Установка Deno
curl -fsSL https://deno.land/install.sh | sh

# Добавить в PATH (для zsh)
echo 'export DENO_INSTALL="$HOME/.deno"' >> ~/.zshrc
echo 'export PATH="$DENO_INSTALL/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Для bash
echo 'export DENO_INSTALL="$HOME/.deno"' >> ~/.bashrc
echo 'export PATH="$DENO_INSTALL/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Проверка установки
deno --version
```

### 2. Установка Swamp CLI

Swamp — это CLI-утилита для управления AI-native workflow и моделями.

```bash
# Установка Swamp
curl -fsSL https://swamp.club/install.sh | sh

# Проверка установки
swamp --version
```

### 3. Клонирование проекта

```bash
# Клонировать репозиторий
git clone <repository-url>
cd test

# Или создать новый проект
mkdir jscad-project
cd jscad-project
```

### 4. Инициализация Swamp репозитория

```bash
# Инициализировать Swamp репозиторий
swamp repo init

# Установить расширения для JSCAD
swamp extension pull @magistr/jscad-cad
swamp extension pull @magistr/jscad-stl-validator
swamp extension pull @magistr/jscad-stl-slicer
```

### 5. Создание моделей

Создайте конфигурации моделей в директории `models/@magistr/`:

**models/@magistr/jscad-cad/box-test.yaml:**
```yaml
type: "@magistr/jscad-cad"
spec:
  name: "box-test"
  description: "JSCAD renderer for 3D models"
```

**models/@magistr/jscad-stl-validator/stl-check.yaml:**
```yaml
type: "@magistr/jscad-stl-validator"
spec:
  name: "stl-check"
  description: "STL file validator"
```

**models/@magistr/jscad-stl-slicer/slicer.yaml:**
```yaml
type: "@magistr/jscad-stl-slicer"
spec:
  name: "slicer"
  description: "STL analyzer for symmetry and profiles"
```

### 6. Проверка установки

```bash
# Добавить Deno в PATH для текущей сессии
export PATH="$HOME/.deno/bin:$PATH"

# Проверить доступные модели
swamp model search

# Проверить типы моделей
swamp model type search jscad
```

---

## Быстрый старт

### 1. Создание входного файла

Создайте файл `test-inputs.yaml`:

```yaml
script: |
  const main = (params = {}) => {
    return primitives.cuboid({ size: [20, 10, 5] });
  };
outputFormat: stl
```

### 2. Рендеринг модели

```bash
# Убедитесь что Deno в PATH
export PATH="$HOME/.deno/bin:$PATH"

# Запустить рендеринг
swamp model method run box-test run \
  --input-file test-inputs.yaml --json
```

### 3. Валидация STL

```bash
swamp model method run stl-check validate \
  --input cadModelName=box-test --json
```

### 4. Копирование результата

```bash
# Найти последнюю версию
swamp data list box-test output

# Скопировать STL файл
cp .swamp/data/@magistr/jscad-cad/*/output/1/raw my-model.stl
```

### 5. Просмотр в браузере

```bash
# Запустить веб-сервер
./start-viewer.sh

# Открыть в браузере
# http://localhost:8080/viewer/?model=my-model.stl
```

---

## Структура проекта

```
.
├── README.md                    # Этот файл
├── USAGE.md                     # Подробная инструкция по использованию
├── UNINSTALL.md                 # Инструкция по удалению
├── CLAUDE.md                    # Конфигурация AI-агента
├── .swamp.yaml                  # Конфигурация Swamp репозитория
├── .swamp/                      # Внутренние данные Swamp (не трогать)
├── models/                      # Конфигурации моделей
│   └── @magistr/
│       ├── jscad-cad/          # Рендерер JSCAD → STL
│       ├── jscad-stl-validator/ # Валидатор STL
│       └── jscad-stl-slicer/   # Анализатор STL
├── extensions/                  # Установленные расширения
│   └── models/
│       └── upstream_extensions.json
├── viewer/                      # 3D-превью в браузере
│   ├── index.html
│   └── dist/
├── workflows/                   # Swamp workflow-ы
├── vaults/                      # Хранилище секретов
├── server.py                    # HTTP-сервер для просмотра
├── start-viewer.sh              # Скрипт запуска вьюера
├── *-inputs.yaml                # Входные файлы со скриптами
└── *.stl                        # Готовые STL-файлы
```

---

## Доступные модели

| Модель | Тип | Методы | Назначение |
|--------|-----|--------|-----------|
| `box-test` | `@magistr/jscad-cad` | `run` | Рендеринг JSCAD → STL/SVG/DXF/OBJ |
| `stl-check` | `@magistr/jscad-stl-validator` | `validate`, `validateFile` | Валидация STL файлов |
| `slicer` | `@magistr/jscad-stl-slicer` | `analyzeSymmetry`, `extractDirectionalProfile` | Анализ геометрии STL |

---

## Поддерживаемые форматы вывода

В YAML-файле можно указать `outputFormat`:

- `stl` — Binary STL (по умолчанию, для 3D-печати)
- `stl-ascii` — ASCII STL (читаемый человеком)
- `dxf` — DXF (2D чертежи)
- `svg` — SVG (векторная графика)
- `obj` — Wavefront OBJ
- `3mf` — 3D Manufacturing Format

---

## Полезные команды

```bash
# Показать все модели
swamp model search --json

# Показать методы модели
swamp model type describe @magistr/jscad-cad --json

# Показать результат рендеринга
swamp data get box-test result --version 1 --json

# Получить STL-файл
swamp data get box-test output --version 1 --json

# Получить логи выполнения
swamp data get box-test log --version 1 --json

# Показать все версии
swamp data list box-test output

# Получить отчёт валидации
swamp data get stl-check report --version 1 --json
```

---

## Устранение неполадок

### Deno не найден

```bash
# Проверить установку
ls -la ~/.deno/bin/deno

# Добавить в PATH
export PATH="$HOME/.deno/bin:$PATH"

# Или добавить в .zshrc/.bashrc
echo 'export PATH="$HOME/.deno/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Swamp не найден

```bash
# Проверить установку
ls -la ~/.local/bin/swamp

# Добавить в PATH
export PATH="$HOME/.local/bin:$PATH"
```

### Модели не найдены

```bash
# Переустановить расширения
swamp extension pull @magistr/jscad-cad
swamp extension pull @magistr/jscad-stl-validator
swamp extension pull @magistr/jscad-stl-slicer

# Проверить установку
swamp model type search jscad
```

---

## Дополнительная документация

- **USAGE.md** — подробная инструкция по использованию с примерами
- **UNINSTALL.md** — инструкция по полному удалению всех компонентов
- **CLAUDE.md** — правила работы с проектом для AI-агентов

---

## Ссылки

- [Swamp Documentation](https://github.com/systeminit/swamp)
- [JSCAD Documentation](https://openjscad.xyz/)
- [Deno Documentation](https://deno.land/)

---

## Лицензия

См. LICENSE файл в корне репозитория.
