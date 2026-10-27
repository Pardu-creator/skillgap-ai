import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

/// SkillGap AI dark theme — ports the web app's palette:
/// deep navy background, indigo→purple→cyan gradients, glassmorphic cards.
class SG {
  // Surfaces
  static const bg = Color(0xFF060814);
  static const bgAlt = Color(0xFF0A0F1E);
  static const card = Color(0xCC0A0F1E);
  static const cardSoft = Color(0x660F172A);
  static const field = Color(0xD90F172A);

  // Accents
  static const indigo = Color(0xFF6366F1);
  static const indigoLight = Color(0xFF818CF8);
  static const purple = Color(0xFF8B5CF6);
  static const purpleLight = Color(0xFFC084FC);
  static const cyan = Color(0xFF0EA5E9);
  static const cyanLight = Color(0xFF38BDF8);
  static const emerald = Color(0xFF10B981);
  static const emeraldLight = Color(0xFF34D399);
  static const amber = Color(0xFFF59E0B);
  static const amberLight = Color(0xFFFBBF24);
  static const rose = Color(0xFFF43F5E);
  static const roseLight = Color(0xFFFDA4AF);

  // Text
  static const text = Color(0xFFF1F5F9);
  static const textSecondary = Color(0xFF94A3B8);
  static const textMuted = Color(0xFF64748B);

  static const border = Color(0x1A6366F1);
  static const borderStrong = Color(0x406366F1);

  static const gradient = LinearGradient(
    colors: [indigo, purple, Color(0xFFA855F7)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const gradientCyan = LinearGradient(
    colors: [indigo, purple, cyan],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static ThemeData theme() {
    final base = ThemeData.dark(useMaterial3: true);
    return base.copyWith(
      scaffoldBackgroundColor: bg,
      colorScheme: const ColorScheme.dark(
        primary: indigo,
        secondary: purple,
        surface: bgAlt,
        error: rose,
      ),
      textTheme: GoogleFonts.interTextTheme(base.textTheme).apply(
        bodyColor: text,
        displayColor: text,
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: field,
        hintStyle: const TextStyle(color: textMuted, fontSize: 13.5),
        labelStyle: const TextStyle(color: textSecondary, fontSize: 13),
        contentPadding:
            const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: border),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: border),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(12),
          borderSide: const BorderSide(color: indigo, width: 1.4),
        ),
      ),
      snackBarTheme: SnackBarThemeData(
        backgroundColor: const Color(0xFF1E293B),
        contentTextStyle: const TextStyle(color: text, fontWeight: FontWeight.w600),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(10),
          side: const BorderSide(color: indigo),
        ),
      ),
      dividerTheme: const DividerThemeData(color: border, thickness: 1),
    );
  }

  /// Full-page atmospheric gradient background.
  static BoxDecoration pageBg() => const BoxDecoration(
        gradient: RadialGradient(
          center: Alignment.topLeft,
          radius: 1.4,
          colors: [Color(0x1F6366F1), Colors.transparent],
        ),
        color: bg,
      );
}
