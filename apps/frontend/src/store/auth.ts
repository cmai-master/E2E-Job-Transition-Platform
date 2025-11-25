/**
 * Auth Store using Zustand
 */

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { User, UserProfile, LoginRequest, SignupRequest, OAuthRequest } from '@/types/auth';
import { authApi, userApi, tokenManager } from '@/lib/api';

interface AuthState {
  user: User | null;
  profile: UserProfile | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: string | null;

  // Actions
  login: (data: LoginRequest) => Promise<void>;
  signup: (data: SignupRequest) => Promise<void>;
  logout: () => Promise<void>;
  oauthLogin: (data: OAuthRequest) => Promise<void>;
  fetchUser: () => Promise<void>;
  fetchProfile: () => Promise<void>;
  updateProfile: (data: Partial<User>) => Promise<void>;
  clearError: () => void;
  checkAuth: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      profile: null,
      isLoading: false,
      isAuthenticated: false,
      error: null,

      login: async (data: LoginRequest) => {
        set({ isLoading: true, error: null });
        try {
          await authApi.login(data);
          const user = await authApi.getCurrentUser();
          set({ user, isAuthenticated: true, isLoading: false });
        } catch (error: unknown) {
          const message = error instanceof Error ? error.message : 'Login failed';
          set({ error: message, isLoading: false });
          throw error;
        }
      },

      signup: async (data: SignupRequest) => {
        set({ isLoading: true, error: null });
        try {
          await authApi.signup(data);
          const user = await authApi.getCurrentUser();
          set({ user, isAuthenticated: true, isLoading: false });
        } catch (error: unknown) {
          const message = error instanceof Error ? error.message : 'Signup failed';
          set({ error: message, isLoading: false });
          throw error;
        }
      },

      logout: async () => {
        set({ isLoading: true });
        try {
          await authApi.logout();
        } finally {
          set({
            user: null,
            profile: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        }
      },

      oauthLogin: async (data: OAuthRequest) => {
        set({ isLoading: true, error: null });
        try {
          await authApi.oauth(data);
          const user = await authApi.getCurrentUser();
          set({ user, isAuthenticated: true, isLoading: false });
        } catch (error: unknown) {
          const message = error instanceof Error ? error.message : 'OAuth login failed';
          set({ error: message, isLoading: false });
          throw error;
        }
      },

      fetchUser: async () => {
        if (!tokenManager.isAuthenticated()) {
          set({ isAuthenticated: false, user: null });
          return;
        }

        set({ isLoading: true });
        try {
          const user = await authApi.getCurrentUser();
          set({ user, isAuthenticated: true, isLoading: false });
        } catch (error) {
          set({ user: null, isAuthenticated: false, isLoading: false });
        }
      },

      fetchProfile: async () => {
        set({ isLoading: true });
        try {
          const profile = await userApi.getProfile();
          set({ profile, user: profile, isLoading: false });
        } catch (error: unknown) {
          const message = error instanceof Error ? error.message : 'Failed to fetch profile';
          set({ error: message, isLoading: false });
        }
      },

      updateProfile: async (data: Partial<User>) => {
        set({ isLoading: true, error: null });
        try {
          const user = await userApi.updateProfile(data);
          set({ user, isLoading: false });
          // Also update profile if it exists
          const currentProfile = get().profile;
          if (currentProfile) {
            set({ profile: { ...currentProfile, ...user } });
          }
        } catch (error: unknown) {
          const message = error instanceof Error ? error.message : 'Failed to update profile';
          set({ error: message, isLoading: false });
          throw error;
        }
      },

      clearError: () => set({ error: null }),

      checkAuth: () => {
        const isAuthenticated = tokenManager.isAuthenticated();
        if (!isAuthenticated) {
          set({ isAuthenticated: false, user: null, profile: null });
        } else if (!get().user) {
          get().fetchUser();
        }
      },
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);
