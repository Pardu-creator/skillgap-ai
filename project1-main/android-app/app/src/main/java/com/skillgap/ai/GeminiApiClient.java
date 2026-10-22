package com.skillgap.ai;

import android.os.Handler;
import android.os.Looper;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import okhttp3.MediaType;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.RequestBody;
import okhttp3.Response;

/**
 * SkillGap AI — API client that routes through the Vercel backend.
 * No API key required in the app — the key is stored securely on the server.
 */
public class GeminiApiClient {

    // ─── Backend URL (Vercel) ──────────────────────────────────
    private static final String BASE_URL = "https://project1-main.vercel.app";
    private static final String ANALYZE_URL = BASE_URL + "/api/analyze";
    private static final String CHAT_URL    = BASE_URL + "/api/chat";
    private static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");

    private final OkHttpClient client;
    private final ExecutorService executor;
    private final Handler mainHandler;
    private final Gson gson;

    public GeminiApiClient() {
        client = new OkHttpClient.Builder()
                .connectTimeout(30, java.util.concurrent.TimeUnit.SECONDS)
                .readTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
                .build();
        executor = Executors.newCachedThreadPool();
        mainHandler = new Handler(Looper.getMainLooper());
        gson = new Gson();
    }

    // ─── Analyze Resume ───────────────────────────────────────
    public interface AnalyzeCallback {
        void onSuccess(AiFeedback feedback);
        void onError(String error);
    }

    public void analyzeResume(String resumeText, String jobDesc, AnalysisResult analysis, AnalyzeCallback callback) {
        executor.execute(() -> {
            try {
                // Build request body for /api/analyze
                JsonObject body = new JsonObject();
                body.addProperty("resumeText", resumeText != null ? resumeText : "");
                body.addProperty("jobDesc", jobDesc != null ? jobDesc : "");
                body.addProperty("matchScore", analysis.matchScore);
                body.addProperty("employabilityScore", analysis.employabilityScore);

                // Add matched/missing/extra skills
                body.add("matched", listToJsonArray(analysis.matched));
                body.add("missing", listToJsonArray(analysis.missing));
                body.add("extra", listToJsonArray(analysis.extra));
                body.add("roles", listToJsonArray(analysis.roles));

                String responseText = postToBackend(ANALYZE_URL, body.toString());

                AiFeedback feedback = parseAiFeedback(responseText);
                mainHandler.post(() -> callback.onSuccess(feedback));

            } catch (Exception e) {
                mainHandler.post(() -> callback.onError(e.getMessage()));
            }
        });
    }

    // ─── Chat ─────────────────────────────────────────────────
    public interface ChatCallback {
        void onSuccess(String reply);
        void onError(String error);
    }

    public void chat(String message, AnalysisResult analysis, ChatCallback callback) {
        executor.execute(() -> {
            try {
                // Build request body for /api/chat
                JsonObject body = new JsonObject();
                body.addProperty("message", message);

                if (analysis != null) {
                    JsonObject analysisObj = new JsonObject();
                    analysisObj.addProperty("employabilityScore", analysis.employabilityScore);
                    analysisObj.addProperty("matchScore", analysis.matchScore);
                    analysisObj.add("matched", listToJsonArray(analysis.matched));
                    analysisObj.add("missing", listToJsonArray(analysis.missing));
                    analysisObj.add("extra", listToJsonArray(analysis.extra));
                    analysisObj.add("roles", listToJsonArray(analysis.roles));
                    body.add("analysis", analysisObj);
                }

                String responseText = postToBackend(CHAT_URL, body.toString());

                // Parse { "reply": "..." }
                JsonObject json = JsonParser.parseString(responseText).getAsJsonObject();
                String reply = json.has("reply") ? json.get("reply").getAsString()
                        : "I'm here to help with your career questions!";

                mainHandler.post(() -> callback.onSuccess(reply));

            } catch (Exception e) {
                mainHandler.post(() -> callback.onError(e.getMessage()));
            }
        });
    }

    // ─── Core HTTP POST ────────────────────────────────────────
    private String postToBackend(String url, String jsonBody) throws IOException {
        Request request = new Request.Builder()
                .url(url)
                .post(RequestBody.create(jsonBody, JSON))
                .addHeader("Content-Type", "application/json")
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("Server error: " + response.code());
            }
            return response.body().string();
        }
    }

    // ─── Helpers ──────────────────────────────────────────────
    private JsonArray listToJsonArray(List<String> list) {
        JsonArray arr = new JsonArray();
        if (list != null) {
            for (String s : list) arr.add(s);
        }
        return arr;
    }

    private AiFeedback parseAiFeedback(String json) {
        AiFeedback feedback = new AiFeedback();
        try {
            String cleaned = json.trim();
            if (cleaned.contains("{")) {
                cleaned = cleaned.substring(cleaned.indexOf("{"));
                int lastBrace = cleaned.lastIndexOf("}");
                if (lastBrace > 0) cleaned = cleaned.substring(0, lastBrace + 1);
            }

            JsonObject obj = JsonParser.parseString(cleaned).getAsJsonObject();

            if (obj.has("overallVerdict"))  feedback.overallVerdict = obj.get("overallVerdict").getAsString();
            if (obj.has("atsScore"))        feedback.atsScore = obj.get("atsScore").getAsInt();

            feedback.resumeStrengths     = jsonArrayToList(obj, "resumeStrengths");
            feedback.criticalImprovements = jsonArrayToList(obj, "criticalImprovements");
            feedback.atsTips             = jsonArrayToList(obj, "atsTips");
            feedback.interviewTopics     = jsonArrayToList(obj, "interviewTopics");

        } catch (Exception e) {
            feedback.overallVerdict = "Analysis completed. Check skill breakdown above.";
            feedback.atsScore = 50;
        }
        return feedback;
    }

    private List<String> jsonArrayToList(JsonObject obj, String key) {
        List<String> list = new ArrayList<>();
        if (obj.has(key) && obj.get(key).isJsonArray()) {
            JsonArray arr = obj.getAsJsonArray(key);
            for (int i = 0; i < arr.size(); i++) {
                list.add(arr.get(i).getAsString());
            }
        }
        return list;
    }

    // ─── AI Feedback Model ────────────────────────────────────
    public static class AiFeedback {
        public String overallVerdict = "";
        public int atsScore = 50;
        public List<String> resumeStrengths = new ArrayList<>();
        public List<String> criticalImprovements = new ArrayList<>();
        public List<String> atsTips = new ArrayList<>();
        public List<String> interviewTopics = new ArrayList<>();
    }
}
