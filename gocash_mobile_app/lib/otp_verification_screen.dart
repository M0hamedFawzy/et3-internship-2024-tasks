import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';

class OtpVerificationScreen extends StatefulWidget {
  const OtpVerificationScreen({super.key});

  @override
  State<OtpVerificationScreen> createState() => _OtpVerificationScreenState();
}

class _OtpVerificationScreenState extends State<OtpVerificationScreen> {
  // Controllers for OTP fields
  final TextEditingController _otp1Controller = TextEditingController();
  final TextEditingController _otp2Controller = TextEditingController();
  final TextEditingController _otp3Controller = TextEditingController();
  final TextEditingController _otp4Controller = TextEditingController();

  // FocusNodes to manage focus between OTP fields
  final FocusNode _otp1Focus = FocusNode();
  final FocusNode _otp2Focus = FocusNode();
  final FocusNode _otp3Focus = FocusNode();
  final FocusNode _otp4Focus = FocusNode();

  @override
  void dispose() {
    // Dispose controllers and focus nodes
    _otp1Controller.dispose();
    _otp2Controller.dispose();
    _otp3Controller.dispose();
    _otp4Controller.dispose();
    _otp1Focus.dispose();
    _otp2Focus.dispose();
    _otp3Focus.dispose();
    _otp4Focus.dispose();
    super.dispose();
  }

  // Function to build individual OTP TextField
  Widget _buildOtpTextField(
      {required TextEditingController controller,
        required FocusNode focusNode,
        required FocusNode? nextFocus}) {
    return Expanded(
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 5.0),
        child: TextFormField(
          controller: controller,
          focusNode: focusNode,
          keyboardType: TextInputType.number,
          textAlign: TextAlign.center,
          maxLength: 1,
          decoration: InputDecoration(
            counterText: "",
            border: OutlineInputBorder(
              borderRadius: BorderRadius.circular(8.0),
            ),
          ),
          onChanged: (value) {
            if (value.length == 1 && nextFocus != null) {
              FocusScope.of(context).requestFocus(nextFocus);
            }
          },
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.black, // Changed from Colors.white to Colors.black
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Top Section with Verifications
            Container(
              height: 90,
              width: double.infinity, // Ensure it spans the full width
              decoration: BoxDecoration(
                color: Colors.black,
                // No borderRadius as per original design
              ),
              child: Center(
                child: Text(
                  'Verifications',
                  style: TextStyle(
                    color: Colors.white,
                    fontSize: 26,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
            // White Container with Rounded Top Corners
            Container(
              width: double.infinity,
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.only(
                  topLeft: Radius.circular(30),
                  topRight: Radius.circular(30),
                ),
              ),
              // Use Padding to ensure content doesn't overlap with rounded corners
              child: Padding(
                padding: const EdgeInsets.only(top: 40.0, bottom: 20.0),
                child: Column(
                  children: [
                    const SizedBox(height: 80),
                    // GoCash Logo or Placeholder
                    Image.asset(
                      'assets/GoCash.png', // Replace with the actual logo path
                      height: 120,
                    ),
                    const SizedBox(height: 80),
                    // Instruction Text
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 30.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Text(
                            'One more step to start your cash journey',
                            textAlign: TextAlign.left,
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          SizedBox(height: 8),
                          Text(
                            'Enter 4-digit code we’ve sent to ******8231',
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 12,
                              color: Colors.grey,
                            ),
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 40),
                    // OTP Input Fields
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 30.0),
                      child: Row(
                        children: [
                          _buildOtpTextField(
                            controller: _otp1Controller,
                            focusNode: _otp1Focus,
                            nextFocus: _otp2Focus,
                          ),
                          _buildOtpTextField(
                            controller: _otp2Controller,
                            focusNode: _otp2Focus,
                            nextFocus: _otp3Focus,
                          ),
                          _buildOtpTextField(
                            controller: _otp3Controller,
                            focusNode: _otp3Focus,
                            nextFocus: _otp4Focus,
                          ),
                          _buildOtpTextField(
                            controller: _otp4Controller,
                            focusNode: _otp4Focus,
                            nextFocus: null,
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 100),
                    // Cancel and Verify Buttons
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 30.0),
                      child: Row(
                        children: [
                          // Cancel Button
                          Expanded(
                            child: OutlinedButton(
                              onPressed: () {
                                // Handle cancel action
                              },
                              style: OutlinedButton.styleFrom(
                                backgroundColor: Colors.white,
                                side: BorderSide(color: Colors.grey),
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                padding: EdgeInsets.symmetric(vertical: 10),
                              ),
                              child: Text(
                                'Cancel',
                                style: TextStyle(
                                  color: Colors.black,
                                  fontSize: 16,
                                ),
                              ),
                            ),
                          ),
                          SizedBox(width: 10),
                          // Verify Button
                          Expanded(
                            child: ElevatedButton(
                              onPressed: () {
                                // Handle verify action
                              },
                              style: ElevatedButton.styleFrom(
                                backgroundColor: Colors.black,
                                shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(8),
                                ),
                                padding: EdgeInsets.symmetric(vertical: 10),
                              ),
                              child: Text(
                                'Verify',
                                style: TextStyle(
                                  color: Colors.white,
                                  fontSize: 16,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    SizedBox(height: 8),
                    // Resend Verification Code Link
                    Row(
                      mainAxisAlignment: MainAxisAlignment.center, // Center the entire row
                      children: [
                        Text(
                          'Didn’t get the code?',
                          style: TextStyle(color: Colors.black),
                        ),
                        TextButton(
                          onPressed: () {
                            // Handle resend verification code
                          },
                          child: Text(
                            'Resend Verification Code',
                            style: TextStyle(color: Colors.blue),
                          ),
                        ),
                      ],
                    ),
                    SizedBox(height: 90),
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
