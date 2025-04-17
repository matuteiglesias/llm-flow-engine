"use client"

import { useEffect, useRef, useState } from "react"
import Editor from "@monaco-editor/react"

type Props = {
  yaml: string
  onChange: (val: string) => void
  filePath?: string
}

export default function YamlEditor({ yaml, onChange, filePath = "pipeline_core/flows/hello.yaml" }: Props) {
  const [value, setValue] = useState(yaml)
  const [isDirty, setIsDirty] = useState(false)
  const initialValueRef = useRef(yaml)

  useEffect(() => {
    setValue(yaml)
    initialValueRef.current = yaml
    setIsDirty(false)
  }, [yaml])

  const handleEditorChange = (val: string | undefined) => {
    if (val !== undefined) {
      setValue(val)
      onChange(val)
      setIsDirty(val !== initialValueRef.current)
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex justify-between items-center text-sm mb-2 px-1">
        <span className="text-gray-700 font-mono">📄 {filePath}</span>
        <span className={`text-xs px-2 py-0.5 rounded ${isDirty ? "bg-yellow-300 text-black" : "bg-green-200 text-green-900"}`}>
          {isDirty ? "Unsaved changes" : "Saved"}
        </span>
      </div>
      <div className="flex-grow border">
        <Editor
          height="100%"
          language="yaml"
          value={value}
          onChange={handleEditorChange}
          theme="vs-light"
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            fontFamily: "monospace",
            automaticLayout: true,
          }}
        />
      </div>
    </div>
  )
}
