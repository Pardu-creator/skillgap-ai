package com.skillgap.ai;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.google.android.material.chip.Chip;
import com.google.android.material.chip.ChipGroup;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class AnalyticsFragment extends Fragment {

    private ChipGroup roleTrackChipGroup;
    private TextView selectedRoleTitle;
    private TextView selectedRoleMatchBadge;
    private ProgressBar selectedRoleProgressBar;
    private ChipGroup roleSkillsChipGroup;
    private TextView roleMarketInsight;

    private static final String[] CAREER_TRACKS = {
            "Full Stack Developer",
            "Frontend Engineer",
            "Backend Engineer",
            "Machine Learning Engineer",
            "Data Scientist / Analyst",
            "Cloud & DevOps Engineer",
            "Cyber Security Analyst",
            "Mobile App Developer",
            "AI/LLM Engineer"
    };

    private String currentSelectedTrack = "Full Stack Developer";

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_analytics, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        roleTrackChipGroup = view.findViewById(R.id.roleTrackChipGroup);
        selectedRoleTitle = view.findViewById(R.id.selectedRoleTitle);
        selectedRoleMatchBadge = view.findViewById(R.id.selectedRoleMatchBadge);
        selectedRoleProgressBar = view.findViewById(R.id.selectedRoleProgressBar);
        roleSkillsChipGroup = view.findViewById(R.id.roleSkillsChipGroup);
        roleMarketInsight = view.findViewById(R.id.roleMarketInsight);

        setupTrackChips();
        updateAnalysisForTrack(currentSelectedTrack);
    }

    @Override
    public void onResume() {
        super.onResume();
        if (getActivity() instanceof MainActivity) {
            UserProfile profile = ((MainActivity) getActivity()).getActiveProfile();
            if (profile != null && profile.targetRole != null) {
                currentSelectedTrack = profile.targetRole;
            }
        }
        updateAnalysisForTrack(currentSelectedTrack);
    }

    private void setupTrackChips() {
        roleTrackChipGroup.removeAllViews();
        for (String track : CAREER_TRACKS) {
            Chip chip = new Chip(getContext());
            chip.setText(track);
            chip.setCheckable(true);
            chip.setClickable(true);
            chip.setTextSize(12f);

            if (track.equals(currentSelectedTrack)) {
                chip.setChecked(true);
                chip.setTextColor(getResources().getColor(R.color.accent_indigo, null));
                chip.setChipBackgroundColorResource(R.drawable.bg_badge_indigo);
            } else {
                chip.setChecked(false);
                chip.setTextColor(getResources().getColor(R.color.text_secondary, null));
                chip.setChipBackgroundColorResource(R.drawable.bg_chip);
            }

            chip.setOnCheckedChangeListener((buttonView, isChecked) -> {
                if (isChecked) {
                    currentSelectedTrack = track;
                    setupTrackChips();
                    updateAnalysisForTrack(track);
                }
            });

            roleTrackChipGroup.addView(chip);
        }
    }

    public void updateAnalysisForTrack(String track) {
        if (!isAdded() || getActivity() == null) return;

        selectedRoleTitle.setText(track);

        MainActivity mainActivity = (MainActivity) getActivity();
        UserProfile profile = mainActivity.getActiveProfile();
        List<String> userSkills = new ArrayList<>();

        if (mainActivity.getLatestResult() != null && mainActivity.getLatestResult().resumeSkills != null) {
            userSkills = mainActivity.getLatestResult().resumeSkills;
        } else if (profile != null && profile.resumeText != null) {
            userSkills = SkillEngine.extractSkills(profile.resumeText);
        }

        String[] requiredSkills = SkillEngine.ROLE_BLUEPRINTS.get(track);
        if (requiredSkills == null) {
            requiredSkills = new String[]{"Python", "Git", "REST API", "SQL"};
        }

        int matchedCount = 0;
        roleSkillsChipGroup.removeAllViews();

        for (String req : requiredSkills) {
            boolean hasSkill = false;
            for (String uSkill : userSkills) {
                if (uSkill.equalsIgnoreCase(req)) {
                    hasSkill = true;
                    break;
                }
            }

            Chip chip = new Chip(getContext());
            chip.setTextSize(11f);

            if (hasSkill) {
                matchedCount++;
                chip.setText("✓ " + req);
                chip.setTextColor(getResources().getColor(R.color.badge_matched_text, null));
                chip.setChipBackgroundColorResource(R.drawable.bg_badge_matched);
            } else {
                chip.setText("⚡ " + req);
                chip.setTextColor(getResources().getColor(R.color.badge_missing_text, null));
                chip.setChipBackgroundColorResource(R.drawable.bg_badge_missing);
            }
            chip.setChipStrokeWidth(0);
            roleSkillsChipGroup.addView(chip);
        }

        int matchPercent = requiredSkills.length > 0 ? (int) Math.round(((double) matchedCount / requiredSkills.length) * 100) : 0;
        selectedRoleMatchBadge.setText(matchPercent + "% Match");
        selectedRoleProgressBar.setProgress(matchPercent);

        // Dynamic market intelligence advice
        String insight;
        if (matchPercent >= 75) {
            insight = "⭐ Excellent Compatibility! Your profile already covers " + matchedCount + " of " + requiredSkills.length + " core industry competencies for " + track + ". Prioritize building a deployed capstone project to highlight production readiness.";
        } else if (matchPercent >= 50) {
            insight = "📈 Strong Foundation. You possess " + matchedCount + " essential competencies. Focus on bridging the remaining " + (requiredSkills.length - matchedCount) + " skill gaps over a 4–6 week targeted sprint to reach interview eligibility.";
        } else {
            insight = "🎯 High Growth Potential. Mastering foundational tools in this track will expand your employability across both startup and enterprise hiring pipelines.";
        }
        roleMarketInsight.setText(insight);
    }
}
