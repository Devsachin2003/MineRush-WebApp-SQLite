// internships.js

document.addEventListener("DOMContentLoaded", function () {
  const internshipForm = document.getElementById("internship-form");
  const internshipContainer = document.getElementById("internship-container");

  // Array to store internships
  let internships = [];

  // Function to add internships to the container
  function renderInternships(internships) {
    internshipContainer.innerHTML = ""; // Clear current content
    internships.forEach((internship) => {
      const internshipCard = document.createElement("div");
      internshipCard.classList.add("internship-card");

      internshipCard.innerHTML = `
        <h5>${internship.title}</h5>
        <p class="meta"><strong>Company:</strong> ${internship.company}</p>
        <p class="meta"><strong>Location:</strong> ${internship.location}</p>
        <p class="meta"><strong>Duration:</strong> ${internship.duration}</p>
        <p>${internship.description}</p>
        <p class="meta"><strong>Requirements:</strong> ${internship.requirement}</p>
        <p class="meta"><strong>Stipend:</strong> ${internship.stipend}</p>
        <p class="meta"><strong>Application Process:</strong> ${internship.process}</p>
        <p class="meta"><strong>Learning Outcomes:</strong> ${internship.outcome}</p>
        <p class="meta"><strong>Contact Information:</strong> ${internship.contact}</p>
      `;

      internshipContainer.appendChild(internshipCard);
    });
  }

  // Handle form submission
  internshipForm.addEventListener("submit", function (event) {
    event.preventDefault();

    const newInternship = {
      title: document.getElementById("title").value,
      company: document.getElementById("company").value,
      location: document.getElementById("location").value,
      duration: document.getElementById("duration").value,
      description: document.getElementById("description").value,
      requirement: document.getElementById("requirement").value,
      stipend: document.getElementById("stipend").value,
      process: document.getElementById("process").value,
      outcome: document.getElementById("outcome").value,
      contact: document.getElementById("contact").value,
    };

    internships.push(newInternship);
    renderInternships(internships);

    // Reset form fields
    internshipForm.reset();
  });
});
