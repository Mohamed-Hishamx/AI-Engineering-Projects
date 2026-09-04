import { auth } from "@clerk/nextjs/server";
import { redirect } from "next/navigation";
import Dashboard from "./components/Dashboard";

export default async function Home() {
  const { userId } = await auth();

  if (userId) {
    return <Dashboard />;
  }

  return (
    <div className="text-center py-20">
      <h2 className="text-4xl font-bold mb-4">Ask questions about your documents</h2>
      <p className="text-gray-500 text-lg mb-8">
        Upload any PDF or Markdown file and get instant AI-powered answers.
      </p>
      <div className="grid grid-cols-3 gap-6 max-w-2xl mx-auto mt-12">
        <div className="p-6 border rounded-xl">
          <div className="text-2xl mb-2">📄</div>
          <h3 className="font-semibold">Upload Docs</h3>
          <p className="text-gray-500 text-sm">PDF and Markdown supported</p>
        </div>
        <div className="p-6 border rounded-xl">
          <div className="text-2xl mb-2">🔍</div>
          <h3 className="font-semibold">Ask Anything</h3>
          <p className="text-gray-500 text-sm">Get answers from your content</p>
        </div>
        <div className="p-6 border rounded-xl">
          <div className="text-2xl mb-2">✅</div>
          <h3 className="font-semibold">Verified Answers</h3>
          <p className="text-gray-500 text-sm">Sources shown with every answer</p>
        </div>
      </div>
    </div>
  );
}