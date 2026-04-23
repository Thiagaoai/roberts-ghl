---
name: naming
description: Gera 10-15 opcoes de nome de empresa/produto, cada uma com tagline, justificativa, check de dominio .com/.com.br, e check de disponibilidade de handle @ em Instagram/TikTok. Usa a familia estetica, o publico, e a oferta do discover-brand como input. Checkpoint skill — usuario escolhe um antes de seguir pra logo/design. Use quando o discovery disser que o usuario quer renomear a empresa ou criar nome pra um novo produto/offer.
---

# Naming

> **Source & credit**: Pattern adapted from naming frameworks em [rohitg00/awesome-claude-design](https://github.com/rohitg00/awesome-claude-design) e os 7 tipos classicos de nome (inventado, descritivo, metaforico, founder-based, acronimo, composto, abstract). Domain availability pelo DNS check direto; handle check via HTTP status das paginas publicas.

## Purpose

Gerar nomes que vendem, nao so nomes bonitos. Um bom nome de empresa:

1. **Pronunciavel** na lingua do publico.
2. **Memoravel** em 5 segundos.
3. **Livre legalmente** (INPI / USPTO quick check) e disponivel em dominio e handle.
4. **Conta uma historia** alinhada com o brief.

## Input

- `./rebrand/01-discovery.md` — especialmente as secoes `Business & offer`, `Audience`, `Positioning`, `Naming`, `Aesthetic`.

## Skip condition

Se `Renomear? = nao` no discovery, nao rode essa skill — retorne um no-op pro orchestrator.

## Procedure

### 1. Pegue os parametros

Do discovery:
- **Estilo preferido**: inventado / descritivo / metaforico / founder / acronimo / composto
- **Idiomas permitidos**: PT-BR / EN / outro
- **.com obrigatorio**: sim / nao
- **Handles precisam bater**: sim / nao
- **Promessa unica** — o core emotional hook
- **Driver emocional** — qual emocao o nome deve disparar

### 2. Brainstorm 25 candidatos internos

Gera 25 nomes pra voce avaliar, nao pro usuario ver. Cobre os 5 tipos classicos:

| Tipo | Exemplo | Quando usa |
| --- | --- | --- |
| **Inventado** | Kodak, Xerox, Spotify | Quer marca forte, escalavel global, livre legalmente |
| **Descritivo** | General Motors, PayPal | Quer SEO, clareza imediata, pouco investimento em marca |
| **Metaforico** | Amazon, Nike, Oracle | Quer historia + emocao |
| **Founder** | Ferrari, Disney, Tesla | Quer autoridade pessoal / legacy |
| **Composto** | Facebook, Salesforce, YouTube | Quer clareza + personalidade |
| **Acronimo** | IBM, AWS, BMW | Ok se ja tem marca; ruim pra comecar |

Regra: se o discovery disse "founder", entrega 3-4 founder-based. Se disse "inventado", entrega 15 inventados e 10 dos outros tipos. Calibre.

### 3. Filtre pra 15

Elimina candidatos:
- Com >12 caracteres (dificil de digitar/lembrar)
- Que parecem com concorrentes diretos (pega o nome deles do discovery)
- Com pronuncia ambigua (ex: "Xylos" em PT-BR quem sabe se e "Zilos" ou "Shilos")
- Que significam algo ruim em outros idiomas relevantes
- Genericos de mais (ex: "SmartPay" quando ja tem 200 "Smart*")

### 4. Checks automatizados

Pros 15 finalistas, em paralelo (via `Bash`):

**Dominio**
```bash
# Checa .com e .com.br em um dig sem autoridade
for n in candidato1 candidato2 ...; do
  for tld in com com.br io app; do
    if dig +short "${n}.${tld}" NS | grep -q .; then
      echo "$n.$tld TAKEN"
    else
      echo "$n.$tld POSSIBLY_FREE"
    fi
  done
done
```
*POSSIBLY_FREE* e um sinal, nao uma garantia — bota um disclaimer no output.

**Handles @ Instagram / TikTok**
```bash
for n in candidato1 ...; do
  for host in instagram.com tiktok.com/@$n; do
    code=$(curl -s -o /dev/null -w "%{http_code}" "https://${host}/${n}")
    echo "$n $host -> $code"  # 404 = livre (provavel), 200 = taken
  done
done
```

**Trademark quick search** — nao e check legal oficial, mas:
- USPTO: `https://tmsearch.uspto.gov/search/search-information?searchText=<nome>`
- INPI (Brasil): `https://busca.inpi.gov.br/pePI/` (nota: INPI nao tem API publica facil, recomende check manual no output)

Marca com ⚠️ qualquer coisa que apareca em trademark search dos concorrentes diretos.

### 5. Gera taglines

Pra cada finalista, 2 taglines:
- Uma **funcional** (o que a empresa faz) — ex: "Checkout em 1 clique"
- Uma **emocional** (como o cliente se sente) — ex: "Compre sem friccao"

Ambas <= 8 palavras.

### 6. Escreve o output

Write `./rebrand/02-naming.md`:

```markdown
# Nomes propostos — <empresa>
_Generated <date> by the `naming` skill_

_15 candidatos. Ordenados por "mais forte pro brief" no topo, nao ordem alfabetica._

## Como escolher
- **Pronuncia**: leia em voz alta 3 vezes. Se tropecar, corta.
- **Teste do avo / crianca**: alguem de fora do nicho consegue repetir e escrever depois de ouvir uma vez?
- **Teste do @**: escreve o handle e ve se fica feio ou confunde (ex: @kodak_oficial vs @kodak).

---

### 1. **Nomix** — _inventado_
> **Tagline funcional**: Pagamentos sem codigo.
> **Tagline emocional**: A fintech que te respeita.
>
> **Por que funciona pro brief**: Curto (5 letras), livre foneticamente, evoca "no mix"/"next mix".
> **Checks**:
> - Dominio: nomix.com TAKEN, nomix.com.br POSSIBLY_FREE, nomix.app POSSIBLY_FREE
> - @instagram/nomix → 404 (livre provavel)
> - @tiktok/nomix → 404
> - Trademark: INPI manual check recomendado
> **Risco**: "nomix" pode soar como "no mix" em EN (ruim se for B2B tech EN).

---

### 2. **<nome>** — _<tipo>_
...
```

### 7. Checkpoint

Chama `AskUserQuestion`:

- Pergunta: "Qual nome segue pra Fase 3 (design/logo)?"
- Options: top 3 finalistas + "Nenhum — quero 10 novos numa direcao diferente".

Se escolher um → grava o slug em `./rebrand/.selected-name`, salva o nome/tagline num json pro logo-design usar:

```json
{
  "selected_name": "Nomix",
  "tagline_functional": "Pagamentos sem codigo.",
  "tagline_emotional": "A fintech que te respeita.",
  "domain_recommended": "nomix.app",
  "handle_recommended": "@nomix"
}
```

Em `./rebrand/.selected-name.json`.

Se escolher "Nenhum" → pergunta o que mudar (estilo / idioma / tom) e regera.

## Quality bar

- **Nunca entregue 15 candidatos do mesmo tipo** — variedade permite o usuario calibrar.
- **Sempre inclua a pronuncia** se o nome nao for obvio em PT-BR.
- **Seja honesto sobre os checks**: "POSSIBLY_FREE" nao e "FREE". Dominio tem que confirmar no registrador. Trademark e check legal.
- **Top 3 tem que ser defensavel**: se o usuario perguntar "por que esse e top 1?", voce tem que responder em 1 frase citando o brief.

## Handoff

Retorna:
- Path pra `02-naming.md`
- Nome selecionado + tagline
- Dominio e handle recomendados
- Bandeiras vermelhas (trademark conflict, dominio pego, etc.)
