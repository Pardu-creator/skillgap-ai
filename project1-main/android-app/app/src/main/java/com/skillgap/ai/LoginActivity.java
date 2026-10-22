package com.skillgap.ai;

import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.text.TextUtils;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;

import com.google.android.material.button.MaterialButton;

/**
 * LoginActivity — collects user's name & email, saves to SharedPreferences,
 * then launches MainActivity.
 */
public class LoginActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        EditText    nameField  = findViewById(R.id.loginName);
        EditText    emailField = findViewById(R.id.loginEmail);
        MaterialButton loginBtn  = findViewById(R.id.loginBtn);
        MaterialButton guestBtn  = findViewById(R.id.guestBtn);

        // ── Sign In ──────────────────────────────────────────────
        loginBtn.setOnClickListener(v -> {
            String name  = nameField.getText().toString().trim();
            String email = emailField.getText().toString().trim();

            if (TextUtils.isEmpty(name)) {
                nameField.setError("Please enter your name");
                nameField.requestFocus();
                return;
            }
            if (TextUtils.isEmpty(email) || !email.contains("@")) {
                emailField.setError("Please enter a valid email");
                emailField.requestFocus();
                return;
            }

            saveUserAndProceed(name, email);
        });

        // ── Guest ────────────────────────────────────────────────
        guestBtn.setOnClickListener(v -> {
            saveUserAndProceed("Guest", "guest@skillgap.ai");
        });
    }

    private void saveUserAndProceed(String name, String email) {
        SharedPreferences prefs = getSharedPreferences("skillgap_prefs", MODE_PRIVATE);
        prefs.edit()
             .putBoolean("is_logged_in", true)
             .putString("user_name", name)
             .putString("user_email", email)
             .apply();

        Toast.makeText(this, "Welcome, " + name + "! 🚀", Toast.LENGTH_SHORT).show();

        startActivity(new Intent(this, MainActivity.class));
        overridePendingTransition(android.R.anim.fade_in, android.R.anim.fade_out);
        finish();
    }
}
