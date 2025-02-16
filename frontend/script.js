document.addEventListener("DOMContentLoaded", function() {
    fetchTransactions();
});

async function fetchTransactions() {
    const category = document.getElementById("category").value;
    const url = category ? `/transactions/${category}` : "/transactions";
    
    try {
        const response = await fetch(url);
        const transactions = await response.json();
        populateTable(transactions);
        renderChart(transactions);
    } catch (error) {
        console.error("Error fetching transactions:", error);
    }
}

function populateTable(transactions) {
    const tableBody = document.getElementById("transactionsTable");
    tableBody.innerHTML = "";
    
    transactions.forEach(tx => {
        const row = `<tr>
            <td>${tx.category}</td>
            <td>${tx.amount}</td>
            <td>${tx.date}</td>
            <td>${tx.description}</td>
        </tr>`;
        tableBody.innerHTML += row;
    });
}

function renderChart(transactions) {
    const ctx = document.getElementById("transactionsChart").getContext("2d");
    
    const categories = {};
    transactions.forEach(tx => {
        categories[tx.category] = (categories[tx.category] || 0) + tx.amount;
    });
    
    const chartData = {
        labels: Object.keys(categories),
        datasets: [{
            label: "Total Amount per Category (RWF)",
            data: Object.values(categories),
            backgroundColor: ["red", "blue", "green", "orange", "purple", "yellow"],
        }]
    };
    
    new Chart(ctx, {
        type: "bar",
        data: chartData,
    });
}
