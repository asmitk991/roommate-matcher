'use client'
import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();
  return (
    <main className="min-h-screen bg-gradient-to-br from-[#f0f4ff] to-white flex items-center justify-center px-4">
      <div className="max-w-4xl w-full flex flex-col md:flex-row items-center gap-12">
        {/* Left: Illustration */}
        <div className="relative w-full md:w-1/2 h-[300px] md:h-[400px]">
          <Image
            src="/roommate.jpg"
            alt="Roommate Illustration"
            fill
            className="object-contain"
            priority
          />
        </div>

        {/* Right: Content */}
        <div className="w-full md:w-1/2 space-y-6 text-center md:text-left">
          <h1 className="text-4xl font-extrabold text-gray-800 leading-tight">
            Find your <span className="text-blue-600">ideal roommate</span>
          </h1>
          <p className="text-gray-600 text-lg">
            Discover your perfect roommate match based on <strong>sleep patterns</strong>,
            <strong> cleanliness</strong>, and <strong>shared interests</strong>. No more awkward pairings!
          </p>
          {/* 🔀 Two CTA Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center md:justify-start">
            <button
              onClick={() => router.push('/otp')}
              className="px-6 py-3 bg-blue-600 text-white rounded-xl text-lg font-medium hover:bg-blue-700 transition shadow-md"
            >
              ✍️ Sign Up
            </button>
            <button
              onClick={() => router.push('/login')}
              className="px-6 py-3 bg-gray-100 text-blue-600 border border-blue-600 rounded-xl text-lg font-medium hover:bg-blue-50 transition shadow-md"
            >
              🔐 Log In
            </button>
          </div>

          <p className="text-sm text-gray-500 pt-4">
            Built with ❤️ using <span className="text-blue-500 font-semibold">Next.js</span> & <span className="text-teal-500 font-semibold">TailwindCSS</span>
          </p>
        </div>
      </div>
    </main>
  );
}
