import { createSupabaseServerClient } from "@/lib/supabase/server";

export async function GET(){
  const supabase=await createSupabaseServerClient();
  const {data:{user}}=await supabase.auth.getUser();
  if(!user)return Response.json({error:"Unauthorized"},{status:401});
  const {data,error}=await supabase.from("birth_profiles")
    .select("id,subject_name,date_of_birth,birth_time,birth_time_precision,birthplace_label,latitude,longitude,timezone,optional_data,created_at")
    .eq("owner_user_id",user.id).order("created_at",{ascending:false});
  if(error)return Response.json({error:error.message},{status:400});
  return Response.json({items:data||[]});
}

export async function POST(request:Request){
  const supabase=await createSupabaseServerClient();
  const {data:{user}}=await supabase.auth.getUser();
  if(!user)return Response.json({error:"Unauthorized"},{status:401});
  const body=await request.json();
  const precision=String(body.birth_time_precision||"exact");
  const payload={
    owner_user_id:user.id,
    subject_name:String(body.subject_name||"").trim(),
    date_of_birth:String(body.date_of_birth||""),
    birth_time:precision==="unknown"?null:String(body.birth_time||""),
    birth_time_precision:precision,
    birthplace_label:String(body.birthplace_label||"").trim(),
    latitude:Number(body.latitude),
    longitude:Number(body.longitude),
    timezone:String(body.timezone||"").trim(),
    optional_data:{
      gender:body.gender||null,
      current_city:body.current_city||null,
      relationship_status:body.relationship_status||null,
      email:body.email||null,
      phone:body.phone||null,
    },
    consent_record:{captured_at:new Date().toISOString(),source:"customer-account"},
  };
  if(!payload.subject_name||!payload.date_of_birth||!payload.birthplace_label||!payload.timezone){
    return Response.json({error:"Required birth-profile fields are missing"},{status:400});
  }
  const {data,error}=await supabase.from("birth_profiles").insert(payload).select().single();
  if(error)return Response.json({error:error.message},{status:400});
  return Response.json(data,{status:201});
}
