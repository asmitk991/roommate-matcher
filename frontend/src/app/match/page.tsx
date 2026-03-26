'use client';

import { useEffect, useState } from 'react';
import api from '@/utils/api';

type MatchData = {
  full_name: string;
  email: string;
  interests: string;
  similarities: string[];
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

    api.get('/api/match-result/', {
      headers: { Authorization: token },
    })
      .then((res) => {
        const data = res.data;
        if (data.matched_with) {
          setMatch({
            full_name: data.matched_with,
            email: data.matched_email,
            interests: data.common_interests.length > 0 ? data.common_interests.join(', ') : 'No exact common interests found',
            similarities: data.similarities || [],
          });
        }
        setLoading(false);
      })
      .catch((err) => {
        if (err.response && err.response.status === 404) {
          setMessage('⏳ Matches are not formed yet. They’ll be available once all students submit their form.');
        } else {
          setMessage('❌ Network error');
        }
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="text-center mt-10">Loading...</div>;

  return (
    <div className="min-h-screen bg-gradient-to-br from-yellow-100 to-white flex items-center justify-center px-4">
      <div className="max-w-lg w-full bg-white p-8 rounded-xl shadow-md space-y-4">
        <h1 className="text-2xl font-bold text-center">🎯 Your Roommate Match</h1>

        {match ? (
          <div className="space-y-4">
            <div className="text-gray-800">
              <p className="text-lg"><strong>Name:</strong> {match.full_name}</p>
              <p className="text-lg"><strong>Email:</strong> {match.email}</p>
            </div>
            
            <div className="bg-blue-50 p-4 rounded-lg shadow-sm border border-blue-100">
              <h3 className="font-bold text-blue-800 border-b border-blue-200 pb-2 mb-2">🔥 Common Interests</h3>
              <p className="capitalize text-gray-700">{match.interests}</p>
            </div>

            {match.similarities && match.similarities.length > 0 && (
              <div className="bg-green-50 p-4 rounded-lg shadow-sm border border-green-100">
                <h3 className="font-bold text-green-800 border-b border-green-200 pb-2 mb-2">✨ Shared Habits & Traits</h3>
                <ul className="list-disc pl-5 text-gray-700">
                  {match.similarities.map((sim, i) => (
                    <li key={i}>{sim}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : (
          <p className="text-center text-gray-600">{message}</p>
        )}
      </div>
    </div>
  );
}
