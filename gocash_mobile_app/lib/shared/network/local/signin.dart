import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../../models/user.dart';

Future<User?> signIn(String phoneNumber) async {
  final url = Uri.parse('http://10.0.2.2:8000/sign_in/');
  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'phone_number': phoneNumber}),
  );

  if (response.statusCode == 200) {
    return userFromJson(response.body);
  } else {
    throw Exception('Failed to sign in. Please check your credentials.');
  }
}
