package com.skillgap.ai;

import android.os.Bundle;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import com.google.android.material.floatingactionbutton.FloatingActionButton;

import java.util.ArrayList;
import java.util.List;

public class ChatFragment extends Fragment {

    private RecyclerView chatMessages;
    private EditText chatInput;
    private FloatingActionButton chatSendBtn;

    private com.google.android.material.button.MaterialButton chipImprove;
    private com.google.android.material.button.MaterialButton chipRoadmap;
    private com.google.android.material.button.MaterialButton chipInterview;

    private ChatAdapter adapter;
    private List<ChatAdapter.ChatMessage> messageList;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_chat, container, false);
        initViews(v);
        setupRecyclerView();
        setupChips();
        setupSend();
        addInitialGreeting();
        return v;
    }

    private void initViews(View v) {
        chatMessages = v.findViewById(R.id.chatMessages);
        chatInput = v.findViewById(R.id.chatInput);
        chatSendBtn = v.findViewById(R.id.chatSendBtn);

        chipImprove = v.findViewById(R.id.chipImprove);
        chipRoadmap = v.findViewById(R.id.chipRoadmap);
        chipInterview = v.findViewById(R.id.chipInterview);
    }

    private void setupRecyclerView() {
        messageList = new ArrayList<>();
        adapter = new ChatAdapter(messageList);
        LinearLayoutManager layoutManager = new LinearLayoutManager(getContext());
        layoutManager.setStackFromEnd(true);
        chatMessages.setLayoutManager(layoutManager);
        chatMessages.setAdapter(adapter);
    }

    private void addInitialGreeting() {
        if (messageList.isEmpty()) {
            AnalysisResult result = getResult();
            String greeting;
            if (result != null && result.suggestedRoles != null && !result.suggestedRoles.isEmpty()) {
                greeting = "Hello! 👋 I'm your AI Career Advisor. I see you're preparing for **" + result.suggestedRoles.get(0) + "** roles.\n\nYou currently have a **" + result.employabilityScore + "% Employability Score**. How can I assist you with your resume, skills, or interview preparation today?";
            } else {
                greeting = "Hello! 👋 I'm your AI Career Advisor & Technical Interview Mentor. Ask me anything about skill gaps, resume bullet points, roadmaps, or technical interview questions!";
            }
            adapter.addMessage(new ChatAdapter.ChatMessage(greeting, ChatAdapter.TYPE_AI));
        }
    }

    private void setupChips() {
        chipImprove.setOnClickListener(v -> sendMessage("How can I quickly improve my resume to score higher for top tech roles?"));
        chipRoadmap.setOnClickListener(v -> sendMessage("Can you break down a 4-week study plan for my missing skills?"));
        chipInterview.setOnClickListener(v -> sendMessage("What are 3 tough technical interview questions I should prepare for?"));
    }

    private void setupSend() {
        chatSendBtn.setOnClickListener(v -> {
            String text = chatInput.getText().toString().trim();
            if (!TextUtils.isEmpty(text)) {
                sendMessage(text);
                chatInput.setText("");
            }
        });
    }

    private void sendMessage(String text) {
        // Add user message
        adapter.addMessage(new ChatAdapter.ChatMessage(text, ChatAdapter.TYPE_USER));
        chatMessages.smoothScrollToPosition(adapter.getItemCount() - 1);

        // Add typing placeholder
        ChatAdapter.ChatMessage typingMsg = new ChatAdapter.ChatMessage("Thinking...", ChatAdapter.TYPE_AI);
        adapter.addMessage(typingMsg);
        int typingPos = adapter.getItemCount() - 1;
        chatMessages.smoothScrollToPosition(typingPos);

        AnalysisResult result = getResult();

        new GeminiApiClient().chat(text, result, new GeminiApiClient.ChatCallback() {
            @Override
            public void onSuccess(String response) {
                if (!isAdded() || getContext() == null) return;

                // Replace typing message with response
                messageList.set(typingPos, new ChatAdapter.ChatMessage(response, ChatAdapter.TYPE_AI));
                adapter.notifyItemChanged(typingPos);
                chatMessages.smoothScrollToPosition(typingPos);
            }

            @Override
            public void onError(String error) {
                if (!isAdded() || getContext() == null) return;

                String fallback = generateOfflineReply(text, result);
                messageList.set(typingPos, new ChatAdapter.ChatMessage(fallback, ChatAdapter.TYPE_AI));
                adapter.notifyItemChanged(typingPos);
            }
        });
    }

    private String generateOfflineReply(String userPrompt, AnalysisResult analysis) {
        String p = userPrompt.toLowerCase();
        String role = (analysis != null && analysis.roles != null && !analysis.roles.isEmpty()) ? analysis.roles.get(0) : "Software Engineer";
        String missing = (analysis != null && analysis.missing != null && !analysis.missing.isEmpty()) ? String.join(", ", analysis.missing.subList(0, Math.min(3, analysis.missing.size()))) : "Docker, Cloud Deployment, System Design";
        String matched = (analysis != null && analysis.matched != null && !analysis.matched.isEmpty()) ? String.join(", ", analysis.matched.subList(0, Math.min(3, analysis.matched.size()))) : "Core Programming, Git";
        int score = analysis != null ? analysis.employabilityScore : 78;

        if (p.contains("score") || p.contains("improve")) {
            return "### 🎯 Score Improvement Strategy\n\n**Current Readiness: " + score + "%**\n\n1. **Bridge Missing Competencies:** Master **" + missing + "** with deployed GitHub repos.\n2. **Quantify Achievements:** Use Google's XYZ formula: *'Accomplished [X] as measured by [Y] by doing [Z]'*.\n3. **Production Deployment:** Add live hosted URLs & clean READMEs to your projects.\n4. **ATS Alignment:** Integrate required job keywords naturally into your experience bullet points.";
        } else if (p.contains("roadmap") || p.contains("learn") || p.contains("study") || p.contains("plan")) {
            return "### 🚀 Personalized Learning Roadmap for " + role + "\n\n- **Weeks 1–3 (Core Gaps):** Focus intensely on **" + missing + "**.\n- **Weeks 4–6 (Applied Projects):** Build an end-to-end full stack capstone featuring automated testing.\n- **Weeks 7–8 (DevOps & Cloud):** Containerize your application with Docker & setup GitHub Actions CI/CD.\n- **Weeks 9–10 (Interview Mastery):** Practice LeetCode data structures & system design architectures.";
        } else if (p.contains("interview") || p.contains("question") || p.contains("prep") || p.contains("mock")) {
            return "### 💼 Technical Interview Preparation for " + role + "\n\n1. *\"Walk me through an end-to-end architecture you built using " + matched + ".\"*\n2. *\"How do you handle error boundaries, rate limiting, and database indexing under high concurrency?\"*\n3. *\"Explain how you would bridge and integrate " + missing + " into a microservices workflow.\"*\n\n💡 **Tip:** Structure all behavioral responses using the STAR method (Situation, Task, Action, Result)!";
        } else if (p.contains("stack") || p.contains("tech") || p.contains("recommend")) {
            return "### 💡 Recommended Technology Stack for " + role + "\n\n- **Languages & Frameworks:** Modern TypeScript/JavaScript & Python (FastAPI/Django).\n- **Database Layer:** PostgreSQL / SQLite with indexed schemas & Redis caching.\n- **Infrastructure:** Docker containerization, AWS/Vercel deployment, and automated CI/CD.\n\n✅ *Your Strength:* You already have verified competencies in **" + matched + "**!";
        } else {
            return "### 🤖 AI Career Mentor Insights\n\nWith **" + score + "% Employability Readiness** for **" + role + "**, you're on a strong trajectory!\n\n- **Key Strengths:** " + matched + "\n- **Priority Growth Targets:** " + missing + "\n\nAsk me for mock interview questions, ATS resume bullet optimization, or week-by-week roadmaps!";
        }
    }

    private AnalysisResult getResult() {
        if (getActivity() instanceof MainActivity) {
            return ((MainActivity) getActivity()).getLatestResult();
        }
        return null;
    }
}
