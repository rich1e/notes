### 2026

```dataviewjs
dv.table(["File", "Genre", "Time Read", "Rating"], dv.pages('"2026"')
    .sort(b => b.file.mtime)
    .map(b => [b.file.link, b.genre, b["time-read"], b.rating]))
```

### 2025

```dataviewjs
dv.table(["File", "Genre", "Time Read", "Rating"], dv.pages('"2025"')
    .sort(b => b.file.mtime)
    .map(b => [b.file.link, b.genre, b["time-read"], b.rating]))
```

### 2024

```dataviewjs
dv.table(["File", "Genre", "Time Read", "Rating"], dv.pages('"2024"')
    .sort(b => b.file.mtime)
    .map(b => [b.file.link, b.genre, b["time-read"], b.rating]))
```

### 2023

```dataviewjs
dv.table(["File", "Genre", "Time Read", "Rating"], dv.pages('"2023"')
    .sort(b => b.file.mtime)
    .map(b => [b.file.link, b.genre, b["time-read"], b.rating]))
```

### 2022

```dataviewjs
// Render a simple table of book info sorted by rating.
dv.table(["File", "Genre", "Time Read", "Rating"], dv.pages('"2022"')
    .sort(b => b.file.mtime)
    .map(b => [b.file.link, b.genre, b["time-read"], b.rating]))

```

### 2021
```dataviewjs
// Render a simple table of book info sorted by rating.
dv.table(["File", "Genre", "Time Read", "Rating"], dv.pages('"2021"')
    .sort(b => b.file.mtime)
    .map(b => [b.file.link, b.genre, b["time-read"], b.rating]))
```