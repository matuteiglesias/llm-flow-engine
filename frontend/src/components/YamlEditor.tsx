"use client"

import Editor from "@monaco-editor/react"
import { useEffect, useRef } from "react"

type Props = {
  filePath: string
  value: string
  onChange: (val: string) => void
}

export default function YamlEditor({ value, onChange, filePath }: Props) {
  const language = filePath.endsWith(".prompty") ? "plaintext" : "yaml"

  // 🧠 Track the original value to compute "dirty" in the parent (if needed)
  const initialValueRef = useRef<string>(value)

  // Optional: Reset the ref if filePath changes (new file)
  useEffect(() => {
    initialValueRef.current = value
  }, [filePath])

  return (
    <Editor
      height="100%"
      language={language}
      value={value}
      onChange={(val) => {
        if (val !== undefined) {
          onChange(val) // delegate dirty tracking to parent
        }
      }}
      theme="vs-light"
      options={{
        fontSize: 14,
        minimap: { enabled: false },
        fontFamily: "monospace",
        automaticLayout: true,
      }}
    />
  )
}
