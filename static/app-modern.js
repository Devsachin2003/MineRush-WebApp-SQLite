(() => {
  const state = { chatHistory: [] };

  function showToast(message, variant = "success") {
    const region = document.getElementById("toastRegion");
    if (!region || !window.bootstrap) {
      alert(message);
      return;
    }
    const toast = document.createElement("div");
    toast.className = `toast align-items-center text-bg-${variant} border-0`;
    toast.setAttribute("role", "status");
    toast.setAttribute("aria-live", "polite");
    toast.setAttribute("aria-atomic", "true");
    toast.innerHTML = `
      <div class="d-flex">
        <div class="toast-body">${escapeHtml(message)}</div>
        <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>`;
    region.appendChild(toast);
    const instance = new bootstrap.Toast(toast, { delay: 4500 });
    toast.addEventListener("hidden.bs.toast", () => toast.remove());
    instance.show();
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  async function parseJsonResponse(response) {
    const data = await response.json().catch(() => ({}));
    if (!response.ok || data.ok === false) {
      throw new Error(data.error || data.message || "Request failed.");
    }
    return data;
  }

  function setBusy(element, busy) {
    if (!element) return;
    element.disabled = busy;
    element.setAttribute("aria-busy", String(busy));
  }

  function setupAsyncForms() {
    document.querySelectorAll("[data-async-form]").forEach((form) => {
      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const terms = form.querySelector("[name='terms_check']");
        if (terms && !terms.checked) {
          showToast("Please agree to the terms before submitting.", "warning");
          terms.focus();
          return;
        }
        const submit = form.querySelector("[type='submit']");
        const status = form.querySelector("[data-form-status]");
        setBusy(submit, true);
        if (status) {
          status.textContent = "Saving...";
          status.className = "alert alert-info";
          status.hidden = false;
        }
        try {
          const response = await fetch(form.action, {
            method: form.method || "POST",
            body: new FormData(form),
            headers: { Accept: "application/json", "X-Requested-With": "fetch" },
          });
          const data = await parseJsonResponse(response);
          const message = data.message || "Saved successfully.";
          showToast(message);
          if (status) {
            status.textContent = message;
            status.className = "alert alert-success";
          }
          if (form.dataset.resetOnSuccess === "true") form.reset();
        } catch (error) {
          showToast(error.message, "danger");
          if (status) {
            status.textContent = error.message;
            status.className = "alert alert-danger";
          }
        } finally {
          setBusy(submit, false);
        }
      });
    });
  }

  function setupClientFilters() {
    document.querySelectorAll("[data-filter-input]").forEach((input) => {
      const targetSelector = input.dataset.filterInput;
      const items = [...document.querySelectorAll(targetSelector)];
      const empty = document.querySelector(input.dataset.filterEmpty || "");
      const counter = document.querySelector(input.dataset.filterCounter || "");
      const apply = () => {
        const query = input.value.trim().toLowerCase();
        let visible = 0;
        items.forEach((item) => {
          const matches = item.textContent.toLowerCase().includes(query);
          item.hidden = !matches;
          if (matches) visible += 1;
        });
        if (empty) empty.hidden = visible > 0;
        if (counter) counter.textContent = `${visible} result${visible === 1 ? "" : "s"}`;
      };
      input.addEventListener("input", apply);
      apply();
    });
  }

  function setupStatusButtons() {
    document.querySelectorAll("[data-status-action]").forEach((button) => {
      button.addEventListener("click", async () => {
        setBusy(button, true);
        try {
          const response = await fetch(button.dataset.statusAction, {
            method: button.dataset.method || "POST",
            headers: { Accept: "application/json", "X-Requested-With": "fetch" },
          });
          const data = await parseJsonResponse(response);
          showToast(data.message || "Status updated.");
          document.querySelectorAll("[data-application-status]").forEach((el) => {
            el.textContent = data.status || "Updated";
          });
          if (data.gmail_url) {
            window.open(data.gmail_url, "_blank", "noopener");
          }
        } catch (error) {
          showToast(error.message, "danger");
        } finally {
          setBusy(button, false);
        }
      });
    });
  }

  function setupNavbar() {
    const navbar = document.querySelector("[data-app-navbar]");
    const menu = document.getElementById("primaryNav");
    const toggle = document.querySelector(".app-navbar__toggle");
    if (!navbar) return;

    const syncScrolled = () => {
      navbar.classList.toggle("is-scrolled", window.scrollY > 8);
    };
    syncScrolled();
    window.addEventListener("scroll", syncScrolled, { passive: true });

    if (menu && toggle) {
      menu.addEventListener("shown.bs.collapse", () => toggle.setAttribute("aria-expanded", "true"));
      menu.addEventListener("hidden.bs.collapse", () => toggle.setAttribute("aria-expanded", "false"));
    }
  }

  function appendChatMessage(container, message, type) {
    const item = document.createElement("div");
    item.className = `chat-message chat-message--${type}`;
    item.innerHTML = escapeHtml(message).replaceAll("\n", "<br>");
    container.appendChild(item);
    container.scrollTop = container.scrollHeight;
    return item;
  }

  function setupChatWidget() {
    const panel = document.getElementById("chatPanel");
    const toggles = [...document.querySelectorAll("[data-chat-toggle]")];
    const close = document.querySelector("[data-chat-close]");
    const form = document.querySelector("[data-chat-form]");
    const input = document.querySelector("[data-chat-input]");
    const messages = document.querySelector("[data-chat-messages]");
    if (!panel || toggles.length === 0 || !form || !input || !messages) return;

    const open = () => {
      panel.classList.add("is-open");
      panel.setAttribute("aria-hidden", "false");
      toggles.forEach((toggle) => toggle.setAttribute("aria-expanded", "true"));
      input.focus();
    };
    const hide = () => {
      panel.classList.remove("is-open");
      panel.setAttribute("aria-hidden", "true");
      toggles.forEach((toggle) => toggle.setAttribute("aria-expanded", "false"));
      toggles[0].focus();
    };

    toggles.forEach((toggle) => {
      toggle.addEventListener("click", () => panel.classList.contains("is-open") ? hide() : open());
    });
    close?.addEventListener("click", hide);
    panel.addEventListener("keydown", (event) => {
      if (event.key === "Escape") hide();
    });

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const message = input.value.trim();
      if (!message) return;
      appendChatMessage(messages, message, "user");
      input.value = "";
      const typing = appendChatMessage(messages, "MineRushBot is typing...", "bot chat-message--typing");
      const send = form.querySelector("button");
      setBusy(send, true);
      try {
        const response = await fetch("/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
            "X-Requested-With": "fetch",
          },
          body: JSON.stringify({ message, history: state.chatHistory }),
        });
        const data = await parseJsonResponse(response);
        typing.remove();
        appendChatMessage(messages, data.message, "bot");
        state.chatHistory = data.history || state.chatHistory;
      } catch (error) {
        typing.remove();
        appendChatMessage(messages, error.message, "bot");
      } finally {
        setBusy(send, false);
      }
    });

    input.addEventListener("keydown", (event) => {
      if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        form.requestSubmit();
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    setupNavbar();
    setupAsyncForms();
    setupClientFilters();
    setupStatusButtons();
    setupChatWidget();
  });
})();
