const TOKEN_KEY = "phungu_admin_token";

function getToken() {
  return localStorage.getItem(TOKEN_KEY) || "";
}

function setToken(t) {
  if (t) localStorage.setItem(TOKEN_KEY, t);
  else localStorage.removeItem(TOKEN_KEY);
}

function authHeaders() {
  const t = getToken();
  return t ? { Authorization: `Bearer ${t}` } : {};
}

function showAuthPrompt() {
  const token = prompt("Admin token required:");
  if (token !== null) setToken(token);
}

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json", ...authHeaders(), ...(opts.headers || {}) },
    ...opts,
  });
  if (res.status === 401) {
    showAuthPrompt();
    throw new Error("Unauthorized");
  }
  if (res.status === 503) {
    throw new Error("Admin token not configured");
  }
  return res.json();
}

// --- Tabs ---
document.querySelectorAll(".nav-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".nav-btn").forEach((b) => b.classList.remove("active"));
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("active"));
    btn.classList.add("active");
    document.getElementById(`tab-${btn.dataset.tab}`).classList.add("active");
    refresh();
  });
});

// --- Health ---
async function loadHealth() {
  try {
    const h = await api("/health");
    const badge = document.getElementById("status-badge");
    badge.textContent = h.status;
    badge.className = `badge ${h.status}`;
    document.getElementById("health-info").innerHTML = `
      <table>
        <tr><th>Status</th><td>${h.status}</td></tr>
        <tr><th>Provider</th><td>${h.provider}</td></tr>
        <tr><th>Model</th><td>${h.model}</td></tr>
        <tr><th>Database</th><td>${h.database}</td></tr>
      </table>`;
  } catch (e) {
    document.getElementById("health-info").innerHTML = `<p class="empty">Error: ${e.message}</p>`;
  }
}

// --- Providers ---
async function loadProviders() {
  try {
    const data = await api("/api/providers");
    const rows = data.providers
      .map(
        (p) => `<tr>
          <td>${p.name}</td>
          <td>${p.enabled ? "yes" : "no"}</td>
          <td><span class="tag ${p.available ? "available" : "unavailable"}">${p.available ? "available" : "unavailable"}</span></td>
          <td>${p.model}</td>
          <td class="muted">${p.base_url}</td>
        </tr>`
      )
      .join("");
    document.getElementById("providers-list").innerHTML = `
      <table>
        <thead><tr><th>Name</th><th>Enabled</th><th>Status</th><th>Model</th><th>Base URL</th></tr></thead>
        <tbody>${rows || '<tr><td colspan="5" class="empty">No providers configured</td></tr>'}</tbody>
      </table>`;
  } catch (e) {
    document.getElementById("providers-list").innerHTML = `<p class="empty">Error: ${e.message}</p>`;
  }
}

// --- Sessions ---
async function loadSessions() {
  try {
    const data = await api("/admin/sessions");
    const rows = (data.sessions || [])
      .map((s) => `<tr><td><code>${s}</code></td><td>${s}</td></tr>`)
      .join("");
    document.getElementById("sessions-list").innerHTML = `
      <table>
        <thead><tr><th>Session ID</th><th></th></tr></thead>
        <tbody>${rows || '<tr><td colspan="2" class="empty">No active sessions</td></tr>'}</tbody>
      </table>`;
  } catch (e) {
    document.getElementById("sessions-list").innerHTML = `<p class="empty">Error: ${e.message}</p>`;
  }
}

document.getElementById("clear-session-btn").addEventListener("click", async () => {
  const sid = document.getElementById("session-id-input").value.trim();
  if (!sid) {
    alert("Enter a session ID");
    return;
  }
  try {
    await api(`/admin/session/${encodeURIComponent(sid)}/clear`, { method: "POST" });
    alert(`Cleared ${sid}`);
    loadSessions();
  } catch (e) {
    alert(e.message);
  }
});

async function refresh() {
  await Promise.all([loadHealth(), loadProviders(), loadSessions()]);
}

refresh();