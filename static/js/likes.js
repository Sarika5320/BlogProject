document.addEventListener("DOMContentLoaded", function () {
  document.querySelectorAll(".like-btn").forEach(button => {
      button.addEventListener("click", function () {
          let blogId = this.getAttribute("data-blog-id");
          let likeCount = this.querySelector("span"); 

          fetch(`/like/${blogId}/`, { method: "POST", headers: { "X-CSRFToken": getCookie("csrftoken") } })
              .then(response => response.json())
              .then(data => {
                  if (data.liked) {
                      button.classList.add("btn-primary");
                      button.classList.remove("btn-outline-primary");
                  } else {
                      button.classList.remove("btn-primary");
                      button.classList.add("btn-outline-primary");
                  }
                  likeCount.innerText = data.total_likes;
              });
      });
  });
});

// Function to Get CSRF Token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
      let cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
          let cookie = cookies[i].trim();
          if (cookie.substring(0, name.length + 1) === (name + "=")) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
