import { AllauthClient } from "@knowsuchagency/allauth-fetch";
import { create } from 'zustand';
import { useRouter } from 'next/navigation';

// Replace the hardcoded backendBaseUrl with an environment variable
const backendBaseUrl = process.env.NEXT_PUBLIC_BACKEND_BASE_URL || "http://localhost:8000";

// Initialize the AllauthClient
export const allauthClient = new AllauthClient("app", backendBaseUrl);

interface AuthState {
  user: {
    display: string | null;
    email: string | null;
    username: string | null;
  };
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  signup: (firstName: string, lastName: string, email: string, password: string) => Promise<void>;
}

export const useAuthState = create<AuthState>((set) => ({
  user: {
    display: null,
    email: null,
    username: null,
  },
  isAuthenticated: false,
  login: async (email: string, password: string) => {
    try {
      const response = await allauthClient.login({ email, password });
      if ('data' in response && response.meta.is_authenticated) {
        set({
          user: 'user' in response.data ? {
            display: response.data.user.display ?? null,
            email: response.data.user.email ?? null,
            username: response.data.user.username ?? null,
          } : undefined,
          isAuthenticated: true,
        });
      } else {
        throw new Error('Login failed');
      }
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  },
  logout: async () => {
    try {
      await allauthClient.logout();
    } catch (error) {
      // Ignore the error if it's a 401 status code
      if (!(error instanceof Error) || !error.message.includes('401')) {
        console.error("Logout error:", error);
        throw error;
      }
    } finally {
      // Always reset the user state, regardless of the response
      set({
        user: { display: null, email: null, username: null },
        isAuthenticated: false,
      });
    }
  },
  signup: async (firstName: string, lastName: string, email: string, password: string) => {
    try {
      const username = `${firstName.toLowerCase()}-${lastName.toLowerCase()}`;
      const response = await allauthClient.signup({ email, username, password });
      if ('data' in response && response.meta.is_authenticated) {
        set({
          user: 'user' in response.data ? {
            display: response.data.user.display ?? null,
            email: response.data.user.email ?? null,
            username: response.data.user.username ?? null,
          } : undefined,
          isAuthenticated: true,
        });
      } else {
        throw new Error('Signup failed');
      }
    } catch (error) {
      console.error("Signup error:", error);
      // Rethrow the error with the response data if available
      if (error instanceof Error && 'response' in error) {
        const errorResponse = error.response as { data?: unknown };
        if (errorResponse && 'data' in errorResponse) {
          throw new Error(JSON.stringify(errorResponse.data));
        }
      }
      throw error; // Rethrow the original error if no response data
    }
  },
}));
