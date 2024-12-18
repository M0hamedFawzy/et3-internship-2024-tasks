document.addEventListener('DOMContentLoaded', () => {
    // Active vs Inactive Users Chart
    new Chart(document.getElementById('active-vs-inactive-users'), {
        type: 'doughnut',
        data: {
            labels: ['Active', 'Inactive'],
            datasets: [{
                data: [
                { active_users_count },
                { inactive_users_count }
                ],
                backgroundColor: ['#4caf50', '#f44336'],
            }]
        }
    });

    // User Subscription Plans Chart
    new Chart(document.getElementById('user-subscription-plans'), {
        type: 'polarArea',
        data: {
            labels: ['Standard', 'Plus', 'Premium'],
            datasets: [{
                data: [
                    { standard_users },
                    { plus_users },
                    { premium_users }
                ],
                backgroundColor: ['#ff5722', '#03a9f4', '#9c27b0']
            }]
        }
    });

    // Green Users Chart
    new Chart(document.getElementById('green-users'), {
        type: 'bar',
        data: {
            labels: ['Leaf', 'Tree', 'Forest'],
            datasets: [{
                label: 'Green Users',
                data: [
                    { leaf_users_count },
                    { tree_users_count },
                    { forest_users_count }
                ],
                backgroundColor: ['#81c784', '#4caf50', '#388e3c']
            }]
        }
    });

    // Wallet Average Balance Chart
    new Chart(document.getElementById('wallet-avg-balance'), {
        type: 'line',
        data: {
            labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            datasets: [{
                label: 'Average Wallet Balance',
                data: { monthly_avg_wallet_balance },
                borderColor: '#03a9f4',
                fill: false,
                tension: 0.4
            }]
        }
    });

    // Active vs Inactive Wallets Chart
    new Chart(document.getElementById('active-vs-inactive-wallets'), {
        type: 'pie',
        data: {
            labels: ['Active', 'Inactive'],
            datasets: [{
                data: [{ active_wallets_count }, { inactive_wallets_count }],
                backgroundColor: ['#4caf50', '#f44336']
            }]
        }
    });

    // Transactions Per Year Chart
    new Chart(document.getElementById('transactions-per-year'), {
        type: 'bar',
        data: {
            labels: { yearly_transaction_labels },
            datasets: [{
                label: 'Transactions',
                data: { yearly_transaction_counts },
                backgroundColor: '#ff9800'
            }]
        }
    });

    // Monthly Transactions Chart
    new Chart(document.getElementById('monthly-transactions'), {
        type: 'line',
        data: {
            labels: { monthly_transaction_labels },
            datasets: [{
                label: 'Transactions',
                data: { monthly_transaction_counts },
                borderColor: '#6200ea',
                fill: false,
                tension: 0.4
            }]
        }
    });

    // Service Type Distribution Chart
    new Chart(document.getElementById('service-type-distribution'), {
        type: 'radar',
        data: {
            labels: ['Deposit', 'Withdrawal', 'Transfer', 'Bill Payment', 'Merchant Payment', 'Subscription', 'Green Plan'],
            datasets: [{
                label: 'Service Types',
                data: [
                    { deposit },
                    { withdrawal },
                    { transfer },
                    { bill_payment },
                    { merchant_payment },
                    { subscription },
                    { green_plan }
                ],
                backgroundColor: 'rgba(103, 58, 183, 0.2)',
                borderColor: '#673ab7'
            }]
        }
    });

    // Transaction Peaks Chart
    new Chart(document.getElementById('transaction-peaks'), {
        type: 'bar',
        data: {
            labels: { peak_transaction_times },
            datasets: [{
                label: 'Transaction Peaks',
                data: { peak_transaction_counts },
                backgroundColor: '#e91e63'
            }]
        }
    });

    // Daily Transaction Volume Chart
    new Chart(document.getElementById('daily-transaction-volume'), {
        type: 'line',
        data: {
            labels: { daily_transaction_labels },
            datasets: [{
                label: 'Transaction Volume',
                data: { daily_transaction_counts },
                borderColor: '#009688',
                fill: false
            }]
        }
    });

    // User Growth Chart
    new Chart(document.getElementById('user-growth'), {
        type: 'line',
        data: {
            labels: { user_growth_labels },
            datasets: [{
                label: 'User Growth',
                data: { user_growth_data },
                borderColor: '#ff5722',
                fill: false
            }]
        }
    });

    // Monthly User Registration Chart
    new Chart(document.getElementById('monthly-user-registration'), {
        type: 'bar',
        data: {
            labels: { registration_labels },
            datasets: [{
                label: 'Monthly Registrations',
                data: { registration_counts },
                backgroundColor: '#00bcd4'
            }]
        }
    });

    new Chart(document.getElementById('transactions-per-year'), {
    type: 'bar',
    data: {
        labels: ['2020', '2021', '2022', '2023', '2024'],
        datasets: [{
            label: 'Transactions',
            data: {{ yearly_transaction_counts|safe }},
            backgroundColor: '#ff9800'
        }]
    }
});

});



