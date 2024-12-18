// To parse this JSON data, do
//
//     final user = userFromJson(jsonString);

import 'dart:convert';

User userFromJson(String str) => User.fromJson(json.decode(str));

String userToJson(User data) => json.encode(data.toJson());

class User {
  String success;
  UserClass user;

  User({
    required this.success,
    required this.user,
  });

  factory User.fromJson(Map<String, dynamic> json) => User(
    success: json["success"],
    user: UserClass.fromJson(json["user"]),
  );

  Map<String, dynamic> toJson() => {
    "success": success,
    "user": user.toJson(),
  };
}

class UserClass {
  String username;
  String phoneNumber;
  String subscriptionPlan;
  String token;

  UserClass({
    required this.username,
    required this.phoneNumber,
    required this.subscriptionPlan,
    required this.token,
  });

  factory UserClass.fromJson(Map<String, dynamic> json) => UserClass(
    username: json["username"],
    phoneNumber: json["phone_number"],
    subscriptionPlan: json["subscription_plan"],
    token: json["token"],
  );

  Map<String, dynamic> toJson() => {
    "username": username,
    "phone_number": phoneNumber,
    "subscription_plan": subscriptionPlan,
    "token": token,
  };
}
