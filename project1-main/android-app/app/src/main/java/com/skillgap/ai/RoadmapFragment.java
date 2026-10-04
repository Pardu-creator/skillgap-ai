package com.skillgap.ai;

import android.os.Bundle;
import android.text.TextUtils;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import java.util.ArrayList;
import java.util.List;

public class RoadmapFragment extends Fragment {

    private LinearLayout roadmapList;
    private View roadmapEmpty;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View v = inflater.inflate(R.layout.fragment_roadmap, container, false);
        roadmapList = v.findViewById(R.id.roadmapList);
        roadmapEmpty = v.findViewById(R.id.roadmapEmpty);
        return v;
    }

    @Override
    public void onResume() {
        super.onResume();
        loadRoadmap();
    }

    private void loadRoadmap() {
        AnalysisResult result = null;
        if (getActivity() instanceof MainActivity) {
            result = ((MainActivity) getActivity()).getLatestResult();
        }

        if (result == null || (result.missing == null || result.missing.isEmpty()) && (result.matched == null || result.matched.isEmpty())) {
            roadmapEmpty.setVisibility(View.VISIBLE);
            roadmapList.setVisibility(View.GONE);
            return;
        }

        roadmapEmpty.setVisibility(View.GONE);
        roadmapList.setVisibility(View.VISIBLE);
        roadmapList.removeAllViews();

        List<String> missing = result.missing != null ? result.missing : new ArrayList<>();
        List<String> matched = result.matched != null ? result.matched : new ArrayList<>();
        String targetRole = (result.suggestedRoles != null && !result.suggestedRoles.isEmpty()) ? result.suggestedRoles.get(0) : "Target Role";

        // Generate 3 Phased Steps
        List<RoadmapPhase> phases = new ArrayList<>();

        // Phase 1: Immediate Gaps
        List<String> p1Skills = new ArrayList<>();
        int countP1 = Math.min(3, missing.size());
        for (int i = 0; i < countP1; i++) {
            p1Skills.add(missing.get(i));
        }
        if (p1Skills.isEmpty()) {
            p1Skills.add("Advanced System Design");
            p1Skills.add("Performance Optimization");
        }
        phases.add(new RoadmapPhase(
                "Phase 1: Core Fundamentals & Prerequisite Gaps",
                "Weeks 1 - 4 • High Priority",
                "Focus on acquiring core missing competencies required for " + targetRole + ".",
                p1Skills,
                "Build a foundational mini-project implementing " + TextUtils.join(" and ", p1Skills) + "."
        ));

        // Phase 2: Advanced Mastery
        List<String> p2Skills = new ArrayList<>();
        for (int i = countP1; i < missing.size(); i++) {
            p2Skills.add(missing.get(i));
        }
        if (p2Skills.isEmpty()) {
            p2Skills.add("CI/CD Automation");
            p2Skills.add("Cloud Deployment & Microservices");
        }
        phases.add(new RoadmapPhase(
                "Phase 2: Advanced Mastery & Specialized Frameworks",
                "Weeks 5 - 8 • Technical Deep Dive",
                "Combine your existing strengths (" + (matched.isEmpty() ? "Core Skills" : matched.get(0)) + ") with new skills to stand out.",
                p2Skills,
                "Develop a full-featured capstone repository with automated testing and production deployment."
        ));

        // Phase 3: Career Ready & Interview Prep
        List<String> p3Skills = new ArrayList<>();
        p3Skills.add("Mock System Design Interviews");
        p3Skills.add("Resume ATS Optimization & Portfolio Review");
        p3Skills.add("LeetCode / Algorithm Speed Drills");
        phases.add(new RoadmapPhase(
                "Phase 3: Portfolio Excellence & Interview Coaching",
                "Weeks 9 - 12 • Hiring Readiness",
                "Polish your professional story, optimize ATS visibility, and practice interview questions for " + targetRole + ".",
                p3Skills,
                "Schedule 3 mock interviews and submit 10 targeted job applications."
        ));

        // Render phases into layout
        LayoutInflater inflater = LayoutInflater.from(getContext());
        int[] phaseColors = {R.color.accent_cyan, R.color.accent_indigo, R.color.accent_emerald};
        String[] phaseNumbers = {"01", "02", "03"};

        for (int i = 0; i < phases.size(); i++) {
            RoadmapPhase phase = phases.get(i);

            // Timeline row: number badge + card
            LinearLayout rowLayout = new LinearLayout(getContext());
            rowLayout.setOrientation(LinearLayout.HORIZONTAL);
            rowLayout.setGravity(android.view.Gravity.TOP);
            LinearLayout.LayoutParams rowLp = new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.MATCH_PARENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
            );
            rowLp.setMargins(0, 0, 0, 24);
            rowLayout.setLayoutParams(rowLp);

            // Phase number badge
            TextView numBadge = new TextView(getContext());
            numBadge.setText(phaseNumbers[i]);
            numBadge.setTextColor(getResources().getColor(phaseColors[i]));
            numBadge.setTextSize(12);
            numBadge.setTypeface(null, android.graphics.Typeface.BOLD);
            numBadge.setBackgroundResource(R.drawable.bg_chip);
            numBadge.setPadding(20, 10, 20, 10);
            LinearLayout.LayoutParams badgeLp = new LinearLayout.LayoutParams(
                    LinearLayout.LayoutParams.WRAP_CONTENT,
                    LinearLayout.LayoutParams.WRAP_CONTENT
            );
            badgeLp.setMargins(0, 4, 16, 0);
            numBadge.setLayoutParams(badgeLp);

            // Card layout
            LinearLayout cardLayout = new LinearLayout(getContext());
            cardLayout.setOrientation(LinearLayout.VERTICAL);
            cardLayout.setBackgroundResource(R.drawable.bg_card);
            cardLayout.setPadding(48, 44, 48, 44);
            LinearLayout.LayoutParams cardLp = new LinearLayout.LayoutParams(
                    0, LinearLayout.LayoutParams.WRAP_CONTENT, 1f
            );
            cardLayout.setLayoutParams(cardLp);

            // Phase Title
            TextView titleTv = new TextView(getContext());
            titleTv.setText(phase.title);
            titleTv.setTextColor(getResources().getColor(R.color.text_primary));
            titleTv.setTextSize(16);
            titleTv.setTypeface(null, android.graphics.Typeface.BOLD);
            titleTv.setPadding(0, 0, 0, 8);

            // Phase Subtitle
            TextView subTv = new TextView(getContext());
            subTv.setText(phase.timeline);
            subTv.setTextColor(getResources().getColor(R.color.accent_cyan));
            subTv.setTextSize(12);
            subTv.setPadding(0, 0, 0, 16);

            // Phase Description
            TextView descTv = new TextView(getContext());
            descTv.setText(phase.description);
            descTv.setTextColor(getResources().getColor(R.color.text_secondary));
            descTv.setTextSize(13);
            descTv.setPadding(0, 0, 0, 16);

            // Skills to learn
            TextView skillsHeader = new TextView(getContext());
            skillsHeader.setText("🎯 Key Milestones & Topics:");
            skillsHeader.setTextColor(getResources().getColor(R.color.accent_indigo));
            skillsHeader.setTextSize(13);
            skillsHeader.setTypeface(null, android.graphics.Typeface.BOLD);
            skillsHeader.setPadding(0, 0, 0, 8);

            TextView skillsListTv = new TextView(getContext());
            skillsListTv.setText("• " + TextUtils.join("\n• ", phase.skills));
            skillsListTv.setTextColor(getResources().getColor(R.color.text_primary));
            skillsListTv.setTextSize(13);
            skillsListTv.setPadding(0, 0, 0, 16);

            // Capstone Project
            TextView projectTv = new TextView(getContext());
            projectTv.setText("🚀 Deliverable: " + phase.capstone);
            projectTv.setTextColor(getResources().getColor(R.color.accent_emerald));
            projectTv.setTextSize(12);
            projectTv.setBackgroundResource(R.drawable.bg_chip);
            projectTv.setPadding(24, 14, 24, 14);

            cardLayout.addView(titleTv);
            cardLayout.addView(subTv);
            cardLayout.addView(descTv);
            cardLayout.addView(skillsHeader);
            cardLayout.addView(skillsListTv);
            cardLayout.addView(projectTv);

            rowLayout.addView(numBadge);
            rowLayout.addView(cardLayout);
            roadmapList.addView(rowLayout);
        }
    }

    private static class RoadmapPhase {
        String title;
        String timeline;
        String description;
        List<String> skills;
        String capstone;

        RoadmapPhase(String title, String timeline, String description, List<String> skills, String capstone) {
            this.title = title;
            this.timeline = timeline;
            this.description = description;
            this.skills = skills;
            this.capstone = capstone;
        }
    }
}
