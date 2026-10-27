import 'package:flutter/material.dart';

import '../app_state.dart';
import '../data/skill_data.dart';
import '../theme.dart';
import '../widgets/widgets.dart';

/// Tab 3 — Role Compatibility & Tech Blueprints: role cards with
/// compatibility %, salaries, and a deep-dive requirements view.
class AnalyticsScreen extends StatefulWidget {
  const AnalyticsScreen({super.key});

  @override
  State<AnalyticsScreen> createState() => _AnalyticsScreenState();
}

class _AnalyticsScreenState extends State<AnalyticsScreen> {
  String _selectedRole = kRoleBlueprints.keys.first;

  int _compatFor(String role) {
    final a = AppState.instance.analysis;
    final skills =
        (a?.resumeSkills ?? const []).map((e) => e.toLowerCase()).toSet();
    final reqs = kRoleBlueprints[role]!;
    if (skills.isEmpty) {
      // baseline demo compatibility
      return 72 + (role.hashCode % 21).abs();
    }
    final hits =
        reqs.where((r) => skills.contains(r.toLowerCase())).length;
    return (55 + (hits / reqs.length) * 45).round().clamp(0, 98);
  }

  @override
  Widget build(BuildContext context) {
    final roles = kRoleBlueprints.keys.toList();
    final blueprint = kRoleBlueprints[_selectedRole]!;

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 4, 16, 24),
      children: [
        const Text('Role Compatibility & Tech Blueprints',
            style: TextStyle(
                fontSize: 19, fontWeight: FontWeight.w900, color: SG.text)),
        const SizedBox(height: 4),
        const Text(
            'Real-time market alignment, salary intelligence, and technical specifications for in-demand roles.',
            style: TextStyle(fontSize: 12.5, color: SG.textSecondary)),
        const SizedBox(height: 16),

        for (final role in roles)
          GlassCard(
            padding: const EdgeInsets.all(16),
            child: InkWell(
              onTap: () => setState(() => _selectedRole = role),
              borderRadius: BorderRadius.circular(12),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Expanded(
                        child: Text(role,
                            style: const TextStyle(
                                fontSize: 15.5,
                                fontWeight: FontWeight.w800,
                                color: SG.text)),
                      ),
                      Text('${_compatFor(role)}%',
                          style: const TextStyle(
                              fontSize: 22,
                              fontWeight: FontWeight.w900,
                              color: SG.indigoLight)),
                    ],
                  ),
                  const SizedBox(height: 6),
                  const Text(
                      'Alignment with your skill inventory and experience level.',
                      style: TextStyle(
                          fontSize: 11.5, color: SG.textSecondary)),
                  const SizedBox(height: 10),
                  ClipRRect(
                    borderRadius: BorderRadius.circular(999),
                    child: LinearProgressIndicator(
                      value: _compatFor(role) / 100,
                      minHeight: 6,
                      backgroundColor: const Color(0x14FFFFFF),
                      valueColor:
                          const AlwaysStoppedAnimation(SG.indigo),
                    ),
                  ),
                  const SizedBox(height: 10),
                  Container(
                    padding: const EdgeInsets.symmetric(
                        horizontal: 12, vertical: 8),
                    decoration: BoxDecoration(
                      color: SG.cardSoft,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Top Tier Match',
                            style: TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.w700,
                                color: SG.emeraldLight)),
                        Text('Est. Comp: ${kRoleSalaries[role] ?? '\$90k+'}',
                            style: const TextStyle(
                                fontSize: 11,
                                fontWeight: FontWeight.w700,
                                color: SG.indigoLight)),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),

        const SizedBox(height: 8),
        GlassCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const CardHeader(
                  icon: Icons.code_rounded,
                  title: 'Role Technical Blueprint',
                  iconColor: SG.cyanLight),
              Wrap(
                spacing: 6,
                runSpacing: 6,
                children: [
                  for (final r in roles)
                    ChipTag(r,
                        color: SG.cyanLight,
                        filled: _selectedRole == r,
                        onTap: () => setState(() => _selectedRole = r)),
                ],
              ),
              const SizedBox(height: 16),
              Text('$_selectedRole Requirements',
                  style: const TextStyle(
                      fontSize: 14,
                      fontWeight: FontWeight.w800,
                      color: SG.text)),
              const SizedBox(height: 10),
              for (final skill in blueprint)
                Container(
                  margin: const EdgeInsets.only(bottom: 6),
                  padding: const EdgeInsets.symmetric(
                      horizontal: 14, vertical: 10),
                  decoration: BoxDecoration(
                    color: SG.cardSoft,
                    borderRadius: BorderRadius.circular(10),
                    border: Border.all(color: SG.border),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.check_box_outlined,
                          size: 15, color: SG.cyanLight),
                      const SizedBox(width: 10),
                      Expanded(
                        child: Text(skill,
                            style: const TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.w700,
                                color: SG.text)),
                      ),
                      if (kLearningCourses.containsKey(skill))
                        Tooltip(
                          message: kLearningCourses[skill]!,
                          triggerMode: TooltipTriggerMode.tap,
                          child: const Icon(Icons.school_outlined,
                              size: 16, color: SG.textMuted),
                        ),
                    ],
                  ),
                ),
            ],
          ),
        ),
      ],
    );
  }
}
