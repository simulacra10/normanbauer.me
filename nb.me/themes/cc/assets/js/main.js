// const sidebar = document.getElementById('sidebar')

// function toggleSidebar(){
//     sidebar.classList.toggle('show')
// }


document.addEventListener('DOMContentLoaded', function () {
    var sidebar = document.getElementById("sidebar");
    var button = document.querySelector("header button"); // Or add an ID to your button

    if (sidebar && button) {
        button.addEventListener("click", function () {
            sidebar.classList.toggle("show");
        });
    }
});
