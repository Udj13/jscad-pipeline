# Uninstall Guide

Удаление всех компонентов, установленных для JSCAD 3D modeling pipeline.

---

## 1. Deno — JavaScript/Deno runtime

**Что это:** Deno — безопасная среда выполнения для JavaScript/TypeScript, альтернатива Node.js.
Swamp использует Deno для выполнения JSCAD-скриптов (CAD-моделирование на JS).

```bash
# Удалить Deno
rm -rf ~/.deno

# Удалить записи из .zshrc (открыть файл и удалить эти две строки):
#   export DENO_INSTALL="$HOME/.deno"
#   export PATH="$DENO_INSTALL/bin:$PATH"

# Или одной командой:
sed -i '' '/DENO_INSTALL/d' ~/.zshrc
sed -i '' '/deno\/bin/d' ~/.zshrc

# Применить изменения
source ~/.zshrc
```

---

## 2. Swamp CLI — оркестрация pipeline

**Что это:** Swamp — CLI-утилита для управления AI-native workflow.
В нашем проекте она запускает JSCAD-рендеринг, валидацию STL и управляет моделями.

```bash
# Удалить бинарный файл
rm ~/.local/bin/swamp

# Удалить кэш (если есть)
rm -rf ~/.swamp 2>/dev/null
```

---

## 3. Данные проекта (удалить сам проект)

**Что это:** Всё, что Swamp сохранила в каталоге проекта — рендеры, STL-файлы, логи, модельные конфигурации.

```bash
# Полное удаление каталога проекта
rm -rf ~/jscad/test
```

---

## Сводная таблица

| Компонент | Размер | Что делает | Команда удаления |
|-----------|--------|------------|------------------|
| **Deno** | ~95 MB | JS/TS runtime для запуска JSCAD-скриптов | `rm -rf ~/.deno` |
| **Swamp CLI** | ~231 MB | Оркестрация pipeline, модели, workflow | `rm ~/.local/bin/swamp` |
| **viewer/** | ~2.5 MB | JSCAD Web UI для 3D-превью в браузере | `rm -rf ~/jscad/test/viewer` |
| **Проект** | variable | Все артефакты проекта | `rm -rf ~/jscad/test` |

---

## Быстрое удаление всего

```bash
rm -rf ~/.deno ~/.local/bin/swamp ~/jscad/test
sed -i '' '/DENO_INSTALL/d' ~/.zshrc
sed -i '' '/deno\/bin/d' ~/.zshrc
source ~/.zshrc
```
