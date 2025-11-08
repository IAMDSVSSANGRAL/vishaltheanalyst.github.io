// Portfolio Interactive Script
console.log('Portfolio loaded successfully');

// Dynamic form logic
document.addEventListener("DOMContentLoaded", function () {
  const userTypeSelect = document.getElementById("user_type");
  const recruiterFields = document.querySelector(".recruiter-fields");
  const clientFields = document.querySelector(".client-fields");
  const studentFields = document.querySelector(".student-fields");

  function hideAll() {
    recruiterFields.classList.add("hidden");
    clientFields.classList.add("hidden");
    studentFields.classList.add("hidden");
  }

  userTypeSelect.addEventListener("change", function () {
    hideAll();
    const value = this.value;

    if (value === "Recruiter") recruiterFields.classList.remove("hidden");
    else if (value === "Client") clientFields.classList.remove("hidden");
    else if (value === "Student") studentFields.classList.remove("hidden");
  });
});
