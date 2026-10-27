import 'package:flutter/material.dart';

import '../app_state.dart';
import '../theme.dart';
import '../widgets/widgets.dart';
import 'auth_screen.dart';
import 'home_shell.dart';

/// Cinematic splash — gradient logo pulse + progress bar, then routes to
/// the dashboard (if a session exists) or the auth screen.
class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late final AnimationController _ctrl;
  late final Animation<double> _scale;
  late final Animation<double> _fade;
  late final Animation<double> _bar;

  @override
  void initState() {
    super.initState();
    _ctrl = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 2100));
    _scale = Tween(begin: 0.8, end: 1.0).animate(CurvedAnimation(
        parent: _ctrl,
        curve: const Interval(0, 0.45, curve: Curves.easeOutCubic)));
    _fade = Tween(begin: 0.0, end: 1.0).animate(CurvedAnimation(
        parent: _ctrl,
        curve: const Interval(0, 0.4, curve: Curves.easeOut)));
    _bar = Tween(begin: 0.0, end: 1.0).animate(CurvedAnimation(
        parent: _ctrl,
        curve: const Interval(0.15, 0.95, curve: Curves.easeInOut)));
    _ctrl.forward().then((_) => _route());
  }

  void _route() {
    if (!mounted) return;
    final loggedIn = AppState.instance.user != null;
    Navigator.of(context).pushReplacement(PageRouteBuilder(
      transitionDuration: const Duration(milliseconds: 500),
      pageBuilder: (_, _, _) =>
          loggedIn ? const HomeShell() : const AuthScreen(),
      transitionsBuilder: (_, anim, _, child) =>
          FadeTransition(opacity: anim, child: child),
    ));
  }

  @override
  void dispose() {
    _ctrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: const BoxDecoration(
          gradient: RadialGradient(
            center: Alignment.center,
            radius: 1.2,
            colors: [Color(0xFF0F172A), SG.bg],
          ),
        ),
        child: Center(
          child: FadeTransition(
            opacity: _fade,
            child: ScaleTransition(
              scale: _scale,
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const BrandLogo(size: 92),
                  const SizedBox(height: 24),
                  const _GradientTitle(),
                  const SizedBox(height: 6),
                  const Text('ADVANCED CAREER INTELLIGENCE',
                      style: TextStyle(
                          fontSize: 11,
                          fontWeight: FontWeight.w700,
                          color: SG.textSecondary,
                          letterSpacing: 3)),
                  const SizedBox(height: 30),
                  SizedBox(
                    width: 170,
                    child: AnimatedBuilder(
                      animation: _bar,
                      builder: (_, _) => ClipRRect(
                        borderRadius: BorderRadius.circular(999),
                        child: LinearProgressIndicator(
                          value: _bar.value,
                          minHeight: 4,
                          backgroundColor: const Color(0x14FFFFFF),
                          valueColor:
                              const AlwaysStoppedAnimation(SG.indigo),
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _GradientTitle extends StatelessWidget {
  const _GradientTitle();

  @override
  Widget build(BuildContext context) {
    return Text.rich(
      TextSpan(children: [
        const TextSpan(text: 'SkillGap ', style: TextStyle(color: Colors.white)),
        TextSpan(
          text: 'AI',
          style: TextStyle(
            foreground: Paint()
              ..shader = const LinearGradient(colors: [SG.indigo, SG.cyanLight])
                  .createShader(const Rect.fromLTWH(0, 0, 60, 40)),
          ),
        ),
      ]),
      style: const TextStyle(
          fontSize: 38, fontWeight: FontWeight.w900, letterSpacing: -1),
    );
  }
}
