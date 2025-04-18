"use client"

import { useEffect, useState } from "react"

type Props = {
  root: string // e.g. "pipeline_core/flows"
  selected: string | null
  onSelect: (path: string) => void
}

export default function FileBrowser({ root, selected, onSelect }: Props) {
  const [files, setFiles] = useState<string[]>([])
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetch(`/api/list_files?root=${encodeURIComponent(root)}`)
      .then((res) => res.json())
      .then((data) => {
        if (data.files) setFiles(data.files)
        else setError("Unexpected response format")
      })
      .catch((err) => {
        console.error("Error fetching files:", err)
        setError("Failed to load file list.")
      })
  }, [root])

  return (
    <div className="h-full flex flex-col text-sm">
      <div className="flex items-center justify-between px-3 py-2 border-b bg-gray-50">
        <strong className="text-gray-700">📁 {root.split("/").pop()}</strong>
        <button
          className="text-xs text-blue-600 hover:underline"
          onClick={() => alert("TODO: open CreateNewModal")}
        >
          + New
        </button>
      </div>

      {error ? (
        <div className="text-red-500 p-2">{error}</div>
      ) : (
        <ul className="flex-1 overflow-auto px-2 py-1">
          {files.map((file) => {
            const fullPath = `${root}/${file}`
            const isActive = fullPath === selected

            return (
              <li
                key={file}
                onClick={() => onSelect(fullPath)}
                className={`cursor-pointer px-2 py-1 rounded mb-1 ${
                  isActive
                    ? "bg-blue-100 text-blue-800 font-semibold"
                    : "hover:bg-gray-100"
                }`}
              >
                📄 {file}
              </li>
            )
          })}
        </ul>
      )}
    </div>
  )
}
