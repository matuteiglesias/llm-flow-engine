"use client"

import dynamic from "next/dynamic"
import EditorToolbar from "./EditorToolbar"
import ValidationBanner from "./ValidationBanner"
import { useEffect, useRef } from "react"

const YamlEditor = dynamic(() => import("./YamlEditor"), { ssr: false })

type Props = {
  filePath: string | null
  content: string
  onChange: (val: string) => void
  onSave: () => void
  onSaveAs: () => void
  onRunFlow?: () => void
  isDirty: boolean
}

export default function EditorPanel({
  filePath,
  content,
  onChange,
  onSave,
  onSaveAs,
  onRunFlow,
  isDirty,
}: Props) {
  const lastContentRef = useRef(content)

  useEffect(() => {
    lastContentRef.current = content
  }, [content])

  if (!filePath) {
    return (
      <div className="h-full flex items-center justify-center text-gray-400">
        Select a file to start editing
      </div>
    )
  }

  return (
    <div className="flex flex-col h-full">
      {/* 🧠 Toolbar */}
      <EditorToolbar
        filePath={filePath}
        isDirty={isDirty}
        onSave={onSave}
        onSaveAs={onSaveAs}
        onRunFlow={onRunFlow}
      />

      {/* ✅ Validation */}
      <ValidationBanner filePath={filePath} content={content} />

      {/* 📝 Monaco Editor */}
      <div className="flex-grow border-t">
        <YamlEditor
          filePath={filePath}
          value={content}
          onChange={onChange}
        />
      </div>
    </div>
  )
}
