/* Deterministic local demonstration of agents/workers.py. No slide/image inference. */
const forbidden = [
  /\bMRN[:#\s-]*\d{4,10}\b/i,
  /\b\d{3}-\d{2}-\d{4}\b/,
  /\b(?:\+?1[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b/,
  /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/,
  /\b(?:DOB|Date of Birth)[:\s]*\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b/i,
  /\b(?:Patient\s+Name|Patient)[:\s]+[A-Z][a-z]+\s+[A-Z][a-z]+\b/i,
  /\b(?:John\s+Doe|Jane\s+Smith|Alice\s+Johnson)\b/i
];
const urgency = { routine: "ROUTINE", elevated: "ELEVATED_RISK", critical: "CRITICAL_STAT_PANIC" };
export function evaluateLocal(payload) {
  for (const name of ["task_id", "target_identifier", "status_descriptor"]) {
    if (typeof payload[name] !== "string" || !payload[name].trim()) {
      throw new Error(name + " is required.");
    }
    if (forbidden.some(pattern => pattern.test(payload[name]))) {
      throw new Error("Potential personal identifier detected; use synthetic identifiers only.");
    }
  }
  for (const name of ["primary_metric", "secondary_metric"]) {
    if (typeof payload[name] !== "number" || !Number.isFinite(payload[name])) {
      throw new Error(name + " must be a finite number.");
    }
  }
  if (typeof payload.is_critical_flag !== "boolean") {
    throw new Error("Critical flag must be a boolean.");
  }
  const alerts = [];
  const add = (origin_worker, level, summary, technical_details, actionable_remediation) => {
    alerts.push({origin_worker, urgency: level, summary, technical_details, actionable_remediation});
  };
  if (payload.primary_metric > 25) {
    add("InvariantQCWorker", urgency.elevated, "Primary Metric Threshold Exceeded",
      "Primary measurement (" + payload.primary_metric.toFixed(2) + ") exceeds configured threshold (25.00).",
      "Review input and assess the configured threshold.");
  }
  if (payload.is_critical_flag || payload.secondary_metric > 12) {
    add("SafetyEscalationWorker", payload.is_critical_flag ? urgency.critical : urgency.elevated,
      "Critical Safety Interlock Triggered",
      "CriticalFlag=" + payload.is_critical_flag + "; secondary index=" + payload.secondary_metric.toFixed(2) + ".",
      "Review flagged data and determine appropriate follow-up.");
  }
  if (["DISCORDANT","ANOMALY","MUTANT","VIOLATION","FAIL","REJECT"].some(word =>
      payload.status_descriptor.toUpperCase().includes(word))) {
    add("ProtocolConformanceWorker", urgency.elevated, "Protocol Conformance Discordance Detected",
      "Descriptor '" + payload.status_descriptor + "' contains an alert keyword.",
      "Review the descriptor and confirm the classification.");
  }
  const critical_alerts_count = alerts.filter(a => a.urgency === urgency.critical).length;
  const overall_urgency = critical_alerts_count ? urgency.critical :
    alerts.length ? urgency.elevated : urgency.routine;
  const integrity_status = critical_alerts_count ? "RECALIBRATION_REQUIRED" :
    alerts.length ? "DISCORDANT_ANOMALY" : "VALIDATED_OPTIMAL";
  return {
    evaluation_mode: "BROWSER_DEMONSTRATION",
    task_id: payload.task_id.trim(),
    target_identifier: payload.target_identifier.trim(),
    overall_urgency,
    integrity_status,
    total_alerts: alerts.length,
    critical_alerts_count,
    alerts,
    audit_hash: null,
    note: "Local deterministic threshold demonstration; no signed audit, WSI processing, or ViT inference."
  };
}
if (typeof document !== "undefined") {
  const byId = id => document.getElementById(id);
  const form = byId("audit-form");
  const output = byId("result");
  const status = byId("execution-status");
  const download = byId("download");
  let lastResult = null;
  form.addEventListener("submit", async event => {
    event.preventDefault();
    download.disabled = true;
    lastResult = null;
    try {
      for (const id of ["primary_metric", "secondary_metric"]) {
        if (!byId(id).value.trim()) throw new Error("Please enter both numeric measurements.");
      }
      const payload = {
        task_id: byId("task_id").value,
        target_identifier: byId("target_identifier").value,
        primary_metric: Number(byId("primary_metric").value),
        secondary_metric: Number(byId("secondary_metric").value),
        status_descriptor: byId("status_descriptor").value,
        is_critical_flag: byId("is_critical_flag").checked
      };
      // Reject obvious personal identifiers in either mode; not a comprehensive PHI detector.
      evaluateLocal(payload);
      const mode = byId("mode").value;
      let result;
      if (mode === "api") {
        const response = await fetch("./api/audit", {
          method: "POST",
          headers: {"Content-Type":"application/json"},
          body: JSON.stringify(payload)
        });
        if (!response.ok) {
          throw new Error("API request failed (HTTP " + response.status + "). Check server configuration and input.");
        }
        result = await response.json();
        result.evaluation_mode = "SERVER_API";
      } else {
        result = evaluateLocal(payload);
      }
      lastResult = result;
      output.textContent = JSON.stringify(result, null, 2);
      status.textContent = mode === "api" ? "Server evaluation complete" : "Local demonstration complete (unsigned)";
      download.disabled = false;
    } catch (error) {
      status.textContent = "Evaluation failed";
      output.textContent = String(error.message || error);
    }
  });
  download.addEventListener("click", () => {
    if (!lastResult) return;
    const objectUrl = URL.createObjectURL(new Blob([JSON.stringify(lastResult, null, 2)],
      {type:"application/json"}));
    const anchor = document.createElement("a");
    anchor.href = objectUrl;
    anchor.download = "wsi-threshold-evaluation.json";
    anchor.click();
    setTimeout(() => URL.revokeObjectURL(objectUrl), 500);
  });
}
