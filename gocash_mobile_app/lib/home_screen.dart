import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool _isBalanceVisible = true;
  PageController _pageController = PageController();
  int _currentPage = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          children: [
            // Header Section
            Container(
              padding: EdgeInsets.symmetric(horizontal: 16.0, vertical: 10.0),
              color: Colors.white,
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        'Home',
                        style: TextStyle(
                          fontSize: 24.0,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      SizedBox(height: 8.0),
                      Row(
                        children: [
                          Text(
                            _isBalanceVisible ? 'EGP 1500' : '#######',
                            style: TextStyle(
                              fontSize: 22.0,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          SizedBox(width: 20.0),
                          GestureDetector(
                            onTap: () {
                              setState(() {
                                _isBalanceVisible = !_isBalanceVisible;
                              });
                            },
                            child: Icon(
                              _isBalanceVisible ? Icons.visibility : Icons.visibility_off,
                              color: Colors.grey,
                            ),
                          ),
                        ],
                      ),
                      Text(
                        'Current balance',
                        style: TextStyle(
                          color: Colors.grey,
                          fontSize: 14.0,
                        ),
                      ),
                    ],
                  ),
                  CircleAvatar(
                    backgroundColor: Colors.grey.shade200,
                    radius: 20.0,
                  ),
                ],
              ),
            ),
            SizedBox(height: 20.0),

            // Action Buttons Section
            SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              padding: EdgeInsets.symmetric(horizontal: 16.0),
              child: Row(
                children: [
                  _buildActionButton(Icons.add, 'Charge wallet', Colors.black, Colors.white),
                  SizedBox(width: 60.0),
                  _buildActionButton(Icons.arrow_forward, 'Send money', Colors.grey.shade300, Colors.black),
                  SizedBox(width: 60.0),
                  _buildActionButton(Icons.swap_horiz, 'Transfers', Colors.white, Colors.black, borderColor: Colors.grey.shade300),
                ],
              ),
            ),
            SizedBox(height: 40.0),

            // Scrollable Banners Section
            Container(
              height: 150.0,
              child: PageView(
                controller: _pageController,
                onPageChanged: (int page) {
                  setState(() {
                    _currentPage = page;
                  });
                },
                children: [
                  Container(
                    margin: EdgeInsets.symmetric(horizontal: 16.0),
                    decoration: BoxDecoration(
                      color: Colors.grey.shade200,
                      borderRadius: BorderRadius.circular(10.0),
                    ),
                  ),
                  Container(
                    margin: EdgeInsets.symmetric(horizontal: 16.0),
                    decoration: BoxDecoration(
                      color: Colors.grey.shade200,
                      borderRadius: BorderRadius.circular(10.0),
                    ),
                  ),
                  Container(
                    margin: EdgeInsets.symmetric(horizontal: 16.0),
                    decoration: BoxDecoration(
                      color: Colors.grey.shade200,
                      borderRadius: BorderRadius.circular(10.0),
                    ),
                  ),
                ],
              ),
            ),
            SizedBox(height: 15.0),
            // Indicator Dots
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: List.generate(
                3, // Number of pages
                    (index) => _buildDot(index == _currentPage),
              ),
            ),
            SizedBox(height: 20.0),

            // Placeholder Illustration
            Expanded(
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Image.asset(
                      'assets/nothing-here.png',
                      height: 220.0,
                    ),
                    SizedBox(height: 1.0),
                    Text(
                      'Nothing here yet',
                      style: TextStyle(
                        color: Colors.grey,
                        fontSize: 16.0,
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        type: BottomNavigationBarType.fixed,
        items: [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.shopping_bag), label: 'Store'),
          BottomNavigationBarItem(icon: Icon(Icons.bar_chart), label: 'Insights'),
          BottomNavigationBarItem(icon: Icon(Icons.eco), label: 'Green'),
        ],
        selectedItemColor: Colors.black,
        unselectedItemColor: Colors.grey,
        showSelectedLabels: false,
        showUnselectedLabels: false,
      ),
    );
  }

  Widget _buildActionButton(IconData icon, String label, Color bgColor, Color iconColor, {Color? borderColor}) {
    return Column(
      children: [
        Container(
          height: 65.0,
          width: 65.0,
          decoration: BoxDecoration(
            color: bgColor,
            shape: BoxShape.circle,
            border: borderColor != null ? Border.all(color: borderColor) : null,
          ),
          child: Icon(icon, color: iconColor),
        ),
        SizedBox(height: 8.0),
        Text(label, style: TextStyle(fontSize: 12.0)),
      ],
    );
  }

  Widget _buildDot(bool isActive) {
    return Container(
      margin: EdgeInsets.symmetric(horizontal: 4.0),
      height: 8.0,
      width: 8.0,
      decoration: BoxDecoration(
        color: isActive ? Colors.blue : Colors.grey,
        shape: BoxShape.circle,
      ),
    );
  }
}
