'use client';

import { useEffect, useState } from 'react';

type MatchData = {
  full_name: string;
  email: string;
  interests: string;
};

export default function MatchPage() {
  const [match, setMatch] = useState<MatchData | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      setMessage('🔐 Please log in first.');
      setLoading(false);
      return;
    }

    fetch('http://127.0.0.1:8000/api/match-result/', {
      headers: { Authorization: token },
    })
      .then(async (res) => {
        const data = await res.json();
        if (res.ok && data.matched_with) {
          // Adapt to your component state
          setMatch({
            full_name: data.matched_with,
            email: data.matched_email,
            interests: data.common_interests.join(', '),
          });
        } else {
          setMessage('⏳ Matches are not formed yet. They’ll be available once all students submit their form.');
        }
        setLoading(false);
      })
      .catch(() => {
        setMessage('❌ Network error');
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center mt-10">Loading...</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-100 to-white flex items-center justify-center px-4">
      <div className="max-w-lg w-full bg-white p-8 rounded-xl shadow-md space-y-4">
        <h1 className="text-2xl font-bold text-center">🎯 Your Roommate Match</h1>

        {match ? (
          <div className="space-y-2">
            <p><strong>Name:</strong> {match.full_name}</p>
            <p><strong>Email:</strong> {match.email}</p>
            <p><strong>Interests:</strong> {match.interests}</p>
          </div>
        ) : (
          <p className="text-center text-gray-600">{message}</p>
        )}
      </div>
    </div>
  );
}
