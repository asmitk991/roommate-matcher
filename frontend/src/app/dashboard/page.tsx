'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import api from '@/utils/api'

type UserData = {
    email: string;
    has_submitted_form: boolean;
  };
export default function DashboardPage() {
  const [userData, setUserData] = useState<UserData | null>(null);
  const [loading, setLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const token = localStorage.getItem('token')
    if (!token) {
      router.push('/login')
      return
    }

    api.get('/api/auth/me/', {
      headers: { Authorization: token },
    })
      .then(res => {
        setUserData(res.data)
        setLoading(false)
      })
      .catch(() => {
        localStorage.removeItem('token')
        router.push('/login')
      })
  }, [])

  if (loading) return <div className="text-center mt-10">Loading...</div>

  const handleFillFormClick = () => {
    if (userData?.has_submitted_form) {
      alert('✅ Your profile is already filled.');
    } else {
      router.push('/form');
    }
  };

  const handleCheckMatchClick = () => {
    if (!userData?.has_submitted_form) {
      alert('❌ Please complete your profile first by filling the form.');
    } else {
      router.push('/match');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-purple-200 flex items-center justify-center px-4">
      <div className="max-w-xl w-full bg-white p-8 rounded-xl shadow-md space-y-4">
        <h1 className="text-2xl font-bold text-center">👋 Welcome to your Dashboard</h1>
        <p><strong>Email:</strong> {userData?.email}</p>
        <p><strong>Form Submitted:</strong> {userData?.has_submitted_form ? '✅ Yes' : '❌ No'}</p>

        <div className="flex justify-around mt-4">
          <button
            className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            onClick={handleFillFormClick}
          >
            📝 Fill Form
          </button>
          <button
            className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
            onClick={handleCheckMatchClick}
          >
            🔍 Check Match
          </button>
        </div>
      </div>
    </div>
  )
}
