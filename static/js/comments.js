document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".reply-btn").forEach(function (button) {
      button.addEventListener("click", function () {
          var commentId = this.getAttribute("data-comment-id");
          var form = document.getElementById("reply-form-" + commentId);
          if (form.style.display === "none") {
              form.style.display = "block";
          } else {
              form.style.display = "none";
          }
      });
  });
});