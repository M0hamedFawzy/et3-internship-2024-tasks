import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class PasswordScreen extends StatefulWidget {
  const PasswordScreen({super.key});

  @override
  State<PasswordScreen> createState() => _PasswordScreenState();
}

class _PasswordScreenState extends State<PasswordScreen> {
  List<String> input = [];
  final int passwordLength = 5;
  final String correctPassword = "12345"; // Example password

  void addInput(String digit) {
    if (input.length < passwordLength) {
      setState(() {
        input.add(digit);
      });

      if (input.length == passwordLength) {
        checkPassword();
      }
    }
  }

  void checkPassword() {
    if (input.join() == correctPassword) {
      // Navigate to another screen if the password is correct
      Navigator.push(context, MaterialPageRoute(builder: (_) => SuccessScreen()));
    } else {
      // Shake animation and change dots to red, then reset
      setState(() {
        // Show error state
      });
      Future.delayed(Duration(seconds: 1), () {
        setState(() {
          input.clear();
        });
      });
    }
  }

  void removeLastInput() {
    if (input.isNotEmpty) {
      setState(() {
        input.removeLast();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Text(
            'Hi, Mohamed',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: 8),
          Text(
            'Enter your password',
            style: TextStyle(
              fontSize: 16,
              color: Colors.grey,
            ),
          ),
          SizedBox(height: 20),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: List.generate(
              passwordLength,
                  (index) => Padding(
                padding: const EdgeInsets.symmetric(horizontal: 4.0),
                child: CircleAvatar(
                  radius: 8,
                  backgroundColor: index < input.length
                      ? (input.length == passwordLength && input.join() != correctPassword
                      ? Colors.red
                      : Colors.blue)
                      : Colors.grey,
                ),
              ),
            ),
          ),
          SizedBox(height: 40),
          buildKeypad(),
          SizedBox(height: 20),
          GestureDetector(
            onTap: () {
              // Navigate to the Forgot Password screen
            },
            child: Text(
              'Forgot Password?',
              style: TextStyle(
                color: Colors.blue,
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget buildKeypad() {
    return GridView.builder(
      shrinkWrap: true,
      itemCount: 12,
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 3,
        mainAxisSpacing: 10,
        crossAxisSpacing: 10,
      ),
      itemBuilder: (context, index) {
        if (index == 9) {
          return SizedBox.shrink(); // Empty space for layout
        } else if (index == 11) {
          return GestureDetector(
            onTap: removeLastInput,
            child: Center(
              child: Icon(
                Icons.backspace,
                size: 24,
              ),
            ),
          );
        } else {
          final digit = index == 10 ? '0' : '${index + 1}';
          return GestureDetector(
            onTap: () => addInput(digit),
            child: Center(
              child: Text(
                digit,
                style: TextStyle(
                  fontSize: 24,
                  fontWeight: FontWeight.bold,
                  color: Colors.black,
                ),
              ),
            ),
          );
        }
      },
    );
  }
}

class SuccessScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(child: Text("Success!")),
    );
  }
}


