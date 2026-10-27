import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../app_state.dart';
import '../services/analyzer.dart';
import '../theme.dart';
import '../widgets/widgets.dart';

/// Tab 4 — Tailored 12-Week Career Upskilling Roadmap timeline.
class RoadmapScreen extends StatelessWidget {
  const RoadmapScreen({super.key});

  static const _phaseColors = [SG.indigo, SG.purple, SG.cyan, SG.emerald];

  List<RoadmapStep> _steps() {
    final a = AppState.instance.analysis;
    if (a != null) return a.roadmap;
    return Analyzer.analyze(
            resumeText: 'python sql git docker rest api',
            jobDescription: 'docker kubernetes aws ci/cd system design')
        .roadmap;
  }

  void _export(BuildContext context, List<RoadmapStep> steps) {
    final buf = StringBuffer('SkillGap AI — 12-Week Career Roadmap\n\n');
    for (final s in steps) {
      buf.writeln(s.phase);
      buf.writeln('  ${s.description}');
      for (final sk in s.skills) {
        buf.writeln('  - ${sk.name}: ${sk.resource}');
      }
      buf.writeln();
    }
    Clipboard.setData(ClipboardData(text: buf.toString()));
    sgToast(context, 'Roadmap copied to clipboard');
  }

  @override
  Widget build(BuildContext context) {
    final steps = _steps();
    final s = AppState.instance;
    final done = s.roadmapDone.length;
    final target = s.analysis?.suggestedRoles.first ??
        s.user?.targetRole ??
        'Full Stack Developer';

    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 4, 16, 24),
      children: [
        GlassCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  const Expanded(
                    child: Text('Tailored 12-Week Career Upskilling Roadmap',
                        style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.w900,
                            color: SG.text)),
                  ),
                  IconButton(
                    tooltip: 'Export Roadmap',
                    icon: const Icon(Icons.download_outlined,
                        size: 20, color: SG.indigoLight),
                    onPressed: () => _export(context, steps),
                  ),
                ],
              ),
              Text('Targeting: $target',
                  style: const TextStyle(
                      fontSize: 12, color: SG.textSecondary)),
            ],
          ),
        ),
        const SizedBox(height: 14),

        // Progress bar
        Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
          decoration: BoxDecoration(
            color: SG.cardSoft,
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: SG.border),
          ),
          child: Column(
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                      'Progress: $done of ${steps.length} Phases Completed',
                      style: const TextStyle(
                          fontSize: 12.5,
                          fontWeight: FontWeight.w600,
                          color: SG.textSecondary)),
                  Text('${(done / steps.length * 100).round()}%',
                      style: const TextStyle(
                          fontSize: 12.5,
                          fontWeight: FontWeight.w800,
                          color: SG.emeraldLight)),
                ],
              ),
              const SizedBox(height: 8),
              ClipRRect(
                borderRadius: BorderRadius.circular(999),
                child: LinearProgressIndicator(
                  value: done / steps.length,
                  minHeight: 8,
                  backgroundColor: const Color(0x14FFFFFF),
                  valueColor: const AlwaysStoppedAnimation(SG.emerald),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 14),

        // Timeline
        for (var i = 0; i < steps.length; i++)
          _TimelineStep(
            step: steps[i],
            color: _phaseColors[i % _phaseColors.length],
            done: s.roadmapDone.contains(i),
            isLast: i == steps.length - 1,
            onToggle: () => s.toggleRoadmapStep(i),
          ),
      ],
    );
  }
}

class _TimelineStep extends StatelessWidget {
  final RoadmapStep step;
  final Color color;
  final bool done;
  final bool isLast;
  final VoidCallback onToggle;

  const _TimelineStep({
    required this.step,
    required this.color,
    required this.done,
    required this.isLast,
    required this.onToggle,
  });

  @override
  Widget build(BuildContext context) {
    return IntrinsicHeight(
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // timeline spine
          Column(
            children: [
              GestureDetector(
                onTap: onToggle,
                child: Container(
                  width: 26,
                  height: 26,
                  decoration: BoxDecoration(
                    color: done ? color : SG.cardSoft,
                    shape: BoxShape.circle,
                    border: Border.all(color: color, width: 2),
                  ),
                  child: done
                      ? const Icon(Icons.check, size: 15, color: Colors.white)
                      : null,
                ),
              ),
              if (!isLast)
                Expanded(
                  child: Container(
                      width: 2,
                      color: color.withValues(alpha: 0.3)),
                ),
            ],
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Container(
              margin: const EdgeInsets.only(bottom: 14),
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: done ? color.withValues(alpha: 0.08) : SG.card,
                borderRadius: BorderRadius.circular(16),
                border: Border.all(color: SG.border),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(step.phase.toUpperCase(),
                      style: TextStyle(
                          fontSize: 10.5,
                          fontWeight: FontWeight.w800,
                          color: color,
                          letterSpacing: 0.8)),
                  const SizedBox(height: 4),
                  Text(step.description,
                      style: const TextStyle(
                          fontSize: 13, color: SG.textSecondary, height: 1.45)),
                  const SizedBox(height: 10),
                  Wrap(
                    spacing: 6,
                    runSpacing: 6,
                    children: [
                      for (final sk in step.skills)
                        Tooltip(
                          message: sk.resource,
                          triggerMode: TooltipTriggerMode.tap,
                          child: ChipTag(sk.name, color: color),
                        ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
