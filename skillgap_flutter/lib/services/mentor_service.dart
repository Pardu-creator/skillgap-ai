import 'dart:convert';

import 'package:http/http.dart' as http;

import 'analyzer.dart';

/// AI Career Mentor. Calls Gemini directly when the user configures an API key
/// in Settings; otherwise falls back to the built-in expert advice engine
/// (ported from backend.py / app.js).
class MentorService {
  static String? geminiApiKey;

  static Future<String> respond({
    required String question,
    AnalysisResult? analysis,
    List<Map<String, String>> history = const [],
  }) async {
    if (geminiApiKey != null && geminiApiKey!.trim().isNotEmpty) {
      try {
        final reply = await _callGemini(question, analysis, history);
        if (reply != null && reply.isNotEmpty) return reply;
      } catch (_) {
        // fall through to offline engine
      }
    }
    return offlineReply(question, analysis);
  }

  static Future<String?> _callGemini(
    String question,
    AnalysisResult? analysis,
    List<Map<String, String>> history,
  ) async {
    final context = analysis == null
        ? ''
        : '''
CANDIDATE ANALYSIS DATA:
- Employability Score: ${analysis.employabilityScore}%
- Target Role Match: ${analysis.matchScore}%
- Matched Skills: ${analysis.matchedSkills.join(', ')}
- Missing Skill Gaps: ${analysis.missingSkills.join(', ')}
- Additional Skills: ${analysis.extraSkills.join(', ')}
- Suggested Roles: ${analysis.suggestedRoles.join(', ')}
''';

    final systemPrompt = '''You are SkillGap AI's Career Mentor - an expert AI career advisor specializing in tech industry careers, resume optimization, interview preparation, and skill development roadmaps.

$context
GUIDELINES:
- Give specific, actionable advice based on the candidate's analysis data above
- Use markdown formatting: **bold** for emphasis, bullet points, numbered lists
- Keep responses concise but thorough (150-300 words)
- Reference specific skills from their profile when giving advice
- Be encouraging but honest about gaps''';

    final contents = <Map<String, dynamic>>[
      {'role': 'user', 'parts': [{'text': systemPrompt}]},
    ];
    for (final m in history.reversed.take(6).toList().reversed) {
      contents.add({
        'role': m['role'] == 'user' ? 'user' : 'model',
        'parts': [{'text': m['content'] ?? ''}],
      });
    }
    contents.add({'role': 'user', 'parts': [{'text': question}]});

    final uri = Uri.parse(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${geminiApiKey!.trim()}');
    final res = await http
        .post(uri,
            headers: {'Content-Type': 'application/json'},
            body: jsonEncode({
              'contents': contents,
              'generationConfig': {'temperature': 0.8, 'maxOutputTokens': 1024},
            }))
        .timeout(const Duration(seconds: 20));
    if (res.statusCode != 200) return null;
    final data = jsonDecode(res.body);
    return data['candidates']?[0]?['content']?['parts']?[0]?['text'] as String?;
  }

  /// Offline expert engine — contextual keyword-based career advice.
  static String offlineReply(String question, AnalysisResult? a) {
    final p = question.toLowerCase();
    final matched = a?.matchedSkills ?? const ["Python", "SQL", "Git"];
    final missing = a?.missingSkills ?? const ["Docker", "Kubernetes", "AWS"];
    final roles = a?.suggestedRoles ?? const ["Software Engineer"];

    if (a == null) {
      return "I'd love to give you personalized advice! Run an analysis on the **Skill Analyzer** tab first by uploading your resume, then come back here.\n\nIn the meantime - focus on building real projects and keeping your GitHub active!";
    }

    if (p.contains('score') || p.contains('improve')) {
      return "**Your Employability Score: ${a.employabilityScore}%**\n\nTo improve:\n1. **Bridge gaps**: Learn ${missing.take(3).join(', ')}\n2. **Add metrics**: Quantify achievements (e.g., \"Reduced load time by 40%\")\n3. **Deploy projects**: Add live links & clean GitHub repos\n4. **Get certified**: Consider AWS/Google Cloud certifications";
    }

    if (p.contains('roadmap') || p.contains('learn')) {
      return "**Personalized Roadmap for ${roles.first}**:\n\n**Weeks 1-3**: Master ${missing.take(2).join(' & ')}\n**Weeks 4-6**: Build 2 portfolio projects with deployment\n**Weeks 7-8**: Learn Docker + CI/CD\n**Weeks 9-12**: LeetCode practice + mock interviews\n\nCheck the **Roadmap** tab for the full timeline!";
    }

    if (p.contains('interview') || p.contains('question') || p.contains('mock')) {
      return "**Interview Prep for ${roles.first}**:\n\n1. \"Walk me through a project using ${matched.take(2).join(' and ')}\"\n2. \"How would you design a scalable ${roles.first.contains('Full') ? 'REST API' : 'data pipeline'}?\"\n3. \"What's the difference between ${matched.isNotEmpty ? matched.first : 'SQL'} and its alternatives?\"\n\n**Tip**: Use the STAR method for behavioral questions!";
    }

    if (p.contains('resume') || p.contains('ats')) {
      return "**Resume Optimization Strategy**\n\n1. **Quantify achievements**: Use the XYZ formula - \"Accomplished X as measured by Y by doing Z\"\n2. **ATS keywords**: Integrate **${missing.take(3).join(', ')}** into project bullet points\n3. **Showcase deployments**: Link live apps with clean GitHub repositories\n4. **Action verbs**: Architected, Spearheaded, Optimized, Engineered";
    }

    return "With **${matched.length} matched skills** and **${a.employabilityScore}%** employability, you're on a great track for **${roles.first}**!\n\nAsk me about:\n- How to improve your score\n- Learning roadmap recommendations\n- Interview question prep\n- Resume optimization tips";
  }
}
