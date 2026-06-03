# Memory System (Grok Port)

## Recall (Gecmis Ogrenimleri Cek)
Use our compound + palace for recall.
```bash
# Example: recall recent high impact via friction_curator or palace recall
```

### Ne Zaman
- Daha once yapilmis bir ise baslarken
- Hata veya zor durumda
- Mimari karar verirken

### Secenekler
- Use layered recall via memory-palace skill + hooks.
- Hybrid with compound friction.

### Skorlar
- Our evolution scores 0-100 on 5 dims.

## Store (Ogrenim Kaydet)
```python
# Via friction record or palace store_memory or compound
```

Tipler: ARCHITECTURAL_DECISION, WORKING_SOLUTION, CODEBASE_PATTERN, FAILED_APPROACH, ERROR_FIX, USER_PREFERENCE, OPEN_THREAD

## Ne Zaman Kaydet
- Zor sorun cozunce
- Mimari karar alinca
- Codebase pattern kesfedince
- Calismayan bir sey bulunca

## Agent'lar ve Memory
- Agent'lar ise baslamadan once memory'ye baksin (via on_agent_spawn hook + palace recall).
- MEMORY MATCH bulunursa kullaniciya kisa bahset.
- Cok alakaliysa detay goster, az alakaliysa atla.
- Her memory match'i soyleme, gereksiz gurultu yapma.

## Backend
- Palace JSONL + index (under .grok/palace/)
- Friction jsonl
- Compound evolution

Scripts in our skills. Docker not needed; pure file + python.

**Grok Note**: Palace memory recall is now complete: full layered-recall skill (4-scope/3-depth progressive, 10-50x savings) + enhanced memory-palace + .grok/projects/ per-project (MEMORY.md, wip-state.jsonl) + pre-compact WIP preservation + auto_palace_save + auto_palace_recall hooks + integration with compound, on_agent_spawn, preflight, cross-project. Use memory-palace + layered-recall for store/recall. Original in ~/.claude/rules/memory-system.md and .claude/skills/layered-recall/ (read-only).