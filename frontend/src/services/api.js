import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
});

export const fetchUsers = async () => {
  const response = await api.get("/users");
  return response.data;
};
