export default function TraceViewer({ traceUrl, runId }: { traceUrl: string; runId: string }) {
    return (
      <>
        {runId ? (
          <iframe
            className="w-full h-full"
            src={`http://localhost:23333/v1.0/ui/traces?collection=${runId}`}
          />
        ) : (
          <div className="p-4 text-gray-500">No trace yet</div>
        )}
      </>
    );
}
  