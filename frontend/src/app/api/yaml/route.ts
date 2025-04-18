// src/app/api/yaml/route.ts

import { NextRequest, NextResponse } from "next/server"
import fs from "fs"
import path from "path"

export async function GET(req: NextRequest) {
  const filePath = req.nextUrl.searchParams.get("path")

  if (!filePath || filePath.includes("..")) {
    return NextResponse.json({ error: "Invalid file path" }, { status: 400 })
  }

  const baseDir = path.resolve(process.cwd(), "..") // go up from /frontend
  const fullPath = path.join(baseDir, filePath)

  try {
    const content = fs.readFileSync(fullPath, "utf8")
    return NextResponse.json({ content }) // ✅ Exactly what your useEffect expects
  } catch (err) {
    console.error("🛑 Failed to read file:", err)
    return NextResponse.json({ error: "File not found or unreadable" }, { status: 500 })
  }
}
