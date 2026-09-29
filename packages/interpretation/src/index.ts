export type EvidenceType="natal"|"dasha"|"transit"|"card"|"combination"|"reader_note"|"source";
export interface EvidenceNode{type:EvidenceType;key:string;summary:string;confidence:number;payload?:unknown}
export interface SynthesisInput{question:string;lifeDomain?:string;evidence:EvidenceNode[]}
export interface SynthesisPacket{question:string;lifeDomain?:string;highConfidence:EvidenceNode[];supporting:EvidenceNode[];cautions:string[]}

export function buildSynthesisPacket(input:SynthesisInput):SynthesisPacket{
  const normalized=input.evidence.map(e=>({...e,confidence:Math.max(0,Math.min(1,e.confidence))}));
  return {question:input.question,lifeDomain:input.lifeDomain,highConfidence:normalized.filter(e=>e.confidence>=0.8),supporting:normalized.filter(e=>e.confidence<0.8),cautions:["Astrology and cards are interpretive tools, not guarantees of future outcomes.","Do not convert uncertainty into a precise prediction that the evidence does not support."]}
}
