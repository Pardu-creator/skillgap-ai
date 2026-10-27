import 'package:flutter/material.dart';

import '../app_state.dart';
import '../data/skill_data.dart';
import '../services/mentor_service.dart';
import '../theme.dart';
import '../widgets/widgets.dart';

/// Settings — account profile, target role, AI engine config, data controls.
class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late final TextEditingController _geminiKey;

  @override
  void initState() {
    super.initState();
    _geminiKey =
        TextEditingController(text: MentorService.geminiApiKey ?? '');
  }

  @override
  void dispose() {
    _geminiKey.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final s = AppState.instance;
    final user = s.user;

    return Scaffold(
      body: Container(
        decoration: SG.pageBg(),
        child: SafeArea(
          child: ListView(
            padding: const EdgeInsets.all(16),
            children: [
              Row(
                children: [
                  IconButton(
                    icon: const Icon(Icons.arrow_back_rounded,
                        color: SG.textSecondary),
                    onPressed: () => Navigator.of(context).pop(),
                  ),
                  const Text('Platform Settings & Account Profile',
                      style: TextStyle(
                          fontSize: 17,
                          fontWeight: FontWeight.w900,
                          color: SG.text)),
                ],
              ),
              const SizedBox(height: 12),

              GlassCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const CardHeader(
                        icon: Icons.person_outline_rounded,
                        title: 'User & Target Career Profile'),
                    _row('User Account', user?.email ?? 'demo@skillgap.ai'),
                    _row('Full Name', user?.fullName ?? 'Demo User'),
                    _row('Experience Level',
                        user?.experienceLevel ?? 'Undergraduate / Fresher'),
                    Padding(
                      padding: const EdgeInsets.symmetric(vertical: 10),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          const Text('Target Role Track',
                              style: TextStyle(
                                  fontSize: 13.5,
                                  fontWeight: FontWeight.w600,
                                  color: SG.textSecondary)),
                          DropdownButton<String>(
                            value: user?.targetRole ?? kTargetRoles.first,
                            dropdownColor: SG.bgAlt,
                            underline: const SizedBox(),
                            style: const TextStyle(
                                fontSize: 13,
                                fontWeight: FontWeight.w700,
                                color: SG.indigoLight),
                            items: kTargetRoles
                                .map((r) => DropdownMenuItem(
                                    value: r,
                                    child: Text(r,
                                        overflow: TextOverflow.ellipsis)))
                                .toList(),
                            onChanged: (v) =>
                                v == null ? null : s.updateTargetRole(v),
                          ),
                        ],
                      ),
                    ),
                    _row('Active Resume Profile',
                        s.lastUploadedName.isEmpty
                            ? 'Default Candidate Baseline'
                            : s.lastUploadedName),
                    _row(
                        'AI Engine Status',
                        MentorService.geminiApiKey != null
                            ? 'Gemini 2.0 Flash Connected'
                            : 'Heuristic Engine Active',
                        valueColor: SG.emeraldLight),
                    _row('Security & Database',
                        'Local PBKDF2-SHA256 · On-Device',
                        valueColor: SG.indigoLight),
                  ],
                ),
              ),
              const SizedBox(height: 14),

              GlassCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const CardHeader(
                        icon: Icons.key_outlined,
                        title: 'AI Engine (Optional)',
                        iconColor: SG.purpleLight),
                    const Text(
                        'Paste a Gemini API key to enable live AI mentor replies and deep analysis. Without one, the built-in expert engine handles everything on-device.',
                        style: TextStyle(
                            fontSize: 12.5,
                            color: SG.textSecondary,
                            height: 1.5)),
                    const SizedBox(height: 12),
                    TextField(
                      controller: _geminiKey,
                      obscureText: true,
                      decoration: const InputDecoration(
                          labelText: 'Gemini API Key',
                          hintText: 'AIza...'),
                    ),
                    const SizedBox(height: 12),
                    Row(
                      children: [
                        Expanded(
                          child: OutlinedButton.icon(
                            onPressed: () async {
                              await s.setGeminiKey(_geminiKey.text);
                              setState(() {});
                              if (context.mounted) {
                                sgToast(context,
                                    _geminiKey.text.trim().isEmpty
                                        ? 'Gemini disconnected — offline engine active'
                                        : 'Gemini API key saved');
                              }
                            },
                            icon: const Icon(Icons.save_outlined, size: 17),
                            label: const Text('Save Key'),
                            style: OutlinedButton.styleFrom(
                              foregroundColor: SG.indigoLight,
                              side: const BorderSide(color: SG.borderStrong),
                              shape: RoundedRectangleBorder(
                                  borderRadius: BorderRadius.circular(10)),
                            ),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
              const SizedBox(height: 14),

              GlassCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const CardHeader(
                        icon: Icons.storage_outlined,
                        title: 'Data & Cache Management',
                        iconColor: SG.amberLight),
                    const Text(
                        'Reset cached resume analysis data and roadmap progress for this session.',
                        style: TextStyle(
                            fontSize: 12.5,
                            color: SG.textSecondary,
                            height: 1.5)),
                    const SizedBox(height: 14),
                    OutlinedButton.icon(
                      onPressed: () async {
                        await s.resetSession();
                        if (context.mounted) {
                          sgToast(context, 'Session data cleared');
                        }
                      },
                      icon: const Icon(Icons.delete_outline, size: 17),
                      label: const Text('Reset All Session Data'),
                      style: OutlinedButton.styleFrom(
                        foregroundColor: SG.roseLight,
                        side: BorderSide(
                            color: SG.rose.withValues(alpha: 0.4)),
                        shape: RoundedRectangleBorder(
                            borderRadius: BorderRadius.circular(10)),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _row(String label, String value, {Color? valueColor}) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 10),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label,
              style: const TextStyle(
                  fontSize: 13.5,
                  fontWeight: FontWeight.w600,
                  color: SG.textSecondary)),
          Flexible(
            child: Text(value,
                textAlign: TextAlign.right,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(
                    fontSize: 13.5,
                    fontWeight: FontWeight.w700,
                    color: valueColor ?? SG.text)),
          ),
        ],
      ),
    );
  }
}
