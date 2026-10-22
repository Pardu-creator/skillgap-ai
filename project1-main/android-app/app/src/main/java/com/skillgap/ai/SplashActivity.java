package com.skillgap.ai;

import android.animation.AnimatorSet;
import android.animation.ObjectAnimator;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.view.animation.DecelerateInterpolator;
import android.widget.ProgressBar;

import androidx.appcompat.app.AppCompatActivity;

/**
 * SplashActivity — shown on every app launch.
 * Animates logo in, checks if user is logged in, then routes to Login or Main.
 */
public class SplashActivity extends AppCompatActivity {

    private static final int SPLASH_DURATION = 2200; // ms

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Hide status/nav bar for full immersive splash
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_FULLSCREEN | View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
        );

        setContentView(R.layout.activity_splash);

        View content   = findViewById(R.id.splashContent);
        ProgressBar pb = findViewById(R.id.splashProgress);

        // Fade + scale in the logo content
        ObjectAnimator fadeIn  = ObjectAnimator.ofFloat(content, "alpha",  0f, 1f);
        ObjectAnimator scaleX  = ObjectAnimator.ofFloat(content, "scaleX", 0.8f, 1f);
        ObjectAnimator scaleY  = ObjectAnimator.ofFloat(content, "scaleY", 0.8f, 1f);
        ObjectAnimator pbFade  = ObjectAnimator.ofFloat(pb,      "alpha",  0f, 1f);

        AnimatorSet set = new AnimatorSet();
        set.playTogether(fadeIn, scaleX, scaleY, pbFade);
        set.setDuration(700);
        set.setInterpolator(new DecelerateInterpolator());
        set.start();

        // After splash duration, navigate
        new Handler(getMainLooper()).postDelayed(() -> {
            SharedPreferences prefs = getSharedPreferences("skillgap_prefs", MODE_PRIVATE);
            boolean loggedIn = prefs.getBoolean("is_logged_in", false);

            Intent intent;
            if (loggedIn) {
                intent = new Intent(SplashActivity.this, MainActivity.class);
            } else {
                intent = new Intent(SplashActivity.this, LoginActivity.class);
            }
            startActivity(intent);

            // Smooth transition
            overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
            finish();

        }, SPLASH_DURATION);
    }
}
