import { ReaderConsole } from "./reader-console";
export default function ReaderPage(){return <main className="shell"><p className="eyebrow">PRIVATE READER WORKSPACE</p><h1>Birth chart console</h1><p className="lede">Enter verified birth data. Exact time produces a full base chart; unknown time triggers an uncertainty sweep instead of a fabricated noon chart.</p><ReaderConsole/></main>}
