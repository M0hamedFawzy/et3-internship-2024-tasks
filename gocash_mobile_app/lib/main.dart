import 'package:flutter/material.dart';
import 'package:gocash_app/charge_confirmation_screen.dart';
import 'package:gocash_app/charge_screen.dart';
import 'package:gocash_app/home_screen.dart';
import 'package:gocash_app/otp_verification_screen.dart';
import 'package:gocash_app/password_screen.dart';
import 'package:gocash_app/register_screen.dart';
import 'package:gocash_app/modules/signin_screen/signin_screen.dart';
import 'package:gocash_app/modules/splash_screen/splash_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      // home: OtpVerificationScreen(),
      // home: RegisterScreen(),
      // home: SigninScreen(),
      // home: HomeScreen(),
      // home: ChargeScreen(),
      // home: ChargeConfirmationScreen(),
      // home: PasswordScreen(),
      home: SplashScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

