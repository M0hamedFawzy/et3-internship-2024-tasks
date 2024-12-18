import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:gocash_app/modules/signin_screen/signin_screen.dart';
// import '';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {

  GlobalKey<FormState> _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black, // Step 2: Change background to black
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Top Section with Register Text
            Container(
              height: 90,
              decoration: BoxDecoration(
                color: Colors.black,
              ),
              child: Center(
                child: Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      'Register',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 28,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    SizedBox(width: 10),
                  ],
                ),
              ),
            ),
            // Step 3: Wrap the rest of the content inside a white Container
            Container(
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(30),
                  topRight: Radius.circular(30),
                ),
              ),
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: 20.0),
                child: Column(
                  children: [
                    SizedBox(height: 80),
                    // GoCash Logo or Placeholder
                    Image.asset(
                      'assets/GoCash.png',
                      height: 120,
                    ),
                    SizedBox(height: 80),
                    // Instruction Text
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 30.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Enter your User Name and Phone Number',
                            textAlign: TextAlign.left,
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          SizedBox(height: 8),
                          Text(
                            'Please confirm your country code and enter your phone number along with your user name.',
                            textAlign: TextAlign.left,
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey,
                            ),
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 30),
                    // Username Field
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 30.0),
                      child: Column(
                        children: [
                          TextFormField(
                            decoration: InputDecoration(
                              labelText: 'Username',
                              border: UnderlineInputBorder(),
                            ),
                          ),
                          SizedBox(height: 30),
                          // Country Code and Phone Number Row
                          Row(
                            children: [
                              Expanded(
                                flex: 1,
                                child: DropdownButtonFormField<String>(
                                  decoration: InputDecoration(
                                    labelText: 'Country Code',
                                    border: UnderlineInputBorder(),
                                  ),
                                  value: '+02',
                                  items: ['+01', '+02', '+03']
                                      .map((code) => DropdownMenuItem(
                                    value: code,
                                    child: Text(code),
                                  ))
                                      .toList(),
                                  onChanged: (value) {},
                                ),
                              ),
                              SizedBox(width: 10),
                              Expanded(
                                flex: 3,
                                child: TextFormField(
                                  decoration: InputDecoration(
                                    labelText: 'Phone number',
                                    border: UnderlineInputBorder(),
                                  ),
                                ),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 80),
                    // Register Button
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 30.0),
                      child: ElevatedButton(
                        onPressed: () {},
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.black,
                          shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(8),
                          ),
                          padding: EdgeInsets.symmetric(vertical: 15),
                        ),
                        child: Center(
                          child: Text(
                            'Register',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                            ),
                          ),
                        ),
                      ),
                    ),
                    SizedBox(height: 8),
                    // Sign In Link
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text(
                          'Already have an account?',
                          style: TextStyle(color: Colors.black),
                        ),
                        TextButton(
                          onPressed: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => SigninScreen(),
                              ),
                            );
                          },
                          child: Text(
                            'SignIn',
                            style: TextStyle(color: Colors.blue),
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 40),
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );

  }
}
