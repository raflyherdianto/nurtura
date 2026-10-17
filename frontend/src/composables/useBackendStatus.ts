import { ref, onMounted } from 'vue';
import { apiClient, type HealthCheckResponse } from '../services/api';

const isConnected = ref<boolean>(false);
const healthData = ref<HealthCheckResponse | null>(null);
const isChecking = ref<boolean>(false);

export function useBackendStatus() {
  const checkStatus = async () => {
    isChecking.value = true;
    try {
      const data = await apiClient.getHealthDetails();
      if (data && data.status === 'healthy') {
        isConnected.value = true;
        healthData.value = data;
      } else {
        isConnected.value = false;
        healthData.value = null;
      }
    } catch {
      isConnected.value = false;
      healthData.value = null;
    } finally {
      isChecking.value = false;
    }
  };

  onMounted(() => {
    checkStatus();
  });

  return {
    isConnected,
    healthData,
    isChecking,
    checkStatus,
  };
}
