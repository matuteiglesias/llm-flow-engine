export default function OutputPanel({ output }: { output: any }) {
    return (
      <pre className="w-full h-full overflow-auto bg-gray-100 p-4 text-sm">
        {JSON.stringify(output, null, 2)}
      </pre>
    )
  }
  