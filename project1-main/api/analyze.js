/**
 * Vercel Serverless Function — AI-Enhanced Resume Analysis
 * Calls Gemini for deep resume feedback beyond keyword matching
 */

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "POST only" });

  const GEMINI_KEY = process.env.GEMINI_API_KEY || "YOUR_API_KEY_HERE";
  if (!GEMINI_KEY) {
    return res.status(500).json({ error: "GEMINI_API_KEY not configured" });
  }

  try {
    const { resumeText, jobDesc, matched, missing, extra, matchScore, employabilityScore, roles } = req.body;
    if (!resumeText) return res.status(400).json({ error: "resumeText required" });

    const prompt = `You are an expert ATS resume reviewer and career coach. Analyze this resume against the target job description and provide actionable feedback.

RESUME:
${resumeText.substring(0, 3000)}

${jobDesc ? `TARGET JOB DESCRIPTION:\n${jobDesc.substring(0, 1500)}` : "No specific job description provided — give general career improvement advice."}

SKILL ANALYSIS (already computed):
- Matched Skills: ${(matched || []).join(", ") || "None"}
- Missing Skills: ${(missing || []).join(", ") || "None"}
- Extra Skills: ${(extra || []).join(", ") || "None"}
- Match Score: ${matchScore || 0}%
- Employability Score: ${employabilityScore || 0}%
- Suggested Roles: ${(roles || []).join(", ")}

Provide your response in EXACTLY this JSON format (no markdown, just raw JSON):
{
  "overallVerdict": "A one-line verdict like 'Strong candidate with key gaps in cloud infrastructure'",
  "resumeStrengths": ["strength 1", "strength 2", "strength 3"],
  "criticalImprovements": ["improvement 1", "improvement 2", "improvement 3"],
  "atsScore": 72,
  "atsTips": ["tip 1", "tip 2"],
  "interviewTopics": ["topic 1", "topic 2", "topic 3"],
  "weekPlan": [
    {"week": "Week 1-2", "focus": "Learn Docker & containerization", "resource": "Docker Mastery on Udemy"},
    {"week": "Week 3-4", "focus": "Build a full-stack project", "resource": "freeCodeCamp Full Stack"},
    {"week": "Week 5-6", "focus": "System design fundamentals", "resource": "Grokking System Design"}
  ]
}`;

    const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_KEY}`;

    const geminiRes = await fetch(geminiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [
          { role: "user", parts: [{ text: prompt }] }
        ],
        generationConfig: {
          temperature: 0.6,
          maxOutputTokens: 1200,
          topP: 0.9,
          responseMimeType: "application/json"
        }
      })
    });

    if (!geminiRes.ok) {
      const errText = await geminiRes.text();
      console.error("Gemini analyze error:", errText);
      return res.status(502).json({ error: "AI service error" });
    }

    const data = await geminiRes.json();
    const raw = data?.candidates?.[0]?.content?.parts?.[0]?.text || "{}";

    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch {
      // Try extracting JSON from markdown code block
      const jsonMatch = raw.match(/\{[\s\S]*\}/);
      parsed = jsonMatch ? JSON.parse(jsonMatch[0]) : { overallVerdict: "Analysis completed. Check skill breakdown above.", resumeStrengths: [], criticalImprovements: [], atsScore: matchScore || 50 };
    }

    return res.status(200).json(parsed);

  } catch (err) {
    console.error("Analyze handler error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
}
