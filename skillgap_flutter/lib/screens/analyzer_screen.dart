import 'dart:io';

import 'package:file_picker/file_picker.dart';
import 'package:flutter/material.dart';

import '../app_state.dart';
import '../data/skill_data.dart';
import '../services/analyzer.dart';
import '../services/pdf_extract.dart';
import '../theme.dart';
import '../widgets/widgets.dart';

/// Tab 2 — Smart Skill Analyzer: resume upload, presets, JD input,
/// results with gauge, matched/missing/extra skill clouds, AI feedback.
class AnalyzerScreen extends StatefulWidget {
  const AnalyzerScreen({super.key});

  @override
  State<AnalyzerScreen> createState() => _AnalyzerScreenState();
}

class _AnalyzerScreenState extends State<AnalyzerScreen> {
  final _resumeCtrl = TextEditingController();
  final _jdCtrl = TextEditingController();
  bool _analyzing = false;
  String _fileStatus = '';
  String? _templateKey;

  @override
  void dispose() {
    _resumeCtrl.dispose();
    _jdCtrl.dispose();
    super.dispose();
  }

  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'txt', 'docx'],
      withData: true,
    );
    if (result == null || result.files.isEmpty) return;
    final file = result.files.single;
    setState(() => _fileStatus = 'Reading ${file.name}...');

    try {
      String text;
      if (file.name.toLowerCase().endsWith('.pdf')) {
        final bytes = file.bytes ??
            (file.path != null ? await File(file.path!).readAsBytes() : null);
        if (bytes == null) throw StateError('no bytes');
        text = PdfTextExtractor.extract(bytes);
        if (text.length < 40) {
          throw StateError('Scanned/image PDF — no extractable text');
        }
      } else {
        final bytes = file.bytes ??
            (file.path != null ? await File(file.path!).readAsBytes() : null);
        text = bytes != null ? String.fromCharCodes(bytes) : '';
      }
      setState(() {
        _resumeCtrl.text = text;
        _fileStatus = 'Extracted text from ${file.name}';
      });
      AppState.instance.lastUploadedName = file.name;
    } catch (e) {
      setState(() => _fileStatus =
          'Could not parse ${file.name}. Please paste text manually.');
    }
  }

  void _applyPreset(SamplePreset p) {
    setState(() {
      _resumeCtrl.text = p.resume;
      _jdCtrl.text = p.jd;
      _fileStatus = 'Loaded sample: ${p.label}';
    });
  }

  Future<void> _analyze() async {
    if (_resumeCtrl.text.trim().isEmpty) {
      sgToast(context, 'Please upload a resume or paste resume text first.');
      return;
    }
    setState(() => _analyzing = true);
    await Future.delayed(const Duration(milliseconds: 600));
    final result = Analyzer.analyze(
      resumeText: _resumeCtrl.text,
      jobDescription: _jdCtrl.text,
      sourceName: AppState.instance.lastUploadedName,
    );
    AppState.instance.setAnalysis(result);
    if (!mounted) return;
    setState(() => _analyzing = false);
    sgToast(context, 'Deep Analysis Complete! Results updated across dashboard.');
  }

  @override
  Widget build(BuildContext context) {
    final a = AppState.instance.analysis;
    return ListView(
      padding: const EdgeInsets.fromLTRB(16, 4, 16, 24),
      children: [
        // ---- Input card ----
        GlassCard(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const CardHeader(
                  icon: Icons.description_outlined,
                  title: 'Resume & Target Role'),
              InkWell(
                onTap: _pickFile,
                borderRadius: BorderRadius.circular(14),
                child: Container(
                  width: double.infinity,
                  padding: const EdgeInsets.symmetric(vertical: 22),
                  decoration: BoxDecoration(
                    color: SG.cardSoft,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(
                        color: SG.indigo.withValues(alpha: 0.3),
                        style: BorderStyle.solid),
                  ),
                  child: Column(
                    children: [
                      Icon(Icons.cloud_upload_outlined,
                          size: 30, color: SG.indigoLight),
                      const SizedBox(height: 8),
                      const Text('Tap to upload your Resume',
                          style: TextStyle(
                              fontSize: 14,
                              fontWeight: FontWeight.w800,
                              color: SG.text)),
                      const SizedBox(height: 2),
                      const Text('Supports PDF, TXT, DOCX (local parsing)',
                          style: TextStyle(
                              fontSize: 11.5, color: SG.textSecondary)),
                      if (_fileStatus.isNotEmpty) ...[
                        const SizedBox(height: 8),
                        Text(_fileStatus,
                            textAlign: TextAlign.center,
                            style: const TextStyle(
                                fontSize: 11.5,
                                fontWeight: FontWeight.w600,
                                color: SG.cyanLight)),
                      ],
                    ],
                  ),
                ),
              ),
              const SizedBox(height: 14),
              const Text('Or try a sample candidate profile',
                  style: TextStyle(
                      fontSize: 11.5,
                      fontWeight: FontWeight.w700,
                      color: SG.textMuted)),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  for (final p in kSamplePresets)
                    ChipTag(p.label,
                        color: SG.purpleLight, onTap: () => _applyPreset(p)),
                ],
              ),
              const SizedBox(height: 14),
              TextField(
                controller: _resumeCtrl,
                maxLines: 6,
                decoration: const InputDecoration(
                  labelText: 'Resume Content',
                  hintText: 'Paste resume text or upload a file above...',
                  alignLabelWithHint: true,
                ),
              ),
              const SizedBox(height: 14),
              DropdownButtonFormField<String>(
                initialValue: _templateKey,
                decoration: const InputDecoration(
                    labelText: 'Role Template (fills Job Description)'),
                dropdownColor: SG.bgAlt,
                isExpanded: true,
                items: const [
                  DropdownMenuItem(
                      value: 'fullstack',
                      child: Text('Full Stack Engineer',
                          overflow: TextOverflow.ellipsis)),
                  DropdownMenuItem(
                      value: 'frontend',
                      child: Text('Frontend Engineer',
                          overflow: TextOverflow.ellipsis)),
                  DropdownMenuItem(
                      value: 'backend',
                      child: Text('Backend Engineer',
                          overflow: TextOverflow.ellipsis)),
                  DropdownMenuItem(
                      value: 'ml',
                      child: Text('Machine Learning Engineer',
                          overflow: TextOverflow.ellipsis)),
                  DropdownMenuItem(
                      value: 'devops',
                      child: Text('DevOps & Cloud Engineer',
                          overflow: TextOverflow.ellipsis)),
                ],
                onChanged: (v) {
                  setState(() {
                    _templateKey = v;
                    if (v != null) _jdCtrl.text = kRoleTemplates[v]!;
                  });
                },
              ),
              const SizedBox(height: 14),
              TextField(
                controller: _jdCtrl,
                maxLines: 4,
                decoration: const InputDecoration(
                  labelText: 'Target Job Description (Optional)',
                  hintText:
                      'Paste target job requirements or pick a template above...',
                  alignLabelWithHint: true,
                ),
              ),
              const SizedBox(height: 16),
              GradientButton(
                label: 'Analyze Employability & Gaps',
                icon: Icons.auto_awesome,
                loading: _analyzing,
                onPressed: _analyze,
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),

        // ---- Results ----
        if (a == null)
          GlassCard(
            padding: const EdgeInsets.symmetric(vertical: 40, horizontal: 24),
            child: Column(
              children: [
                Icon(Icons.bar_chart_rounded,
                    size: 44, color: SG.indigo.withValues(alpha: 0.5)),
                const SizedBox(height: 12),
                const Text('No Assessment Generated Yet',
                    style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.w800,
                        color: SG.text)),
                const SizedBox(height: 6),
                const Text(
                    'Upload your resume or tap a sample preset to view your Employability Score and Skill Gap breakdown.',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                        fontSize: 12.5, color: SG.textSecondary, height: 1.5)),
              ],
            ),
          )
        else
          GlassCard(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const CardHeader(
                    icon: Icons.bar_chart_rounded,
                    title: 'Assessment Results',
                    iconColor: SG.cyanLight),
                Center(child: ScoreGauge(percent: a.employabilityScore)),
                const SizedBox(height: 18),
                MetricBar('Target Role Match', a.matchScore,
                    color: SG.cyanLight),
                const SizedBox(height: 12),
                MetricBar('Skill Breadth Depth', a.breadthScore,
                    color: SG.indigoLight),
                const SizedBox(height: 18),

                // Top role banner
                Container(
                  padding: const EdgeInsets.all(14),
                  decoration: BoxDecoration(
                    color: SG.cardSoft,
                    borderRadius: BorderRadius.circular(14),
                    border: Border.all(color: SG.border),
                  ),
                  child: Row(
                    children: [
                      Container(
                        width: 42,
                        height: 42,
                        decoration: BoxDecoration(
                          gradient: SG.gradient,
                          borderRadius: BorderRadius.circular(12),
                        ),
                        child: const Icon(Icons.emoji_events_outlined,
                            color: Colors.white, size: 22),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text('Top Role Alignment',
                                style: TextStyle(
                                    fontSize: 11,
                                    fontWeight: FontWeight.w700,
                                    color: SG.textMuted)),
                            Text(a.suggestedRoles.take(2).join(' · '),
                                style: const TextStyle(
                                    fontSize: 14,
                                    fontWeight: FontWeight.w800,
                                    color: SG.text)),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 18),

                // AI feedback (heuristic engine)
                _AiFeedback(analysis: a),
                const SizedBox(height: 18),

                _SkillSection(
                    'Matched Skills', a.matchedSkills, SG.emeraldLight,
                    prefix: '✓ '),
                _SkillSection(
                    'Missing Skill Gaps', a.missingSkills, SG.roseLight,
                    prefix: '✗ '),
                _SkillSection(
                    'Additional Candidate Skills', a.extraSkills, SG.cyanLight,
                    prefix: '+ '),

                const SizedBox(height: 8),
                const Text('RESUME SUGGESTIONS',
                    style: TextStyle(
                        fontSize: 10.5,
                        fontWeight: FontWeight.w800,
                        color: SG.textMuted,
                        letterSpacing: 1.2)),
                const SizedBox(height: 8),
                for (final tip in a.suggestions)
                  Padding(
                    padding: const EdgeInsets.only(bottom: 6),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Icon(Icons.check_circle_outline,
                            size: 14, color: SG.indigoLight),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(tip,
                              style: const TextStyle(
                                  fontSize: 12.5,
                                  color: SG.textSecondary,
                                  height: 1.4)),
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

class _AiFeedback extends StatelessWidget {
  final AnalysisResult analysis;
  const _AiFeedback({required this.analysis});

  @override
  Widget build(BuildContext context) {
    final a = analysis;
    final tips = <String>[
      if (a.missingSkills.isNotEmpty)
        'Bridge your top skill gaps: ${a.missingSkills.take(3).join(', ')}',
      'Add quantifiable metrics to experience bullets (e.g., "Improved API response time by 40%")',
      'Include links to live deployed projects and clean GitHub repos',
      if (a.matchedSkills.length < 5)
        'Consider obtaining a relevant certification to strengthen your profile',
    ];

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: SG.cardSoft,
        borderRadius: BorderRadius.circular(14),
        border: Border.all(color: SG.indigo.withValues(alpha: 0.25)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(children: [
            Icon(Icons.auto_awesome, size: 16, color: SG.purpleLight),
            SizedBox(width: 7),
            Text('AI Resume Analysis',
                style: TextStyle(
                    fontSize: 13.5,
                    fontWeight: FontWeight.w800,
                    color: SG.text)),
          ]),
          const SizedBox(height: 12),
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Icon(Icons.analytics_outlined,
                  size: 30, color: SG.indigoLight),
              const SizedBox(width: 10),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Quick Analysis',
                        style: TextStyle(
                            fontSize: 12.5,
                            fontWeight: FontWeight.w800,
                            color: SG.text)),
                    Text(
                        'Matched ${a.matchedSkills.length} of ${a.requiredSkills.length} target skills. ${a.missingSkills.isNotEmpty ? "Focus on bridging ${a.missingSkills.length} gap${a.missingSkills.length > 1 ? 's' : ''}." : "Great skill coverage!"}',
                        style: const TextStyle(
                            fontSize: 12,
                            color: SG.textSecondary,
                            height: 1.45)),
                  ],
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),
          const Text('Improvement Tips',
              style: TextStyle(
                  fontSize: 12, fontWeight: FontWeight.w800, color: SG.text)),
          const SizedBox(height: 6),
          for (final t in tips)
            Padding(
              padding: const EdgeInsets.only(bottom: 5),
              child: Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('• ',
                      style: TextStyle(color: SG.purpleLight, fontSize: 13)),
                  Expanded(
                    child: Text(t,
                        style: const TextStyle(
                            fontSize: 12,
                            color: SG.textSecondary,
                            height: 1.4)),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}

class _SkillSection extends StatelessWidget {
  final String title;
  final List<String> skills;
  final Color color;
  final String prefix;
  const _SkillSection(this.title, this.skills, this.color,
      {this.prefix = ''});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(title,
                  style: const TextStyle(
                      fontSize: 13,
                      fontWeight: FontWeight.w800,
                      color: SG.text)),
              CountPill('${skills.length}', color: color),
            ],
          ),
          const SizedBox(height: 8),
          if (skills.isEmpty)
            const Text('None detected',
                style: TextStyle(fontSize: 12, color: SG.textMuted))
          else
            Wrap(
              spacing: 6,
              runSpacing: 6,
              children: [
                for (final s in skills)
                  ChipTag('$prefix$s', color: color),
              ],
            ),
        ],
      ),
    );
  }
}
