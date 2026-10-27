import 'dart:convert';
import 'dart:math';
import 'dart:typed_data';

import 'package:crypto/crypto.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../data/skill_data.dart';

/// Local user record.
class AppUser {
  final String email;
  final String username;
  final String fullName;
  final String role;
  final String targetRole;
  final String experienceLevel;
  final String passwordHash;
  final String salt;
  final int failedAttempts;
  final int lockedUntilMs;

  const AppUser({
    required this.email,
    required this.username,
    required this.fullName,
    required this.role,
    required this.targetRole,
    required this.experienceLevel,
    required this.passwordHash,
    required this.salt,
    this.failedAttempts = 0,
    this.lockedUntilMs = 0,
  });

  String get initials {
    final parts = fullName.trim().split(RegExp(r'\s+'));
    return parts.take(2).map((p) => p.isNotEmpty ? p[0].toUpperCase() : '').join();
  }

  Map<String, dynamic> toJson() => {
        'email': email,
        'username': username,
        'fullName': fullName,
        'role': role,
        'targetRole': targetRole,
        'experienceLevel': experienceLevel,
        'passwordHash': passwordHash,
        'salt': salt,
        'failedAttempts': failedAttempts,
        'lockedUntilMs': lockedUntilMs,
      };

  factory AppUser.fromJson(Map<String, dynamic> j) => AppUser(
        email: j['email'] ?? '',
        username: j['username'] ?? '',
        fullName: j['fullName'] ?? '',
        role: j['role'] ?? 'Student',
        targetRole: j['targetRole'] ?? 'Full Stack Developer',
        experienceLevel: j['experienceLevel'] ?? 'Undergraduate / Fresher',
        passwordHash: j['passwordHash'] ?? '',
        salt: j['salt'] ?? '',
        failedAttempts: j['failedAttempts'] ?? 0,
        lockedUntilMs: j['lockedUntilMs'] ?? 0,
      );

  AppUser copyWith({int? failedAttempts, int? lockedUntilMs, String? targetRole}) =>
      AppUser(
        email: email,
        username: username,
        fullName: fullName,
        role: role,
        targetRole: targetRole ?? this.targetRole,
        experienceLevel: experienceLevel,
        passwordHash: passwordHash,
        salt: salt,
        failedAttempts: failedAttempts ?? this.failedAttempts,
        lockedUntilMs: lockedUntilMs ?? this.lockedUntilMs,
      );
}

/// Result wrapper for auth operations.
class AuthResult {
  final bool ok;
  final String message;
  final AppUser? user;
  const AuthResult(this.ok, this.message, [this.user]);
}

/// PBKDF2-HMAC-SHA256 password hashing (mirrors the Python backend).
const int _kPbkdf2Iterations = 20000; // reduced for mobile UX; original: 200k
const int _kLockoutMinutes = 15;
const int _kMaxAttempts = 5;

class AuthService {
  static const _usersKey = 'skillgap_users_v1';
  static const _sessionKey = 'skillgap_session_email';

  final SharedPreferences _prefs;
  AuthService(this._prefs);

  static Future<AuthService> create() async {
    final prefs = await SharedPreferences.getInstance();
    final svc = AuthService(prefs);
    await svc._seedDemoAccounts();
    return svc;
  }

  // ---- crypto helpers ----

  static String _randomSalt() {
    final rng = Random.secure();
    final bytes = List<int>.generate(16, (_) => rng.nextInt(256));
    return bytes.map((b) => b.toRadixString(16).padLeft(2, '0')).join();
  }

  /// PBKDF2-HMAC-SHA256.
  static String _hashPassword(String password, String salt) {
    final hmacSha256 = Hmac(sha256, utf8.encode(password));
    final saltBytes = utf8.encode(salt);
    // Single block (dkLen <= hLen) PBKDF2:
    // U1 = HMAC(password, salt || INT(1)); iterate.
    final block = Uint8List(saltBytes.length + 4)
      ..setRange(0, saltBytes.length, saltBytes)
      ..[saltBytes.length + 3] = 1;
    var u = hmacSha256.convert(block).bytes;
    var result = List<int>.from(u);
    for (var i = 1; i < _kPbkdf2Iterations; i++) {
      u = hmacSha256.convert(u).bytes;
      for (var j = 0; j < result.length; j++) {
        result[j] ^= u[j];
      }
    }
    return result.map((b) => b.toRadixString(16).padLeft(2, '0')).join();
  }

  /// Password strength (0-100, label) — same rules as database.py.
  static (int, String) passwordStrength(String password) {
    if (password.isEmpty) return (0, "Empty");
    var score = 0;
    if (password.length >= 6) score += 25;
    if (password.length >= 10) score += 15;
    if (RegExp(r'[a-z]').hasMatch(password)) score += 15;
    if (RegExp(r'[A-Z]').hasMatch(password)) score += 15;
    if (RegExp(r'[0-9]').hasMatch(password)) score += 15;
    if (RegExp(r'''[@$!%*#?&^()_+={}\[\]:;<>,.?~\\/\-]''').hasMatch(password)) score += 15;
    score = score.clamp(0, 100);
    final label = score < 40
        ? "Weak"
        : score < 70
            ? "Medium"
            : score < 90
                ? "Strong"
                : "Excellent";
    return (score, label);
  }

  // ---- user store ----

  Map<String, AppUser> _loadUsers() {
    final raw = _prefs.getString(_usersKey);
    if (raw == null) return {};
    try {
      final map = jsonDecode(raw) as Map<String, dynamic>;
      return map.map((k, v) => MapEntry(k, AppUser.fromJson(v)));
    } catch (_) {
      return {};
    }
  }

  Future<void> _saveUsers(Map<String, AppUser> users) {
    return _prefs.setString(
        _usersKey, jsonEncode(users.map((k, v) => MapEntry(k, v.toJson()))));
  }

  Future<void> _seedDemoAccounts() async {
    final users = _loadUsers();
    var changed = false;
    for (final d in kDemoAccounts) {
      if (!users.containsKey(d.email)) {
        final salt = _randomSalt();
        users[d.email] = AppUser(
          email: d.email,
          username: d.email.split('@').first,
          fullName: d.fullName,
          role: d.role,
          targetRole: d.targetRole,
          experienceLevel: kExperienceLevels.first,
          passwordHash: _hashPassword(d.password, salt),
          salt: salt,
        );
        changed = true;
      }
    }
    if (changed) await _saveUsers(users);
  }

  // ---- public API ----

  Future<AuthResult> register({
    required String email,
    required String password,
    required String fullName,
    String targetRole = 'Full Stack Developer',
    String experienceLevel = 'Undergraduate / Fresher',
  }) async {
    email = email.trim().toLowerCase();
    if (email.isEmpty || !email.contains('@')) {
      return const AuthResult(false, "Please provide a valid email address.");
    }
    if (password.length < 6) {
      return const AuthResult(false, "Password must be at least 6 characters long.");
    }
    final users = _loadUsers();
    if (users.containsKey(email)) {
      return const AuthResult(false, "An account with this email already exists.");
    }
    final salt = _randomSalt();
    final user = AppUser(
      email: email,
      username: email.split('@').first,
      fullName: fullName.trim().isEmpty ? email.split('@').first : fullName.trim(),
      role: 'Student',
      targetRole: targetRole,
      experienceLevel: experienceLevel,
      passwordHash: _hashPassword(password, salt),
      salt: salt,
    );
    users[email] = user;
    await _saveUsers(users);
    await setSession(email);
    return AuthResult(true, "Account registered successfully!", user);
  }

  Future<AuthResult> login(String identifier, String password) async {
    identifier = identifier.trim().toLowerCase();
    if (identifier.isEmpty || password.isEmpty) {
      return const AuthResult(false, "Please enter both identifier and password.");
    }
    final users = _loadUsers();
    AppUser? user = users[identifier];
    if (user == null) {
      // try username match
      for (final u in users.values) {
        if (u.username.toLowerCase() == identifier) {
          user = u;
          break;
        }
      }
    }
    if (user == null) {
      return const AuthResult(false, "Invalid email/username or password.");
    }

    // lockout check
    if (user.lockedUntilMs > 0) {
      final remaining = user.lockedUntilMs - DateTime.now().millisecondsSinceEpoch;
      if (remaining > 0) {
        final mins = (remaining / 60000).ceil();
        return AuthResult(false,
            "Account locked due to $_kMaxAttempts failed attempts. Retry in $mins minute(s).");
      } else {
        user = user.copyWith(failedAttempts: 0, lockedUntilMs: 0);
      }
    }

    if (_hashPassword(password, user.salt) != user.passwordHash) {
      final fails = user.failedAttempts + 1;
      final lockMs = fails >= _kMaxAttempts
          ? DateTime.now().millisecondsSinceEpoch + _kLockoutMinutes * 60000
          : 0;
      users[user.email] = user.copyWith(failedAttempts: fails, lockedUntilMs: lockMs);
      await _saveUsers(users);
      return AuthResult(
          false,
          fails >= _kMaxAttempts
              ? "Account locked for $_kLockoutMinutes minutes due to $_kMaxAttempts failed attempts."
              : "Invalid password. Attempt $fails of $_kMaxAttempts before lockout.");
    }

    users[user.email] = user.copyWith(failedAttempts: 0, lockedUntilMs: 0);
    await _saveUsers(users);
    await setSession(user.email);
    return AuthResult(true, "Welcome back, ${user.fullName}!", user);
  }

  Future<AuthResult> resetPassword(String email, String newPassword) async {
    email = email.trim().toLowerCase();
    if (!email.contains('@')) {
      return const AuthResult(false, "Please enter a valid registered email.");
    }
    if (newPassword.length < 6) {
      return const AuthResult(false, "New password must be at least 6 characters.");
    }
    final users = _loadUsers();
    final user = users[email];
    if (user == null) {
      return const AuthResult(false, "No account found matching this email address.");
    }
    final salt = _randomSalt();
    users[email] = AppUser(
      email: user.email,
      username: user.username,
      fullName: user.fullName,
      role: user.role,
      targetRole: user.targetRole,
      experienceLevel: user.experienceLevel,
      passwordHash: _hashPassword(newPassword, salt),
      salt: salt,
    );
    await _saveUsers(users);
    return const AuthResult(true, "Password updated! You can now sign in.");
  }

  Future<AppUser?> loginDemo(String email) async {
    final res = await login(email, 'Password123!');
    return res.user;
  }

  Future<void> updateTargetRole(String email, String role) async {
    final users = _loadUsers();
    final user = users[email];
    if (user == null) return;
    users[email] = user.copyWith(targetRole: role);
    await _saveUsers(users);
  }

  // ---- session ----

  Future<void> setSession(String email) => _prefs.setString(_sessionKey, email);

  Future<void> clearSession() => _prefs.remove(_sessionKey);

  AppUser? currentUser() {
    final email = _prefs.getString(_sessionKey);
    if (email == null) return null;
    return _loadUsers()[email];
  }
}
