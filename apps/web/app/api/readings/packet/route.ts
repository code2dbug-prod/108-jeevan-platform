import { buildSynthesisPacket, type EvidenceNode } from "@jeevan/interpretation";

export async function POST(request:Request){
  const body=await request.json();
  if(typeof body.question!=="string"||!Array.isArray(body.evidence))return Response.json({error:"question and evidence are required"},{status:400});
  return Response.json(buildSynthesisPacket({question:body.question,lifeDomain:body.lifeDomain,evidence:body.evidence as EvidenceNode[]}));
}
