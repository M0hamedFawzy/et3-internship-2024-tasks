// transaction.js

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('authToken'); // Ensure this key matches how you store the token
    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Token ${token}`
    };

    const transactionHistoryContainer = document.getElementById('transaction-history');
    const actionButtonsContainer = document.getElementById('action-buttons');
    const logoutLink = document.getElementById('logout-link');
    const userNameHeader = document.getElementById('user-name');
    const paginationControls = document.getElementById('pagination-controls');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const pageInfo = document.getElementById('page-info');

    let transactions = []; // To store all transactions
    const transactionsPerPage = 10;
    let currentPage = 1;
    let totalPages = 1;

    // Logout Function
    logoutLink.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('authToken'); // Ensure you remove the correct token key
        window.location.href = '/signin.html'; // Redirect to login page
    });

    // Fetch User Details (Assuming an endpoint exists to get user info)
    fetch('http://localhost:8000/dashboard/', {
        method: 'GET',
        headers: headers
    })
    .then(response => {
        if (response.status === 200) return response.json();
        else throw new Error('Failed to fetch user details');
    })
    .then(user => {
        userNameHeader.textContent = `GoCash | ${user.username}’s Transactions`;
        loadTransactions();
    })
    .catch(error => {
        console.error(error);
        // If fetching user details fails, assume user is not authenticated
        window.location.href = '/signin.html';
    });

    // Load Transactions
    function loadTransactions() {
        fetch('http://localhost:8000/transactions/', {
            method: 'GET',
            headers: headers
        })
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                transactions = data;
                totalPages = Math.ceil(transactions.length / transactionsPerPage);
                if (totalPages > 1) {
                    paginationControls.style.display = 'flex';
                } else {
                    paginationControls.style.display = 'none';
                }
                renderPage(currentPage);
                renderActionButtons();
            } else if (data.detail && data.detail.includes('wallet not created')) {
                // New registered user without a wallet
                renderWalletCreationPrompt();
                paginationControls.style.display = 'none';
            } else if (data.detail && data.detail.includes('wallet is')) {
                // Wallet is deleted or in the process of deletion
                renderWalletStatusMessage(data.detail);
                paginationControls.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error fetching transactions:', error);
            transactionHistoryContainer.innerHTML = '<p>Error loading transactions.</p>';
            paginationControls.style.display = 'none';
        });
    }

    // Render Action Buttons
    function renderActionButtons() {
        actionButtonsContainer.innerHTML = `
            <div class="cta">
                <button id="send-money-btn">Send Money</button>
            </div>
            <div class="cta">
                <button id="withdrawal-btn">Withdrawal</button>
            </div>
            <div class="export">
                <button id="export-btn">Export</button>
                <div class="export-options" id="export-options">
                    <button id="export-excel">Export as Excel</button>
                    <button id="export-pdf">Export as PDF</button>
                </div>
            </div>
        `;

        document.getElementById('send-money-btn').addEventListener('click', () => {
            window.location.href = '/Transactions/send_money.html'; // Redirect to Send Money page
        });

        document.getElementById('withdrawal-btn').addEventListener('click', () => {
            window.location.href = '/Transactions/withdrawal.html'; // Redirect to Withdrawal page
        });

        // Export Button Functionality
        const exportBtn = document.getElementById('export-btn');
        const exportOptions = document.getElementById('export-options');

        exportBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent event bubbling
            exportOptions.style.display = exportOptions.style.display === 'block' ? 'none' : 'block';
        });

        // Hide export options when clicking outside
        document.addEventListener('click', (e) => {
            if (!exportOptions.contains(e.target) && e.target !== exportBtn) {
                exportOptions.style.display = 'none';
            }
        });

        // Export as Excel
        const exportExcelBtn = document.getElementById('export-excel');
        exportExcelBtn.addEventListener('click', () => {
            exportExcel();
            exportOptions.style.display = 'none';
        });

        // Export as PDF
        const exportPdfBtn = document.getElementById('export-pdf');
        exportPdfBtn.addEventListener('click', () => {
            exportPDF();
            exportOptions.style.display = 'none';
        });
    }

    // Render Transaction Table for a Specific Page
    function renderPage(page) {
        const start = (page - 1) * transactionsPerPage;
        const end = start + transactionsPerPage;
        const pageTransactions = transactions.slice(start, end);

        if (pageTransactions.length === 0) {
            transactionHistoryContainer.innerHTML = '<p>No transactions found.</p>';
            return;
        }

        let tableHTML = `
            <div class="history-header">
                <h2>Transaction History</h2>
            </div>
            <table class="history-table">
                <thead>
                    <tr>
                        <th>Sender Number</th>
                        <th>Receiver Number</th>
                        <th>Service Type</th>
                        <th>Service Name</th>
                        <th>Amount</th>
                        <th>Fees</th>
                        <th>Balance Before</th>
                        <th>Balance After</th>
                        <th>Transaction Date</th>
                    </tr>
                </thead>
                <tbody>
        `;

        pageTransactions.forEach(transaction => {
            const serviceIcon = getServiceIcon(transaction.service_type);
            const formattedDate = new Date(transaction.transaction_date).toLocaleString();
            tableHTML += `
                <tr>
                    <td>${transaction.sender}</td>
                    <td>${transaction.receiver || '-'}</td>
                    <td>${serviceIcon} ${transaction.service_type}</td>
                    <td>${transaction.service_name}</td>
                    <td>${transaction.amount}</td>
                    <td>${transaction.fees}</td>
                    <td>${transaction.balance_before}</td>
                    <td>${transaction.balance_after}</td>
                    <td>${formattedDate}</td>
                </tr>
            `;
        });

        tableHTML += `
                </tbody>
            </table>
        `;

        transactionHistoryContainer.innerHTML = tableHTML;
        updatePaginationControls();
    }

    // Get Service Type Icon
    function getServiceIcon(serviceType) {
        switch (serviceType.toLowerCase()) {
            case 'deposit':
                return '<i class="fa-solid fa-arrow-up" style="color: #0D995F"></i>';
            case 'withdrawal':
                return '<i class="fa-solid fa-arrow-down" style="color: #AE3A1A"></i>';
            case 'transaction':
                return '<i class="fa-solid fa-arrow-right-arrow-left" style="color: #C37F1F"></i>';
            case 'bill payment':
                return '<i class="fa-solid fa-money-bill-wave" style="color: #1F76C3"></i>';
            case 'mobile bills':
                return '<i class="fa-solid fa-mobile-screen-button" style="color:rgb(216, 109, 27)"></i>';
            case 'merchant payment':
                return '<i class="fa-solid fa-store" style="color: #C31F92"></i>';
            case 'account subscription':
                return '<i class="fa-solid fa-gem" style="color:rgb(139, 73, 126)"></i>';
            case 'green subscription':
                return '<i class="fa-solid fa-leaf" style="color:rgb(34, 145, 99)"></i>';
            default:
                return '';
        }
    }

    // Update Pagination Controls
    function updatePaginationControls() {
        pageInfo.textContent = `Page ${currentPage} of ${totalPages}`;

        // Disable Previous button on first page
        if (currentPage === 1) {
            prevBtn.disabled = true;
        } else {
            prevBtn.disabled = false;
        }

        // Disable Next button on last page
        if (currentPage === totalPages) {
            nextBtn.disabled = true;
        } else {
            nextBtn.disabled = false;
        }
    }

    // Handle Previous Button Click
    prevBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderPage(currentPage);
        }
    });

    // Handle Next Button Click
    nextBtn.addEventListener('click', () => {
        if (currentPage < totalPages) {
            currentPage++;
            renderPage(currentPage);
        }
    });

    // Render Wallet Creation Prompt for New Users
    function renderWalletCreationPrompt() {
        transactionHistoryContainer.innerHTML = `
            <div class="form-container">
                <h2>Create a Wallet</h2>
                <p>You need to create a wallet first to perform transactions.</p>
                <button id="create-wallet-btn">Move to Wallet</button>
            </div>
        `;

        document.getElementById('create-wallet-btn').addEventListener('click', () => {
            window.location.href = '/Wallet/wallet.html'; // Redirect to Wallet creation page
        });
    }

    // Render Wallet Status Message
    function renderWalletStatusMessage(message) {
        transactionHistoryContainer.innerHTML = `
            <div class="form-container">
                <p>${message}</p>
            </div>
        `;
    }

    // Export Transactions as Excel
    function exportExcel() {
        if (transactions.length === 0) {
            alert('No transactions to export.');
            return;
        }

        // Prepare data for SheetJS
        const data = transactions.map(tx => ({
            'Sender Number': tx.sender,
            'Receiver Number': tx.receiver || '-',
            'Service Type': tx.service_type,
            'Service Name': tx.service_name,
            'Amount': tx.amount,
            'Fees': tx.fees,
            'Balance Before': tx.balance_before,
            'Balance After': tx.balance_after,
            'Transaction Date': new Date(tx.transaction_date).toLocaleString()
        }));

        // Create a new workbook and worksheet
        const wb = XLSX.utils.book_new();
        const ws = XLSX.utils.json_to_sheet(data);

        // Append worksheet to workbook
        XLSX.utils.book_append_sheet(wb, ws, 'Transactions');

        // Generate Excel file and trigger download
        XLSX.writeFile(wb, `transactions_${new Date().toISOString().slice(0, 10)}.xlsx`);
    }

    // Export Transactions as PDF
    function exportPDF() {
        if (transactions.length === 0) {
            alert('No transactions to export.');
            return;
        }

        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        doc.setFontSize(18);
        doc.text('Transaction History', 14, 22);
        doc.setFontSize(12);
        doc.setTextColor(100);

        const columns = ['Sender Number', 'Receiver Number', 'Service Type', 'Service Name', 'Amount', 'Fees', 'Balance Before', 'Balance After', 'Transaction Date'];
        const rows = transactions.map(tx => [
            tx.sender,
            tx.receiver || '-',
            tx.service_type,
            tx.service_name,
            tx.amount,
            tx.fees,
            tx.balance_before,
            tx.balance_after,
            new Date(tx.transaction_date).toLocaleString()
        ]);

        // Use autoTable for better table formatting
        doc.autoTable({
            head: [columns],
            body: rows,
            startY: 30,
            styles: { fontSize: 8 },
            headStyles: { fillColor: [38, 38, 38] },
            alternateRowStyles: { fillColor: [240, 240, 240] },
            theme: 'striped',
        });

        doc.save(`transactions_${new Date().toISOString().slice(0, 10)}.pdf`);
    }
});


