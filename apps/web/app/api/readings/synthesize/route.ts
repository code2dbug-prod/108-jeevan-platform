import { buildSynthesisPacket, systemPromptForReading, type EvidenceNode } from "@jeevan/interpretation";

export async function POST(request: Request) {
  const body = await request.json();
  if (typeof body.question !== "string" || !Array.isArray(body.evidence)) {
    return Response.json({ error: "question and evidence are required" }, { status: 400 });
  }
  const packet = buildSynthesisPacket({
    question: body.question,
    lifeDomain: body.lifeDomain,
    evidence: body.evidence as EvidenceNode[],
  });
  const key = process.env.OPENAI_API_KEY;
  if (!key) return Response.json({ packet, synthesis: null, mode: "packet-only" });

  const response = await fetch("https://api.openai.com/v1/responses", {
    method: "POST",
    headers: { "content-type": "application/json", authorization: `Bearer ${key}` },
    body: JSON.stringify({
      model: process.env.OPENAI_MODEL || "gpt-5.6",
      input: systemPromptForReading(packet),
    }),
  });
  if (!response.ok) {
    const text = await response.text();
    return Response.json({ error: "AI synthesis failed", detail: text, packet }, { status: 502 });
  }
  const data = await response.json();
  const text = data.output_text || data.output?.flatMap((x:any)=>x.content||[]).find((x:any)=>x.type==="output_text")?.text || "";
  return Response.json({ packet, synthesis: text, mode: "ai" });
}
