import 'package:flutter/material.dart';

import '../app_state.dart';
import '../data/skill_data.dart';
import '../services/auth_service.dart';
import '../theme.dart';
import '../widgets/widgets.dart';
import 'home_shell.dart';

/// Sign In / Create Account / Reset Password — port of the auth modal.
class AuthScreen extends StatefulWidget {
  const AuthScreen({super.key});

  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  int _tab = 0;
  bool _busy = false;

  final _signinId = TextEditingController();
  final _signinPwd = TextEditingController();
  final _regName = TextEditingController();
  final _regEmail = TextEditingController();
  final _regPwd = TextEditingController();
  final _regPwd2 = TextEditingController();
  final _resetEmail = TextEditingController();
  final _resetPwd = TextEditingController();
  final _resetPwd2 = TextEditingController();

  String _regRole = kTargetRoles.first;
  String _regExp = kExperienceLevels.first;
  (int, String) _pwdStrength = (0, 'Empty');

  @override
  void dispose() {
    for (final c in [
      _signinId, _signinPwd, _regName, _regEmail, _regPwd, _regPwd2,
      _resetEmail, _resetPwd, _resetPwd2,
    ]) {
      c.dispose();
    }
    super.dispose();
  }

  void _err(String msg) => sgToast(context, msg);

  Future<void> _goHome(AppUser user) async {
    AppState.instance.setUser(user);
    if (!mounted) return;
    Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (_) => const HomeShell()));
  }

  Future<void> _signIn() async {
    setState(() => _busy = true);
    final res = await AppState.instance.auth!
        .login(_signinId.text, _signinPwd.text);
    if (!mounted) return;
    setState(() => _busy = false);
    if (res.ok) {
      await _goHome(res.user!);
    } else {
      _err(res.message);
    }
  }

  Future<void> _demoLogin(DemoAccount d) async {
    setState(() => _busy = true);
    final user = await AppState.instance.auth!.loginDemo(d.email);
    if (!mounted) return;
    setState(() => _busy = false);
    if (user != null) {
      sgToast(context, 'Logged in as ${user.fullName}');
      await _goHome(user);
    } else {
      _err('Demo login failed.');
    }
  }

  Future<void> _register() async {
    if (_regName.text.trim().isEmpty || _regEmail.text.trim().isEmpty) {
      _err('Please fill in all required fields.');
      return;
    }
    if (!_regEmail.text.contains('@')) {
      _err('Please enter a valid email address.');
      return;
    }
    if (_regPwd.text.length < 6) {
      _err('Password must be at least 6 characters.');
      return;
    }
    if (_regPwd.text != _regPwd2.text) {
      _err('Passwords do not match.');
      return;
    }
    setState(() => _busy = true);
    final res = await AppState.instance.auth!.register(
      email: _regEmail.text,
      password: _regPwd.text,
      fullName: _regName.text,
      targetRole: _regRole,
      experienceLevel: _regExp,
    );
    if (!mounted) return;
    setState(() => _busy = false);
    if (res.ok) {
      sgToast(context, res.message);
      await _goHome(res.user!);
    } else {
      _err(res.message);
    }
  }

  Future<void> _reset() async {
    if (_resetPwd.text != _resetPwd2.text) {
      _err('Passwords do not match.');
      return;
    }
    setState(() => _busy = true);
    final res = await AppState.instance.auth!
        .resetPassword(_resetEmail.text, _resetPwd.text);
    if (!mounted) return;
    setState(() => _busy = false);
    sgToast(context, res.message);
    if (res.ok) setState(() => _tab = 0);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: RadialGradient(
            center: Alignment(0, -0.8),
            radius: 1.4,
            colors: [Color(0x336366F1), SG.bg],
          ),
        ),
        child: SafeArea(
          child: Center(
            child: SingleChildScrollView(
              padding: const EdgeInsets.all(24),
              child: ConstrainedBox(
                constraints: const BoxConstraints(maxWidth: 440),
                child: Column(
                  children: [
                    const BrandLogo(size: 58),
                    const SizedBox(height: 14),
                    Text.rich(
                      TextSpan(children: [
                        const TextSpan(text: 'SkillGap '),
                        TextSpan(
                            text: 'AI',
                            style: TextStyle(
                                foreground: Paint()
                                  ..shader = const LinearGradient(
                                          colors: [SG.indigo, SG.cyanLight])
                                      .createShader(
                                          const Rect.fromLTWH(0, 0, 50, 30)))),
                      ]),
                      style: const TextStyle(
                          fontSize: 26,
                          fontWeight: FontWeight.w900,
                          color: Colors.white,
                          letterSpacing: -0.5),
                    ),
                    const SizedBox(height: 4),
                    const Text(
                        'Welcome back · Sign in to access your career roadmap',
                        textAlign: TextAlign.center,
                        style:
                            TextStyle(fontSize: 13, color: SG.textSecondary)),
                    const SizedBox(height: 22),
                    GlassCard(
                      radius: 18,
                      padding: const EdgeInsets.all(6),
                      child: Row(
                        children: [
                          _tabBtn(0, Icons.lock_outline, 'Sign In'),
                          _tabBtn(1, Icons.auto_awesome, 'Create'),
                          _tabBtn(2, Icons.key_outlined, 'Reset'),
                        ],
                      ),
                    ),
                    const SizedBox(height: 18),
                    GlassCard(
                      radius: 18,
                      child: AnimatedSize(
                        duration: const Duration(milliseconds: 250),
                        child: _tab == 0
                            ? _signInPane()
                            : _tab == 1
                                ? _registerPane()
                                : _resetPane(),
                      ),
                    ),
                    const SizedBox(height: 20),
                    const Text('Secured by local storage · PBKDF2-SHA256',
                        style: TextStyle(fontSize: 11, color: SG.textMuted)),
                  ],
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }

  Widget _tabBtn(int i, IconData icon, String label) {
    final active = _tab == i;
    return Expanded(
      child: GestureDetector(
        onTap: () => setState(() => _tab = i),
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          padding: const EdgeInsets.symmetric(vertical: 10),
          decoration: BoxDecoration(
            color: active ? SG.indigo.withValues(alpha: 0.2) : Colors.transparent,
            borderRadius: BorderRadius.circular(12),
          ),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon,
                  size: 15, color: active ? SG.indigoLight : SG.textSecondary),
              const SizedBox(width: 6),
              Text(label,
                  style: TextStyle(
                      fontSize: 12.5,
                      fontWeight: FontWeight.w700,
                      color: active ? SG.indigoLight : SG.textSecondary)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _signInPane() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        _demoStrip(),
        const SizedBox(height: 16),
        TextField(
          controller: _signinId,
          keyboardType: TextInputType.emailAddress,
          decoration: const InputDecoration(
              labelText: 'Email or Username', hintText: 'demo@skillgap.ai'),
        ),
        const SizedBox(height: 12),
        TextField(
          controller: _signinPwd,
          obscureText: true,
          onSubmitted: (_) => _signIn(),
          decoration: const InputDecoration(labelText: 'Password'),
        ),
        const SizedBox(height: 16),
        GradientButton(
            label: 'Sign In to Dashboard',
            icon: Icons.login_rounded,
            loading: _busy,
            onPressed: _signIn),
      ],
    );
  }

  Widget _demoStrip() {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: SG.indigo.withValues(alpha: 0.08),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: SG.indigo.withValues(alpha: 0.25)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('QUICK ONE-CLICK DEMO PROFILES',
              style: TextStyle(
                  fontSize: 10.5,
                  fontWeight: FontWeight.w800,
                  color: SG.indigoLight,
                  letterSpacing: 0.8)),
          const SizedBox(height: 10),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: [
              for (final d in kDemoAccounts)
                ChipTag('${d.fullName} (${d.targetRole.split(' ').first})',
                    color: SG.indigoLight, onTap: () => _demoLogin(d)),
            ],
          ),
        ],
      ),
    );
  }

  Widget _registerPane() {
    final (score, label) = _pwdStrength;
    final color = score < 40
        ? SG.rose
        : score < 70
            ? SG.amber
            : SG.emerald;
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        TextField(
            controller: _regName,
            decoration: const InputDecoration(
                labelText: 'Full Name', hintText: 'Jane Doe')),
        const SizedBox(height: 12),
        TextField(
            controller: _regEmail,
            keyboardType: TextInputType.emailAddress,
            decoration: const InputDecoration(
                labelText: 'Email Address', hintText: 'jane@example.com')),
        const SizedBox(height: 12),
        TextField(
          controller: _regPwd,
          obscureText: true,
          onChanged: (v) =>
              setState(() => _pwdStrength = AuthService.passwordStrength(v)),
          decoration: const InputDecoration(
              labelText: 'Password', hintText: 'At least 6 characters'),
        ),
        const SizedBox(height: 8),
        Row(children: [
          Expanded(
            child: ClipRRect(
              borderRadius: BorderRadius.circular(999),
              child: LinearProgressIndicator(
                value: score / 100,
                minHeight: 5,
                backgroundColor: const Color(0x14FFFFFF),
                valueColor: AlwaysStoppedAnimation(color),
              ),
            ),
          ),
          const SizedBox(width: 10),
          Text(label,
              style: TextStyle(
                  fontSize: 11, fontWeight: FontWeight.w700, color: color)),
        ]),
        const SizedBox(height: 12),
        TextField(
            controller: _regPwd2,
            obscureText: true,
            decoration:
                const InputDecoration(labelText: 'Confirm Password')),
        const SizedBox(height: 12),
        _dropdown('Target Career Track', _regRole, kTargetRoles,
            (v) => setState(() => _regRole = v!)),
        const SizedBox(height: 12),
        _dropdown('Experience Level', _regExp, kExperienceLevels,
            (v) => setState(() => _regExp = v!)),
        const SizedBox(height: 16),
        GradientButton(
            label: 'Create Free Account',
            icon: Icons.auto_awesome,
            loading: _busy,
            onPressed: _register),
      ],
    );
  }

  Widget _resetPane() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        const Text(
            'Enter your registered email and choose a new password.',
            style: TextStyle(fontSize: 13, color: SG.textSecondary)),
        const SizedBox(height: 14),
        TextField(
            controller: _resetEmail,
            keyboardType: TextInputType.emailAddress,
            decoration:
                const InputDecoration(labelText: 'Registered Email')),
        const SizedBox(height: 12),
        TextField(
            controller: _resetPwd,
            obscureText: true,
            decoration:
                const InputDecoration(labelText: 'New Password')),
        const SizedBox(height: 12),
        TextField(
            controller: _resetPwd2,
            obscureText: true,
            decoration:
                const InputDecoration(labelText: 'Confirm New Password')),
        const SizedBox(height: 16),
        GradientButton(
            label: 'Update Password',
            icon: Icons.key_rounded,
            loading: _busy,
            onPressed: _reset),
      ],
    );
  }

  Widget _dropdown(String label, String value, List<String> items,
      ValueChanged<String?> onChanged) {
    return DropdownButtonFormField<String>(
      initialValue: value,
      items: items
          .map((e) => DropdownMenuItem(
              value: e,
              child: Text(e,
                  style: const TextStyle(fontSize: 13.5),
                  overflow: TextOverflow.ellipsis)))
          .toList(),
      onChanged: onChanged,
      decoration: InputDecoration(labelText: label),
      dropdownColor: SG.bgAlt,
      isExpanded: true,
    );
  }
}
