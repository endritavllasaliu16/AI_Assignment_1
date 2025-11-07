# Social Golfers – Exhaustive Uninformed Search

This folder contains a pure backtracking solver for the classic Social Golfers Problem (SGP). The code in `social_golfers_solution.py` explores the search space only with uninformed depth-first strategies (standard DFS and depth-limited DFS) in an effort to schedule as many conflict-free weeks as possible.

## Mathematical Model

Let:

- \(G = \{0, 1, \dots, n-1\}\) be the set of golfers, with \(n = 32\).
- \(s = 4\) be the fixed group size, so each week contains \(m = n / s = 8\) groups.
- \(W = \{1, 2, \dots, T\}\) denote calendar weeks we attempt to schedule.

We seek a collection of groups \( \mathcal{P}_t = \{g_{t,1}, \dots, g_{t,m}\} \) for every week \(t \in W\) such that:

1. **Group formation**
   \[
   \forall t, \quad g_{t,k} \subseteq G, \ |g_{t,k}| = s, \text{ and } g_{t,i} \cap g_{t,j} = \varnothing \text{ for } i \neq j
   \]
   which implies \( \bigcup_{k=1}^{m} g_{t,k} = G \).

2. **Pairwise constraint**
   \[
   \forall t_1 < t_2, \ \forall a \neq b \in G,\quad \mathbf{1}[(a,b) \in g_{t_1,k}] + \mathbf{1}[(a,b) \in g_{t_2,\ell}] \le 1
   \]
   meaning any ordered pair of golfers can appear together in at most one group over all weeks.

3. **Objective**  
   Maximize \(T\) (the number of feasible weeks) under the above constraints.

## CSP Representation

The solver treats the problem as a constraint satisfaction problem:

- **Variables** – each slot \(x_{t,k,j}\) represents the golfer occupying position \(j \in \{1,\dots,s\}\) of group \(k \in \{1,\dots,m\}\) in week \(t\).
- **Domains** – \(D(x_{t,k,j}) = G\), i.e., any golfer can occupy any slot before constraints are applied.
- **Intra-week constraints**
  - *All-different per week*: every golfer must appear exactly once per week (implemented by tracking the `available` list while building a week).
  - *Group validity*: partial groups are checked via `is_valid_group` before committing.
- **Inter-week constraint**
  - `played_together` stores all unordered pairs already used; attempting to add a group violating this set triggers backtracking so that no pair repeats in later weeks.
- **Search control**
  - `_complete_group_exhaustive` performs DFS over combinations for a single group.
  - `_build_week_with_backtrack` stacks groups to form a week and unwinds when constraints fail.
  - `exhaustive_dfs` and `depth_limited_exhaustive` vary exploration order (through deterministic offsets/seeds) but remain uninformed—they never use heuristics or cost estimates.

## Time and Space Complexity

Let \(N = n\) golfers, \(S = s\) group size, \(M = N / S\) groups per week, and \(T\) the target depth (weeks).

- **Time (DFS / DLS)** – constructing a single week may enumerate up to
  \[
  \frac{N!}{(S!)^{M} \, M!}
  \]
  distinct partitions (number of set partitions into equal-sized groups). In the worst case, DFS explores that many combinations for every depth level, so the upper bound before pruning is
  \[
  O\!\left(\left(\frac{N!}{(S!)^{M} \, M!}\right)^{T}\right),
  \]
  which is exponential in both \(N\) and \(T\). Depth-limited search enforces \(T\) as a hard limit but shares the same branching behavior within the explored depth.
- **Space** – the algorithm keeps:
  - The current partial schedule containing at most \(T\) weeks, each storing \(N\) golfer ids ⇒ \(O(NT)\).
  - The recursion stack for DFS/DLS of depth \(O(NT)\) (per-slot decisions).
  - The `played_together` set storing at most \(\binom{N}{2}\) unordered pairs ⇒ \(O(N^{2})\).

Thus, asymptotically the space consumption is \(O(N^{2} + NT)\), dominated by the pair-tracking structure when \(T \le N\).

The actual runtime is far smaller than the worst case thanks to early pruning (rejecting invalid groups as soon as a conflicting pair appears), but the algorithm remains an uninformed exponential backtracking search.***
