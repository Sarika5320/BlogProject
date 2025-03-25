document.addEventListener("DOMContentLoaded", function() {
  const themeToggle = document.getElementById("theme-toggle");
  const body = document.body;

  themeToggle.addEventListener("click", function() {
      body.classList.toggle("dark-mode");
      if (body.classList.contains("dark-mode")) {
          themeToggle.textContent = "☀️ Light Mode";
          localStorage.setItem("theme", "dark");
      } else {
          themeToggle.textContent = "🌙 Dark Mode";
          localStorage.setItem("theme", "light");
      }
  });

  // Load saved theme preference
  if (localStorage.getItem("theme") === "dark") {
      body.classList.add("dark-mode");
      themeToggle.textContent = "☀️ Light Mode";
  }
});



