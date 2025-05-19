async function fetchPrices() {
  const product = document.getElementById("productInput").value;
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "🔍 Searching...";

  try {
    const response = await fetch(`/get-prices?product=${encodeURIComponent(product)}`);
    const data = await response.json();

    const prices = {};
    for (const [site, value] of Object.entries(data)) {
      const numericPrice = parseFloat(value);
      if (!isNaN(numericPrice)) {
        prices[site] = numericPrice;
      }
    }

    let minSite = null;
    let minPrice = Infinity;

    for (const [site, price] of Object.entries(prices)) {
      if (price < minPrice) {
        minPrice = price;
        minSite = site;
      }
    }

    resultsDiv.innerHTML = `
      <p><strong>Amazon:</strong> ₹${data.amazon}</p>
      <p><strong>Flipkart:</strong> ₹${data.flipkart}</p>
      <!-- <p><strong>Croma:</strong> ₹${data.croma}</p> -->
      ${
        minSite
          ? `<p style="color: green;"><strong>Lowest Price:</strong> ₹${minPrice} on <strong>${minSite.charAt(0).toUpperCase() + minSite.slice(1)}</strong></p>`
          : `<p style="color: red;">No valid prices found.</p>`
      }
    `;
  } catch (error) {
    resultsDiv.innerHTML = `<p style="color: red;">Error fetching prices. Please try again.</p>`;
    console.error(error);
  }
}