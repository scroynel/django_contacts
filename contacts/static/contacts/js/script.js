function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + "=")) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}



function displayFileName(input) {
  const fileName = input.files[0] ? input.files[0].name : "No file..."; 
  document.getElementById('file-chosen').textContent = fileName;
  // Optional: Add a green glow when a file is ready
  document.getElementById('file-chosen').classList.add('text-green-600', 'not-italic', 'font-medium');
}


$('#contacts').on('click', '.delete-link', function(e) {
  e.preventDefault();
  $.ajax({
    url: $(this).attr('href'),
    type: "POST",
    dataType: "json",
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": getCookie("csrftoken"), // function to get coookie by name 
    },
    success: (data) => {
        if (data.status == 1) {
          const $item = $(this).closest('.contact-item')
          $item.addClass('fade-out')
          setTimeout(() => {
            $item.remove()
            
          }, 500)
        }
    },
    error: (error) => {
      console.log(error);
    }
  })
})
