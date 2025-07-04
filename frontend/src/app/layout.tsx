import '../styles/globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import AuthProvider from '@/components/AuthProvider'  // ✅ Import the AuthProvider

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'Roommate Matcher',
  description: 'Find your ideal roommate at Rishihood University',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AuthProvider> {/* 👈 Wrap entire app */}
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
