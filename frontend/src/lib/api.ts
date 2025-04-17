export async function runFlow(yamlPath: string) {
  const res = await fetch("http://localhost:8000/api/run_flow", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ flow_path: yamlPath })
  })
  return await res.json()
}
