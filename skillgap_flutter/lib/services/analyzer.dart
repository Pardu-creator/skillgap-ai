import '../data/skill_data.dart';

/// Result of running the resume/job-description analysis engine.
class AnalysisResult {
  final List<String> resumeSkills;
  final List<String> requiredSkills;
  final List<String> matchedSkills;
  final List<String> missingSkills;
  final List<String> extraSkills;
  final int matchScore;
  final int employabilityScore;
  final int breadthScore;
  final List<String> suggestedRoles;
  final List<String> suggestions;
  final List<RoadmapStep> roadmap;
  final String sourceName;

  const AnalysisResult({
    required this.resumeSkills,
    required this.requiredSkills,
    required this.matchedSkills,
    required this.missingSkills,
    required this.extraSkills,
    required this.matchScore,
    required this.employabilityScore,
    required this.breadthScore,
    required this.suggestedRoles,
    required this.suggestions,
    required this.roadmap,
    this.sourceName = '',
  });
}

/// One milestone in the personalized learning roadmap.
class RoadmapStep {
  final String phase;
  final String description;
  final List<RoadmapSkill> skills;
  const RoadmapStep(this.phase, this.description, this.skills);
}

class RoadmapSkill {
  final String name;
  final String resource;
  const RoadmapSkill(this.name, this.resource);
}

/// On-device resume analysis engine. Ports the client-side scoring
/// algorithm from the original web app (app.js).
class Analyzer {
  static String normalize(String text) {
    var t = text.toLowerCase().replaceAll('-', ' ').replaceAll('_', ' ');
    t = t.replaceAll(RegExp(r'[^a-zA-Z0-9+#. ]'), ' ');
    t = t.replaceAll(RegExp(r'\s+'), ' ');
    return t.trim();
  }

  static List<String> extractSkills(String text) {
    final norm = ' ${normalize(text)} ';
    final found = <String>{};
    for (final skill in kSkillDatabase) {
      final pattern = RegExp('\\b${RegExp.escape(normalize(skill))}\\b');
      if (pattern.hasMatch(norm)) found.add(skill);
    }
    return found.toList()..sort();
  }

  static List<String> suggestRoles(List<String> skills) {
    final lower = skills.map((s) => s.toLowerCase()).toSet();
    final scored = <MapEntry<String, int>>[];
    kRoleBlueprints.forEach((role, reqs) {
      final hits = reqs.where((r) => lower.contains(r.toLowerCase())).length;
      if (hits >= 2) scored.add(MapEntry(role, hits));
    });
    scored.sort((a, b) => b.value.compareTo(a.value));
    if (scored.isEmpty) {
      return ["Software Developer Trainee", "Junior Web Developer"];
    }
    return scored.map((e) => e.key).toList();
  }

  static AnalysisResult analyze({
    required String resumeText,
    String jobDescription = '',
    String sourceName = '',
  }) {
    final resumeSkills = extractSkills(resumeText);
    var requiredSkills = jobDescription.trim().isNotEmpty
        ? extractSkills(jobDescription)
        : <String>[];
    if (requiredSkills.isEmpty) requiredSkills = kDefaultRequiredSkills;

    final reqLower = requiredSkills.map((s) => s.toLowerCase()).toSet();
    final resLower = resumeSkills.map((s) => s.toLowerCase()).toSet();

    final matched = requiredSkills
        .where((s) => resLower.contains(s.toLowerCase()))
        .toList()
      ..sort();
    final missing = requiredSkills
        .where((s) => !resLower.contains(s.toLowerCase()))
        .toList()
      ..sort();
    final extra = resumeSkills
        .where((s) => !reqLower.contains(s.toLowerCase()))
        .toList()
      ..sort();

    final matchScore =
        ((matched.length / requiredSkills.length) * 100).round();
    final skillWeight =
        resumeSkills.length * 5 > 40 ? 40 : resumeSkills.length * 5;
    final matchWeight = (matchScore * 0.45).round();
    final bonusWeight = matched.length >= 4 ? 15 : matched.length * 3;
    var employability = skillWeight + matchWeight + bonusWeight;
    if (employability > 100) employability = 100;
    if (employability < 0) employability = 0;
    final breadth =
        ((resumeSkills.length / 15) * 100).round().clamp(0, 100);

    final roles = suggestRoles(resumeSkills);

    return AnalysisResult(
      resumeSkills: resumeSkills,
      requiredSkills: requiredSkills,
      matchedSkills: matched,
      missingSkills: missing,
      extraSkills: extra,
      matchScore: matchScore,
      employabilityScore: employability,
      breadthScore: breadth,
      suggestedRoles: roles,
      suggestions: _suggestions(resumeText, missing),
      roadmap: _roadmap(missing, roles.first),
      sourceName: sourceName,
    );
  }

  static List<String> _suggestions(String resumeText, List<String> missing) {
    final text = resumeText.toLowerCase();
    final tips = <String>[];
    if (missing.isNotEmpty) {
      tips.add("Improve these missing skills: ${missing.join(', ')}");
    } else {
      tips.add("Your resume has good skill alignment with the job description.");
    }
    if (!text.contains('project')) {
      tips.add("Add at least 2 to 3 strong projects related to your target job role.");
    }
    if (!text.contains('internship')) {
      tips.add("Add internship, training, certification, or practical experience details.");
    }
    if (!text.contains('github')) {
      tips.add("Add your GitHub profile link and project repository links.");
    }
    if (!text.contains('linkedin')) {
      tips.add("Add your LinkedIn profile for better professional visibility.");
    }
    if (!text.contains('achievement')) {
      tips.add("Add achievements, certifications, hackathons, workshops, or awards.");
    }
    if (!text.contains('sql')) {
      tips.add("Add SQL knowledge because it is important for most data and software roles.");
    }
    if (!text.contains('communication')) {
      tips.add("Mention communication, teamwork, and problem-solving skills.");
    }
    return tips;
  }

  static String _resourceFor(String skill) =>
      kLearningCourses[skill] ??
      "Search for top-rated courses on Coursera / Udemy";

  /// The 12-week 4-phase roadmap from the web app.
  static List<RoadmapStep> _roadmap(List<String> missing, String targetRole) {
    final gapSkills = missing
        .take(3)
        .map((s) => RoadmapSkill(s, _resourceFor(s)))
        .toList();

    return [
      RoadmapStep(
        "Phase 1: High Priority Skill Gaps (Weeks 1-3)",
        missing.isNotEmpty
            ? "Master core requirements: ${missing.take(3).join(', ')}"
            : "Deepen expertise in your strongest skills and explore advanced patterns",
        gapSkills.isNotEmpty
            ? gapSkills
            : [const RoadmapSkill("Advanced Topics", "Explore deep-dive content in your core stack")],
      ),
      RoadmapStep(
        "Phase 2: Project-Based Application (Weeks 4-6)",
        "Build a production-grade portfolio project matching real $targetRole requirements.",
        const [
          RoadmapSkill("Hands-on Projects", "Build 2-3 real-world projects with deployment"),
          RoadmapSkill("Clean Code", "Clean Code by Robert Martin & Refactoring Guru"),
          RoadmapSkill("Unit Testing", "Jest/Pytest + TDD methodology"),
        ],
      ),
      RoadmapStep(
        "Phase 3: Cloud & Deployment (Weeks 7-8)",
        "Containerize and deploy with CI/CD pipelines and monitoring.",
        [
          RoadmapSkill("Docker", _resourceFor("Docker")),
          const RoadmapSkill("CI/CD", "GitHub Actions + Vercel/AWS deployment"),
          const RoadmapSkill("Cloud Hosting", "AWS Free Tier / Vercel / Railway"),
        ],
      ),
      RoadmapStep(
        "Phase 4: Interview Mastery (Weeks 9-12)",
        "Technical interviews, system design, and behavioral prep with STAR method.",
        [
          const RoadmapSkill("DSA Practice", "LeetCode 75 + NeetCode roadmap"),
          RoadmapSkill("System Design", _resourceFor("System Design")),
          const RoadmapSkill("Mock Interviews", "Pramp.com + interviewing.io"),
        ],
      ),
    ];
  }
}
