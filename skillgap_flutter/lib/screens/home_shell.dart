import 'package:flutter/material.dart';

import '../app_state.dart';
import '../theme.dart';
import '../widgets/widgets.dart';
import 'analytics_screen.dart';
import 'analyzer_screen.dart';
import 'auth_screen.dart';
import 'mentor_screen.dart';
import 'overview_screen.dart';
import 'roadmap_screen.dart';
import 'settings_screen.dart';

/// Main dashboard shell: brand app bar + user pill, bottom navigation dock.
class HomeShell extends StatefulWidget {
  const HomeShell({super.key});

  @override
  State<HomeShell> createState() => _HomeShellState();
}

class _HomeShellState extends State<HomeShell> {
  static const _tabs = [
    (Icons.dashboard_rounded, 'Overview'),
    (Icons.document_scanner_outlined, 'Analyzer'),
    (Icons.bar_chart_rounded, 'Analytics'),
    (Icons.map_outlined, 'Roadmap'),
    (Icons.smart_toy_outlined, 'Mentor'),
  ];

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: AppState.instance,
      builder: (context, _) {
        final user = AppState.instance.user;
        final tab = AppState.instance.activeTab;
        return Scaffold(
          body: Container(
            decoration: SG.pageBg(),
            child: SafeArea(
              child: Column(
                children: [
                  _topBar(user),
                  Expanded(child: _body(tab)),
                ],
              ),
            ),
          ),
          bottomNavigationBar: NavigationBar(
            selectedIndex: tab,
            onDestinationSelected: AppState.instance.setTab,
            backgroundColor: const Color(0xE60A0F1E),
            indicatorColor: SG.indigo.withValues(alpha: 0.3),
            height: 68,
            labelBehavior: NavigationDestinationLabelBehavior.alwaysShow,
            destinations: [
              for (final (icon, label) in _tabs)
                NavigationDestination(icon: Icon(icon), label: label),
            ],
          ),
        );
      },
    );
  }

  Widget _body(int tab) {
    switch (tab) {
      case 1:
        return const AnalyzerScreen();
      case 2:
        return const AnalyticsScreen();
      case 3:
        return const RoadmapScreen();
      case 4:
        return const MentorScreen();
      default:
        return const OverviewScreen();
    }
  }

  Widget _topBar(dynamic user) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 12, 12, 10),
      child: Row(
        children: [
          const BrandLogo(size: 40),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(children: [
                  const Text('SkillGap AI',
                      style: TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.w900,
                          color: SG.text,
                          letterSpacing: -0.4)),
                  const SizedBox(width: 8),
                  Container(
                    padding:
                        const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
                    decoration: BoxDecoration(
                      color: SG.emerald.withValues(alpha: 0.14),
                      borderRadius: BorderRadius.circular(999),
                      border: Border.all(
                          color: SG.emerald.withValues(alpha: 0.3)),
                    ),
                    child: const Row(mainAxisSize: MainAxisSize.min, children: [
                      PulseDot(color: SG.emeraldLight),
                      SizedBox(width: 5),
                      Text('Live App',
                          style: TextStyle(
                              fontSize: 9.5,
                              fontWeight: FontWeight.w800,
                              color: SG.emeraldLight)),
                    ]),
                  ),
                ]),
                const Text('Career Intelligence · AI Mentor · Roadmaps',
                    style: TextStyle(fontSize: 11, color: SG.textMuted)),
              ],
            ),
          ),
          if (user != null)
            GestureDetector(
              onTap: () => Navigator.of(context).push(MaterialPageRoute(
                  builder: (_) => const SettingsScreen())),
              child: Container(
                padding: const EdgeInsets.fromLTRB(4, 4, 10, 4),
                decoration: BoxDecoration(
                  color: SG.cardSoft,
                  borderRadius: BorderRadius.circular(999),
                  border: Border.all(color: Colors.white12),
                ),
                child: Row(children: [
                  CircleAvatar(
                    radius: 15,
                    backgroundColor: SG.indigo,
                    child: Text(user.initials,
                        style: const TextStyle(
                            fontSize: 11,
                            fontWeight: FontWeight.w800,
                            color: Colors.white)),
                  ),
                  const SizedBox(width: 8),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(user.fullName,
                          style: const TextStyle(
                              fontSize: 12,
                              fontWeight: FontWeight.w700,
                              color: SG.text)),
                      Text(user.targetRole,
                          style: const TextStyle(
                              fontSize: 9.5,
                              fontWeight: FontWeight.w700,
                              color: SG.indigoLight)),
                    ],
                  ),
                ]),
              ),
            ),
          const SizedBox(width: 4),
          IconButton(
            tooltip: 'Log out',
            icon: const Icon(Icons.logout_rounded,
                size: 20, color: SG.textSecondary),
            onPressed: () async {
              await AppState.instance.logout();
              if (!mounted) return;
              if (context.mounted) {
                Navigator.of(context).pushAndRemoveUntil(
                    MaterialPageRoute(builder: (_) => const AuthScreen()),
                    (_) => false);
              }
            },
          ),
        ],
      ),
    );
  }
}
