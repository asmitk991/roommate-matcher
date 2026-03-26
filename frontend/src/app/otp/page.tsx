'use client';

import { useState, useEffect } from 'react';

import api from '@/utils/api';

export default function OTPVerificationPage() {
  const [email, setEmail] = useState('');
  const [otpSent, setOtpSent] = useState(false);
  const [otp, setOtp] = useState('');
  const [message, setMessage] = useState('');

  const sendOtp = async () => {
    setMessage(""); // Clear old message
  
    try {
      const res = await api.post('/api/send-otp/', { email });
      if (res.status === 200) {
        setOtpSent(true);
        setMessage('✅ OTP sent successfully. Check your email.');
      }
    } catch (error: any) {
      const data = error.response?.data || {};
      if (data.error === 'Account already exists. Please log in.') {
        setMessage('⚠️ Account already exists. Redirecting to login...');
        setTimeout(() => {
          window.location.href = '/login';
        }, 2000);
      } else if (data.error === 'Invalid email domain') {
        setMessage('❌ Please use your college email address.');
      } else {
        setMessage('❌ Failed to send OTP. Please try again.');
      }
    }
  };

  const verifyOtp = async () => {
    try {
      const res = await api.post('/api/verify-otp/', { email, otp });
      if (res.status === 200) {
        setMessage('✅ ' + res.data.message || 'OTP verified!');
        localStorage.setItem('verifiedEmail', email);
        localStorage.setItem('verified', 'true');

        setTimeout(() => {
          window.location.href = '/set-password';
        }, 1000);
      }
    } catch (error) {
      setMessage('❌ Invalid OTP. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-200 to-purple-200 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white p-8 rounded-xl shadow-md space-y-6">
        <h1 className="text-2xl font-bold text-center">📧 Email Verification</h1>

        <input
          type="email"
          placeholder="Enter your college email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="w-full px-4 py-2 border rounded-lg"
          disabled={otpSent}
        />

        {!otpSent && (
          <button
            onClick={sendOtp}
            className="w-full py-2 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700"
          >
            🚀 Send OTP
          </button>
        )}

        {otpSent && (
          <>
            <input
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
              className="w-full px-4 py-2 border rounded-lg"
            />
            <button
              onClick={verifyOtp}
              className="w-full py-2 bg-green-600 text-white font-semibold rounded-lg hover:bg-green-700"
            >
              ✅ Verify OTP
            </button>
          </>
        )}

        {message && <p className="text-center text-sm text-gray-700">{message}</p>}
      </div>
    </div>
  );
}
