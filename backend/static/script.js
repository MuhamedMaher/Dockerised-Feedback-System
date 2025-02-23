document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("feedbackForm");
  if (form) {
    form.addEventListener("submit", async function(e) {
      e.preventDefault();
      const productId = document.getElementById("product").value;
      const choice = document.getElementById("choice").value;
      try {
        const response = await fetch("/api/feedback", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ product_id: Number(productId), choice: choice })
        });
        const data = await response.json();
        alert("Feedback submitted: " + JSON.stringify(data));
      } catch (error) {
        alert("Error submitting feedback: " + error);
      }
    });
  }

  const resultsDiv = document.getElementById("results");
  if (resultsDiv) {
    async function fetchResults() {
      try {
        const response = await fetch("/api/results");
        const results = await response.json();
        let html = "";
        for (const productId in results) {
          html += `<h2>Product ${productId}</h2><ul>`;
          for (const choice in results[productId]) {
            html += `<li>${choice}: ${results[productId][choice]} votes</li>`;
          }
          html += "</ul>";
        }
        resultsDiv.innerHTML = html;
      } catch (error) {
        resultsDiv.innerHTML = `<p>Error loading results: ${error}</p>`;
      }
    }
    fetchResults();
    setInterval(fetchResults, 5000);
  }
});

