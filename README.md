# 🎤 Intelligent Speech Therapy Platform

An AI-powered speech therapy platform that provides real-time pronunciation analysis, personalized feedback, and adaptive exercises for English language learners.

## 🎯 Project Overview

The Intelligent Speech Therapy Platform analyzes users' spoken English by comparing recorded sentences against reference pronunciations. Using advanced speech processing and machine learning techniques, it identifies phoneme-level errors, scores pronunciation accuracy and fluency, and provides personalized recommendations for improvement.

### Key Features

- 🎤 **Real-time Speech Analysis**: Record speech via microphone or upload audio files
- 🧠 **AI-Powered Feedback**: Phoneme-level pronunciation scoring using Wav2Vec2/HuBERT embeddings
- 📊 **Progress Tracking**: Visual dashboards showing improvement over time
- 🎯 **Adaptive Exercises**: Personalized practice recommendations based on weak phonemes
- 👥 **Role-Based Access**: Separate interfaces for users and administrators
- 🔐 **Secure Authentication**: Supabase-powered user management with JWT tokens

## 🏗️ System Architecture

### Frontend (Streamlit)
- **Main App**: Landing page and navigation
- **Authentication**: Login/signup pages with role-based access
- **User Dashboard**: Personal progress tracking and analytics
- **Practice Page**: Speech recording and analysis interface
- **Admin Panel**: System management and content administration

### Backend Components
- **Audio Processing**: Normalization, silence trimming, format conversion
- **Speech Analysis**: Forced alignment and phoneme extraction
- **Scoring Engine**: Pronunciation and fluency assessment
- **Recommendation System**: Adaptive exercise suggestions
- **Database Layer**: Supabase integration with PostgreSQL

### Database Schema (Supabase)
- **profiles**: User accounts with role-based access control
- **sessions**: Practice session results and scores
- **phoneme_scores**: Detailed phoneme-level analysis
- **sentence_bank**: Repository of practice sentences
- **user_progress**: Aggregated progress tracking
- **recommendations**: Personalized exercise suggestions

## 🔐 Authentication & Security

### Authentication Flow

The platform uses **Supabase Auth** for secure user management with email/password authentication and JWT-based sessions.

#### User Registration (Users Only)
1. User provides email and password
2. System validates input and creates account in `auth.users`
3. Profile created in `profiles` table with default role 'user'
4. Email verification sent (optional)
5. User can log in and access practice features

#### Login Process (Users & Admins)
1. User enters credentials
2. Supabase Auth validates and returns JWT token
3. System fetches user profile and role from `profiles` table
4. Session initialized in Streamlit with user data and role
5. User redirected to appropriate dashboard based on role

#### Role-Based Access Control

**User Role (`user`)**:
- ✅ Can sign up via UI
- ✅ Can record and analyze speech
- ✅ Can view personal dashboard and progress
- ✅ Can access practice exercises and recommendations
- ❌ Cannot access admin features or other users' data

**Admin Role (`admin`)**:
- ❌ Cannot sign up via UI (manually assigned)
- ✅ Can access all user features
- ✅ Can manage sentence bank (add/edit/delete)
- ✅ Can view platform-wide analytics
- ✅ Can manage user accounts and roles
- ✅ Can access system settings and configuration

### Security Implementation

#### Authentication Guard System
```python
# Protect pages with role-based access
require_auth(allowed_roles=["user"])  # User-only access
require_admin()                       # Admin-only access
require_auth()                        # Any authenticated user
```

#### Row Level Security (RLS)
- Database policies ensure users can only access their own data
- Admins have read-only access to aggregated analytics
- Sensitive operations require proper role verification

#### Session Management
- JWT tokens stored securely in Streamlit session state
- Automatic session cleanup on logout
- Session validation on each protected page access

### Why Supabase Auth?

1. **Streamlit Compatible**: Works seamlessly with Streamlit's session state
2. **Production Ready**: Enterprise-grade security with JWT tokens
3. **No External Dependencies**: Self-contained authentication solution
4. **Row Level Security**: Built-in database-level access control
5. **Scalable**: Handles user management without custom backend code

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Supabase account and project
- Microphone access (for speech recording)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd speech-therapy
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Supabase**
   - Create a new Supabase project
   - Run the SQL schema from `db/schema.sql`
   - Get your project URL and anon key

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your Supabase credentials
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

### Environment Variables

```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key

# Application Settings
DEBUG=True
LOG_LEVEL=INFO

# Audio Processing Settings
SAMPLE_RATE=16000
AUDIO_FORMAT=wav
MAX_AUDIO_LENGTH=30

# Scoring Thresholds
PRONUNCIATION_THRESHOLD=0.7
FLUENCY_THRESHOLD=0.6
ACCURACY_THRESHOLD=0.8
```

## 📁 Project Structure

```
speech-therapy/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── README.md              # This file
│
├── auth/                  # Authentication system
│   ├── login.py          # User login page
│   ├── signup.py         # User registration page
│   └── auth_guard.py     # Role-based access control
│
├── pages/                 # Streamlit pages
│   ├── user_dashboard.py # User progress dashboard
│   ├── practice.py       # Speech practice interface
│   └── admin_panel.py    # Admin management interface
│
├── audio/                 # Audio processing modules
│   ├── preprocess.py     # Audio normalization and cleanup
│   ├── alignment.py      # Forced alignment implementation
│   └── features.py       # Audio feature extraction
│
├── scoring/               # Pronunciation scoring
│   ├── phoneme_scoring.py # Phoneme-level analysis
│   └── feedback.py       # Feedback generation
│
├── recommendation/        # Adaptive learning
│   └── engine.py         # Exercise recommendation logic
│
├── db/                    # Database layer
│   ├── supabase_client.py # Supabase integration
│   └── schema.sql        # Database schema
│
└── data/                  # Static data
    └── sentence_bank.csv  # Practice sentences
```

## 🔧 Module Implementation

### 1. Audio Processing Module (`audio/`)
- **Preprocessing**: Noise reduction, normalization, silence trimming
- **Format Conversion**: Standardize to 16kHz WAV format
- **Feature Extraction**: MFCC, spectrograms for analysis

### 2. Speech Analysis Pipeline
- **G2P Conversion**: Text to phoneme mapping using `g2p-en`
- **Forced Alignment**: Audio-to-phoneme timestamp alignment
- **Phoneme Extraction**: Individual sound segment isolation

### 3. Scoring Engine (`scoring/`)
- **Embedding Generation**: Wav2Vec2/HuBERT feature extraction
- **Similarity Scoring**: Cosine similarity between user and reference
- **Threshold-Based Assessment**: Configurable accuracy thresholds

### 4. Feedback System
- **Deterministic Templates**: Rule-based feedback generation
- **Phoneme-Specific Guidance**: Targeted improvement suggestions
- **Progress Tracking**: Historical performance analysis

### 5. Recommendation Engine (`recommendation/`)
- **Weakness Detection**: Identify problematic phonemes
- **Adaptive Difficulty**: Adjust exercise complexity
- **Personalized Sentences**: Match practice content to user needs

## 📊 Database Design

### Core Tables

**profiles**
- User account information and roles
- Links to Supabase auth.users table
- Role-based access control

**sessions**
- Practice session results
- Accuracy and fluency scores
- Links to user profiles

**phoneme_scores**
- Detailed phoneme-level analysis
- Similarity scores and timestamps
- Links to sessions

**sentence_bank**
- Repository of practice sentences
- Phoneme targeting and difficulty levels
- Usage tracking and analytics

### Analytics Views
- **user_performance_summary**: Aggregated user statistics
- **phoneme_difficulty_analysis**: Platform-wide phoneme challenges

## 🎯 Usage Guide

### For Users
1. **Sign Up**: Create account with email/password
2. **Practice**: Record speech or upload audio files
3. **Analyze**: Get AI-powered pronunciation feedback
4. **Improve**: Follow personalized exercise recommendations
5. **Track**: Monitor progress through visual dashboards

### For Administrators
1. **Login**: Use admin credentials (manually assigned)
2. **Manage Content**: Add/edit practice sentences
3. **Monitor Users**: View platform-wide analytics
4. **System Settings**: Configure scoring thresholds
5. **Analytics**: Export usage and performance data

## 🚀 Deployment

### Streamlit Cloud Deployment
1. Push code to GitHub repository
2. Connect Streamlit Cloud to repository
3. Add environment variables in Streamlit Cloud settings
4. Deploy with automatic SSL and domain

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your credentials

# Run development server
streamlit run app.py
```

## 🔮 Future Enhancements

### Technical Improvements
- **Real-time Processing**: WebRTC integration for live analysis
- **Advanced Models**: Custom fine-tuned speech recognition models
- **Multi-language Support**: Extend beyond English pronunciation
- **Mobile App**: React Native or Flutter mobile interface

### Feature Additions
- **Group Learning**: Classroom and teacher management features
- **Gamification**: Achievement system and learning streaks
- **Social Features**: Peer comparison and community challenges
- **Advanced Analytics**: ML-powered learning insights

### Performance Optimizations
- **Caching Layer**: Redis for session and analysis caching
- **CDN Integration**: Fast audio file delivery
- **Background Processing**: Async analysis for large files
- **Database Optimization**: Query optimization and indexing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Supabase**: Authentication and database infrastructure
- **Streamlit**: Rapid web application development
- **Hugging Face**: Pre-trained speech processing models
- **Montreal Forced Alignment**: Speech-to-phoneme alignment
- **OpenAI**: AI-powered feedback generation concepts

## 📞 Support

For questions, issues, or contributions:
- 📧 Email: support@speechtherapy.ai
- 🐛 Issues: GitHub Issues page
- 📖 Documentation: Wiki section
- 💬 Discussions: GitHub Discussions

---

**Built with ❤️ for language learners worldwide**
