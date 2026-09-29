export type EvidenceType="natal"|"dasha"|"transit"|"card"|"combination"|"reader_note"|"source";
export interface EvidenceNode{type:EvidenceType;key:string;summary:string;confidence:number;payload?:unknown}
export interface SynthesisInput{question:string;lifeDomain?:string;evidence:EvidenceNode[]}
export interface SynthesisPacket{question:string;lifeDomain?:string;highConfidence:EvidenceNode[];supporting:EvidenceNode[];cautions:string[]}

const DOMAIN_RULES: Record<string,string[]> = {
  career:["job","career","business","work","promotion","salary","company"],
  relationship:["love","marriage","partner","relationship","spouse"],
  finance:["money","finance","investment","loan","income","wealth"],
  family:["family","parent","mother","father","child","children"],
  wellbeing:["health","wellbeing","stress","sleep","energy"],
  spiritual:["spiritual","dharma","meaning","purpose","practice"],
};

export function classifyLifeDomain(question:string):string{
  const q=question.toLowerCase();
  for(const [domain,terms] of Object.entries(DOMAIN_RULES)) if(terms.some(t=>q.includes(t))) return domain;
  return "general";
}

export function buildSynthesisPacket(input:SynthesisInput):SynthesisPacket{
  const normalized=input.evidence.map(e=>({...e,confidence:Math.max(0,Math.min(1,e.confidence))}));
  return {
    question:input.question,
    lifeDomain:input.lifeDomain||classifyLifeDomain(input.question),
    highConfidence:normalized.filter(e=>e.confidence>=0.8),
    supporting:normalized.filter(e=>e.confidence<0.8),
    cautions:[
      "Astrology and cards are interpretive tools, not guarantees of future outcomes.",
      "Do not convert uncertainty into a precise prediction that the evidence does not support.",
      "Any statement about natal placements must be traceable to deterministic chart evidence."
    ]
  };
}

export function systemPromptForReading(packet:SynthesisPacket):string{
  return [
    "You are the 108-Jeevan synthesis layer, not an astrology calculator.",
    "Use only the supplied evidence packet. Never invent a planet, house, nakshatra, dasha, transit, card, or date.",
    "Separate deterministic Jyotisha evidence from original 108-Jeevan card interpretation.",
    "Use calibrated language: indicators, themes, windows, tensions, supports; never deterministic guarantees.",
    "If evidence conflicts, explain the conflict instead of forcing one answer.",
    "Return sections: Answer, Astrological Evidence, Cards, Combined Reading, Timing, Marga, Uncertainty.",
    JSON.stringify(packet)
  ].join("\n");
}
