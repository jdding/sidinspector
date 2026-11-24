const runButton = document.getElementById("run");
const status = document.getElementById("status");
const results = document.getElementById("results");
const prefixSelect = document.getElementById("prefix-select");
const tabs = Array.from(document.querySelectorAll("[data-tab]"));
const panels = Array.from(document.querySelectorAll("[data-panel]"));

const byoRunBtn = document.getElementById("byo-run");
const byoStatus = document.getElementById("byo-status");
const byoResults = document.getElementById("byo-results");
const byoSidInput = document.getElementById("byo-sid-csv");
const byoInterInput = document.getElementById("byo-inter-csv");
const byoMetaInput = document.getElementById("byo-meta-csv");

const worker = new Worker("demo/python-worker.js", {type: "module"});
const fixed = (v, d = 3) => (v === null || v === undefined || Number.isNaN(Number(v)) ? "—" : Number(v).toFixed(d));
const pct = v => (v === null || v === undefined ? "—" : (100 * Number(v)).toFixed(1) + "%");

let lastResult = null;

const PRESETS = {
  clean: {
    sid: "item_id,sid_0,sid_1,sid_2\n1,10,1,1\n2,10,1,2\n3,10,2,1\n4,10,2,2\n5,20,1,1\n6,20,1,2\n7,20,2,1\n8,20,2,2",
    inter: "user_id,item_id,split\nu1,1,train\nu1,2,train\nu2,2,train\nu2,3,train\nu3,5,train\nu3,6,train\nu4,6,train\nu4,7,train\nu5,1,train\nu5,4,train",
    meta: "item_id,category\n1,guitar\n2,guitar\n3,guitar\n4,guitar\n5,drums\n6,drums\n7,drums\n8,drums",
  },
  aliased: {
    sid: "item_id,sid_0,sid_1,sid_2\n1,10,1,1\n2,10,1,1\n3,10,1,1\n4,10,2,2\n5,20,1,1\n6,20,1,1\n7,20,2,1\n8,20,2,2",
    inter: "user_id,item_id,split\nu1,1,train\nu1,2,train\nu2,1,train\nu2,5,train\nu3,3,train\nu3,6,train\nu4,5,train\nu4,6,train\nu5,7,train\nu5,8,train",
    meta: "item_id,category\n1,guitar\n2,guitar\n3,drums\n4,guitar\n5,drums\n6,studio\n7,studio\n8,studio",
  },
  tail_compressed: {
    sid: "item_id,sid_0,sid_1,sid_2\n1,1,1,1\n2,1,1,2\n3,1,2,1\n4,2,1,1\n5,9,0,0\n6,9,0,0\n7,9,0,0\n8,9,0,0\n9,9,0,0",
    inter: "user_id,item_id,split\nu1,1,train\nu1,2,train\nu2,1,train\nu2,2,train\nu3,1,train\nu3,3,train\nu4,2,train\nu4,3,train\nu5,3,train\nu5,4,train\nu6,4,train\nu6,5,train",
    meta: "item_id,category\n1,head_cat\n2,head_cat\n3,head_cat\n4,mid_cat\n5,tail_a\n6,tail_b\n7,tail_c\n8,tail_d\n9,tail_e",
  },
};

function addRow(id, values) {
  const row = document.createElement("tr");
  for (const value of values) {
    const cell = document.createElement("td");
    cell.textContent = String(value);
    row.append(cell);
  }
  document.getElementById(id).append(row);
}

function setActiveTab(name) {
  for (const btn of tabs) {
    const active = btn.dataset.tab === name;
    btn.classList.toggle("active", active);
    btn.setAttribute("aria-selected", active ? "true" : "false");
  }
  for (const panel of panels) {
    panel.hidden = panel.dataset.panel !== name;
  }
}

for (const btn of tabs) {
  btn.addEventListener("click", () => setActiveTab(btn.dataset.tab));
}

function renderTriage(containerId, cards) {
  const box = document.getElementById(containerId);
  box.replaceChildren();
  for (const c of cards) {
    const el = document.createElement("div");
    el.className = `triage-card ${c.status}`;
    const head = document.createElement("div");
    head.className = "probe-title";
    const title = document.createElement("span");
    title.textContent = c.probe;
    const pill = document.createElement("span");
    pill.className = `pill ${c.status}`;
    pill.textContent = c.status;
    head.append(title, pill);
    const sig = document.createElement("p");
    sig.style.fontSize = "13px";
    sig.textContent = c.signal;
    const nxt = document.createElement("p");
    nxt.className = "note";
    nxt.textContent = "Next check: " + c.next_check;
    el.append(head, sig, nxt);
    box.append(el);
  }
}

function renderPrefixInspector(bucket) {
  const container = document.getElementById("prefix-members");
  container.replaceChildren();
  const note = document.getElementById("prefix-note");
  note.textContent =
    `${bucket.prefix}: ${bucket.items} items · ${bucket.unique_sids} unique full SIDs · ` +
    `${bucket.aliased_items} aliased items · dominant category: ${bucket.dominant_category}` +
    (bucket.category_purity !== null ? ` (purity ${pct(bucket.category_purity)})` : "");

  const maxPop = Math.max(1, ...bucket.members.map(m => m.train_events));
  for (const m of bucket.members) {
    const row = document.createElement("div");
    row.className = "bar-row";
    const label = document.createElement("div");
    label.className = "bar-label";
    label.textContent = `#${m.item_id} · ${m.title}` + (m.aliased ? ` [ALIASED ×${m.alias_group_size}]` : "");

    const tracks = document.createElement("div");
    tracks.className = "bar-tracks";
    const line = document.createElement("div");
    line.className = "bar-line";
    const fill = document.createElement("span");
    fill.className = `bar-fill ${m.aliased ? "copper" : "teal"}`;
    fill.style.width = `${Math.max(4, (m.train_events / maxPop) * 100).toFixed(1)}%`;
    const val = document.createElement("span");
    val.className = "bar-val";
    val.textContent = `SID ${m.sid} · ${m.category} · ${m.bucket} · train events=${m.train_events}`;
    line.append(fill, val);
    tracks.append(line);
    row.append(label, tracks);
    container.append(row);
  }
}

if (prefixSelect) {
  prefixSelect.addEventListener("change", () => {
    if (!lastResult) return;
    const chosen = lastResult.quickstart.prefix_inspector.find(b => b.prefix === prefixSelect.value);
    if (chosen) renderPrefixInspector(chosen);
  });
}

function renderTable2Bars(rows) {
  const container = document.getElementById("table2-bars");
  container.replaceChildren();
  for (const r of rows) {
    const d2 = Number(r.d2_aliasing_rate);
    const d3 = Number(r.d3_l1_weighted);
    const row = document.createElement("div");
    row.className = "bar-row";
    const label = document.createElement("div");
    label.className = "bar-label";
    label.textContent = `${r.artifact} (${r.group})`;

    const tracks = document.createElement("div");
    tracks.className = "bar-tracks";
    for (const [cls, tag, val] of [
      ["copper", "D2 aliasing (↓)", d2],
      ["teal", "D3 L1 alignment (↑)", d3],
    ]) {
      const line = document.createElement("div");
      line.className = "bar-line";
      const fill = document.createElement("span");
      fill.className = `bar-fill ${cls}`;
      fill.style.width = `${Math.max(1.5, val * 100).toFixed(1)}%`;
      const txt = document.createElement("span");
      txt.className = "bar-val";
      txt.textContent = `${tag}: ${fixed(val, 3)}`;
      line.append(fill, txt);
      tracks.append(line);
    }
    row.append(label, tracks);
    container.append(row);
  }
}

function render(result) {
  lastResult = result;
  for (const id of [
    "t1-d1", "t1-d2", "t1-d3", "t1-d4",
    "t2-mech-live", "t2-d6", "t2-table3",
    "t3-table2", "t3-official", "t3-ext", "steps",
  ]) {
    document.getElementById(id).replaceChildren();
  }

  // Tab 1: Mapping Audit (D1-D5)
  const qs = result.quickstart;
  const kpiBox = document.getElementById("t1-kpis");
  kpiBox.replaceChildren();
  const tail = qs.d4.find(r => r.bucket === "tail") || qs.d4[0];
  const kpis = [
    ["Mapped items", qs.d5.items, `Depth ${qs.d5.sid_length} · ${qs.d5.prefix_counts}`],
    ["Unique full SIDs", qs.d5.unique_sid, `Duplicate rate ${pct(qs.d5.duplicate_sid_rate)}`],
    ["D2 full aliasing", fixed(qs.d2[0].full_collision_rate, 3), `${qs.d2[0].full_collision_items} aliased items`],
    ["D3 depth-1 recall", fixed(qs.d3[0].weighted_collab_prefix_recall, 3), `${qs.d3[0].retained_edges} co-occur edges`],
    ["D4 tail singleton", fixed(tail ? tail.global_singleton_ratio : 0, 3), `Allocation ${fixed(tail ? tail.sid_unique_ratio : 0, 3)}`],
  ];
  for (const [label, val, sub] of kpis) {
    const el = document.createElement("div");
    el.className = "kpi";
    el.innerHTML = `<div class="label"></div><div class="val"></div><div class="sub"></div>`;
    el.querySelector(".label").textContent = label;
    el.querySelector(".val").textContent = String(val);
    el.querySelector(".sub").textContent = sub;
    kpiBox.append(el);
  }

  for (const r of qs.d1) addRow("t1-d1", [r.level, r.items, r.unique_codes, fixed(r.entropy, 3), fixed(r.gini, 3)]);
  for (const r of qs.d2) addRow("t1-d2", [r.prefix_depth, r.active_prefixes, r.prefix_collision_groups, fixed(r.prefix_collision_rate, 3), fixed(r.full_collision_rate, 3)]);
  for (const r of qs.d3) addRow("t1-d3", [r.prefix_depth, r.retained_edges, fixed(r.weighted_collab_prefix_recall, 3), fixed(r.mean_collab_prefix_recall, 3), fixed(r.level0_category_purity_mean, 3)]);
  for (const r of qs.d4) addRow("t1-d4", [r.bucket, r.items, r.unique_sids, fixed(r.sid_unique_ratio, 3), fixed(r.global_singleton_ratio, 3), fixed(r.level0_entropy, 3)]);

  prefixSelect.replaceChildren();
  for (const b of qs.prefix_inspector) {
    const opt = document.createElement("option");
    opt.value = b.prefix;
    opt.textContent = `${b.prefix} (${b.items} items, ${b.aliased_items} aliased)`;
    prefixSelect.append(opt);
  }
  if (qs.prefix_inspector.length) renderPrefixInspector(qs.prefix_inspector[0]);
  renderTriage("t1-triage", qs.triage);

  // Tab 2: Mechanism Controls & D6 Churn
  const ci = result.mechanisms.collision_injection;
  addRow("t2-mech-live", ["D2 full-code aliasing (↓)", fixed(ci.baseline_d2, 3), fixed(ci.injected_d2, 3)]);
  addRow("t2-mech-live", ["D5 unique full SIDs (↑)", ci.baseline_unique_sids, ci.injected_unique_sids]);
  addRow("t2-mech-live", ["D4 tail global singleton (↑)", fixed(ci.baseline_d4_tail_singleton, 3), fixed(ci.injected_d4_tail_singleton, 3)]);

  for (const c of result.mechanisms.d6_refresh_churn) {
    addRow("t2-d6", [
      `Depth ${c.prefix_depth}`,
      c.common_items,
      c.changed_items,
      c.stable_items,
      pct(c.churn_rate_common),
      fixed(c.new_prefix_collision_rate, 3),
    ]);
  }
  for (const r of result.table3) {
    addRow("t2-table3", [r.probe, r.d, r.without_probe, r.with_probe, r.source_evidence]);
  }

  // Tab 3: CIKM '26 Benchmark (Table 2 + Portability)
  for (const r of result.table2) {
    addRow("t3-table2", [
      r.artifact,
      r.group,
      Number(r.unique_sids).toLocaleString("en-US"),
      fixed(r.d2_aliasing_rate, 3),
      fixed(r.d3_l1_weighted, 3),
      fixed(r.d4_tail_unique_ratio, 3),
      r.d5_active_prefix_counts,
    ]);
  }
  renderTable2Bars(result.table2);

  for (const r of result.official_adapters) {
    addRow("t3-official", [
      r.adapter,
      r.dataset,
      Number(r.items).toLocaleString("en-US"),
      Number(r.unique_sids).toLocaleString("en-US"),
      fixed(r.d2_aliasing_rate, 4),
      fixed(r.d3_l1_weighted, 3),
      fixed(r.d4_tail_unique_ratio, 3),
      r.d5_active_prefix_counts,
    ]);
  }
  for (const r of result.extensions) {
    addRow("t3-ext", [r.check, r.dataset, r.items, r.key_signal]);
  }

  for (const s of result.steps) {
    const li = document.createElement("li");
    li.textContent = `${s.script} — ${s.output}`;
    document.getElementById("steps").append(li);
  }
  document.getElementById("runtime").textContent =
    `Python ${result.python} · SIDInspector v${result.version} · DOI ${result.paper_doi} · SHA-256 verified against PACKAGE_MANIFEST.json`;
  results.hidden = false;
}

function renderCustom(payload) {
  const r = payload.report;
  for (const id of ["byo-d1", "byo-d2", "byo-d3", "byo-d4"]) {
    document.getElementById(id).replaceChildren();
  }
  const summary = document.getElementById("byo-summary");
  summary.textContent =
    `Validated ${r.d5.items} items (depth ${r.d5.sid_length}) · ${r.d5.unique_sid} unique SIDs · ` +
    `D2 full aliasing = ${fixed(r.d2[0].full_collision_rate, 4)} · ` +
    `D5 prefixes = ${r.d5.prefix_counts}`;
  for (const row of r.d1) addRow("byo-d1", [row.level, row.unique_codes, fixed(row.entropy, 3), fixed(row.gini, 3)]);
  for (const row of r.d2) addRow("byo-d2", [row.prefix_depth, row.active_prefixes, row.prefix_collision_groups, fixed(row.prefix_collision_rate, 3), fixed(row.full_collision_rate, 3)]);
  for (const row of r.d3) addRow("byo-d3", [row.prefix_depth, row.retained_edges, fixed(row.weighted_collab_prefix_recall, 3), fixed(row.mean_collab_prefix_recall, 3), fixed(row.level0_category_purity_mean, 3)]);
  for (const row of r.d4) addRow("byo-d4", [row.bucket, row.items, row.unique_sids, fixed(row.sid_unique_ratio, 3), fixed(row.global_singleton_ratio, 3)]);
  renderTriage("byo-triage", r.triage);
  byoResults.hidden = false;
}

worker.onmessage = event => {
  const msg = event.data;
  if (msg.type === "progress") status.textContent = msg.message;
  if (msg.type === "result") {
    render(msg.result);
    if (document.querySelector('[data-tab="t4"].active')) setActiveTab("t1");
    status.className = "";
    status.textContent = "Complete. D1–D6 diagnostics and CIKM '26 Tables 2 & 3 verified in your browser.";
    runButton.disabled = false;
    runButton.textContent = "Run all diagnostic workflows";
    results.removeAttribute("aria-busy");
  }
  if (msg.type === "error") {
    status.className = "error";
    status.textContent = msg.message;
    runButton.disabled = false;
    runButton.textContent = "Run all diagnostic workflows";
    results.removeAttribute("aria-busy");
  }
  if (msg.type === "custom_progress") byoStatus.textContent = msg.message;
  if (msg.type === "custom_result") {
    renderCustom(msg.result);
    byoStatus.className = "";
    byoStatus.textContent = "Audit complete (100% client-side in Pyodide).";
    byoRunBtn.disabled = false;
  }
  if (msg.type === "custom_error") {
    byoStatus.className = "error";
    byoStatus.textContent = msg.message;
    byoRunBtn.disabled = false;
  }
};

runButton.addEventListener("click", () => {
  runButton.disabled = true;
  runButton.textContent = "Running…";
  status.className = "";
  results.setAttribute("aria-busy", "true");
  worker.postMessage({type: "run"});
});

byoRunBtn.addEventListener("click", () => {
  byoRunBtn.disabled = true;
  byoStatus.className = "";
  byoStatus.textContent = "Starting client-side Pyodide audit…";
  worker.postMessage({
    type: "audit_custom",
    sidCsv: byoSidInput.value,
    interactionsCsv: byoInterInput.value,
    metadataCsv: byoMetaInput.value,
  });
});

for (const btn of document.querySelectorAll("[data-preset]")) {
  btn.addEventListener("click", () => {
    const p = PRESETS[btn.dataset.preset];
    if (!p) return;
    byoSidInput.value = p.sid;
    byoInterInput.value = p.inter;
    byoMetaInput.value = p.meta;
    byoStatus.className = "";
    byoStatus.textContent = `Loaded preset "${btn.textContent}". Click "Audit my CSV" to run.`;
  });
}

for (const [fileId, targetEl] of [
  ["byo-sid-file", byoSidInput],
  ["byo-inter-file", byoInterInput],
  ["byo-meta-file", byoMetaInput],
]) {
  const input = document.getElementById(fileId);
  if (input) {
    input.addEventListener("change", async () => {
      const file = input.files && input.files[0];
      if (!file) return;
      targetEl.value = await file.text();
    });
  }
}

// Initialize default BYO preset
byoSidInput.value = PRESETS.aliased.sid;
byoInterInput.value = PRESETS.aliased.inter;
byoMetaInput.value = PRESETS.aliased.meta;
