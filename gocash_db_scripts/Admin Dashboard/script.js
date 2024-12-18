// document.addEventListener('DOMContentLoaded', async () => {
//   const DB_CONFIG = {
//       dbname: "DWBI",
//       user: "postgres",
//       password: "1234",
//       host: "localhost",
//       port: 5432
//   };

//   async function fetchData(query) {
//       const { Client } = require("pg");
//       const client = new Client(DB_CONFIG);
//       await client.connect();
//       const res = await client.query(query);
//       await client.end();
//       return res.rows;
//   }

//   // Fetch and populate data for charts
//   const populateCharts = async () => {
//       // Active vs Inactive Users
//       const users = await fetchData("SELECT * FROM dim_user;");
//       const activeUsers = users.filter(user => user.is_active);
//       const inactiveUsers = users.filter(user => !user.is_active);

//       new Chart(document.getElementById('active-vs-inactive-users'), {
//           type: 'doughnut',
//           data: {
//               labels: ['Active', 'Inactive'],
//               datasets: [{
//                   data: [activeUsers.length, inactiveUsers.length],
//                   backgroundColor: ['#4caf50', '#f44336']
//               }]
//           }
//       });

//       // Subscription Plans Distribution
//       const plans = await fetchData("SELECT subscription_plan, COUNT(*) as count FROM dim_user GROUP BY subscription_plan;");
//       const planLabels = plans.map(plan => plan.subscription_plan);
//       const planCounts = plans.map(plan => plan.count);

//       new Chart(document.getElementById('user-subscription-plans'), {
//           type: 'bar',
//           data: {
//               labels: planLabels,
//               datasets: [{
//                   label: 'Users per Plan',
//                   data: planCounts,
//                   backgroundColor: ['#ff9800', '#2196f3', '#8bc34a']
//               }]
//           }
//       });

//       // Green Users Breakdown
//       const greenUsers = await fetchData("SELECT green_plan, COUNT(*) as count FROM dim_user WHERE green_plan IS NOT NULL GROUP BY green_plan;");
//       const greenLabels = greenUsers.map(green => green.green_plan);
//       const greenCounts = greenUsers.map(green => green.count);

//       new Chart(document.getElementById('green-users'), {
//           type: 'pie',
//           data: {
//               labels: greenLabels,
//               datasets: [{
//                   data: greenCounts,
//                   backgroundColor: ['#4caf50', '#8bc34a', '#cddc39']
//               }]
//           }
//       });

//       // Wallet Average Balance
//       const walletData = await fetchData("SELECT AVG(balance) as avg_balance FROM dim_wallet;");
//       const avgBalance = walletData[0]?.avg_balance || 0;

//       new Chart(document.getElementById('wallet-avg-balance'), {
//           type: 'bar',
//           data: {
//               labels: ['Average Wallet Balance'],
//               datasets: [{
//                   data: [avgBalance],
//                   backgroundColor: ['#03a9f4']
//               }]
//           }
//       });

//       // Active vs Inactive Wallets
//       const wallets = await fetchData("SELECT * FROM dim_wallet;");
//       const activeWallets = wallets.filter(wallet => wallet.is_active);
//       const inactiveWallets = wallets.filter(wallet => !wallet.is_active);

//       new Chart(document.getElementById('active-vs-inactive-wallets'), {
//           type: 'doughnut',
//           data: {
//               labels: ['Active', 'Inactive'],
//               datasets: [{
//                   data: [activeWallets.length, inactiveWallets.length],
//                   backgroundColor: ['#4caf50', '#f44336']
//               }]
//           }
//       });

//       // Transactions Per Year
//       const transactionsPerYear = await fetchData("SELECT EXTRACT(YEAR FROM transaction_date) as year, COUNT(*) as count FROM fact_transaction GROUP BY year ORDER BY year;");
//       const transactionYears = transactionsPerYear.map(tx => tx.year);
//       const transactionCounts = transactionsPerYear.map(tx => tx.count);

//       new Chart(document.getElementById('transactions-per-year'), {
//           type: 'line',
//           data: {
//               labels: transactionYears,
//               datasets: [{
//                   label: 'Transactions Per Year',
//                   data: transactionCounts,
//                   borderColor: '#673ab7',
//                   fill: false
//               }]
//           }
//       });

//       // Monthly Transactions
//       const monthlyTransactions = await fetchData("SELECT EXTRACT(MONTH FROM transaction_date) as month, COUNT(*) as count FROM fact_transaction WHERE EXTRACT(YEAR FROM transaction_date) = EXTRACT(YEAR FROM CURRENT_DATE) GROUP BY month ORDER BY month;");
//       const transactionMonths = monthlyTransactions.map(tx => `Month ${tx.month}`);
//       const transactionCountsMonthly = monthlyTransactions.map(tx => tx.count);

//       new Chart(document.getElementById('monthly-transactions'), {
//           type: 'bar',
//           data: {
//               labels: transactionMonths,
//               datasets: [{
//                   label: 'Monthly Transactions',
//                   data: transactionCountsMonthly,
//                   backgroundColor: ['#3f51b5']
//               }]
//           }
//       });

//       // Service Type Distribution
//       const serviceTypes = await fetchData("SELECT service_type, COUNT(*) as count FROM fact_transaction GROUP BY service_type;");
//       const serviceLabels = serviceTypes.map(st => st.service_type);
//       const serviceCounts = serviceTypes.map(st => st.count);

//       new Chart(document.getElementById('service-type-distribution'), {
//           type: 'pie',
//           data: {
//               labels: serviceLabels,
//               datasets: [{
//                   data: serviceCounts,
//                   backgroundColor: ['#ff5722', '#607d8b', '#9c27b0', '#e91e63']
//               }]
//           }
//       });

//       // Transaction Peaks
//       const dailyTransactions = await fetchData("SELECT transaction_date, COUNT(*) as count FROM fact_transaction GROUP BY transaction_date ORDER BY transaction_date;");
//       const transactionDates = dailyTransactions.map(tx => tx.transaction_date);
//       const transactionDailyCounts = dailyTransactions.map(tx => tx.count);

//       new Chart(document.getElementById('transaction-peaks'), {
//           type: 'line',
//           data: {
//               labels: transactionDates,
//               datasets: [{
//                   label: 'Transactions Per Day',
//                   data: transactionDailyCounts,
//                   borderColor: '#009688',
//                   fill: false
//               }]
//           }
//       });
//   };

//   // Run the chart population
//   await populateCharts();
// });


document.addEventListener('DOMContentLoaded', async () => {
  // Include sql.js library
  const SQL = await initSqlJs({
      locateFile: file => `https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.8.0/sql-wasm.wasm`,
  });

  // Initialize the SQLite database
  const db = new SQL.Database();

  // Create mock tables and data
  db.run(`
      CREATE TABLE dim_user (id INTEGER, subscription_plan TEXT, green_plan TEXT, is_active INTEGER);
      INSERT INTO dim_user VALUES
      (1, 'Standard', 'Leaf', 1),
      (2, 'Premium', 'Tree', 0),
      (3, 'Plus', 'Forest', 1);

      CREATE TABLE dim_wallet (id INTEGER, balance REAL, is_active INTEGER);
      INSERT INTO dim_wallet VALUES
      (1, 150.00, 1),
      (2, 200.00, 0);

      CREATE TABLE fact_transaction (id INTEGER, transaction_date TEXT, service_type TEXT);
      INSERT INTO fact_transaction VALUES
      (1, '2024-01-01', 'Deposit'),
      (2, '2024-01-02', 'Withdrawal'),
      (3, '2024-01-03', 'Transfer');
  `);

  // Function to fetch data
  async function fetchData(query) {
      const result = db.exec(query);
      return result[0]?.values || [];
  }

  // Fetch and populate data for charts
  const populateCharts = async () => {
      // Active vs Inactive Users
      const users = await fetchData("SELECT is_active FROM dim_user;");
      const activeUsers = users.filter(user => user[0] === 1).length;
      const inactiveUsers = users.length - activeUsers;

      new Chart(document.getElementById('active-vs-inactive-users'), {
          type: 'doughnut',
          data: {
              labels: ['Active', 'Inactive'],
              datasets: [{
                  data: [activeUsers, inactiveUsers],
                  backgroundColor: ['#4caf50', '#f44336'],
              }],
          },
      });

      // Subscription Plans Distribution
      const plans = await fetchData("SELECT subscription_plan, COUNT(*) as count FROM dim_user GROUP BY subscription_plan;");
      const planLabels = plans.map(plan => plan[0]);
      const planCounts = plans.map(plan => plan[1]);

      new Chart(document.getElementById('user-subscription-plans'), {
          type: 'bar',
          data: {
              labels: planLabels,
              datasets: [{
                  label: 'Users per Plan',
                  data: planCounts,
                  backgroundColor: ['#ff9800', '#2196f3', '#8bc34a'],
              }],
          },
      });

      // Wallet Average Balance
      const walletData = await fetchData("SELECT AVG(balance) FROM dim_wallet;");
      const avgBalance = walletData[0]?.[0] || 0;

      new Chart(document.getElementById('wallet-avg-balance'), {
          type: 'bar',
          data: {
              labels: ['Average Wallet Balance'],
              datasets: [{
                  data: [avgBalance],
                  backgroundColor: ['#03a9f4'],
              }],
          },
      });

      // Active vs Inactive Wallets
      const wallets = await fetchData("SELECT is_active FROM dim_wallet;");
      const activeWallets = wallets.filter(wallet => wallet[0] === 1).length;
      const inactiveWallets = wallets.length - activeWallets;

      new Chart(document.getElementById('active-vs-inactive-wallets'), {
          type: 'doughnut',
          data: {
              labels: ['Active', 'Inactive'],
              datasets: [{
                  data: [activeWallets, inactiveWallets],
                  backgroundColor: ['#4caf50', '#f44336'],
              }],
          },
      });

      // Transactions Per Year
      const transactionsPerYear = await fetchData("SELECT substr(transaction_date, 1, 4) as year, COUNT(*) FROM fact_transaction GROUP BY year;");
      const transactionYears = transactionsPerYear.map(tx => tx[0]);
      const transactionCounts = transactionsPerYear.map(tx => tx[1]);

      new Chart(document.getElementById('transactions-per-year'), {
          type: 'line',
          data: {
              labels: transactionYears,
              datasets: [{
                  label: 'Transactions Per Year',
                  data: transactionCounts,
                  borderColor: '#673ab7',
                  fill: false,
              }],
          },
      });

      // Service Type Distribution
      const serviceTypes = await fetchData("SELECT service_type, COUNT(*) FROM fact_transaction GROUP BY service_type;");
      const serviceLabels = serviceTypes.map(st => st[0]);
      const serviceCounts = serviceTypes.map(st => st[1]);

      new Chart(document.getElementById('service-type-distribution'), {
          type: 'pie',
          data: {
              labels: serviceLabels,
              datasets: [{
                  data: serviceCounts,
                  backgroundColor: ['#ff5722', '#607d8b', '#9c27b0', '#e91e63'],
              }],
          },
      });
  };

  // Run the chart population
  await populateCharts();
});
