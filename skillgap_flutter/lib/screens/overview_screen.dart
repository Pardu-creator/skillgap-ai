import 'dart:math';

import 'package:flutter/material.dart';

import '../app_state.dart';
import '../theme.dart';
import '../widgets/widgets.dart';

/// Tab 1 — Executive Overview: welcome hero, quick action tiles,
/// 4 KPI cards, skill landscape, job match intelligence, AI recommendation.
class OverviewScreen extends StatelessWidget {
  const OverviewScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final s = AppState.instance;
    final user = s.user;
    final a = s.analysis;

    final emp = a?.employabilityScore ?? 84;
    final match = a?.matchScore ?? 78;
    final skills = a?.resumeSkills ??
        const ["Python", "SQL", "Machine Learning", "Docker", "Git", "REST API", "Data Analysis", "Linux"];
    final missing = a?.missingSkills ??
        const ["AWS", "Kubernetes", "CI/CD", "FastAPI"];
    final roles = a?.suggestedRoles ??
        const ["Machine Learning Engineer", "Backend Developer", "Data Analyst"];

    final rng = Random(7);

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 4, 16, 24),
      children: [
        // Welcome hero
        Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Welcome back, ${user?.fullName ?? 'User'}',
                      style: const TextStyle(
                          fontSize: 21,
                          fontWeight: FontWeight.w900,
                          color: SG.text,
                          letterSpacing: -0.4)),
                  const SizedBox(height: 4),
                  Text.rich(TextSpan(children: [
                    const TextSpan(text: 'Target Career Track: '),
                    TextSpan(
                        text: user?.targetRole ?? 'Full Stack Developer',
                        style: const TextStyle(
                            color: SG.indigoLight, fontWeight: FontWeight.w700)),
                  ]),
                      style: const TextStyle(
                          fontSize: 12.5, color: SG.textSecondary)),
                ],
              ),
            ),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
              decoration: BoxDecoration(
                color: SG.cyan.withValues(alpha: 0.12),
                borderRadius: BorderRadius.circular(999),
                border: Border.all(color: SG.cyan.withValues(alpha: 0.3)),
              ),
              child: const Row(mainAxisSize: MainAxisSize.min, children: [
                PulseDot(color: SG.cyanLight),
                SizedBox(width: 6),
                Text('Track Active',
                    style: TextStyle(
                        fontSize: 10.5,
                        fontWeight: FontWeight.w800,
                        color: SG.cyanLight)),
              ]),
            ),
          ],
        ),
        const SizedBox(height: 18),

        // Quick action tiles
        const _SectionLabel('QUICK APP ACTIONS'),
        const SizedBox(height: 8),
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          mainAxisSpacing: 10,
          crossAxisSpacing: 10,
          childAspectRatio: 2.5,
          children: [
            _ActionTile(Icons.document_scanner_outlined, 'Scan Resume',
                'AI skill extraction', SG.indigoLight, () => s.setTab(1)),
            _ActionTile(Icons.bar_chart_rounded, 'Role Blueprint',
                'Tech specs & comp', SG.cyanLight, () => s.setTab(2)),
            _ActionTile(Icons.flag_outlined, '12-Wk Roadmap',
                'Milestones & tasks', SG.purpleLight, () => s.setTab(3)),
            _ActionTile(Icons.smart_toy_outlined, 'AI Mentor',
                'Advice & prep', SG.emeraldLight, () => s.setTab(4)),
          ],
        ),
        const SizedBox(height: 18),

        // KPI grid
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          mainAxisSpacing: 10,
          crossAxisSpacing: 10,
          childAspectRatio: 1.75,
          children: [
            _KpiTile('Employability Score', '$emp%', Icons.emoji_events_outlined,
                SG.indigoLight, 'Top 12% Candidate'),
            _KpiTile('Resume Match Index', '$match%', Icons.document_scanner_outlined,
                SG.purpleLight, 'High Role Fit'),
            _KpiTile('Verified Skills', '${skills.length}', Icons.check_circle_outline,
                SG.emeraldLight, 'Verified Core'),
            _KpiTile('Skill Gaps', '${missing.length}', Icons.warning_amber_rounded,
                SG.amberLight, 'Learning Targets'),
          ],
        ),
        const SizedBox(height: 18),

        // Skill landscape
        GlassCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const CardHeader(
                  icon: Icons.trending_up_rounded,
                  title: 'Skill Landscape & Proficiency',
                  iconColor: SG.indigoLight),
              for (final sk in skills.take(6))
                _SkillRow(
                    name: sk,
                    value: '${82 + rng.nextInt(15)}%',
                    badge: 'Current Level',
                    color: SG.emeraldLight),
              if (missing.isNotEmpty) ...[
                const Padding(
                  padding: EdgeInsets.only(top: 14, bottom: 8),
                  child: Text('Priority Gaps to Close',
                      style: TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w700,
                          color: SG.roseLight)),
                ),
                for (final g in missing.take(4))
                  _SkillRow(
                      name: g,
                      value: 'Gap',
                      badge: 'Recommended',
                      color: SG.roseLight),
              ],
            ],
          ),
        ),
        const SizedBox(height: 14),

        // Job match intelligence
        GlassCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const CardHeader(
                  icon: Icons.work_outline_rounded,
                  title: 'Job Match Intelligence',
                  iconColor: SG.cyanLight),
              for (final r in roles.take(3))
                Container(
                  margin: const EdgeInsets.only(bottom: 10),
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: SG.cardSoft,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: SG.border),
                  ),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Expanded(
                            child: Text(r,
                                style: const TextStyle(
                                    fontSize: 14.5,
                                    fontWeight: FontWeight.w800,
                                    color: SG.text)),
                          ),
                          Text('${84 + rng.nextInt(13)}%',
                              style: const TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.w900,
                                  color: SG.indigoLight)),
                        ],
                      ),
                      const SizedBox(height: 8),
                      const Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Text('Status: Ready to Apply',
                              style: TextStyle(
                                  fontSize: 11.5, color: SG.emeraldLight)),
                          Text('Avg: \$110k-\$145k',
                              style: TextStyle(
                                  fontSize: 11.5, color: SG.textSecondary)),
                        ],
                      ),
                    ],
                  ),
                ),
              Container(
                padding: const EdgeInsets.all(14),
                decoration: BoxDecoration(
                  gradient: LinearGradient(colors: [
                    SG.indigo.withValues(alpha: 0.1),
                    SG.purple.withValues(alpha: 0.07)
                  ]),
                  borderRadius: BorderRadius.circular(14),
                  border: Border.all(color: SG.indigo.withValues(alpha: 0.2)),
                ),
                child: const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(children: [
                      Icon(Icons.auto_awesome, size: 15, color: SG.indigoLight),
                      SizedBox(width: 6),
                      Text('AI Recommendation',
                          style: TextStyle(
                              fontSize: 12.5,
                              fontWeight: FontWeight.w800,
                              color: SG.indigoLight)),
                    ]),
                    SizedBox(height: 6),
                    Text(
                        'Upload your resume in the Skill Analyzer tab to recalibrate your AI match index and unlock salary-tier guidance.',
                        style: TextStyle(
                            fontSize: 12.5, color: SG.textSecondary, height: 1.5)),
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

class _SectionLabel extends StatelessWidget {
  final String text;
  const _SectionLabel(this.text);

  @override
  Widget build(BuildContext context) => Text(text,
      style: const TextStyle(
          fontSize: 10.5,
          fontWeight: FontWeight.w800,
          color: SG.textMuted,
          letterSpacing: 1.2));
}

class _ActionTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String subtitle;
  final Color color;
  final VoidCallback onTap;
  const _ActionTile(
      this.icon, this.title, this.subtitle, this.color, this.onTap);

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(16),
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: SG.cardSoft,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: SG.border),
        ),
        child: Row(
          children: [
            Container(
              width: 38,
              height: 38,
              decoration: BoxDecoration(
                color: color.withValues(alpha: 0.15),
                borderRadius: BorderRadius.circular(11),
              ),
              child: Icon(icon, size: 19, color: color),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(title,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                          fontSize: 13,
                          fontWeight: FontWeight.w800,
                          color: SG.text)),
                  Text(subtitle,
                      maxLines: 1,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                          fontSize: 10.5, color: SG.textSecondary)),
                ],
              ),
            ),
            const Icon(Icons.chevron_right_rounded,
                size: 18, color: SG.textMuted),
          ],
        ),
      ),
    );
  }
}

class _KpiTile extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color color;
  final String pill;
  const _KpiTile(this.label, this.value, this.icon, this.color, this.pill);

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(14),
      decoration: BoxDecoration(
        color: SG.card,
        borderRadius: BorderRadius.circular(18),
        border: Border.all(color: SG.border),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: Text(label.toUpperCase(),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(
                        fontSize: 9.5,
                        fontWeight: FontWeight.w800,
                        color: SG.textMuted,
                        letterSpacing: 0.6)),
              ),
              Container(
                width: 30,
                height: 30,
                decoration: BoxDecoration(
                  color: color.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(9),
                  border: Border.all(color: color.withValues(alpha: 0.25)),
                ),
                child: Icon(icon, size: 15, color: color),
              ),
            ],
          ),
          Text(value,
              style: const TextStyle(
                  fontSize: 27,
                  fontWeight: FontWeight.w900,
                  color: SG.text,
                  letterSpacing: -0.8)),
          CountPill(pill, color: color),
        ],
      ),
    );
  }
}

class _SkillRow extends StatelessWidget {
  final String name;
  final String value;
  final String badge;
  final Color color;
  const _SkillRow(
      {required this.name,
      required this.value,
      required this.badge,
      required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(bottom: 6),
      padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
      decoration: BoxDecoration(
        color: SG.cardSoft,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: SG.border),
      ),
      child: Row(
        children: [
          Icon(Icons.bolt_rounded, size: 15, color: color),
          const SizedBox(width: 10),
          Expanded(
            child: Text(name,
                style: const TextStyle(
                    fontSize: 13.5,
                    fontWeight: FontWeight.w700,
                    color: SG.text)),
          ),
          Text(value,
              style: TextStyle(
                  fontSize: 12.5, fontWeight: FontWeight.w700, color: color)),
          const SizedBox(width: 10),
          CountPill(badge, color: color),
        ],
      ),
    );
  }
}
