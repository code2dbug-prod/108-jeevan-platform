"use client";
import { FormEvent, useState } from "react";
import { createSupabaseBrowserClient } from "@/lib/supabase/client";

export default function LoginPage(){
  const [message,setMessage]=useState("");
  const [loading,setLoading]=useState(false);

  async function passwordLogin(e:FormEvent<HTMLFormElement>){
    e.preventDefault();
    setLoading(true);
    setMessage("");
    const f=new FormData(e.currentTarget);
    const email=String(f.get("email")||"").trim();
    const password=String(f.get("password")||"");
    const supabase=createSupabaseBrowserClient();
    const {error}=await supabase.auth.signInWithPassword({email,password});
    if(error){
      setMessage(error.message);
      setLoading(false);
      return;
    }
    window.location.assign("/reader");
  }

  async function sendMagicLink(){
    const emailInput=document.querySelector<HTMLInputElement>('input[name="email"]');
    const email=(emailInput?.value||"").trim();
    if(!email){
      setMessage("Enter your email first.");
      return;
    }
    setLoading(true);
    setMessage("");
    const supabase=createSupabaseBrowserClient();
    const {error}=await supabase.auth.signInWithOtp({
      email,
      options:{emailRedirectTo:window.location.origin+"/auth/callback?next=/reader"}
    });
    setMessage(error?error.message:"Check your email for the secure sign-in link.");
    setLoading(false);
  }

  return <main className="shell">
    <p className="eyebrow">ACCOUNT ACCESS</p>
    <h1>Sign in</h1>
    <form className="panel form narrow" onSubmit={passwordLogin}>
      <label>Email<input name="email" type="email" required autoComplete="email"/></label>
      <label>Password<input name="password" type="password" required autoComplete="current-password"/></label>
      <button type="submit" disabled={loading}>{loading?"Signing in...":"Sign in with password"}</button>
      <button type="button" className="secondary" onClick={sendMagicLink} disabled={loading}>Send magic link instead</button>
      {message&&<p>{message}</p>}
    </form>
  </main>
}
