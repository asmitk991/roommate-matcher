'use client';

import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import api from '@/utils/api';

export default function SetPasswordPage() {
  const router = useRouter();
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');

  useEffect(() => {
    const storedEmail = localStorage.getItem('verifiedEmail');
    if (!storedEmail) {
      router.push('/otp');
    } else {
      setEmail(storedEmail);
    }
  }, []);

  const handleSubmit = async () => {
    if (password !== confirmPassword) {
      setMessage('❌ Passwords do not match.');
      return;
    }

    try {
      const res = await api.post('/api/set-password/', {
        email,
        password,
      });

      if (res.status === 200) {
        localStorage.setItem('token', res.data.token);
        setMessage('✅ Password set successfully! Redirecting...');
        setTimeout(() => {
          router.push('/dashboard');
        }, 1000);
      } else {
        setMessage('❌ Something went wrong.');
      }
    } catch (err) {
      setMessage('❌ Failed to set password.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-200 to-blue-300 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white p-8 rounded-xl shadow-lg space-y-6">
        <h1 className="text-2xl font-bold text-center">🔒 Set Your Password</h1>

        <input
          type="password"
          placeholder="Enter Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg"
        />

        <input
          type="password"
          placeholder="Confirm Password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg"
        />

        <button
          onClick={handleSubmit}
          className="w-full py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700"
        >
          ✅ Set Password
        </button>

        {message && <p className="text-center text-sm text-gray-700">{message}</p>}
      </div>
    </div>
  );
}
