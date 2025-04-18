// pages/api/list_files.ts

import fs from "fs"
import path from "path"
import type { NextApiRequest, NextApiResponse } from "next"

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const root = req.query.root as string
  
  console.log("📥 API Request for root =", root)

  if (!root || root.includes("..")) {
    return res.status(400).json({ error: "Invalid root path" })
  }

  const dirPath = path.join(process.cwd(), root)
  

  try {
    const entries = fs.readdirSync(dirPath, { withFileTypes: true })
    const files = entries
      .filter((entry) => entry.isFile())
      .map((entry) => entry.name)

    res.status(200).json({ files })
  } catch (err) {
    console.error("🛑 Failed to read directory:", err)
    res.status(500).json({ error: "Could not read directory" })
  }
}
