# Cross-Project Learning (Grok Port)

Pattern'ler proje bazında tag'lenir / capture edilir, 2+ projede tekrarlayan pattern'ler global'e promote edilir (compound + palace üzerinden).

**Grok adaptation note:** .claude counterpart'ından (readonly) uyarlandı. Grok'ta legacy "instincts" yerine mevcut executable sistemler kullanılır:
- compound-friction.jsonl + friction-curator (high-impact pattern'leri curates, skill/rule/persona önerileri üretir).
- memory-palace (Wings = projects, Rooms = domains, Drawers = decisions; layered recall ile).
- sessions/ + thoughts/ + palace/ (per-project context).
- compound-learnings skill (observe → draft → review → promote).
- Future: .grok/projects/{hash}/ + instincts promotion (2+ proj / 5+ repeat → global) + passive-learner style hook.

Tam 1:1 kopya değil; Grok güçlü yanlarını (executable Python, hooks, compound flywheel) korur. Hiç .claude/ touch.

## Nasıl Çalışır (Grok'ta)

1. **Capture (her ajan/orchestrator sonunda):** friction + compound via on_run_completion, on_bounded_loop_end, on_friction_recorded, auto_* hooks. Proje context (cwd hash veya palace project name) eklenir.
2. **Consolidation (session / compound sonunda):** friction-curator + compound-learnings analyzer yüksek değerli pattern'leri (tekrar eden friction, başarılı recovery, arch decision) curates. Proje-özel vs global ayırır.
3. **Promotion:** 2+ projede görülen + 5+ toplam tekrar (veya compound confidence 80+) → global compound drafts veya palace global room'a promote. Cross-project learning aktif hale gelir.
4. **Recall (session başlangıcı / agent spawn):** memory-palace recall + compound recall + on_agent_spawn injection ile proje-özel + global pattern'ler context'e enjekte edilir. Legacy fallback: compound-friction.jsonl + palace default.

## Dosya Yapısı (Grok)

```
~/.grok/
  compound-friction.jsonl          # Ham friction (+ project context via hooks)
  palace/                          # Wings (projects) > Rooms > Drawers (JSONL + index)
    <project-hash>/                # Per-project (future instincts/mature + MEMORY.md)
  sessions/<encoded-cwd>/          # Session state, plan.md, terminal logs
  thoughts/                        # Per-agent thoughts, drafts
  skills-drafts/                   # Compound tarafından üretilen SKILL.md draft'ları
  bundled/skills/compound-learnings/
  bundled/skills/friction-curator/
```

Mevcut: palace + compound-friction + friction-curator + compound-learnings + memory-palace skill + auto_palace + palace-recall hook + layered-recall.

Eksik / gelecek: tam .grok/projects/ + instinct-projects.json + global-instincts.json + passive-learner hook + instinct-consolidator/loader (compound + palace ile emüle ediliyor).

## CLI / Kullanım (Grok)

- compound-learnings skill: pattern extraction + draft önerileri.
- friction-curator: high-impact curating, dedup, pre-flight suggestion.
- memory-palace + recall: project bazlı semantic recall.
- /learn veya friction record: manuel capture.
- palace recall hook (session start): otomatik enjeksiyon.

## Promotion Kuralları (Grok'ta)

- 2+ projede görülmüş (cwd / palace project ayırımı ile).
- Toplam 5+ tekrar veya compound confidence 80+.
- Örnek: "add-error-handling + ledger" 3x Proje A + 4x Proje B = promote → global compound draft veya palace global room + rule önerisi.

## Entegrasyon

- auto-skill-activation + on_agent_spawn: proje tespiti + recall (project patterns + global).
- compound flywheel: draft'lar skills-drafts/ veya rules/ veya bundled/agents/ 'a promote edilebilir.
- Pre-Flight: friction ledger'da proje-özel yüksek friction varsa uyarır.
- Cross-project: palace + compound ile halihazırda kısmi çalışıyor; tam promotion için compound + palace genişletmesi planlanıyor.

Bu rule, Thanos (Grok port of the original Claude Code AI software team system)'ün cross-project learning felsefesini Grok'un memory + self-improvement sistemlerine taşır. Tekrar eden acı (friction) boşa gitmez — global iyileşmeye dönüşür.