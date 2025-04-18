type Props = {
    filePath: string
    isDirty: boolean
    onSave: () => void
    onSaveAs: () => void
    onRunFlow?: () => void // optional
  }
  
  export default function EditorToolbar({
    filePath,
    isDirty,
    onSave,
    onSaveAs,
    onRunFlow,
  }: Props) {
    const isYaml = filePath.endsWith(".yaml")
    const isFlow = filePath.includes("flows")
  
    return (
      <div className="flex items-center justify-between px-3 py-2 bg-gray-50 border-b">
        {/* File Info */}
        <div className="flex items-center gap-2 font-mono text-sm text-gray-700">
          📄 {filePath}
          <span
            className={`text-xs px-2 py-0.5 rounded ${
              isDirty ? "bg-yellow-300 text-black" : "bg-green-200 text-green-900"
            }`}
          >
            {isDirty ? "Unsaved changes" : "Saved"}
          </span>
        </div>
  
        {/* Action Buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={onSave}
            className="bg-green-600 text-white px-3 py-1 rounded text-sm"
          >
            💾 Save
          </button>
          <button
            onClick={onSaveAs}
            className="bg-gray-300 text-gray-800 px-3 py-1 rounded text-sm"
          >
            📝 Save As
          </button>
          {isYaml && isFlow && onRunFlow && (
            <button
              onClick={onRunFlow}
              className="bg-blue-600 text-white px-3 py-1 rounded text-sm"
            >
              ▶️ Run
            </button>
          )}
        </div>
      </div>
    )
  }
  