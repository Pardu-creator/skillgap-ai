import 'package:flutter/material.dart';

import 'app_state.dart';
import 'screens/splash_screen.dart';
import 'theme.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(const SkillGapApp());
}

class SkillGapApp extends StatefulWidget {
  const SkillGapApp({super.key});

  @override
  State<SkillGapApp> createState() => _SkillGapAppState();
}

class _SkillGapAppState extends State<SkillGapApp> {
  bool _ready = false;

  @override
  void initState() {
    super.initState();
    AppState.instance.init().then((_) {
      if (mounted) setState(() => _ready = true);
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'SkillGap AI',
      debugShowCheckedModeBanner: false,
      theme: SG.theme(),
      home: _ready
          ? const SplashScreen()
          : const Scaffold(
              backgroundColor: SG.bg,
              body: Center(child: CircularProgressIndicator(color: SG.indigo)),
            ),
    );
  }
}
