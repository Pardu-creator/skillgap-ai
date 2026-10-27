import 'package:flutter/material.dart';

import '../app_state.dart';
import '../services/mentor_service.dart';
import '../theme.dart';
import '../widgets/widgets.dart';

/// Tab 5 — AI Career Mentor chat (Gemini when configured, offline engine
/// fallback).
class MentorScreen extends StatefulWidget {
  const MentorScreen({super.key});

  @override
  State<MentorScreen> createState() => _MentorScreenState();
}

class _MentorScreenState extends State<MentorScreen> {
  final _input = TextEditingController();
  final _scroll = ScrollController();
  bool _thinking = false;

  static const _chips = [
    'How can I improve my score?',
    'What is the best learning roadmap?',
    'Give me interview questions for my role',
    'How do I beat ATS scanners?',
    'What portfolio projects should I build?',
  ];

  @override
  void initState() {
    super.initState();
    if (AppState.instance.mentorChat.isEmpty) {
      AppState.instance.addChat('assistant',
          "Hello! I am your **AI Career Mentor**. I have analyzed your background and I am ready to help you with technical interview prep, resume improvements, and personalized learning roadmaps. Pick a question below or ask anything!");
    }
  }

  @override
  void dispose() {
    _input.dispose();
    _scroll.dispose();
    super.dispose();
  }

  void _scrollDown() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scroll.hasClients) {
        _scroll.animateTo(_scroll.position.maxScrollExtent,
            duration: const Duration(milliseconds: 300), curve: Curves.easeOut);
      }
    });
  }

  Future<void> _send([String? preset]) async {
    final text = (preset ?? _input.text).trim();
    if (text.isEmpty || _thinking) return;
    _input.clear();
    final s = AppState.instance;
    s.addChat('user', text);
    setState(() => _thinking = true);
    _scrollDown();

    final reply = await MentorService.respond(
      question: text,
      analysis: s.analysis,
      history: s.mentorChat,
    );
    s.addChat('assistant', reply);
    setState(() => _thinking = false);
    _scrollDown();
  }

  @override
  Widget build(BuildContext context) {
    final s = AppState.instance;
    final msgs = s.mentorChat;

    return Column(
      children: [
        // header
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 4, 8, 8),
          child: Row(
            children: [
              const Icon(Icons.smart_toy_outlined,
                  size: 20, color: SG.indigoLight),
              const SizedBox(width: 8),
              const Expanded(
                child: Text('AI Career Advisor & Interview Mentor',
                    style: TextStyle(
                        fontSize: 15,
                        fontWeight: FontWeight.w800,
                        color: SG.text)),
              ),
              Container(
                padding:
                    const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: SG.emerald.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(999),
                  border:
                      Border.all(color: SG.emerald.withValues(alpha: 0.3)),
                ),
                child: Row(mainAxisSize: MainAxisSize.min, children: [
                  const PulseDot(),
                  const SizedBox(width: 5),
                  Text(
                      MentorService.geminiApiKey != null
                          ? 'Gemini'
                          : 'Offline',
                      style: const TextStyle(
                          fontSize: 10,
                          fontWeight: FontWeight.w800,
                          color: SG.emeraldLight)),
                ]),
              ),
              IconButton(
                tooltip: 'Clear chat',
                icon: const Icon(Icons.refresh_rounded,
                    size: 19, color: SG.textSecondary),
                onPressed: () => s.clearChat(),
              ),
            ],
          ),
        ),

        // messages
        Expanded(
          child: ListView.builder(
            controller: _scroll,
            padding: const EdgeInsets.symmetric(horizontal: 16),
            itemCount: msgs.length + (_thinking ? 1 : 0),
            itemBuilder: (_, i) {
              if (i == msgs.length) return const _TypingBubble();
              final m = msgs[i];
              final isUser = m['role'] == 'user';
              return _Bubble(text: m['content']!, isUser: isUser);
            },
          ),
        ),

        // suggestion chips
        SizedBox(
          height: 38,
          child: ListView.separated(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 16),
            itemCount: _chips.length,
            separatorBuilder: (_, _) => const SizedBox(width: 8),
            itemBuilder: (_, i) =>
                ChipTag(_chips[i], color: SG.purpleLight, onTap: () => _send(_chips[i])),
          ),
        ),
        const SizedBox(height: 10),

        // input bar
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 0, 16, 14),
          child: Row(
            children: [
              Expanded(
                child: TextField(
                  controller: _input,
                  onSubmitted: (_) => _send(),
                  decoration: const InputDecoration(
                    hintText: 'Ask your AI Mentor anything...',
                    isDense: true,
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Container(
                decoration: BoxDecoration(
                  gradient: SG.gradient,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: IconButton(
                  icon: const Icon(Icons.send_rounded,
                      color: Colors.white, size: 19),
                  onPressed: () => _send(),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}

class _Bubble extends StatelessWidget {
  final String text;
  final bool isUser;
  const _Bubble({required this.text, required this.isUser});

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: isUser ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 11),
        constraints: BoxConstraints(
            maxWidth: MediaQuery.of(context).size.width * 0.82),
        decoration: BoxDecoration(
          gradient: isUser ? SG.gradient : null,
          color: isUser ? null : SG.cardSoft,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: Radius.circular(isUser ? 16 : 4),
            bottomRight: Radius.circular(isUser ? 4 : 16),
          ),
          border: isUser ? null : Border.all(color: SG.border),
        ),
        child: isUser
            ? Text(text,
                style: const TextStyle(
                    fontSize: 13.5, color: Colors.white, height: 1.45))
            : MarkdownText(text),
      ),
    );
  }
}

class _TypingBubble extends StatefulWidget {
  const _TypingBubble();

  @override
  State<_TypingBubble> createState() => _TypingBubbleState();
}

class _TypingBubbleState extends State<_TypingBubble>
    with SingleTickerProviderStateMixin {
  late final AnimationController _c;

  @override
  void initState() {
    super.initState();
    _c = AnimationController(
        vsync: this, duration: const Duration(milliseconds: 900))
      ..repeat();
  }

  @override
  void dispose() {
    _c.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.only(bottom: 10),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
        decoration: BoxDecoration(
          color: SG.cardSoft,
          borderRadius: BorderRadius.circular(16),
          border: Border.all(color: SG.border),
        ),
        child: AnimatedBuilder(
          animation: _c,
          builder: (_, _) => Row(
            mainAxisSize: MainAxisSize.min,
            children: List.generate(3, (i) {
              final t = ((_c.value * 3) - i).clamp(0.0, 1.0);
              final opacity = (0.3 + 0.7 * (1 - (t - 0.5).abs() * 2))
                  .clamp(0.3, 1.0);
              return Padding(
                padding: const EdgeInsets.symmetric(horizontal: 2.5),
                child: Opacity(
                  opacity: opacity,
                  child: const CircleAvatar(
                      radius: 3.5, backgroundColor: SG.textMuted),
                ),
              );
            }),
          ),
        ),
      ),
    );
  }
}
