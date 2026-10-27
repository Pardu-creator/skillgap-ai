import 'package:flutter_test/flutter_test.dart';
import 'package:skillgap_flutter/services/analyzer.dart';
import 'package:skillgap_flutter/data/skill_data.dart';

void main() {
  test('skill extraction finds known skills', () {
    final skills = Analyzer.extractSkills(
        'I have experience with Python, React, and Docker on AWS.');
    expect(skills, containsAll(['Python', 'React', 'Docker', 'AWS']));
    expect(skills, isNot(contains('Kubernetes')));
  });

  test('analysis produces employability score and gaps', () {
    final a = Analyzer.analyze(
      resumeText: kSamplePresets.first.resume,
      jobDescription: kSamplePresets.first.jd,
    );
    expect(a.employabilityScore, inInclusiveRange(0, 100));
    expect(a.matchedSkills, isNotEmpty);
    expect(a.suggestedRoles, isNotEmpty);
    expect(a.roadmap.length, 4);
  });
}
