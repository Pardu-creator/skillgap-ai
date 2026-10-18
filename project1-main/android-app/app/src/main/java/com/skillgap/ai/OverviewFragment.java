package com.skillgap.ai;

import android.animation.ValueAnimator;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ProgressBar;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import com.google.android.material.chip.Chip;
import com.google.android.material.chip.ChipGroup;

import java.util.List;

public class OverviewFragment extends Fragment {

    private TextView headerUserAvatar;
    private TextView headerUserName;
    private View btnProfilePill;

    private TextView overviewWelcomeText;
    private TextView overviewTrackSubtitle;

    private View actionScanResume;
    private View actionAnalytics;
    private View actionRoadmap;
    private View actionMentor;

    private ProgressBar overviewGaugeProgress;
    private TextView overviewGaugeValue;
    private ProgressBar overviewMatchBar;
    private TextView overviewMatchScore;
    private ProgressBar overviewBreadthBar;
    private TextView overviewBreadthScore;

    private ChipGroup overviewMatchedChips;
    private ChipGroup overviewMissingChips;

    private Button btnCandidateDemo;
    private Button btnCandidateAlex;
    private Button btnCandidatePriya;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_overview, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        headerUserAvatar = view.findViewById(R.id.headerUserAvatar);
        headerUserName = view.findViewById(R.id.headerUserName);
        btnProfilePill = view.findViewById(R.id.btnProfilePill);

        overviewWelcomeText = view.findViewById(R.id.overviewWelcomeText);
        overviewTrackSubtitle = view.findViewById(R.id.overviewTrackSubtitle);

        actionScanResume = view.findViewById(R.id.actionScanResume);
        actionAnalytics = view.findViewById(R.id.actionAnalytics);
        actionRoadmap = view.findViewById(R.id.actionRoadmap);
        actionMentor = view.findViewById(R.id.actionMentor);

        overviewGaugeProgress = view.findViewById(R.id.overviewGaugeProgress);
        overviewGaugeValue = view.findViewById(R.id.overviewGaugeValue);
        overviewMatchBar = view.findViewById(R.id.overviewMatchBar);
        overviewMatchScore = view.findViewById(R.id.overviewMatchScore);
        overviewBreadthBar = view.findViewById(R.id.overviewBreadthBar);
        overviewBreadthScore = view.findViewById(R.id.overviewBreadthScore);

        overviewMatchedChips = view.findViewById(R.id.overviewMatchedChips);
        overviewMissingChips = view.findViewById(R.id.overviewMissingChips);

        btnCandidateDemo = view.findViewById(R.id.btnCandidateDemo);
        btnCandidateAlex = view.findViewById(R.id.btnCandidateAlex);
        btnCandidatePriya = view.findViewById(R.id.btnCandidatePriya);

        setupActionClicks();
        setupCandidateButtons();
        updateUI();
    }

    @Override
    public void onResume() {
        super.onResume();
        updateUI();
    }

    private void setupActionClicks() {
        actionScanResume.setOnClickListener(v -> {
            if (getActivity() instanceof MainActivity) {
                ((MainActivity) getActivity()).navigateToTab(R.id.nav_analyzer);
            }
        });

        actionAnalytics.setOnClickListener(v -> {
            if (getActivity() instanceof MainActivity) {
                ((MainActivity) getActivity()).navigateToTab(R.id.nav_analytics);
            }
        });

        actionRoadmap.setOnClickListener(v -> {
            if (getActivity() instanceof MainActivity) {
                ((MainActivity) getActivity()).navigateToTab(R.id.nav_roadmaps);
            }
        });

        actionMentor.setOnClickListener(v -> {
            if (getActivity() instanceof MainActivity) {
                ((MainActivity) getActivity()).navigateToTab(R.id.nav_mentor);
            }
        });

        btnProfilePill.setOnClickListener(v -> {
            if (getActivity() instanceof MainActivity) {
                ((MainActivity) getActivity()).cycleNextProfile();
                updateUI();
            }
        });
    }

    private void setupCandidateButtons() {
        btnCandidateDemo.setOnClickListener(v -> {
            if (getActivity() instanceof MainActivity) {
                ((MainActivity) getActivity()).setActiveProfile(UserProfile.getDemoProfile());
                updateUI();
            }
        });

        btnCandidateAlex.setOnClickListener(v -> {
            if (getActivity() instanceof MainActivity) {
                ((MainActivity) getActivity()).setActiveProfile(UserProfile.getAlexProfile());
                updateUI();
            }
        });

        btnCandidatePriya.setOnClickListener(v -> {
            if (getActivity() instanceof MainActivity) {
                ((MainActivity) getActivity()).setActiveProfile(UserProfile.getPriyaProfile());
                updateUI();
            }
        });
    }

    public void updateUI() {
        if (!isAdded() || getActivity() == null) return;

        MainActivity mainActivity = (MainActivity) getActivity();
        UserProfile profile = mainActivity.getActiveProfile();
        AnalysisResult result = mainActivity.getLatestResult();

        if (profile != null) {
            headerUserAvatar.setText(profile.initials);
            headerUserName.setText(profile.name);
            overviewWelcomeText.setText("Welcome back, " + profile.name + " 👋");
            overviewTrackSubtitle.setText("Target Career Track: " + profile.targetRole + " • Profile updated from latest resume");

            // Update candidate button states
            btnCandidateDemo.setBackgroundResource("demo".equals(profile.id) ? R.drawable.bg_button_primary : R.drawable.bg_chip);
            btnCandidateAlex.setBackgroundResource("alex".equals(profile.id) ? R.drawable.bg_button_primary : R.drawable.bg_chip);
            btnCandidatePriya.setBackgroundResource("priya".equals(profile.id) ? R.drawable.bg_button_primary : R.drawable.bg_chip);
        }

        if (result != null) {
            animateGauge(result.employabilityScore);
            overviewMatchBar.setProgress(result.matchScore);
            overviewMatchScore.setText(result.matchScore + "%");
            overviewBreadthBar.setProgress(result.breadthScore);
            overviewBreadthScore.setText(result.breadthScore + "%");

            populateChips(overviewMatchedChips, result.matched, R.color.badge_matched_text, R.drawable.bg_badge_matched, "✓ ");
            populateChips(overviewMissingChips, result.missing, R.color.badge_missing_text, R.drawable.bg_badge_missing, "⚡ ");
        } else {
            // Default preview scores
            animateGauge(78);
            overviewMatchBar.setProgress(82);
            overviewMatchScore.setText("82%");
            overviewBreadthBar.setProgress(75);
            overviewBreadthScore.setText("75%");
        }
    }

    private void animateGauge(int targetScore) {
        ValueAnimator anim = ValueAnimator.ofInt(0, targetScore);
        anim.setDuration(700);
        anim.addUpdateListener(animation -> {
            int val = (int) animation.getAnimatedValue();
            if (overviewGaugeProgress != null) overviewGaugeProgress.setProgress(val);
            if (overviewGaugeValue != null) overviewGaugeValue.setText(val + "%");
        });
        anim.start();
    }

    private void populateChips(ChipGroup group, List<String> items, int textColorRes, int bgRes, String prefix) {
        group.removeAllViews();
        if (items == null || items.isEmpty()) {
            Chip emptyChip = new Chip(getContext());
            emptyChip.setText("None detected");
            emptyChip.setTextSize(11f);
            emptyChip.setTextColor(getResources().getColor(R.color.text_muted, null));
            group.addView(emptyChip);
            return;
        }

        int count = Math.min(items.size(), 6);
        for (int i = 0; i < count; i++) {
            String skill = items.get(i);
            Chip chip = new Chip(getContext());
            chip.setText(prefix + skill);
            chip.setTextSize(11f);
            chip.setTextColor(getResources().getColor(textColorRes, null));
            chip.setChipBackgroundColorResource(bgRes);
            chip.setChipStrokeWidth(0);
            group.addView(chip);
        }
    }
}
