"use client"
import { useEffect, useState } from "react"
import YamlEditor from "@/components/YamlEditor"
import TraceViewer from "@/components/TraceViewer"
import OutputPanel from "@/components/OutputPanel"
import { runFlow } from "@/lib/api"
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels";


export default function Home() {
  const [yaml, setYaml] = useState("")
  const [output, setOutput] = useState<string | null>(null)
  const [traceUrl, setTraceUrl] = useState("")
  const [runId, setRunId] = useState<string | null>(null)

  const flowPath = "pipeline_core/flows/hello.yaml" // 🧠 Avoid magic strings

  // 🧩 Load YAML from file on first load
  useEffect(() => {
    if (!flowPath) return;
    console.log("📂 Fetching YAML for path:", flowPath);
  
    fetch(`/api/yaml?path=${encodeURIComponent(flowPath)}`) // ✅ goes through Next.js proxy
      .then((res) => res.json())
      .then((data) => setYaml(data.content))
      .catch((err) => console.error("Failed to load YAML:", err));
  }, []);

  // 🧠 Save to backend
  const handleSave = async () => {
    const res = await fetch("/api/save_yaml", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path: flowPath, content: yaml }),
    })

    if (res.ok) {
      console.log("✅ YAML saved.")
    } else {
      console.error("❌ Failed to save YAML")
    }
  }

  // ▶️ Trigger run and update output + trace
  const handleRun = async () => {
    // Optionally save before running
    await handleSave()

    const response = await fetch("/api/run_flow", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ flow_path: flowPath }),
    })

    const data = await response.json()
    setOutput(JSON.stringify(data.output, null, 2))
    setRunId(data.run_id)
    if (data.run_id) {
      setTraceUrl(`http://localhost:23333/v1.0/ui/traces/?run=${data.run_id}`)
    }
  }

return (
  <main className="h-screen w-screen overflow-hidden">
  <PanelGroup direction="horizontal" className="h-full w-full">
    {/* YAML Panel */}
    <Panel defaultSize={30} minSize={20} maxSize={50}>
      <div className="h-full p-4 border-r flex flex-col">
        <h2 className="font-bold mb-2">YAML Editor</h2>
        <YamlEditor yaml={yaml} onChange={setYaml} />
        <div className="flex gap-2 mt-4">
          <button
            onClick={handleSave}
            className="p-2 bg-green-600 text-white rounded"
          >
            💾 Save
          </button>
          <button
            onClick={handleRun}
            className="p-2 bg-blue-600 text-white rounded"
          >
            ▶️ Run
          </button>
        </div>
      </div>
    </Panel>

    {/* Draggable Handle */}
    <PanelResizeHandle className="w-2 bg-gray-200 cursor-col-resize" />

    {/* Trace Viewer Panel */}
    <Panel defaultSize={70} minSize={30}>
      <div className="h-full p-4 overflow-auto">
        <h2 className="font-bold mb-2">Trace Viewer</h2>
        <TraceViewer traceUrl={traceUrl} runId={runId || ""} />
      </div>
    </Panel>
  </PanelGroup>
    </main>
  );
}



// "use client"
// import { useEffect, useState } from "react";
// import YamlEditor from "@/components/YamlEditor"
// import TraceViewer from "@/components/TraceViewer"
// import OutputPanel from "@/components/OutputPanel"
// import { runFlow } from "@/lib/api"


// export default function Home() {
//   const [yaml, setYaml] = useState("");
//   // const [yaml, setYaml] = useState(`flow_path: pipeline_core/flows/hello.yaml`)
//   const [output, setOutput] = useState<string | null>(null)
//   const [traceUrl, setTraceUrl] = useState("")
//   const [runId, setRunId] = useState<string | null>(null);

//   useEffect(() => {
//     fetch("/api/yaml?path=pipeline_core/flows/hello.yaml")
//       .then((res) => res.json())
//       .then((data) => setYaml(data.content));
//   }, []);

//   const handleRun = async () => {
//     const result = await runFlow("pipeline_core/flows/hello.yaml")
//     setOutput(result.output)
//     if (result.run_id) {
//       setTraceUrl(`http://localhost:23333/v1.0/ui/traces/?run=${result.run_id}`)
//     }

//     const response = await fetch("/api/run_flow", {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ flow_path: "pipeline_core/flows/hello.yaml" }),
//     });
    
//     const data = await response.json();
//     setOutput(JSON.stringify(data.output, null, 2));  // Update right pane
//     setRunId(data.run_id);  // 🔥 This makes the iframe visible!
//   }

//   return (
//     <div className="grid grid-cols-3 h-screen">
//       <div className="border-r p-4 flex flex-col">
//         <h2 className="font-bold mb-2">YAML Editor</h2>
//         <YamlEditor yaml={yaml} onChange={(val) => setYaml(val)} />

//         <button
//     onClick={async () => {
//       await fetch("/api/save_yaml", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({
//           path: "pipeline_core/flows/hello.yaml",
//           content: yaml,
//         }),
//       });
//       console.log("✅ YAML saved.");
//     }}
//     className="p-2 bg-green-500 text-white rounded"
//   >
//     💾 Save
//   </button>

//         <button
//           onClick={handleRun}
//           className="mt-4 p-2 bg-blue-500 text-white rounded"
//         >
//           ▶️ Run
//         </button>


//       </div>

//       <div className="border-r p-4">
//         <h2 className="font-bold mb-2">Trace Viewer</h2>
//         <TraceViewer traceUrl={traceUrl} runId={runId || ""} />
//       </div>

//       <div className="p-4">
//         <h2 className="font-bold mb-2">Output</h2>
//         <OutputPanel output={output} />
//       </div>
//     </div>
//   )
// }