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

                String fallback = "I'm currently operating in offline mode. Based on your skill gap profile, I recommend prioritizing high-frequency missing skills and building hands-on portfolio projects to present to recruiters.";
                messageList.set(typingPos, new ChatAdapter.ChatMessage(fallback, ChatAdapter.TYPE_AI));
                adapter.notifyItemChanged(typingPos);
            }
        });
    }

    private AnalysisResult getResult() {
        if (getActivity() instanceof MainActivity) {
            return ((MainActivity) getActivity()).getLatestResult();
        }
        return null;
    }
}
