/**
 * Vercel Serverless Function — AI Career Mentor Chat
 * Calls Gemini API for real AI responses
 */

export default async function handler(req, res) {
  // CORS
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
    const { message, analysis } = req.body;
    if (!message) return res.status(400).json({ error: "message required" });

    // Build context from analysis data
    let context = "";
    if (analysis) {
      context = `
CANDIDATE ANALYSIS DATA:
- Employability Score: ${analysis.employabilityScore}%
- Target Role Match: ${analysis.matchScore}%
- Matched Skills: ${(analysis.matched || []).join(", ") || "None analyzed yet"}
- Missing Skill Gaps: ${(analysis.missing || []).join(", ") || "None"}
- Additional Skills: ${(analysis.extra || []).join(", ") || "None"}
- Suggested Roles: ${(analysis.roles || []).join(", ") || "Not determined"}
- Total Resume Skills: ${(analysis.resumeSkills || []).length}
`;
    }

    const systemPrompt = `You are SkillGap AI's Career Mentor — an expert AI career advisor specializing in tech industry careers, resume optimization, interview preparation, and skill development roadmaps.

${context}

GUIDELINES:
- Give specific, actionable advice based on the candidate's analysis data above
- Use markdown formatting: **bold** for emphasis, bullet points, numbered lists
- Keep responses concise but thorough (150-300 words)
- Reference specific skills from their profile when giving advice
- For interview questions, give actual sample questions with brief answer frameworks
- For roadmaps, give week-by-week plans with specific resources
- Be encouraging but honest about gaps
- If no analysis data is available, encourage them to run an analysis first but still give general career advice`;

    const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${GEMINI_KEY}`;

    const geminiRes = await fetch(geminiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [
          { role: "user", parts: [{ text: systemPrompt + "\n\nUser question: " + message }] }
        ],
        generationConfig: {
          temperature: 0.8,
          maxOutputTokens: 1024,
          topP: 0.95,
        }
      })
    });

    if (!geminiRes.ok) {
      const errText = await geminiRes.text();
      console.error("Gemini API error:", errText);
      return res.status(502).json({ error: "AI service error", details: errText });
    }

    const data = await geminiRes.json();
    const reply = data?.candidates?.[0]?.content?.parts?.[0]?.text || "I couldn't generate a response. Please try again.";

    return res.status(200).json({ reply });

  } catch (err) {
    console.error("Chat handler error:", err);
    return res.status(500).json({ error: "Internal server error" });
  }
}
