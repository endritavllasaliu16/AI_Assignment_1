# Social Golfers Problem - README.md

## Pershkrimi i Problemit
Problemi i Golfisteve Sociale (Social Golfers Problem) eshte nje problem klasik i planifikimit dhe optimizimit ne inteligjencen artificiale dhe shkencen kompjuterike. Ai konsiston ne planifikimin e lojerave te golfit per nje numer te caktuar lojtaresh, te organizuar ne grupe, duke respektuar kufizime te caktuara.

- **Pershkrimi specifik**: Ka 32 lojtare golfi qe luajne nje here ne jave, ne grupe me nga 4 lojtare. Qellimi eshte te gjejme numrin maksimal te javeve ku mund te planifikohen lojerat ne menyre qe dy lojtare te mos luajne se bashku ne te njejtin grup me shume se nje here.
- **Generalizimi**: Per n = g × p lojtare (ku g eshte numri i grupeve dhe p eshte madhesia e grupit), a eshte e mundur te planifikohen w jave pa perseritje te çifteve ne grupe?


## Modelimi i Problemit
Problemi modelizohet si nje problem kerkimi ne hapesire gjendjesh (state-space search), por mund te formalizohet matematikisht duke perdorur koncepte nga teoria e grupeve, kombinatorika dhe dizajni i blloqeve. Ne veçanti, ai eshte i ngjashem me nje **resolvable pairwise balanced design (RPBD)** ose nje variant te **balanced incomplete block design (BIBD)** ku çdo çift lojtaresh bashkohet se shumti nje here.

### Formalizimi Matematikor
- **Bashkesia e lojtareve**: Le te jete V = {0, 1, …, 31} bashkesia e lojtareve (v = 32).
- **Grupet**: Çdo grup eshte nje nenbashkesi G ⊆ V me |G| = k = 4.
- **Java**: Nje jave W eshte nje ndarje e V ne g = v / k = 8 grupe te pavarura:  
  W = {G₁, G₂, …, G₈},  
  ku G₁ ∪ G₂ ∪ … ∪ G₈ = V dhe Gᵢ ∩ Gⱼ = ∅ per i ≠ j.
- **Orari (Schedule)**: Orari eshte nje sekuence javesh  
  S = {W₁, W₂, …, W_w},  
  ku per çdo çift lojtaresh {i, j} ⊆ V (i ≠ j), ekziston se shumti nje grup G ne te gjithe S qe permban {i, j}.  
  Kjo do te thote qe çdo çift shfaqet maksimum nje here ne te gjitha javet.

---

### Kufizimi kryesor (pa perseritje)

```
Per çdo i < j ∈ V:
Σ (t=1→w) Σ (m=1→g) I[{i,j} ⊆ Gₜ,ₘ] ≤ 1
```

ku Gₜ,ₘ eshte grupi m ne javen t, dhe I eshte funksioni indikator (1 nese e vertete, 0 perndryshe).

---

### Qellimi
Maksimizo numrin e javeve **w**, subjekt i kufizimeve te mesiperme:

- Çdo jave mbulon te gjithe lojtaret: |Wₜ| = 8, dhe Σₘ |Gₜ,ₘ| = 32.  
- Çdo lojtar luan saktesisht nje here ne jave: per çdo t dhe çdo i, ekziston saktesisht nje m ku i ∈ Gₜ,ₘ.

---

### Kufiri i siperm teorik
Numri maksimal i javeve eshte i kufizuar nga numri i çifteve qe nje lojtar mund te kete pa perseritje.  
Nje lojtar luan me (k−1) = 3 te tjere çdo jave, dhe ka (v−1) = 31 te tjere ne total.

Pra:

```
w ≤ ⌊(v−1) / (k−1)⌋ = ⌊31 / 3⌋ = 10
```

---

### Modelimi si problem optimizimi (Integer Programming)
Mund te modelizohet si nje problem programimi integer (IP) me variabla binare:

```
xₜ,ₘ,ᵢ = 1  nese lojtari i eshte ne grupin m te javes t
```

**Kufizime:**

1. Σᵢ xₜ,ₘ,ᵢ = 4  (madhesia e grupit)  
2. Σₘ xₜ,ₘ,ᵢ = 1  (çdo lojtar ne nje grup per jave)  
3. Per çdo çift {i, j}: Σₜ,ₘ (xₜ,ₘ,ᵢ × xₜ,ₘ,ⱼ) ≤ 1

---

## Reprezentimi i Problemit
- **Variablat (Variables)**:
  - Grupet per çdo jave: 8 grupe me nga 4 lojtare secila.
  - Set `played_together` qe permban te gjitha çiftet e lojtareve qe kane luajtur bashke.
- **Domeni (Domain)**:
  - Lojtaret: {0, 1, …, 31}
  - Grupet: te gjitha kombinimet e mundshme te 4 lojtareve pa perseritje çiftesh.
- **Gjendja fillestare (Initial State)**: orar bosh dhe set bosh i çifteve.
- **Funksioni i suksesit (Successor Function)**: shton nje grup te ri ne javen e radhes nese eshte valid.
- **Testi i qellimit (Goal Test)**: nese numri i javeve arrin vleren target.
- **Kostoja (Cost)**: uniforme (1 per çdo hap).


```


## Kompleksiteti i Kohes dhe Hapesires

**Kompleksiteti i Kohes:**
- Per DFS/DLS: O(b^d), ku b eshte faktori i degezimit dhe d numri i javeve.
- Per 32 lojtare dhe 7 jave, hapesira e kerkimit eshte rreth 10²⁰ ose me shume pa pruning.
- Backtracking redukton ndjeshem deget invalide.
- Ne praktike, per timeout 300s, zakonisht arrihen 6–7 jave.

**Kompleksiteti i Hapesires:**
- O(d × g × p) per orarin (d = jave, g = grupe, p = lojtare)
- Plus O(n² / 2) per setin e çifteve (maksimum 496 per 32 lojtare)
- Stack i rekursionit: O(d) per DLS, O(num_golfers) per DFS ne nivel grupi.
- Koha eshte bottleneck-i kryesor, jo memoria.

---
