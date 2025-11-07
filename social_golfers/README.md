# Social Golfers Problem - README.md

## Përshkrimi i Problemit
Problemi i Golfistëve Socialë (Social Golfers Problem) është një problem klasik i planifikimit dhe optimizimit në inteligjencën artificiale dhe shkencën kompjuterike. Ai konsiston në planifikimin e lojërave të golfit për një numër të caktuar lojtarësh, të organizuar në grupe, duke respektuar kufizime të caktuara.

- **Përshkrimi specifik**: Ka 32 lojtarë golfi që luajnë një herë në javë, në grupe me nga 4 lojtarë. Qëllimi është të gjejmë numrin maksimal të javëve ku mund të planifikohen lojërat në mënyrë që dy lojtarë të mos luajnë së bashku në të njëjtin grup më shumë se një herë.
- **Generalizimi**: Për n = g × p lojtarë (ku g është numri i grupeve dhe p është madhësia e grupit), a është e mundur të planifikohen w javë pa përsëritje të çifteve në grupe?

**Shembull**:
- Në javën 1: Grupet janë si në tabelën e dhënë (p.sh., Group 1: 0,1,2,3; Group 2: 4,5,22,23; etj.).

Problemi është NP-hard dhe kërkon teknika kërkimi për të gjetur zgjidhje të mundshme.

## Modelimi i Problemit
Problemi modelizohet si një problem kërkimi në hapësirë gjendjesh (state-space search), por mund të formalizohet matematikisht duke përdorur koncepte nga teoria e grupeve, kombinatorika dhe dizajni i blloqeve. Në veçanti, ai është i ngjashëm me një **resolvable pairwise balanced design (RPBD)** ose një variant të **balanced incomplete block design (BIBD)** ku çdo çift lojtarësh bashkohet së shumti një herë.

### Formalizimi Matematikor
- **Bashkësia e lojtarëve**: Le të jetë \( V = \{0, 1, \dots, 31\} \) bashkësia e lojtarëve (v = 32).
- **Grupet**: Çdo grup është një nënbashkësi \( G \subseteq V \) me \( |G| = k = 4 \).
- **Java**: Një javë \( W \) është një particion i \( V \) në g = v / k = 8 grupe të pavarura:  
  \( W = \{G_1, G_2, \dots, G_8\} \),  
  ku \( \bigcup_{i=1}^8 G_i = V \) dhe \( G_i \cap G_j = \emptyset \) për \( i \neq j \).
- **Orari**: Orari është një sekuencë javësh  
  \( S = \{W_1, W_2, \dots, W_w\} \),  
  ku për çdo çift lojtarësh \( \{i, j\} \subseteq V \) (i ≠ j), ekziston së shumti një grup \( G \) në të gjithë \( S \) që përmban \( \{i, j\} \). Kjo do të thotë që numri i bashkimeve të çdo çifti është \( \lambda_{ij} \leq 1 \).

**Kufizimi kryesor** (pa përsëritje):

\[
\forall i < j \in V, \quad \sum_{t=1}^w \sum_{m=1}^g \mathbb{I}_{\{i,j\} \subseteq G_{t,m}} \leq 1
\]

ku \( G_{t,m} \) është grupi m në javën t, dhe \( \mathbb{I} \) është funksioni indikator (1 nëse e vërtetë, 0 përndryshe).

**Qëllimi**: Maksimizo numrin e javëve w, subjekt i kufizimeve të mësipërme dhe:
- Çdo javë mbulon të gjithë lojtarët: \( |W_t| = 8 \), \( \sum_{m=1}^8 |G_{t,m}| = 32 \).
- Çdo lojtar luan saktësisht një herë në javë: Për çdo t dhe i, ekziston saktësisht një m ku \( i \in G_{t,m} \).

**Kufiri i sipërm teorik** (nga teoria e dizajnit të blloqeve):
Numri maksimal i javëve është i kufizuar nga numri i çifteve të mundshme që një lojtar mund të ketë pa përsëritje. Për një lojtar të vetëm, ai luan me (k-1) = 3 të tjerë çdo javë, dhe ka (v-1) = 31 të tjerë në total, pra:

\[
w \leq \left\lfloor \frac{v-1}{k-1} \right\rfloor = \left\lfloor \frac{31}{3} \right\rfloor = 10
\]

Por në praktikë, për (g=8, p=4), zgjidhja e njohur maksimale është w=9 ose 10, varësisht nga literatura (për 32 lojtarë, maksimumi është 9).

**Modelimi si problem optimizimi (Integer Programming - opsional për përshkrim)**:
Mund të modelizohet si IP duke përdorur variablat binare:
- \( x_{t,m,i} = 1 \) nëse lojtari i është në grupin m të javës t.
- Kufizime:
  - \( \sum_{i} x_{t,m,i} = 4 \) (madhësia e grupit).
  - \( \sum_{m} x_{t,m,i} = 1 \) (çdo lojtar në një grup për javë).
  - Për çiftet: \( \sum_{t,m} x_{t,m,i} \cdot x_{t,m,j} \leq 1 \) për çdo {i,j}.

Por ky model është i rëndë kompjuterikisht, prandaj përdoren metoda kërkimi si DFS dhe DLS.

- **Gjendja (State)**: Përfaqëson orarin aktual \( S \), setin e çifteve të përdorura \( P = \{\{i,j\} \mid \exists G \in S: \{i,j\} \subseteq G\}\).
- **Operacionet (Actions)**: Shto një grup të ri \( G \) në një javë të re, nëse \( G \) nuk përmban asnjë çift nga P.
- **Testi i qëllimit**: \( |S| = w \) (target).

Problemi mund të shihet gjithashtu si ngjyrimi i grafit të çifteve ose si mbulim i skajeve me kliqe të madhësisë 4.

## Reprezentimi i Problemit
- **Variablat (Variables)**: 
  - Variablat kryesore janë grupet për çdo javë. Për çdo javë, kemi 8 grupe (pasi 32 / 4 = 8), dhe çdo grup është një listë me 4 lojtarë (numra nga 0 deri në 31).
  - Një variabël ndihmës është seti i çifteve që kanë luajtur së bashku (`played_together`), i cili është një set tuplesh të renditura (p.sh., (1,2)).
- **Domeni (Domain)**: 
  - Për çdo lojtar, domeni është {0, 1, ..., 31}.
  - Për grupe, domeni është të gjitha kombinimet e mundshme të 4 lojtarëve nga të disponueshmit, duke respektuar kufizimet (pa çifte të përsëritura).
- **Gjendja fillestare (Initial State)**: Orar bosh (pa javë), set bosh i çifteve.
- **Funksioni i suksesit (Successor Function)**: Gjeneron gjendje të reja duke shtuar një grup të ri ose një javë të re, duke kontrolluar validitetin me `is_valid_group`.
- **Testi i qëllimit (Goal Test)**: Nëse numri i javëve arrin targetin (p.sh., 7) pa konflikte.
- **Kostoja (Cost)**: Uniforme (çdo hap ka kosto 1), por në praktikë, nuk përdoret pasi është kërkim pa informacion.

Reprezentimi përdor struktura të dhënash si lista për orarin (`schedule: List[List[List[int]]]`), lista për lojtarët e disponueshëm, dhe sete për çiftet për efikasitet O(1) në kontroll.

## Implementimi i Depth First Search (DFS) me Backtracking
DFS me backtracking implementohet në metodën `exhaustive_dfs` dhe funksionet ndihmës si `_build_schedule_exhaustive`, `_build_week_with_backtrack`, dhe `_complete_group_exhaustive`.

- **Algoritmi**:
  - Fillimisht, resetohet seti i çifteve.
  - Për secilën javë, ndërtohet një javë e re duke zgjedhur grupe me backtracking.
  - Përdoret rekursion për të plotësuar grupet duke provuar të gjitha kombinimet e mundshme të lojtarëve.
  - Nëse një grup nuk është valid (ka çifte të përsëritura), backtrack (hiq grupin dhe provoj tjetër).
  - Provohet në renditje të ndryshme duke përdorur një "seed" për të eksploruar degë të ndryshme të pemës së kërkimit.
  - Ndërpritet nëse arrin targetin ose timeout.

- **Kodi kryesor** (pjesë nga kodi i dhënë):
  ```python
  def exhaustive_dfs(self, target_weeks: int, timeout: int = 300) -> List[List[List[int]]]:
      # ... (kodi si në skedar)
  ```

Kjo është një version exhaustive i DFS, pa heuristikë, por me provë të renditjeve të ndryshme për të qenë më thorough.

## Implementimi i Depth Limited Search (DLS) me Backtracking
DLS me backtracking implementohet në metodën `depth_limited_exhaustive` dhe `_dls_recursive`.

- **Algoritmi**:
  - Si DFS, por me limit në thellësi (numri i javëve = max_depth).
  - Rekursion në nivel javësh: Shto një javë, rekurso për javën tjetër, nëse dështon backtrack duke hequr çiftet.
  - Përdor offset për të variuar rendin e zgjedhjes së lojtarëve.
  - Provohet në tentativa të shumta (p.sh., 50) për të eksploruar rrugë të ndryshme.
  - Ndërpritet nëse arrin thellësinë maksimale ose timeout.

- **Kodi kryesor** (pjesë nga kodi i dhënë):
  ```python
  def depth_limited_exhaustive(self, target_weeks: int, timeout: int = 300) -> List[List[List[int]]]:
      # ... (kodi si në skedar)
  ```

Kjo kufizon thellësinë për të shmangur kërkimin e pafund, por ende është exhaustive brenda limitit.

## Kompleksiteti i Kohës dhe Hapësirës
- **Kompleksiteti i Kohës**:
  - Për DFS dhe DLS: Në rastin më të keq, O(b^d), ku b është faktori i degëzimit (numri i kombinimeve të mundshme për grupe, i cili është C(32,4) për grupin e parë, etj., por reduktohet me backtracking), dhe d është thellësia (numri i javëve).
  - Për 32 lojtarë dhe 7 javë, hapësira e kërkimit është e madhe (rreth 10^20 ose më shumë pa pruning), por backtracking redukton duke prerë degë invalide. Në praktikë, me timeout 300s, arrihet deri në 6-7 javë varësisht nga renditja.
  - Exhaustive provon tentativa të shumta, duke rritur kohën lineare me numrin e tentativave (p.sh., 100 x koha e një DFS).

- **Kompleksiteti i Hapësirës**:
  - O(d * g * p) për orarin (d javë, g grupe, p lojtarë), plus O(n^2 / 2) për setin e çifteve (maksimum 32*31/2 = 496 çifte).
  - Stack i rekursionit: O(d) për DLS (thellësia e limituar), O(num_golfers) për DFS në nivel grupi.
  - Në përgjithësi, hapësira është modeste (nuk ruhet e tërë pema), por koha është bottleneck për instanca të mëdha.
