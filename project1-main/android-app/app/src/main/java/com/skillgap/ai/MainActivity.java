package com.skillgap.ai;

import android.os.Bundle;
import android.view.MenuItem;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentManager;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.navigation.NavigationBarView;

public class MainActivity extends AppCompatActivity {

    private BottomNavigationView bottomNav;
    private AnalysisResult latestResult;
    private UserProfile activeProfile;

    private Fragment overviewFragment;
    private Fragment analyzerFragment;
    private Fragment analyticsFragment;
    private Fragment roadmapFragment;
    private Fragment chatFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        activeProfile = UserProfile.getDemoProfile();

        // Calculate baseline analysis immediately so all tabs have rich data
        latestResult = SkillEngine.analyze(activeProfile.resumeText, activeProfile.jobDesc);

        bottomNav = findViewById(R.id.bottomNav);

        overviewFragment = new OverviewFragment();
        analyzerFragment = new AnalyzerFragment();
        analyticsFragment = new AnalyticsFragment();
        roadmapFragment = new RoadmapFragment();
        chatFragment = new ChatFragment();

        // Default tab: Overview Dashboard
        loadFragment(overviewFragment);

        bottomNav.setOnItemSelectedListener(new NavigationBarView.OnItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                int itemId = item.getItemId();
                if (itemId == R.id.nav_overview) {
                    loadFragment(overviewFragment);
                    return true;
                } else if (itemId == R.id.nav_analyzer) {
                    loadFragment(analyzerFragment);
                    return true;
                } else if (itemId == R.id.nav_analytics) {
                    loadFragment(analyticsFragment);
                    return true;
                } else if (itemId == R.id.nav_roadmaps) {
                    loadFragment(roadmapFragment);
                    return true;
                } else if (itemId == R.id.nav_mentor) {
                    loadFragment(chatFragment);
                    return true;
                }
                return false;
            }
        });
    }

    public void navigateToTab(int tabId) {
        if (bottomNav != null) {
            bottomNav.setSelectedItemId(tabId);
        }
    }

    private void loadFragment(Fragment fragment) {
        FragmentManager fragmentManager = getSupportFragmentManager();
        fragmentManager.beginTransaction()
                .replace(R.id.fragmentContainer, fragment)
                .commit();
    }

    public AnalysisResult getLatestResult() {
        return latestResult;
    }

    public void setLatestResult(AnalysisResult result) {
        this.latestResult = result;
    }

    public UserProfile getActiveProfile() {
        return activeProfile;
    }

    public void setActiveProfile(UserProfile profile) {
        this.activeProfile = profile;
        this.latestResult = SkillEngine.analyze(profile.resumeText, profile.jobDesc);

        if (analyzerFragment instanceof AnalyzerFragment && analyzerFragment.isAdded()) {
            ((AnalyzerFragment) analyzerFragment).loadProfile(profile);
        }
        if (analyticsFragment instanceof AnalyticsFragment && analyticsFragment.isAdded()) {
            ((AnalyticsFragment) analyticsFragment).updateAnalysisForTrack(profile.targetRole);
        }
    }

    public void cycleNextProfile() {
        if (activeProfile == null || "priya".equals(activeProfile.id)) {
            setActiveProfile(UserProfile.getDemoProfile());
        } else if ("demo".equals(activeProfile.id)) {
            setActiveProfile(UserProfile.getAlexProfile());
        } else {
            setActiveProfile(UserProfile.getPriyaProfile());
        }
    }
}
