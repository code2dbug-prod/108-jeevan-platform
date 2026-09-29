import { astrologyPost } from "@/lib/astrology";
export async function POST(request:Request){
  try{return Response.json(await astrologyPost("/v1/places/timezone",await request.json()))}
  catch(error){return Response.json({error:error instanceof Error?error.message:"Unknown error"},{status:502})}
}
