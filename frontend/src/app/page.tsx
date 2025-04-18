"use client"

import { useEffect, useState } from "react"
import EditorPanel from "@/components/EditorPanel"
import FileBrowser from "@/components/FileBrowser"
// import CreateNewModal from "@/components/CreateNewModal"
// import SaveAsModal from "@/components/SaveAsModal"
import { Panel, PanelGroup, PanelResizeHandle } from "react-resizable-panels"
import TraceViewer from "@/components/TraceViewer"

export default function EditorPage() {
  const [activeTab, setActiveTab] = useState<"flows" | "prompts">("flows")
  const [selectedFile, setSelectedFile] = useState<string | null>(null)
  const [fileContent, setFileContent] = useState("")
  const [originalContent, setOriginalContent] = useState("")
  const [isDirty, setIsDirty] = useState(false)

  const [traceUrl, setTraceUrl] = useState("")
  const [runId, setRunId] = useState<string | null>(null)

  const rootPath = activeTab === "flows" ? "pipeline_core/flows" : "pipeline_core/prompts"

  // 🧩 Load content on file select
  useEffect(() => {
    if (!selectedFile) return

    //    console.log(data) // Removed undefined variable usage

    fetch(`/api/yaml?path=${encodeURIComponent(selectedFile)}`)
      .then((res) => res.json())
      .then((data) => {
        setFileContent(data.content)
        setIsDirty(false)
      })
      .catch((err) => console.error("Failed to load file:", err))
  }, [selectedFile])

  // 💾 Save handler
  const handleSave = async () => {
    if (!selectedFile) return
    const res = await fetch("/api/save_yaml", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ path: selectedFile, content: fileContent }),
    })
    if (res.ok) {
      console.log("✅ File saved.")
      setIsDirty(false)
    } else {
      console.error("❌ Failed to save")
    }
  }

  // EditorPanel onChange handler:
  const handleEditorChange = (newVal: string) => {
    setFileContent(newVal)
    setIsDirty(newVal !== originalContent)
  }


  // ▶️ Run flow (only if valid .yaml under flows/)
  const handleRun = async () => {
    if (!selectedFile || !selectedFile.endsWith(".yaml") || !selectedFile.includes("flows")) return
    await handleSave()
    const res = await fetch("/api/run_flow", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ flow_path: selectedFile }),
    })
    const data = await res.json()
    if (data.run_id) {
      setRunId(data.run_id)
      setTraceUrl(`http://localhost:23333/v1.0/ui/traces/?run=${data.run_id}`)
    }
  }

  return (
    <main className="h-screen w-screen overflow-hidden">
      {/* Tabs */}
      <div className="p-2 bg-gray-100 flex gap-4">
        {["flows", "prompts"].map((tab) => (
          <button
            key={tab}
            onClick={() => {
              setActiveTab(tab as "flows" | "prompts")
              setSelectedFile(null)
              setFileContent("")
              setRunId(null)
            }}
            className={`px-3 py-1 rounded ${activeTab === tab ? "bg-white shadow font-bold" : "text-gray-600"}`}
          >
            {tab === "flows" ? "🧮 Flows" : "🧠 Prompts"}
          </button>
        ))}
      </div>

      {/* Panels */}
      <PanelGroup direction="horizontal" className="h-full w-full">
        {/* Left: File Browser + Editor */}
        <Panel defaultSize={40} minSize={25} maxSize={60}>
          <div className="flex h-full border-r">
            <div className="w-1/3 border-r">
              <FileBrowser
                root={rootPath}
                selected={selectedFile}
                onSelect={(path) => setSelectedFile(path)}
              />
            </div>
            <div className="w-2/3 h-full">
              <EditorPanel
                filePath={selectedFile}
                content={fileContent}
                onChange={(val) => {
                  setFileContent(val)
                  setIsDirty(true)
                }}
                isDirty={isDirty}
                onSave={handleSave}
                onSaveAs={() => {/* TODO: open SaveAs modal */}}
                onRunFlow={handleRun}
              />
            </div>
          </div>
        </Panel>

        <PanelResizeHandle className="w-2 bg-gray-200 cursor-col-resize" />

        {/* Right: Trace Panel */}
        <Panel defaultSize={60} minSize={30}>
          <div className="h-full p-4 overflow-auto">
            <h2 className="font-bold mb-2">Trace Viewer</h2>
            {runId ? <TraceViewer traceUrl={traceUrl} runId={runId} /> : <p>No run yet.</p>}
          </div>
        </Panel>
      </PanelGroup>
    </main>
  )
}
