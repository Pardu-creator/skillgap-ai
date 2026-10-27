import 'dart:math' as math;

import 'package:flutter/material.dart';

import '../theme.dart';

/// Glassmorphic card used across the dashboard.
class GlassCard extends StatelessWidget {
  final Widget child;
  final EdgeInsetsGeometry padding;
  final Color? color;
  final double radius;
  const GlassCard({
    super.key,
    required this.child,
    this.padding = const EdgeInsets.all(20),
    this.color,
    this.radius = 20,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: padding,
      decoration: BoxDecoration(
        color: color ?? SG.card,
        borderRadius: BorderRadius.circular(radius),
        border: Border.all(color: SG.border),
        boxShadow: const [
          BoxShadow(color: Colors.black38, blurRadius: 24, offset: Offset(0, 8)),
        ],
      ),
      child: child,
    );
  }
}

/// Card header with icon + title + optional trailing widget.
class CardHeader extends StatelessWidget {
  final IconData icon;
  final String title;
  final Widget? trailing;
  final Color iconColor;
  const CardHeader({
    super.key,
    required this.icon,
    required this.title,
    this.trailing,
    this.iconColor = SG.indigoLight,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 14),
      child: Row(
        children: [
          Icon(icon, size: 20, color: iconColor),
          const SizedBox(width: 8),
          Expanded(
            child: Text(title,
                style: const TextStyle(
                    fontSize: 16, fontWeight: FontWeight.w800, color: SG.text)),
          ),
          ?trailing,
        ],
      ),
    );
  }
}

/// Primary gradient action button.
class GradientButton extends StatelessWidget {
  final String label;
  final IconData? icon;
  final VoidCallback? onPressed;
  final bool loading;
  const GradientButton({
    super.key,
    required this.label,
    this.icon,
    this.onPressed,
    this.loading = false,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: 48,
      width: double.infinity,
      child: DecoratedBox(
        decoration: BoxDecoration(
          gradient: SG.gradient,
          borderRadius: BorderRadius.circular(12),
          boxShadow: const [
            BoxShadow(
                color: Color(0x666366F1), blurRadius: 20, offset: Offset(0, 8)),
          ],
        ),
        child: ElevatedButton(
          onPressed: loading ? null : onPressed,
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.transparent,
            shadowColor: Colors.transparent,
            disabledBackgroundColor: Colors.transparent,
            shape:
                RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
          ),
          child: loading
              ? const SizedBox(
                  width: 20,
                  height: 20,
                  child: CircularProgressIndicator(
                      strokeWidth: 2, color: Colors.white))
              : Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    ?(icon != null
                        ? Padding(
                            padding: const EdgeInsets.only(right: 8),
                            child: Icon(icon,
                                size: 18, color: Colors.white))
                        : null),
                    Flexible(
                      child: Text(label,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.w800,
                              fontSize: 14.5)),
                    ),
                  ],
                ),
        ),
      ),
    );
  }
}

/// Small pill chip.
class ChipTag extends StatelessWidget {
  final String label;
  final Color color;
  final bool filled;
  final VoidCallback? onTap;
  const ChipTag(this.label,
      {super.key,
      this.color = SG.indigoLight,
      this.filled = false,
      this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(999),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: filled ? color.withValues(alpha: 0.2) : color.withValues(alpha: 0.08),
          borderRadius: BorderRadius.circular(999),
          border: Border.all(color: color.withValues(alpha: 0.35)),
        ),
        child: Text(label,
            style: TextStyle(
                fontSize: 12, fontWeight: FontWeight.w700, color: color)),
      ),
    );
  }
}

/// Colored count pill like "12 Skills".
class CountPill extends StatelessWidget {
  final String label;
  final Color color;
  const CountPill(this.label, {super.key, this.color = SG.emeraldLight});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(999),
        border: Border.all(color: color.withValues(alpha: 0.3)),
      ),
      child: Text(label,
          style: TextStyle(
              fontSize: 11, fontWeight: FontWeight.w800, color: color)),
    );
  }
}

/// Circular employability gauge (SVG arc port).
class ScoreGauge extends StatelessWidget {
  final int percent; // 0-100
  final double size;
  final String label;
  const ScoreGauge(
      {super.key, required this.percent, this.size = 150, this.label = 'Employability'});

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: size,
      height: size,
      child: Stack(
        alignment: Alignment.center,
        children: [
          CustomPaint(size: Size(size, size), painter: _GaugePainter(percent)),
          Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('$percent%',
                  style: TextStyle(
                      fontSize: size * 0.21,
                      fontWeight: FontWeight.w900,
                      color: SG.text)),
              Text(label,
                  style: const TextStyle(
                      fontSize: 11,
                      fontWeight: FontWeight.w700,
                      color: SG.textMuted,
                      letterSpacing: 0.5)),
            ],
          ),
        ],
      ),
    );
  }
}

class _GaugePainter extends CustomPainter {
  final int percent;
  _GaugePainter(this.percent);

  @override
  void paint(Canvas canvas, Size size) {
    final center = size.center(Offset.zero);
    final radius = size.width / 2 - 10;
    const stroke = 10.0;

    final bgPaint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = stroke
      ..color = const Color(0x1AFFFFFF)
      ..strokeCap = StrokeCap.round;
    canvas.drawCircle(center, radius, bgPaint);

    final rect = Rect.fromCircle(center: center, radius: radius);
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = stroke
      ..strokeCap = StrokeCap.round
      ..shader = const SweepGradient(
        colors: [SG.cyan, SG.indigo, SG.purple, SG.cyan],
      ).createShader(rect);

    // Start at -90° (top), sweep percent of the circle.
    const start = -math.pi / 2;
    final sweep = 2 * math.pi * (percent.clamp(0, 100) / 100);
    canvas.drawArc(rect, start, sweep, false, paint);
  }

  @override
  bool shouldRepaint(covariant _GaugePainter old) => old.percent != percent;
}

/// Horizontal labelled metric progress bar.
class MetricBar extends StatelessWidget {
  final String label;
  final int percent;
  final Color color;
  const MetricBar(this.label, this.percent,
      {super.key, this.color = SG.cyanLight});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(label,
                style: const TextStyle(
                    fontSize: 12.5,
                    fontWeight: FontWeight.w600,
                    color: SG.textSecondary)),
            Text('$percent%',
                style: TextStyle(
                    fontSize: 12.5, fontWeight: FontWeight.w800, color: color)),
          ],
        ),
        const SizedBox(height: 6),
        ClipRRect(
          borderRadius: BorderRadius.circular(999),
          child: LinearProgressIndicator(
            value: percent.clamp(0, 100) / 100,
            minHeight: 7,
            backgroundColor: const Color(0x14FFFFFF),
            valueColor: AlwaysStoppedAnimation(color),
          ),
        ),
      ],
    );
  }
}

/// Minimal markdown renderer for chat messages: **bold**, ### headers,
/// bullet lists, *italic*, `code`.
class MarkdownText extends StatelessWidget {
  final String text;
  final TextStyle? baseStyle;
  const MarkdownText(this.text, {super.key, this.baseStyle});

  @override
  Widget build(BuildContext context) {
    final base = baseStyle ??
        const TextStyle(fontSize: 13.5, color: SG.text, height: 1.5);
    final lines = text.split('\n');
    final children = <Widget>[];

    for (final raw in lines) {
      var line = raw;
      var style = base;
      Widget? prefix;

      if (line.startsWith('###')) {
        line = line.replaceFirst(RegExp(r'^#+\s*'), '');
        style = base.copyWith(fontWeight: FontWeight.w800, fontSize: 14.5);
      } else if (RegExp(r'^\s*[-•*]\s').hasMatch(line)) {
        line = line.replaceFirst(RegExp(r'^\s*[-•*]\s'), '');
        prefix = Text('•  ', style: base.copyWith(color: SG.indigoLight));
      } else if (RegExp(r'^\s*\d+\.\s').hasMatch(line)) {
        final m = RegExp(r'^\s*(\d+\.\s)').firstMatch(line)!;
        prefix = Text(m.group(1)!, style: base.copyWith(fontWeight: FontWeight.w700, color: SG.indigoLight));
        line = line.substring(m.end);
      }

      children.add(Padding(
        padding: const EdgeInsets.only(bottom: 3),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ?prefix,
            Expanded(child: _inline(line, style)),
          ],
        ),
      ));
    }
    return Column(crossAxisAlignment: CrossAxisAlignment.start, children: children);
  }

  Widget _inline(String line, TextStyle base) {
    final spans = <InlineSpan>[];
    final pattern = RegExp(r'\*\*(.+?)\*\*|\*(.+?)\*|`(.+?)`');
    var idx = 0;
    for (final m in pattern.allMatches(line)) {
      if (m.start > idx) {
        spans.add(TextSpan(text: line.substring(idx, m.start), style: base));
      }
      if (m.group(1) != null) {
        spans.add(TextSpan(
            text: m.group(1),
            style: base.copyWith(fontWeight: FontWeight.w800, color: SG.text)));
      } else if (m.group(2) != null) {
        spans.add(TextSpan(
            text: m.group(2),
            style: base.copyWith(fontStyle: FontStyle.italic)));
      } else {
        spans.add(TextSpan(
            text: m.group(3),
            style: base.copyWith(
                fontFamily: 'monospace',
                backgroundColor: const Color(0x1AFFFFFF),
                fontSize: base.fontSize! - 1)));
      }
      idx = m.end;
    }
    if (idx < line.length) {
      spans.add(TextSpan(text: line.substring(idx), style: base));
    }
    return RichText(text: TextSpan(children: spans));
  }
}

/// Pulse "online" status dot.
class PulseDot extends StatelessWidget {
  final Color color;
  const PulseDot({super.key, this.color = SG.emeraldLight});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: 8,
      height: 8,
      decoration: BoxDecoration(
        color: color,
        shape: BoxShape.circle,
        boxShadow: [BoxShadow(color: color.withValues(alpha: 0.7), blurRadius: 8)],
      ),
    );
  }
}

/// Brand logo box (gradient rounded square with brain icon).
class BrandLogo extends StatelessWidget {
  final double size;
  const BrandLogo({super.key, this.size = 46});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        gradient: SG.gradient,
        borderRadius: BorderRadius.circular(size * 0.3),
        boxShadow: const [
          BoxShadow(color: Color(0x596366F1), blurRadius: 18, offset: Offset(0, 6)),
        ],
      ),
      child: Icon(Icons.psychology_alt_rounded,
          color: Colors.white, size: size * 0.52),
    );
  }
}

void sgToast(BuildContext context, String msg) {
  ScaffoldMessenger.of(context)
    ..hideCurrentSnackBar()
    ..showSnackBar(SnackBar(content: Text(msg)));
}
