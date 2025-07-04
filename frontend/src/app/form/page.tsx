"use client";

import { useEffect, useState } from "react";
import { useRouter } from 'next/navigation';


export default function MatchForm() {
  const router = useRouter();

  useEffect(() => {
    const verifiedEmail = localStorage.getItem('verifiedEmail');
    if (!verifiedEmail) {
      router.push('/verify');
    }
  }, []);
  
  const [formData, setFormData] = useState({
    email: "",
    full_name: "",
    gender: "",
    course: "",
    sleep_schedule: "",
    cleanliness: "",
    introvert_extrovert: "",
    interests: "",
  });

  const [isSubmitted, setIsSubmitted] = useState(false);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "cleanliness" ? parseInt(value) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitted(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/api/profile/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ ...formData, is_submitted: true }),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Something went wrong");
      alert("✅ Profile submitted successfully!");
    } catch (err) {
      alert("❌ Submission failed.");
      console.error(err);
      setIsSubmitted(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 to-blue-300 flex items-center justify-center px-4">
      <div className="w-full max-w-md bg-white shadow-xl rounded-xl p-8 space-y-6">
        <h2 className="text-2xl font-bold text-gray-800 text-center">
          🎯 Roommate Match Form
        </h2>

        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="College Email"
            className="w-full px-4 py-2 border rounded-lg"
            required
            disabled={isSubmitted}
          />

          <input
            name="full_name"
            type="text"
            value={formData.full_name}
            onChange={handleChange}
            placeholder="Full Name"
            className="w-full px-4 py-2 border rounded-lg"
            required
            disabled={isSubmitted}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Gender
            </label>
            <select
              name="gender"
              value={formData.gender}
              onChange={handleChange}
              className="w-full px-4 py-2 border rounded-lg"
              required
              disabled={isSubmitted}
            >
              <option value="">Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Course
            </label>
            <select
              name="course"
              value={formData.course}
              onChange={handleChange}
              className="w-full px-4 py-2 border rounded-lg"
              required
              disabled={isSubmitted}
            >
              <option value="">Select course</option>
              <option value="csai">BTech CSAI</option>
              <option value="csds">BTech CSDS</option>
              <option value="dsai">BTech DS & Analytics</option>
              <option value="design">Design</option>
              <option value="psych">Psychology</option>
              <option value="bba">BBA</option>
            </select>
          </div>

          <input
            name="sleep_schedule"
            type="text"
            value={formData.sleep_schedule}
            onChange={handleChange}
            placeholder="Night Owl / Early Bird"
            className="w-full px-4 py-2 border rounded-lg"
            required
            disabled={isSubmitted}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Cleanliness Level
            </label>
            <select
              name="cleanliness"
              value={formData.cleanliness}
              onChange={handleChange}
              className="w-full px-4 py-2 border rounded-lg"
              required
              disabled={isSubmitted}
            >
              <option value="">Select cleanliness level</option>
              <option value={1}>1 - Very Messy</option>
              <option value={2}>2 - Messy</option>
              <option value={3}>3 - Average</option>
              <option value={4}>4 - Neat</option>
              <option value={5}>5 - Very Neat</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Personality Type
            </label>
            <select
              name="introvert_extrovert"
              value={formData.introvert_extrovert}
              onChange={handleChange}
              className="w-full px-4 py-2 border rounded-lg"
              required
              disabled={isSubmitted}
            >
              <option value="">Select personality type</option>
              <option>Introvert</option>
              <option>Ambivert</option>
              <option>Extrovert</option>
            </select>
          </div>

          <textarea
            name="interests"
            value={formData.interests}
            onChange={handleChange}
            placeholder="Comma-separated interests (e.g., anime, football, coding)"
            className="w-full px-4 py-2 border rounded-lg"
            required
            disabled={isSubmitted}
          />

          <button
            type="submit"
            className="relative w-full py-2 px-4 text-white font-semibold rounded-lg overflow-hidden group bg-blue-600 disabled:opacity-60"
            disabled={isSubmitted}
          >
            <span className="absolute inset-0 w-full h-full transition-all duration-300 ease-out transform translate-x-0 group-hover:translate-x-full bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500"></span>
            <span className="relative z-10">🚀 Submit</span>
          </button>
        </form>
      </div>
    </div>
  );
}
