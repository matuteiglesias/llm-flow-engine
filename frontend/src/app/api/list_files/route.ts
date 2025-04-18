
import { NextRequest, NextResponse } from "next/server"
import fs from "fs"
import path from "path"

export async function GET(req: NextRequest) {
  const root = req.nextUrl.searchParams.get("root")


  if (!root || root.includes("..")) {
    return NextResponse.json({ error: "Invalid root path" }, { status: 400 })
  }

  // 👇 FIX: resolve from project root (one level up from frontend/)
  const baseDir = path.resolve(process.cwd(), "..") // parent of /frontend
  const dirPath = path.join(baseDir, root)

  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true })
    const files = entries
      .filter((entry) => entry.isFile())
      .map((entry) => entry.name)

    return NextResponse.json({ files })
  } catch (err) {
    console.error("🛑 Failed to read directory:", err)
    return NextResponse.json({ error: "Could not read directory" }, { status: 500 })
  }
}