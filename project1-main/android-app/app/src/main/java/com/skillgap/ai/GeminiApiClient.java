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
 * Centralized Gemini API client.
 * API key is read from BuildConfig (compiled into APK, not in plain text).
 */
public class GeminiApiClient {

    private static final String GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=";
    private static final MediaType JSON = MediaType.parse("application/json; charset=utf-8");

    private final OkHttpClient client;
    private final ExecutorService executor;
    private final Handler mainHandler;
    private final String apiKey;
    private final Gson gson;

    public GeminiApiClient() {
        client = new OkHttpClient.Builder()
                .connectTimeout(30, java.util.concurrent.TimeUnit.SECONDS)
                .readTimeout(60, java.util.concurrent.TimeUnit.SECONDS)
                .build();
        executor = Executors.newCachedThreadPool();
        mainHandler = new Handler(Looper.getMainLooper());
        apiKey = BuildConfig.GEMINI_API_KEY;
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
                String prompt = buildAnalyzePrompt(resumeText, jobDesc, analysis);
                String responseText = callGemini(prompt, 0.6, 1200, true);

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
                String prompt = buildChatPrompt(message, analysis);
                String responseText = callGemini(prompt, 0.8, 1024, false);
                mainHandler.post(() -> callback.onSuccess(responseText));
            } catch (Exception e) {
                mainHandler.post(() -> callback.onError(e.getMessage()));
            }
        });
    }

    // ─── Core API Call ────────────────────────────────────────
    private String callGemini(String prompt, double temperature, int maxTokens, boolean jsonMode) throws IOException {
        JsonObject userPart = new JsonObject();
        userPart.addProperty("text", prompt);

        JsonObject userContent = new JsonObject();
        userContent.addProperty("role", "user");
        JsonArray parts = new JsonArray();
        parts.add(userPart);
        userContent.add("parts", parts);

        JsonArray contents = new JsonArray();
        contents.add(userContent);

        JsonObject genConfig = new JsonObject();
        genConfig.addProperty("temperature", temperature);
        genConfig.addProperty("maxOutputTokens", maxTokens);
        genConfig.addProperty("topP", 0.9);
        if (jsonMode) {
            genConfig.addProperty("responseMimeType", "application/json");
        }

        JsonObject body = new JsonObject();
        body.add("contents", contents);
        body.add("generationConfig", genConfig);

        Request request = new Request.Builder()
                .url(GEMINI_URL + apiKey)
                .post(RequestBody.create(body.toString(), JSON))
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) {
                throw new IOException("API error: " + response.code());
            }
            String responseBody = response.body().string();
            JsonObject json = JsonParser.parseString(responseBody).getAsJsonObject();
            return json.getAsJsonArray("candidates")
                    .get(0).getAsJsonObject()
                    .getAsJsonObject("content")
                    .getAsJsonArray("parts")
                    .get(0).getAsJsonObject()
                    .get("text").getAsString();
        }
    }

    // ─── Prompt Builders ──────────────────────────────────────
    private String buildAnalyzePrompt(String resumeText, String jobDesc, AnalysisResult analysis) {
        StringBuilder sb = new StringBuilder();
        sb.append("You are an expert ATS resume reviewer and career coach. Analyze this resume against the target job description.\n\n");
        sb.append("RESUME:\n").append(resumeText.length() > 3000 ? resumeText.substring(0, 3000) : resumeText).append("\n\n");

        if (jobDesc != null && !jobDesc.isEmpty()) {
            sb.append("TARGET JOB DESCRIPTION:\n").append(jobDesc.length() > 1500 ? jobDesc.substring(0, 1500) : jobDesc).append("\n\n");
        } else {
            sb.append("No specific job description provided — give general career improvement advice.\n\n");
        }

        sb.append("SKILL ANALYSIS (already computed):\n");
        sb.append("- Matched Skills: ").append(listJoin(analysis.matched)).append("\n");
        sb.append("- Missing Skills: ").append(listJoin(analysis.missing)).append("\n");
        sb.append("- Extra Skills: ").append(listJoin(analysis.extra)).append("\n");
        sb.append("- Match Score: ").append(analysis.matchScore).append("%\n");
        sb.append("- Employability Score: ").append(analysis.employabilityScore).append("%\n");
        sb.append("- Suggested Roles: ").append(listJoin(analysis.roles)).append("\n\n");

        sb.append("Provide your response in EXACTLY this JSON format (no markdown, just raw JSON):\n");
        sb.append("{\n");
        sb.append("  \"overallVerdict\": \"A one-line verdict\",\n");
        sb.append("  \"resumeStrengths\": [\"strength 1\", \"strength 2\", \"strength 3\"],\n");
        sb.append("  \"criticalImprovements\": [\"improvement 1\", \"improvement 2\", \"improvement 3\"],\n");
        sb.append("  \"atsScore\": 72,\n");
        sb.append("  \"atsTips\": [\"tip 1\", \"tip 2\"],\n");
        sb.append("  \"interviewTopics\": [\"topic 1\", \"topic 2\", \"topic 3\"]\n");
        sb.append("}");

        return sb.toString();
    }

    private String buildChatPrompt(String message, AnalysisResult analysis) {
        StringBuilder sb = new StringBuilder();
        sb.append("You are SkillGap AI's Career Mentor — an expert AI career advisor specializing in tech industry careers, resume optimization, interview preparation, and skill development roadmaps.\n\n");

        if (analysis != null) {
            sb.append("CANDIDATE ANALYSIS DATA:\n");
            sb.append("- Employability Score: ").append(analysis.employabilityScore).append("%\n");
            sb.append("- Target Role Match: ").append(analysis.matchScore).append("%\n");
            sb.append("- Matched Skills: ").append(listJoin(analysis.matched)).append("\n");
            sb.append("- Missing Skill Gaps: ").append(listJoin(analysis.missing)).append("\n");
            sb.append("- Additional Skills: ").append(listJoin(analysis.extra)).append("\n");
            sb.append("- Suggested Roles: ").append(listJoin(analysis.roles)).append("\n");
            sb.append("- Total Resume Skills: ").append(analysis.resumeSkills.size()).append("\n\n");
        }

        sb.append("GUIDELINES:\n");
        sb.append("- Give specific, actionable advice based on the candidate's data\n");
        sb.append("- Use **bold** for emphasis, bullet points, numbered lists\n");
        sb.append("- Keep responses concise but thorough (150-300 words)\n");
        sb.append("- Be encouraging but honest about gaps\n\n");

        sb.append("User question: ").append(message);

        return sb.toString();
    }

    // ─── Helpers ──────────────────────────────────────────────
    private String listJoin(List<String> list) {
        if (list == null || list.isEmpty()) return "None";
        return String.join(", ", list);
    }

    private AiFeedback parseAiFeedback(String json) {
        AiFeedback feedback = new AiFeedback();
        try {
            // Try to extract JSON if wrapped in markdown
            String cleaned = json.trim();
            if (cleaned.contains("{")) {
                cleaned = cleaned.substring(cleaned.indexOf("{"));
                int lastBrace = cleaned.lastIndexOf("}");
                if (lastBrace > 0) cleaned = cleaned.substring(0, lastBrace + 1);
            }

            JsonObject obj = JsonParser.parseString(cleaned).getAsJsonObject();

            if (obj.has("overallVerdict")) feedback.overallVerdict = obj.get("overallVerdict").getAsString();
            if (obj.has("atsScore")) feedback.atsScore = obj.get("atsScore").getAsInt();

            feedback.resumeStrengths = jsonArrayToList(obj, "resumeStrengths");
            feedback.criticalImprovements = jsonArrayToList(obj, "criticalImprovements");
            feedback.atsTips = jsonArrayToList(obj, "atsTips");
            feedback.interviewTopics = jsonArrayToList(obj, "interviewTopics");

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
