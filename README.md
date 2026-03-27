# 🏠 Roommate Matcher

A full-stack application that intelligently matches roommates based on compatibility scores, constraints, and preferences using graph-based algorithms.

---

## 🚀 Overview

Finding the right roommate is a non-trivial matching problem involving multiple constraints and subjective preferences. This project models the problem as a **weighted graph matching system**, where users are nodes and compatibility scores form weighted edges.

The system computes optimal roommate pairs by balancing:
- User preferences
- Hard constraints
- Mutual compatibility

---

## 🧠 Key Features

- 🔐 **Domain-Restricted Authentication**
  - Only university emails allowed
  - OTP-based verification

- 👤 **Profile Management**
  - Lifestyle preferences (sleep cycle, cleanliness, habits, etc.)
  - Personal constraints and requirements

- 🔗 **Graph-Based Matching Engine**
  - Users represented as nodes
  - Compatibility scores as weighted edges
  - Matching optimized for mutual best fit

- ⚡ **Production-Ready Backend**
  - Django + DRF APIs
  - PostgreSQL database
  - Deployed backend + frontend separation

---

## 🏗️ Tech Stack

**Backend:**
- Python
- Django & Django REST Framework
- PostgreSQL
- NetworkX (Graph Algorithms)

**Frontend:**
- React
- TypeScript

**Deployment:**
- Backend: Render  
- Frontend: Vercel  

---

## ⚙️ System Design

### Matching Pipeline

1. User registers & verifies email  
2. Profile data collected (preferences + constraints)  
3. Compatibility scores computed between users  
4. Graph constructed:
   - Nodes → Users  
   - Edges → Compatibility scores  
5. Matching algorithm selects optimal roommate pairs  

---

## 🧮 Core Algorithm

The matching problem is modeled as a **weighted graph optimization problem**:

- Each user = node  
- Edge weight = compatibility score (0–100)  
- Constraints filter invalid edges  
- Goal = maximize total compatibility across matches  

This ensures:
- No invalid pairings (constraint satisfaction)  
- Globally optimal matching instead of greedy pairing  

---

## 📊 Algorithm Applicability

While this project focuses on roommate matching, the core matching algorithm 
is applicable to various two-sided matching problems:

### **Healthcare Applications:**
- Patient-Doctor matching based on specialty, location, insurance  
- Hospital bed allocation based on patient needs and availability  
- Nurse-shift scheduling based on skills and preferences  

### **Technical Approach:**
The weighted graph algorithm considers multiple factors:
1. Preference scoring (0-100 compatibility)  
2. Constraint satisfaction (hard requirements)  
3. Optimization for mutual best matches  

This same approach applies to healthcare appointment booking where:
- Patients have preferences (doctor specialty, time slots, location)  
- Doctors have constraints (availability, patient type)  
- System optimizes for best mutual fit  

---

## 📦 Setup Instructions

```bash
# Clone repo
git clone https://github.com/asmitk991/roommate-matcher.git
cd roommate-matcher

# Backend setup
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Frontend setup
cd ../frontend
npm install
npm run dev
