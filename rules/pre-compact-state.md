# Pre-Compact State Preservation (Grok Port)

Context window daraldiginda (kompres uyarisi geldiginde) session state'ini koru. Bu manuel bir disiplin pattern'idir.

## Ne Zaman Tetiklenir
- Context window son %20'ye girdiginde
- Sistem "conversation will be compressed" uyarisi verdiginde
- Uzun session'larda buyuk isler yapilirken

## Koruma Kontrol Listesi
PreCompact aninda su bilgileri kaydet/dump et:

### 1. Active Task State
```
AKTIF TASK: [task aciklamasi]
DURUM: [nerede kaldik]
TAMAMLANAN: [bitirdigimiz kisimlar]
KALAN: [yapmamiz gerekenler]
```

### 2. Modified Files
```
DEGISEN DOSYALAR:
- [dosya1]: [ne degisti]
- [dosya2]: [ne degisti]
COMMIT DURUMU: [committed/uncommitted]
```

### 3. Decision Context
```
ALINAN KARARLAR:
- [karar 1]: [neden]
- [karar 2]: [neden]
BEKLEYEN KARARLAR:
- [karar]: [secenekler]
```

### 4. WIP (Work in Progress)
```
YARIM KALAN IS:
- [dosya:satir]: [ne yapiliyordu]
GEREKLI CONTEXT:
- [hangi bilgi tekrar lazim olacak]
```

## Nereye Kaydet
1. Mevcut task'a (TaskUpdate ile description guncelle)
2. Cok kritikse: `~/.grok/palace/<project>/wip-state.md` dosyasina (our palace)
3. Compass analog: use our session-compressor hook + palace.

## Kurallar
- Kompres uyarisi geldiginde ONCE state dump et, SONRA ise devam et
- State dump'i kisa tut, sadece recovery icin gerekli bilgi
- Git diff kaydet (uncommitted degisiklikler icin)
- Token tasarrufu icin dosya iceriklerini DEGIL, ozet bilgiyi kaydet

**Grok Note**: Pre-compact state preservation now wired: auto_session_compressor + auto_palace_save saves WIP to .grok/projects/<project>/wip-state.jsonl + palace. Layered-recall for efficient recovery. Use before compaction. Original in ~/.claude/rules/pre-compact-state.md.