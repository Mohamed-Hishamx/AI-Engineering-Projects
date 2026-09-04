"use client";

import { useState } from "react";
import { useAuth } from "@clerk/nextjs";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Dashboard() {
  const { userId } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<string | null>(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState<string | null>(null);
  const [sources, setSources] = useState<any[]>([]);
  const [evaluation, setEvaluation] = useState<any>(null);
  const [asking, setAsking] = useState(false);

  async function handleUpload() {
    if (!file) return;
    setUploading(true);
    setUploadResult(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setUploadResult(`✅ Uploaded "${data.filename}" — ${data.chunks_stored} chunks stored.`);
    } catch (e) {
      setUploadResult("❌ Upload failed. Is the backend running?");
    } finally {
      setUploading(false);
    }
  }

  async function handleAsk() {
    if (!question.trim()) return;
    setAsking(true);
    setAnswer(null);
    setSources([]);
    setEvaluation(null);

    try {
      const res = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, user_id: userId || "anonymous" }),
      });
      const data = await res.json();
      setAnswer(data.answer);
      setSources(data.sources || []);
      setEvaluation(data.evaluation);
    } catch (e) {
      setAnswer("❌ Request failed. Is the backend running?");
    } finally {
      setAsking(false);
    }
  }

  return (
    <div className="space-y-8">
      {/* Upload Section */}
      <div className="border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">📄 Upload Document</h2>
        <div className="flex gap-3 items-center">
          <input
            type="file"
            accept=".pdf,.md,.txt,.markdown"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="flex-1 border rounded-lg p-2 text-sm"
          />
          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className="bg-black text-white px-4 py-2 rounded-lg disabled:opacity-50"
          >
            {uploading ? "Uploading..." : "Upload"}
          </button>
        </div>
        {uploadResult && (
          <p className="mt-3 text-sm text-gray-600">{uploadResult}</p>
        )}
      </div>

      {/* Ask Section */}
      <div className="border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">🔍 Ask a Question</h2>
        <div className="flex gap-3">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleAsk()}
            placeholder="What is the refund policy?"
            className="flex-1 border rounded-lg p-2 text-sm"
          />
          <button
            onClick={handleAsk}
            disabled={!question.trim() || asking}
            className="bg-black text-white px-4 py-2 rounded-lg disabled:opacity-50"
          >
            {asking ? "Thinking..." : "Ask"}
          </button>
        </div>

        {answer && (
          <div className="mt-4 space-y-4">
            <div className="bg-gray-50 rounded-lg p-4">
              <h3 className="font-semibold mb-2">Answer</h3>
              <p className="text-gray-700 text-sm">{answer}</p>
            </div>

            {sources.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2 text-sm">Sources</h3>
                <div className="space-y-2">
                  {sources.map((s, i) => (
                    <div key={i} className="bg-gray-50 rounded p-3 text-xs text-gray-600">
                      <span className="font-medium">Chunk {s.chunk_id}</span> — {s.preview}...
                    </div>
                  ))}
                </div>
              </div>
            )}

            {evaluation && evaluation.faithfulness > 0 && (
              <div className="flex gap-4 text-sm">
                <span className="bg-green-100 text-green-700 px-3 py-1 rounded-full">
                  Faithfulness: {evaluation.faithfulness}/5
                </span>
                <span className="bg-blue-100 text-blue-700 px-3 py-1 rounded-full">
                  Relevance: {evaluation.relevance}/5
                </span>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}