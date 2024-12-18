import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import '../../otp_verification_screen.dart';
import '../../register_screen.dart';
import '../../shared/network/local/signin.dart';

class SigninScreen extends StatefulWidget {
  const SigninScreen({super.key});

  @override
  State<SigninScreen> createState() => _SigninScreenState();
}

class _SigninScreenState extends State<SigninScreen> {
  final _phoneController = TextEditingController();
  String _countryCode = '+02';

  @override
  void dispose() {
    _phoneController.dispose();
    super.dispose();
  }

  // Function to validate Egyptian phone number
  bool isValidEgyptianNumber(String phoneNumber) {
    final regex = RegExp(r'^0(11|12|10|15)\d{8}$');
    return regex.hasMatch(phoneNumber) && phoneNumber.length == 11;
  }

  // Function to handle sign in
  Future<void> _handleSignIn() async {
    final phoneNumber = _phoneController.text.trim();

    if (_countryCode == '+02' && !isValidEgyptianNumber(phoneNumber)) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Invalid phone number.')),
      );
      return;
    }

    try {
      final user = await signIn(phoneNumber);
      if (user != null) {
        // Navigate to the OTP verification screen on success
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => OtpVerificationScreen()),
        );
      }
    } catch (error) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Sign-in failed: $error')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black,
      body: SingleChildScrollView(
        child: Column(
          children: [
            // UI code remains unchanged...
            Container(
              height: 90,
              decoration: const BoxDecoration(
                color: Colors.black,
              ),
              child: Center(
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Text(
                      'Sign In',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ],
                ),
              ),
            ),
            // Rest of the UI code...
            Container(
              decoration: const BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(30),
                  topRight: Radius.circular(30),
                ),
              ),
              child: Column(
                children: [
                  const SizedBox(height: 80),
                  Image.asset(
                    'assets/GoCash.png',
                    height: 120,
                  ),
                  const SizedBox(height: 80),
                  const Padding(
                    padding: EdgeInsets.symmetric(horizontal: 30.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Enter your Phone Number',
                          textAlign: TextAlign.left,
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                        SizedBox(height: 8),
                        Text(
                          'Please confirm your country code and enter your phone number.',
                          textAlign: TextAlign.left,
                          style: TextStyle(
                            fontSize: 12,
                            color: Colors.grey,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 50),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 30.0),
                    child: Row(
                      children: [
                        Expanded(
                          flex: 1,
                          child: DropdownButtonFormField<String>(
                            decoration: const InputDecoration(
                              labelText: 'Country Code',
                              border: UnderlineInputBorder(),
                            ),
                            value: _countryCode,
                            items: ['+02']
                                .map((code) => DropdownMenuItem(
                              value: code,
                              child: Text(code),
                            ))
                                .toList(),
                            onChanged: (value) {
                              setState(() {
                                _countryCode = value!;
                              });
                            },
                          ),
                        ),
                        const SizedBox(width: 10),
                        Expanded(
                          flex: 3,
                          child: TextFormField(
                            controller: _phoneController,
                            decoration: const InputDecoration(
                              labelText: 'Phone number',
                              border: UnderlineInputBorder(),
                            ),
                            keyboardType: TextInputType.phone,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 120),
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 30.0),
                    child: ElevatedButton(
                      onPressed: _handleSignIn,
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.black,
                        shape: RoundedRectangleBorder(
                          borderRadius: BorderRadius.circular(8),
                        ),
                        padding: const EdgeInsets.symmetric(vertical: 15),
                      ),
                      child: const Center(
                        child: Text(
                          'Sign In',
                          style: TextStyle(
                            color: Colors.white,
                            fontSize: 16,
                          ),
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Text(
                        'Don\'t have an account?',
                        style: TextStyle(color: Colors.black),
                      ),
                      TextButton(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => RegisterScreen(),
                            ),
                          );
                        },
                        child: const Text(
                          'Create one',
                          style: TextStyle(color: Colors.blue),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 100),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
