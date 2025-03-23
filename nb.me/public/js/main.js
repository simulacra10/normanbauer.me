(() => {
  // <stdin>
  document.addEventListener("DOMContentLoaded", function() {
    var sidebar = document.getElementById("sidebar");
    var button = document.querySelector("header button");
    if (sidebar && button) {
      button.addEventListener("click", function() {
        sidebar.classList.toggle("show");
      });
    }
  });
})();
