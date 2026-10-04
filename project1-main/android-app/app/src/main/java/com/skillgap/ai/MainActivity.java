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

    private Fragment analyzerFragment;
    private Fragment roadmapFragment;
    private Fragment chatFragment;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        bottomNav = findViewById(R.id.bottomNav);

        analyzerFragment = new AnalyzerFragment();
        roadmapFragment = new RoadmapFragment();
        chatFragment = new ChatFragment();

        // Default tab: Analyzer
        loadFragment(analyzerFragment);

        bottomNav.setOnItemSelectedListener(new NavigationBarView.OnItemSelectedListener() {
            @Override
            public boolean onNavigationItemSelected(@NonNull MenuItem item) {
                int itemId = item.getItemId();
                if (itemId == R.id.nav_analyzer) {
                    loadFragment(analyzerFragment);
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
}
