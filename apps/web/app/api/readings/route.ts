import { createSupabaseServerClient } from "@/lib/supabase/server";

export async function GET(){
  const supabase=await createSupabaseServerClient();
  const {data:{user}}=await supabase.auth.getUser();
  if(!user)return Response.json({error:"Unauthorized"},{status:401});
  const {data,error}=await supabase.from("reading_sessions")
    .select("id,birth_profile_id,question,life_domain,spread_key,status,published_at,created_at,updated_at")
    .order("created_at",{ascending:false}).limit(100);
  if(error)return Response.json({error:error.message},{status:400});
  return Response.json({items:data||[]});
}

export async function POST(request:Request){
  const supabase=await createSupabaseServerClient();
  const {data:{user}}=await supabase.auth.getUser();
  if(!user)return Response.json({error:"Unauthorized"},{status:401});
  const {data:profile}=await supabase.from("profiles").select("role").eq("id",user.id).maybeSingle();
  if(profile?.role!=="reader")return Response.json({error:"Reader access required"},{status:403});
  const body=await request.json();
  const payload={
    reader_user_id:user.id,
    customer_user_id:body.customer_user_id||null,
    birth_profile_id:String(body.birth_profile_id||""),
    chart_snapshot_id:body.chart_snapshot_id||null,
    question:body.question?String(body.question):null,
    life_domain:body.life_domain?String(body.life_domain):null,
    spread_key:body.spread_key?String(body.spread_key):null,
    status:"draft",
  };
  if(!payload.birth_profile_id)return Response.json({error:"birth_profile_id is required"},{status:400});
  const {data,error}=await supabase.from("reading_sessions").insert(payload).select().single();
  if(error)return Response.json({error:error.message},{status:400});
  return Response.json(data,{status:201});
}
