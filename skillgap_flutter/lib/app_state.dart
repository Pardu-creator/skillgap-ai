import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'services/analyzer.dart';
import 'services/auth_service.dart';
import 'services/mentor_service.dart';

/// Global app state — user session, analysis result, chat history,
/// roadmap progress, and selected tab. Singleton ChangeNotifier.
class AppState extends ChangeNotifier {
  AppState._();
  static final AppState instance = AppState._();

  AuthService? auth;
  SharedPreferences? prefs;

  AppUser? user;
  AnalysisResult? analysis;
  String lastUploadedName = '';
  int activeTab = 0;
  final List<Map<String, String>> mentorChat = [];
  final Set<int> roadmapDone = {};
  bool aiBusy = false;

  Future<void> init() async {
    auth = await AuthService.create();
    prefs = await SharedPreferences.getInstance();
    MentorService.geminiApiKey = prefs!.getString('gemini_api_key');
    user = auth!.currentUser();
    final done = prefs!.getStringList('roadmap_done') ?? const [];
    roadmapDone.addAll(done.map(int.parse));
    notifyListeners();
  }

  void setTab(int i) {
    activeTab = i;
    notifyListeners();
  }

  void setUser(AppUser? u) {
    user = u;
    notifyListeners();
  }

  void setAnalysis(AnalysisResult a, {String fileName = ''}) {
    analysis = a;
    if (fileName.isNotEmpty) lastUploadedName = fileName;
    roadmapDone.clear();
    notifyListeners();
  }

  void toggleRoadmapStep(int index) {
    if (roadmapDone.contains(index)) {
      roadmapDone.remove(index);
    } else {
      roadmapDone.add(index);
    }
    prefs?.setStringList(
        'roadmap_done', roadmapDone.map((e) => e.toString()).toList());
    notifyListeners();
  }

  Future<void> updateTargetRole(String role) async {
    if (user == null || auth == null) return;
    await auth!.updateTargetRole(user!.email, role);
    user = user!.copyWith(targetRole: role);
    notifyListeners();
  }

  Future<void> setGeminiKey(String key) async {
    MentorService.geminiApiKey = key.trim().isEmpty ? null : key.trim();
    await prefs?.setString('gemini_api_key', key.trim());
    notifyListeners();
  }

  void addChat(String role, String content) {
    mentorChat.add({'role': role, 'content': content});
    notifyListeners();
  }

  void clearChat() {
    mentorChat.clear();
    notifyListeners();
  }

  Future<void> resetSession() async {
    analysis = null;
    lastUploadedName = '';
    mentorChat.clear();
    roadmapDone.clear();
    await prefs?.remove('roadmap_done');
    notifyListeners();
  }

  Future<void> logout() async {
    await auth?.clearSession();
    await resetSession();
    user = null;
    activeTab = 0;
    notifyListeners();
  }
}
