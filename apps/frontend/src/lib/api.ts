/**
 * API Client for CareerNavigator Backend
 */

import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import type { Token, LoginRequest, SignupRequest, User, UserProfile, ApiError, OAuthRequest, Skill, CareerHistory, Education } from '@/types/auth';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Token storage keys
const ACCESS_TOKEN_KEY = 'access_token';
const REFRESH_TOKEN_KEY = 'refresh_token';

// Create axios instance
const api: AxiosInstance = axios.create({
  baseURL: `${API_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Token management
export const tokenManager = {
  getAccessToken: (): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  },

  getRefreshToken: (): string | null => {
    if (typeof window === 'undefined') return null;
    return localStorage.getItem(REFRESH_TOKEN_KEY);
  },

  setTokens: (token: Token) => {
    if (typeof window === 'undefined') return;
    localStorage.setItem(ACCESS_TOKEN_KEY, token.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, token.refresh_token);
  },

  clearTokens: () => {
    if (typeof window === 'undefined') return;
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
  },

  isAuthenticated: (): boolean => {
    return !!tokenManager.getAccessToken();
  },
};

// Request interceptor - add auth token
api.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = tokenManager.getAccessToken();
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError<ApiError>) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

    // If 401 and not already retrying, try to refresh token
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      const refreshToken = tokenManager.getRefreshToken();
      if (refreshToken) {
        try {
          const response = await axios.post<Token>(`${API_URL}/api/v1/auth/refresh`, {
            refresh_token: refreshToken,
          });

          tokenManager.setTokens(response.data);

          // Retry original request with new token
          if (originalRequest.headers) {
            originalRequest.headers.Authorization = `Bearer ${response.data.access_token}`;
          }
          return api(originalRequest);
        } catch (refreshError) {
          // Refresh failed, clear tokens
          tokenManager.clearTokens();
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  signup: async (data: SignupRequest): Promise<Token> => {
    const response = await api.post<Token>('/auth/signup', data);
    tokenManager.setTokens(response.data);
    return response.data;
  },

  login: async (data: LoginRequest): Promise<Token> => {
    const response = await api.post<Token>('/auth/login', data);
    tokenManager.setTokens(response.data);
    return response.data;
  },

  logout: async (): Promise<void> => {
    const refreshToken = tokenManager.getRefreshToken();
    if (refreshToken) {
      try {
        await api.post('/auth/logout', { refresh_token: refreshToken });
      } catch (e) {
        // Ignore errors during logout
      }
    }
    tokenManager.clearTokens();
  },

  refresh: async (): Promise<Token> => {
    const refreshToken = tokenManager.getRefreshToken();
    if (!refreshToken) {
      throw new Error('No refresh token');
    }
    const response = await api.post<Token>('/auth/refresh', {
      refresh_token: refreshToken,
    });
    tokenManager.setTokens(response.data);
    return response.data;
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get<User>('/auth/me');
    return response.data;
  },

  oauth: async (data: OAuthRequest): Promise<Token> => {
    const response = await api.post<Token>('/auth/oauth', data);
    tokenManager.setTokens(response.data);
    return response.data;
  },

  changePassword: async (currentPassword: string, newPassword: string): Promise<void> => {
    await api.post('/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },
};

// User API
export const userApi = {
  getProfile: async (): Promise<UserProfile> => {
    const response = await api.get<UserProfile>('/users/me');
    return response.data;
  },

  updateProfile: async (data: Partial<User>): Promise<User> => {
    const response = await api.put<User>('/users/me', data);
    return response.data;
  },

  // Skills
  getSkills: async (): Promise<Skill[]> => {
    const response = await api.get<Skill[]>('/users/me/skills');
    return response.data;
  },

  addSkill: async (data: Omit<Skill, 'id' | 'user_id' | 'created_at'>): Promise<Skill> => {
    const response = await api.post<Skill>('/users/me/skills', data);
    return response.data;
  },

  addSkillsBulk: async (skills: Array<Omit<Skill, 'id' | 'user_id' | 'created_at'>>): Promise<Skill[]> => {
    const response = await api.post<Skill[]>('/users/me/skills/bulk', skills);
    return response.data;
  },

  updateSkill: async (skillId: string, data: Partial<Skill>): Promise<Skill> => {
    const response = await api.put<Skill>(`/users/me/skills/${skillId}`, data);
    return response.data;
  },

  deleteSkill: async (skillId: string): Promise<void> => {
    await api.delete(`/users/me/skills/${skillId}`);
  },

  // Career History
  getCareerHistory: async (): Promise<CareerHistory[]> => {
    const response = await api.get<CareerHistory[]>('/users/me/career');
    return response.data;
  },

  addCareerHistory: async (data: Omit<CareerHistory, 'id' | 'user_id' | 'created_at' | 'updated_at'>): Promise<CareerHistory> => {
    const response = await api.post<CareerHistory>('/users/me/career', data);
    return response.data;
  },

  updateCareerHistory: async (careerId: string, data: Partial<CareerHistory>): Promise<CareerHistory> => {
    const response = await api.put<CareerHistory>(`/users/me/career/${careerId}`, data);
    return response.data;
  },

  deleteCareerHistory: async (careerId: string): Promise<void> => {
    await api.delete(`/users/me/career/${careerId}`);
  },

  // Education
  getEducation: async (): Promise<Education[]> => {
    const response = await api.get<Education[]>('/users/me/education');
    return response.data;
  },

  addEducation: async (data: Omit<Education, 'id' | 'user_id' | 'created_at'>): Promise<Education> => {
    const response = await api.post<Education>('/users/me/education', data);
    return response.data;
  },

  updateEducation: async (educationId: string, data: Partial<Education>): Promise<Education> => {
    const response = await api.put<Education>(`/users/me/education/${educationId}`, data);
    return response.data;
  },

  deleteEducation: async (educationId: string): Promise<void> => {
    await api.delete(`/users/me/education/${educationId}`);
  },

  // Resume
  uploadResume: async (file: File): Promise<User> => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await api.post<User>('/users/me/resume', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },
};

export default api;
