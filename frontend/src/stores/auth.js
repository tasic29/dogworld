import { defineStore } from "pinia";
import { ref, computed } from "vue";
import axios from "axios";

export const useAuthStore = defineStore("auth", () => {
  const jwtToken = ref(localStorage.getItem("jwtToken") || null);
  const user = ref(null);
  const isLoading = ref(false);

  if (jwtToken.value) {
    axios.defaults.headers.common["Authorization"] = `Bearer ${jwtToken.value}`;
  }

  const isAuthenticated = computed(() => !!jwtToken.value);

  const setToken = (token) => {
    jwtToken.value = token;
    localStorage.setItem("jwtToken", token);
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
  };

  const clearToken = () => {
    jwtToken.value = null;
    localStorage.removeItem("jwtToken");
    delete axios.defaults.headers.common["Authorization"];
  };

  const login = async (credentials) => {
    isLoading.value = true;
    try {
      const response = await axios.post("/auth/jwt/create/", credentials);
      setToken(response.data.access);
      await fetchUser(); // Optional
    } catch (error) {
      throw error;
    } finally {
      isLoading.value = false;
    }
  };

  const fetchUser = async () => {
    if (!jwtToken.value) return;
    try {
      const response = await axios.get("/auth/users/me/");
      user.value = response.data;
    } catch {
      clearToken();
    }
  };

  const logout = () => {
    clearToken();
    user.value = null;
  };

  return {
    jwtToken,
    user,
    isLoading,
    isAuthenticated,
    login,
    fetchUser,
    logout,
    setToken,
    clearToken,
  };
});
