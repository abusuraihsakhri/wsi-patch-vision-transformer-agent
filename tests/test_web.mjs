import test from "node:test";
import assert from "node:assert/strict";
import {evaluateLocal} from "../web/app.mjs";

const sample = {
  task_id: "T-1", target_identifier: "SPEC-1", primary_metric: 5,
  secondary_metric: 3, status_descriptor: "NOMINAL", is_critical_flag: false
};
test("routine threshold path is stable", () => {
  const result = evaluateLocal(sample);
  assert.equal(result.overall_urgency, "ROUTINE");
  assert.equal(result.total_alerts, 0);
  assert.equal(result.audit_hash, null);
});
test("critical flag dominates other warnings", () => {
  const result = evaluateLocal({...sample, primary_metric: 30, is_critical_flag: true});
  assert.equal(result.overall_urgency, "CRITICAL_STAT_PANIC");
  assert.equal(result.critical_alerts_count, 1);
  assert.equal(result.total_alerts, 2);
});
test("secondary breach produces elevated rather than critical outcome", () => {
  const result = evaluateLocal({...sample, secondary_metric: 13});
  assert.equal(result.overall_urgency, "ELEVATED_RISK");
});
test("descriptor keyword raises alert", () => {
  const result = evaluateLocal({...sample, status_descriptor: "DISCORDANT"});
  assert.equal(result.total_alerts, 1);
});
test("rejects nonfinite and sensitive identifiers", () => {
  assert.throws(() => evaluateLocal({...sample, primary_metric: Infinity}), /finite/);
  assert.throws(() => evaluateLocal({...sample, task_id: "MRN-123456"}), /personal identifier/);
  assert.throws(() => evaluateLocal({...sample, task_id: " "}), /required/);
});
