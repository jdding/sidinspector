const PYODIDE_BASE = "https://cdn.jsdelivr.net/pyodide/v314.0.7/full/";
const FILES = [
  "RELEASE_STATUS.json",
  "src/sidinspector/pure_diagnostics.py",
  "demo/browser_example.py",
  "tools/build_paper_tables.py",
  "examples/reviewer_quickstart_data/sid_codes.csv",
  "examples/reviewer_quickstart_data/interactions.csv",
  "examples/reviewer_quickstart_data/item_metadata.csv",
  "docs/reproducibility/table2_musical_diagnostic.csv",
  "docs/reproducibility/table3_probe_calibration.csv",
  "docs/reproducibility/official_adapter_metrics_snapshot.csv",
  "docs/reproducibility/extension_checks_snapshot.csv",
  "docs/reproducibility/sources/grid_ft_seed_summary.csv",
  "docs/reproducibility/sources/grid_resid_comparison.csv",
  "docs/reproducibility/sources/control_summary.csv",
  "docs/reproducibility/sources/rqmin_reference.csv",
  "docs/reproducibility/sources/controller_qualified_aliasing.csv",
  "docs/reproducibility/sources/controller_capacity_budget.csv",
  "docs/reproducibility/sources/controller_variable_depth.csv",
  "docs/reproducibility/sources/grid_cap_metrics/coverage_report.csv",
  "docs/reproducibility/sources/grid_cap_metrics/d2_collision.csv",
  "docs/reproducibility/sources/grid_cap_metrics/d3_alignment.csv",
  "docs/reproducibility/sources/grid_cap_metrics/d4_head_tail.csv",
  "docs/reproducibility/sources/grid_cap_metrics/d5a_deployment_cost.csv",
];

let runtime;

async function initialize(base) {
  postMessage({type: "progress", message: "Loading pinned Pyodide Python 3.14 runtime in your browser…"});
  const {loadPyodide} = await import(PYODIDE_BASE + "pyodide.mjs");
  const python = await loadPyodide({indexURL: PYODIDE_BASE});
  const response = await fetch(new URL("PACKAGE_MANIFEST.json", base));
  if (!response.ok) throw new Error("PACKAGE_MANIFEST.json is unavailable.");
  const manifest = await response.json();
  const hashes = new Map(manifest.files.map(row => [row.path, row.sha256]));

  postMessage({type: "progress", message: `Verifying SHA-256 hashes for ${FILES.length} release files…`});
  for (const path of FILES) {
    const resource = await fetch(new URL(path, base));
    if (!resource.ok) throw new Error("Could not load " + path);
    const bytes = new Uint8Array(await resource.arrayBuffer());
    const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", bytes));
    const actual = Array.from(digest, byte => byte.toString(16).padStart(2, "0")).join("");
    if (hashes.get(path) !== actual) throw new Error("SHA-256 integrity check failed: " + path);
    const target = "/sidinspector/" + path;
    python.FS.mkdirTree(target.slice(0, target.lastIndexOf("/")));
    python.FS.writeFile(target, bytes);
  }
  return python;
}

self.onmessage = async event => {
  try {
    const base = new URL("../", self.location.href);
    runtime ??= initialize(base);
    const python = await runtime;

    if (event.data.type === "audit_custom") {
      postMessage({type: "custom_progress", message: "Running D1–D5 preflight and diagnostics client-side…"});
      python.globals.set("_BYO_SID_CSV", event.data.sidCsv || "");
      python.globals.set("_BYO_INTER_CSV", event.data.interactionsCsv || "");
      python.globals.set("_BYO_META_CSV", event.data.metadataCsv || "");
      const out = await python.runPythonAsync(`
import json, runpy
mod = runpy.run_path('/sidinspector/demo/browser_example.py')
json.dumps(mod['audit_custom_csv'](_BYO_SID_CSV, _BYO_INTER_CSV, _BYO_META_CSV))
`);
      postMessage({type: "custom_result", result: JSON.parse(out)});
      return;
    }

    postMessage({type: "progress", message: "Running D1–D6 diagnostics and verifying CIKM '26 Tables 2 & 3…"});
    const result = await python.runPythonAsync(`
import json, runpy
mod = runpy.run_path('/sidinspector/demo/browser_example.py')
json.dumps(mod['run_example']())
`);
    postMessage({type: "result", result: JSON.parse(result)});
  } catch (error) {
    if (event.data.type === "audit_custom") {
      postMessage({type: "custom_error", message: String(error.message || error)});
    } else {
      runtime = undefined;
      postMessage({type: "error", message: String(error.message || error)});
    }
  }
};
