# External Review Prompt Round 1

Use only after explicit egress approval from the user.

System:

You are a senior CIKM Resource Track reviewer with recommender-systems and
generative retrieval expertise. Review the manuscript as a resource/toolkit
paper, not as a full research paper proposing a new tokenizer.

User prompt:

Please review the current AUDIT-SID manuscript for CIKM 2026 Resource Track.
The target is a high-confidence resource-paper submission, estimated score
7.5+/10.

Judge only what is visible in the manuscript. Do not assume unreported
experiments. Be strict about artifact usability, coverage, reproducibility,
figure/table clarity, and claim/evidence alignment.

Required output:

1. Overall score from 0 to 10, where 6 is weak accept, 7 is accept, and 8 is
   strong accept for a resource-track paper.
2. Resource-track verdict: reject / borderline / weak accept / accept / strong
   accept.
3. Top strengths, ranked.
4. Top weaknesses, ranked as P0/P1/P2.
5. For each P0/P1 issue, give a concrete fix that can be implemented in the
   current paper or artifact package.
6. Identify any claim overreach, proxy misattribution, missing caveat, or
   reviewer attack surface.
7. Review Fig. 1 and Tables 1-3: does each have a clear reader takeaway, enough
   evidence density, and a caption that matches the claim?
8. State the minimum changes needed to reach 7.5+/10.

Manuscript files to review in the repository:

- `paper/main.tex`
- `paper/sections/1_introduction.tex`
- `paper/sections/2_toolkit.tex`
- `paper/sections/3_resource_demo.tex`
- `paper/sections/4_availability_limits.tex`
- `paper/main.pdf`
- `paper/figures/fig1_audit_sid_pipeline.pdf`

Context files allowed:

- `docs/PAPER_STRICT_CLAIM_AUDIT.md`
- `docs/SID_CLUSTER_DIAGNOSTIC_REFRESH.md`
- `docs/CURRENT_STATE.md`

Do not request downstream Recall/NDCG as a blocker unless the current paper
claims downstream system quality. It does not; it claims artifact diagnostics.
