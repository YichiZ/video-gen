import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const videoAPI = {
  /**
   * Generate a video from a prompt
   * @param {string} prompt - The text prompt describing the video
   * @returns {Promise} Response with operation_id
   */
  generateVideo: async (prompt) => {
    const response = await apiClient.post('/video/generate', { prompt })
    return response.data
  },

  /**
   * Get the status of a video generation operation
   * @param {string} operationId - The operation ID
   * @returns {Promise} Response with status and video URL if ready
   */
  getStatus: async (operationId) => {
    const response = await apiClient.get(`/video/status/${operationId}`)
    return response.data
  },

  /**
   * Download a generated video
   * @param {string} operationId - The operation ID
   * @returns {Promise} Blob of the video file
   */
  downloadVideo: async (operationId) => {
    const response = await apiClient.get(`/video/download/${operationId}`, {
      responseType: 'blob',
    })
    return response.data
  },

  /**
   * Get all operations
   * @returns {Promise} List of all operations
   */
  getAllOperations: async () => {
    const response = await apiClient.get('/video/operations')
    return response.data
  },
}

export default apiClient
