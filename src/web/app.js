async function jget(url) {
  const r = await fetch(url);
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

async function jpost(url, body) {
  const r = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

function fillTable(tableId, rows, mapper) {
  const body = document.querySelector(`#${tableId} tbody`);
  body.innerHTML = "";
  for (const row of rows) {
    const tr = document.createElement("tr");
    for (const col of mapper(row)) {
      const td = document.createElement("td");
      td.textContent = col;
      tr.appendChild(td);
    }
    if (tableId === "attendance-table") {
      tr.style.cursor = "pointer";
      tr.title = "Click to copy student id into override form";
      tr.addEventListener("click", () => {
        document.getElementById("ov-student-id").value = row.student_id || "";
      });
    }
    body.appendChild(tr);
  }
}

async function refreshPeriods() {
  const rows = await jget("/periods?limit=50");
  fillTable("periods-table", rows, (r) => [
    String(r.period_id),
    r.class_id,
    r.status,
    r.started_at || "",
    r.ended_at || "",
  ]);
}

async function loadAttendance(periodId) {
  const rows = await jget(`/periods/${periodId}/attendance`);
  fillTable("attendance-table", rows, (r) => [
    r.student_id,
    r.full_name,
    `${r.detections_count}/${r.checks_count}`,
    `${Math.round((r.detection_ratio || 0) * 100)}%`,
    r.ai_status,
    r.final_status,
  ]);
}

document.getElementById("run-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const status = document.getElementById("run-status");
  status.textContent = "Running period. Wait for completion...";
  try {
    const payload = {
      class_id: document.getElementById("class-id").value.trim(),
      duration_minutes: Number(document.getElementById("duration").value),
      checks_count: Number(document.getElementById("checks").value),
      threshold: Number(document.getElementById("threshold").value),
      min_instances: Number(document.getElementById("min-instances").value),
      seconds_per_minute: Number(document.getElementById("spm").value),
    };
    const out = await jpost("/periods/run", payload);
    status.textContent = `Completed. period_id=${out.period_id}`;
    document.getElementById("period-id").value = String(out.period_id);
    document.getElementById("ov-period-id").value = String(out.period_id);
    await refreshPeriods();
    await loadAttendance(out.period_id);
  } catch (err) {
    status.textContent = `Run failed: ${err.message}`;
  }
});

document.getElementById("refresh-periods").addEventListener("click", async () => {
  try {
    await refreshPeriods();
  } catch (err) {
    alert(err.message);
  }
});

document.getElementById("load-period").addEventListener("click", async () => {
  const periodId = Number(document.getElementById("period-id").value);
  if (!periodId) return;
  document.getElementById("ov-period-id").value = String(periodId);
  try {
    await loadAttendance(periodId);
  } catch (err) {
    alert(err.message);
  }
});

document.getElementById("override-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const msg = document.getElementById("ov-status-msg");
  const btn = e.target.querySelector("button[type='submit']");
  try {
    const periodId = Number(document.getElementById("ov-period-id").value);
    const studentId = document.getElementById("ov-student-id").value.trim();
    if (!periodId) throw new Error("Enter valid Period ID.");
    if (!studentId) throw new Error("Enter valid Student ID.");
    const payload = {
      student_id: studentId,
      new_status: document.getElementById("ov-status").value,
      lecturer: document.getElementById("ov-lecturer").value.trim(),
      reason: document.getElementById("ov-reason").value.trim(),
    };
    btn.disabled = true;
    await jpost(`/periods/${periodId}/override`, payload);
    msg.textContent = "Override applied.";
    await loadAttendance(periodId);
  } catch (err) {
    msg.textContent = `Override failed: ${err.message}`;
  } finally {
    btn.disabled = false;
  }
});

refreshPeriods().catch(console.error);
