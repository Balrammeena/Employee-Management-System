// ================= PAGE LOAD =================
document.addEventListener("DOMContentLoaded", function () {
  // Close dropdowns/menus on ESC
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      closeAllMenus();
    }
  });
});

// ================= CONFIRMATIONS =================
function confirmDelete() {
  return confirm("Are you sure you want to delete this employee?");
}

function confirmLogout() {
  return confirm("Do you really want to logout?");
}

// ================= VALIDATIONS =================
function validateLoginForm() {
  const username = document.querySelector('input[name="username"]')?.value.trim();
  const password = document.querySelector('input[name="password"]')?.value.trim();

  if (!username || !password) {
    alert("Username and Password are required");
    return false;
  }
  return true;
}

function validateEmployeeForm() {
  const name = document.querySelector('input[name="name"]')?.value.trim();
  const email = document.querySelector('input[name="email"]')?.value.trim();
  const department = document.querySelector('input[name="department"]')?.value.trim();
  const salary = document.querySelector('input[name="salary"]')?.value.trim();

  if (!name || !email || !department || !salary) {
    alert("All fields are required");
    return false;
  }

  if (!validateEmail(email)) {
    alert("Enter a valid email address");
    return false;
  }

  if (isNaN(salary) || Number(salary) <= 0) {
    alert("Salary must be a positive number");
    return false;
  }

  return true;
}

function validateEmail(email) {
  const pattern = /^[^ ]+@[^ ]+\.[a-z]{2,}$/i;
  return pattern.test(email);
}

// ================= SIDEBAR TOGGLE =================
function toggleSidebar() {
  const sb = document.getElementById("sidebar");
  if (sb) sb.classList.toggle("open");
}

// ================= DROPDOWN (All Employees) =================
function toggleDropdown() {
  const dd = document.getElementById("empDropdown");
  if (dd) dd.classList.toggle("show");
}

// ================= TOP-RIGHT ICON MENUS =================
function toggleMenu(id) {
  // close others first
  document.querySelectorAll(".icon-menu").forEach(m => {
    if (m.id !== id) m.classList.remove("show");
  });

  const menu = document.getElementById(id);
  if (menu) menu.classList.toggle("show");
}

// ================= CLOSE MENUS ON OUTSIDE CLICK =================
document.addEventListener("click", function (e) {
  // close All Employees dropdown if clicked outside
  const dropdown = e.target.closest(".dropdown");
  if (!dropdown) {
    document.getElementById("empDropdown")?.classList.remove("show");
  }

  // close icon menus if clicked outside
  document.querySelectorAll(".icon-menu").forEach(menu => {
    if (!menu.parentElement.contains(e.target)) {
      menu.classList.remove("show");
    }
  });
});

function closeAllMenus() {
  document.getElementById("empDropdown")?.classList.remove("show");
  document.querySelectorAll(".icon-menu").forEach(m => m.classList.remove("show"));
}
