/**
 * Authentication related types
 */

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  phone: string | null;
  location: {
    city?: string;
    country?: string;
  } | null;
  bio: string | null;
  linkedin_url: string | null;
  github_url: string | null;
  portfolio_url: string | null;
  avatar_url: string | null;
  is_email_verified: boolean;
  target_roles: string[] | null;
  target_salary_min: number | null;
  target_salary_max: number | null;
  target_locations: string[] | null;
  resume_url: string | null;
  created_at: string;
  updated_at: string;
}

export interface Skill {
  id: string;
  user_id: string;
  skill_name: string;
  category: string | null;
  proficiency_level: number | null;
  years_used: number | null;
  created_at: string;
}

export interface CareerHistory {
  id: string;
  user_id: string;
  company_name: string;
  title: string;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  description: string | null;
  responsibilities: string[] | null;
  achievements: Record<string, unknown> | null;
  location: string | null;
  created_at: string;
  updated_at: string;
}

export interface Education {
  id: string;
  user_id: string;
  institution: string;
  degree: string | null;
  field_of_study: string | null;
  start_date: string | null;
  end_date: string | null;
  grade: string | null;
  description: string | null;
  created_at: string;
}

export interface UserProfile extends User {
  skills: Skill[];
  career_history: CareerHistory[];
  education: Education[];
}

export interface Token {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface SignupRequest {
  email: string;
  password: string;
  full_name?: string;
}

export interface OAuthRequest {
  provider: 'google' | 'linkedin';
  access_token: string;
  id_token?: string;
}

export interface ApiError {
  type: string;
  title: string;
  status: number;
  detail: string;
  instance: string;
  errors?: Array<{
    field: string;
    message: string;
  }>;
}
