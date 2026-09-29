import { redirect } from "next/navigation";
import { createSupabaseServerClient } from "@/lib/supabase/server";

export default async function AccountPage(){
  const supabase=await createSupabaseServerClient();
  const {data:{user}}=await supabase.auth.getUser();
  if(!user)redirect("/login");
  const {data:profile}=await supabase.from("profiles").select("full_name,role,email,phone,current_city,relationship_status").eq("id",user.id).maybeSingle();
  const {data:birthProfiles}=await supabase.from("birth_profiles").select("id,subject_name,date_of_birth,birth_time_precision,birthplace_label,created_at").eq("owner_user_id",user.id).order("created_at",{ascending:false});
  return <main className="shell"><p className="eyebrow">CUSTOMER ACCOUNT</p><h1>{profile?.full_name||"Your account"}</h1><section className="grid"><article className="panel"><h2>Profile</h2><p>{user.email}</p><p>Role: {profile?.role||"customer"}</p></article><article className="panel"><h2>Birth profiles</h2>{birthProfiles?.length?<ul>{birthProfiles.map(p=><li key={p.id}>{p.subject_name} — {p.date_of_birth} — {p.birth_time_precision}</li>)}</ul>:<p>No birth profile saved yet.</p>}</article></section></main>
}
