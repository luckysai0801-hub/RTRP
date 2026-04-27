document.addEventListener("DOMContentLoaded", () => {
  const currentPath = window.location.pathname;
  document.querySelectorAll(".nav-links a").forEach((link) => {
    if (link.getAttribute("href") === currentPath) {
      link.classList.add("active");
    }
  });

  const tabLogin = document.getElementById("tab-login");
  const tabSignup = document.getElementById("tab-signup");
  const formLogin = document.getElementById("form-login");
  const formSignup = document.getElementById("form-signup");

  if (tabLogin && tabSignup && formLogin && formSignup) {
    tabLogin.addEventListener("click", () => switchTab("login"));
    tabSignup.addEventListener("click", () => switchTab("signup"));
  }

  function switchTab(tab) {
    const isLogin = tab === "login";
    tabLogin.classList.toggle("tab-active", isLogin);
    tabSignup.classList.toggle("tab-active", !isLogin);
    formLogin.style.display = isLogin ? "block" : "none";
    formSignup.style.display = isLogin ? "none" : "block";
    clearAlerts();
  }

  const loginForm = document.getElementById("login-form-el");
  if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const btn = loginForm.querySelector('button[type="submit"]');
      setLoading(btn, true);

      try {
        const res = await fetch("/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: document.getElementById("login-email").value.trim(),
            password: document.getElementById("login-password").value,
          }),
        });
        const data = await res.json();
        if (res.ok && data.status === "success") {
          showAlert("login-alert", "success", "Login successful. Redirecting...");
          window.setTimeout(() => {
            window.location.href = data.redirect || "/dashboard";
          }, 900);
        } else {
          showAlert("login-alert", "error", data.message || "Login failed.");
        }
      } catch (error) {
        showAlert("login-alert", "error", "Server error. Please try again.");
      } finally {
        setLoading(btn, false);
      }
    });
  }

  const signupForm = document.getElementById("signup-form-el");
  if (signupForm) {
    signupForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const btn = signupForm.querySelector('button[type="submit"]');
      setLoading(btn, true);

      try {
        const res = await fetch("/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: document.getElementById("signup-name").value.trim(),
            roll_number: document.getElementById("signup-roll").value.trim(),
            email: document.getElementById("signup-email").value.trim(),
            password: document.getElementById("signup-password").value,
          }),
        });
        const data = await res.json();
        if (res.ok && data.status === "success") {
          showAlert("signup-alert", "success", "Account created. You can log in now.");
          signupForm.reset();
          window.setTimeout(() => switchTab("login"), 1000);
        } else {
          showAlert("signup-alert", "error", data.message || "Signup failed.");
        }
      } catch (error) {
        showAlert("signup-alert", "error", "Server error. Please try again.");
      } finally {
        setLoading(btn, false);
      }
    });
  }

  const bars = document.querySelectorAll(".progress-fill");
  if (bars.length) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.style.width = entry.target.dataset.width || "0%";
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.3 });

    bars.forEach((bar) => {
      bar.style.width = "0%";
      observer.observe(bar);
    });
  }

  document.querySelectorAll("[data-count]").forEach((el) => {
    const target = parseInt(el.dataset.count || "0", 10);
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 40));
    const timer = window.setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        window.clearInterval(timer);
      }
      el.textContent = current;
    }, 20);
  });

  const exportBtn = document.getElementById("btn-export");
  if (exportBtn) {
    exportBtn.addEventListener("click", () => {
      window.location.href = "/export/reports.csv";
    });
  }

  const searchInput = document.getElementById("search-input");
  const reportsTable = document.getElementById("reports-table");
  const emptyState = document.getElementById("reports-empty");
  const reportSummary = document.getElementById("report-summary");
  if (searchInput && reportsTable) {
    const rows = Array.from(reportsTable.querySelectorAll("tbody tr"));
    const totalRows = rows.length;
    searchInput.addEventListener("input", () => {
      const term = searchInput.value.trim().toLowerCase();
      let visible = 0;
      rows.forEach((row) => {
        const matches = row.dataset.search.includes(term);
        row.style.display = matches ? "" : "none";
        if (matches) {
          visible += 1;
        }
      });
      if (emptyState) {
        emptyState.style.display = visible === 0 ? "block" : "none";
      }
      if (reportSummary) {
        reportSummary.textContent = `Showing ${visible} of ${totalRows} students · Sorted by Skill Score`;
      }
    });
  }

  const editProfileBtn = document.getElementById("edit-profile-btn");
  if (editProfileBtn) {
    editProfileBtn.addEventListener("click", () => {
      showToast("Profile editing can be the next feature. The core report flow is ready.");
    });
  }

  const shareReportBtn = document.getElementById("share-report-btn");
  if (shareReportBtn) {
    shareReportBtn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(window.location.href);
        shareReportBtn.textContent = "Link Copied";
        window.setTimeout(() => {
          shareReportBtn.textContent = "Share Report";
        }, 1500);
      } catch (error) {
        showToast("Could not copy the link automatically.");
      }
    });
  }

  const profileForm = document.getElementById("profile-form");
  if (profileForm) {
    profileForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const btn = profileForm.querySelector('button[type="submit"]');
      const originalLabel = btn.dataset.label || btn.textContent;
      setLoading(btn, true);
      try {
        const res = await fetch("/api/profile", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: document.getElementById("profile-name").value.trim(),
            headline: document.getElementById("profile-headline").value.trim(),
            department: document.getElementById("profile-department").value.trim(),
            semester: document.getElementById("profile-semester").value.trim(),
            skills: document.getElementById("profile-skills").value.trim(),
          }),
        });
        const data = await res.json();
        if (res.ok && data.status === "success") {
          showAlert("dashboard-alert", "success", data.message);
          window.setTimeout(() => window.location.reload(), 700);
        } else {
          showAlert("dashboard-alert", "error", data.message || "Profile update failed.");
        }
      } catch (error) {
        showAlert("dashboard-alert", "error", "Could not update profile.");
      } finally {
        btn.dataset.label = originalLabel;
        setLoading(btn, false);
      }
    });
  }

  const projectForm = document.getElementById("project-form");
  if (projectForm) {
    projectForm.addEventListener("submit", async (event) => {
      event.preventDefault();
      const btn = projectForm.querySelector('button[type="submit"]');
      const originalLabel = btn.dataset.label || btn.textContent;
      setLoading(btn, true);
      try {
        const res = await fetch("/api/projects", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            title: document.getElementById("project-title").value.trim(),
            description: document.getElementById("project-description").value.trim(),
            stack: document.getElementById("project-stack").value.trim(),
            status: document.getElementById("project-status").value,
          }),
        });
        const data = await res.json();
        if (res.ok && data.status === "success") {
          showAlert("dashboard-alert", "success", data.message);
          projectForm.reset();
          window.setTimeout(() => window.location.reload(), 700);
        } else {
          showAlert("dashboard-alert", "error", data.message || "Project upload failed.");
        }
      } catch (error) {
        showAlert("dashboard-alert", "error", "Could not add project.");
      } finally {
        btn.dataset.label = originalLabel;
        setLoading(btn, false);
      }
    });
  }

  const forgotPasswordLink = document.getElementById("forgot-password-link");
  if (forgotPasswordLink) {
    forgotPasswordLink.addEventListener("click", (event) => {
      event.preventDefault();
      showToast("Demo mode: use the seeded credentials or create a fresh account.");
    });
  }

  function showAlert(id, type, msg) {
    const el = document.getElementById(id);
    if (!el) {
      return;
    }
    el.className = `alert alert-${type} show`;
    el.textContent = msg;
  }

  function clearAlerts() {
    document.querySelectorAll(".alert").forEach((el) => {
      el.classList.remove("show");
    });
  }

  function setLoading(btn, loading) {
    if (!btn) {
      return;
    }
    if (!btn.dataset.label) {
      btn.dataset.label = btn.textContent;
    }
    btn.disabled = loading;
    btn.textContent = loading ? "Please wait..." : btn.dataset.label || btn.textContent;
  }

  function showToast(message) {
    const toast = document.createElement("div");
    toast.textContent = message;
    toast.style.cssText = [
      "position:fixed",
      "bottom:30px",
      "right:30px",
      "background:var(--navy,#1E2761)",
      "color:#fff",
      "padding:14px 22px",
      "border-radius:50px",
      "font-family:'Poppins',sans-serif",
      "font-size:.88rem",
      "box-shadow:0 8px 24px rgba(0,0,0,.2)",
      "z-index:9999",
    ].join(";");
    document.body.appendChild(toast);
    window.setTimeout(() => toast.remove(), 2500);
  }
});
