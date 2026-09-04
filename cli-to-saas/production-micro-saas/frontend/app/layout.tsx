import type { Metadata } from "next";
import { Geist } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";
import { auth } from "@clerk/nextjs/server";
import { SignInButton, UserButton } from "@clerk/nextjs";
import "./globals.css";

const geist = Geist({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Docs Q&A",
  description: "Ask questions about your documents",
};

async function Navbar() {
  const { userId } = await auth();
  return (
    <nav className="flex justify-between items-center p-4 border-b">
      <h1 className="text-xl font-bold">Docs Q&A</h1>
      <div>
        {userId ? (
          <UserButton />
        ) : (
          <SignInButton mode="modal">
            <button className="bg-black text-white px-4 py-2 rounded-lg">
              Sign In
            </button>
          </SignInButton>
        )}
      </div>
    </nav>
  );
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={geist.className}>
          <Navbar />
          <main className="max-w-4xl mx-auto p-6">{children}</main>
        </body>
      </html>
    </ClerkProvider>
  );
}