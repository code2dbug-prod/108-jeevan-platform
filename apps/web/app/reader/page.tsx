import { redirect } from "next/navigation";
import { createSupabaseServerClient } from "@/lib/supabase/server";
import { ReaderConsole } from "./reader-console";

export default async function ReaderPage(){
  const supabase=await createSupabaseServerClient();
  const {data:{user}}=await supabase.auth.getUser();

  if(!user)redirect("/login");

  const {data:profile,error}=await supabase
    .from("profiles")
    .select("role")
    .eq("id",user.id)
    .maybeSingle();

  if(error||profile?.role!=="reader")redirect("/account");

  return <main className="shell">
    <p className="eyebrow">PRIVATE READER WORKSPACE</p>
    <h1>Birth chart console</h1>
    <p className="lede">Enter verified birth data. Exact time produces a full base chart; unknown time triggers an uncertainty sweep instead of a fabricated noon chart.</p>
    <ReaderConsole/>
  </main>
}
