"use client"

import { useEffect, useState } from "react"
import yaml from "js-yaml"

type Props = {
  filePath: string
  content: string
}

export default function ValidationBanner({ filePath, content }: Props) {
  const [isValid, setIsValid] = useState(true)
  const [errorMsg, setErrorMsg] = useState<string | null>(null)

  useEffect(() => {
    const isYaml = filePath.endsWith(".yaml")
    const isPrompty = filePath.endsWith(".prompty")

    if (isYaml) {
      try {
        yaml.load(content)
        setIsValid(true)
        setErrorMsg(null)
      } catch (err: any) {
        setIsValid(false)
        setErrorMsg(err.message)
      }
    } else if (isPrompty) {
      // For now, just check it's not empty — future: validate placeholders
      if (content.trim().length === 0) {
        setIsValid(false)
        setErrorMsg("Prompt file is empty.")
      } else {
        setIsValid(true)
        setErrorMsg(null)
      }
    } else {
      setIsValid(true)
      setErrorMsg(null)
    }
  }, [content, filePath])

  if (isValid) {
    return (
      <div className="text-sm px-4 py-1 bg-green-50 text-green-800 border-b border-green-300">
        ✅ File looks good.
      </div>
    )
  }

  return (
    <div className="text-sm px-4 py-1 bg-red-50 text-red-800 border-b border-red-300">
      ❌ Validation failed: <span className="font-mono">{errorMsg}</span>
    </div>
  )
}
