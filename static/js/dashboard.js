const statusMessage = document.querySelector("#status");
const transactionsOutput = document.querySelector("#transactions");
const monthFilter = document.querySelector("#month-filter");
const transactionDialog = document.querySelector("#transaction-dialog");
const transactionForm = document.querySelector("#transaction-form");
const categorySelect = document.querySelector("#transaction-category");
const paymentSelect = document.querySelector("#transaction-payment");
const transactionError = document.querySelector("#transaction-error");
let editingTransactionId = null;
let cashFlowChart;

function formatMoney(value) {
    return Number(value).toLocaleString(undefined, {
        style: "currency",
        currency: "USD",
    });
}

function renderTransactions(transactions) {
    transactionsOutput.replaceChildren();

    if (transactions.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 6;
        cell.textContent = "No transactions this month.";
        row.appendChild(cell);
        transactionsOutput.appendChild(row);
        return;
    }

    for (const [transactionId, transactionDate, category, paymentMethod, description, amount] of transactions) {
        const row = document.createElement("tr");
        const values = [
            transactionDate,
            category,
            description || "-",
            paymentMethod || "-",
            formatMoney(amount),
        ];

        values.forEach((value, index) => {
            const cell = document.createElement("td");
            cell.textContent = value;
            if (index === 4) {
                cell.classList.add(Number(amount) >= 0 ? "amount-income" : "amount-expense");
            }
            row.appendChild(cell);
        });

        const actionsCell = document.createElement("td");
        const editButton = document.createElement("button");
        editButton.type = "button";
        editButton.textContent = "Edit";
        editButton.addEventListener("click", () => openEditDialog({
            transactionId,
            amount,
            category,
            transactionDate,
            paymentMethod,
            description,
        }));

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.textContent = "Delete";
        deleteButton.addEventListener("click", () => deleteTransaction(transactionId));

        actionsCell.append(editButton, deleteButton);
        row.appendChild(actionsCell);

        transactionsOutput.appendChild(row);
    }
}

function openCreateDialog() {
    editingTransactionId = null;
    transactionForm.reset();
    transactionError.textContent = "";
    document.querySelector("#dialog-title").textContent = "Add transaction";
    document.querySelector("#transaction-date").value = `${monthFilter.value}-01`;
    transactionDialog.showModal();
}

function openEditDialog(transaction) {
    editingTransactionId = transaction.transactionId;
    transactionError.textContent = "";
    document.querySelector("#dialog-title").textContent = "Edit transaction";
    document.querySelector("#transaction-amount").value = transaction.amount;
    const defaultCategory = [...categorySelect.options]
        .some((option) => option.value === transaction.category);
    categorySelect.value = defaultCategory ? transaction.category : "Other";
    const defaultPayment = [...paymentSelect.options]
        .some((option) => option.value === transaction.paymentMethod);
    paymentSelect.value = defaultPayment ? transaction.paymentMethod : "Other";
    document.querySelector("#transaction-date").value = transaction.transactionDate;
    document.querySelector("#transaction-payment").value = transaction.paymentMethod || "";
    document.querySelector("#transaction-description").value = transaction.description || "";
    transactionDialog.showModal();
}

async function deleteTransaction(transactionId) {
    if (!window.confirm("Delete this transaction?")) return;

    const response = await fetch(`/api/transactions/${transactionId}`, {
        method: "DELETE",
        credentials: "same-origin",
    });

    if (!response.ok) {
        const result = await response.json();
        statusMessage.textContent = result.error;
        return;
    }

    loadDashboard(monthFilter.value);
}

transactionForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const amount = Number(document.querySelector("#transaction-amount").value);
    const category = categorySelect.value;
    const paymentMethod = paymentSelect.value || null;
    const transactionDate = document.querySelector("#transaction-date").value;

    if (!Number.isFinite(amount) || amount === 0) {
        transactionError.textContent = "Enter a nonzero amount.";
        return;
    }
    if (!category) {
        transactionError.textContent = "Choose a category.";
        return;
    }
    if (!transactionDate) {
        transactionError.textContent = "Choose a transaction date.";
        return;
    }
    transactionError.textContent = "";
    const transaction = {
        amount,
        category,
        transaction_date: transactionDate,
        payment_method: paymentMethod,
        description: document.querySelector("#transaction-description").value || null,
    };
    const url = editingTransactionId === null
        ? "/api/transactions"
        : `/api/transactions/${editingTransactionId}`;
    const method = editingTransactionId === null ? "POST" : "PUT";
    const response = await fetch(url, {
        method,
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify(transaction),
    });

    const result = await response.json();
    if (!response.ok) {
        statusMessage.textContent = result.error;
        return;
    }

    transactionDialog.close();
    loadDashboard(monthFilter.value);
});

document.querySelector("#add-transaction").addEventListener("click", openCreateDialog);
document.querySelector("#cancel-transaction").addEventListener("click", () => transactionDialog.close());

function renderChart(transactions) {
    if (cashFlowChart) cashFlowChart.destroy();

    const dailyTotals = new Map();
    for (const [, transactionDate, , , , amount] of transactions) {
        if (!dailyTotals.has(transactionDate)) {
            dailyTotals.set(transactionDate, { income: 0, expenses: 0 });
        }

        if (amount >= 0) {
            dailyTotals.get(transactionDate).income += Number(amount);
        } else {
            dailyTotals.get(transactionDate).expenses += Math.abs(Number(amount));
        }
    }

    const dates = [...dailyTotals.keys()].sort();
    let cumulativeIncome = 0;
    let cumulativeExpenses = 0;
    const incomeTotals = dates.map((date) => {
        cumulativeIncome += dailyTotals.get(date).income;
        return cumulativeIncome;
    });
    const expenseTotals = dates.map((date) => {
        cumulativeExpenses += dailyTotals.get(date).expenses;
        return cumulativeExpenses;
    });

    cashFlowChart = new Chart(document.querySelector("#cash-flow-chart"), {
        type: "line",
        data: {
            labels: dates,
            datasets: [
                {
                    label: "Cumulative income",
                    data: incomeTotals,
                    borderColor: "#2f855a",
                    backgroundColor: "#2f855a",
                    tension: 0.2,
                },
                {
                    label: "Cumulative expenses",
                    data: expenseTotals,
                    borderColor: "#c53030",
                    backgroundColor: "#c53030",
                    tension: 0.2,
                },
            ],
        },
        options: {
            responsive: true,
            scales: { y: { beginAtZero: true } },
        },
    });
}

function currentMonthValue() {
    const current = new Date();
    return `${current.getFullYear()}-${String(current.getMonth() + 1).padStart(2, "0")}`;
}

async function loadDashboard(month) {
    const response = await fetch(`/api/dashboard?month=${month}`, {
        credentials: "same-origin",
    });
    const result = await response.json();

    if (response.status === 401) {
        window.location.href = "/login";
        return;
    }

    if (!response.ok) {
        statusMessage.textContent = result.error;
        return;
    }

    const summary = result.summary;
    document.querySelector("#expense-ratio").textContent = summary.expense_to_income_ratio === null
        ? "N/A"
        : `${(summary.expense_to_income_ratio * 100).toFixed(1)}%`;
    document.querySelector("#income").textContent = formatMoney(summary.income);
    document.querySelector("#expenses").textContent = formatMoney(summary.expenses);
    document.querySelector("#balance").textContent = formatMoney(summary.balance);
    renderTransactions(result.transactions);
    renderChart(result.transactions);
}

monthFilter.addEventListener("change", () => loadDashboard(monthFilter.value));
monthFilter.value = currentMonthValue();
loadDashboard(monthFilter.value);
