import { ref, onMounted, onUnmounted } from 'vue';

export function useCamera() {
  const videoRef = ref<HTMLVideoElement | null>(null);
  const stream = ref<MediaStream | null>(null);
  const isStreaming = ref(false);
  const error = ref<string | null>(null);
  const devices = ref<MediaDeviceInfo[]>([]);
  const selectedDeviceId = ref<string>('');

  // Get available camera devices
  const getDevices = async () => {
    try {
      const deviceList = await navigator.mediaDevices.enumerateDevices();
      devices.value = deviceList.filter(device => device.kind === 'videoinput');
      
      if (devices.value.length > 0 && !selectedDeviceId.value) {
        selectedDeviceId.value = devices.value[0].deviceId;
      }
    } catch (err) {
      error.value = 'Failed to get camera devices';
      console.error('Error getting devices:', err);
    }
  };

  // Start camera stream
  const startCamera = async (deviceId?: string) => {
    try {
      error.value = null;
      
      const constraints: MediaStreamConstraints = {
        video: {
          deviceId: deviceId || selectedDeviceId.value || undefined,
          width: { ideal: 1280 },
          height: { ideal: 720 }
        }
      };

      stream.value = await navigator.mediaDevices.getUserMedia(constraints);
      
      if (videoRef.value) {
        videoRef.value.srcObject = stream.value;
        await videoRef.value.play();
        isStreaming.value = true;
      }
    } catch (err) {
      error.value = 'Failed to access camera';
      console.error('Error starting camera:', err);
      isStreaming.value = false;
    }
  };

  // Stop camera stream
  const stopCamera = () => {
    if (stream.value) {
      stream.value.getTracks().forEach(track => track.stop());
      stream.value = null;
    }
    
    if (videoRef.value) {
      videoRef.value.srcObject = null;
    }
    
    isStreaming.value = false;
  };

  // Switch camera device
  const switchCamera = async (deviceId: string) => {
    selectedDeviceId.value = deviceId;
    if (isStreaming.value) {
      stopCamera();
      await startCamera(deviceId);
    }
  };

  // Take a photo
  const takePhoto = (): string | null => {
    if (!videoRef.value || !isStreaming.value) return null;
    
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    
    if (!context) return null;
    
    canvas.width = videoRef.value.videoWidth;
    canvas.height = videoRef.value.videoHeight;
    
    context.drawImage(videoRef.value, 0, 0);
    
    return canvas.toDataURL('image/jpeg');
  };

  // Initialize on mount
  onMounted(() => {
    getDevices();
  });

  // Cleanup on unmount
  onUnmounted(() => {
    stopCamera();
  });

  return {
    videoRef,
    stream,
    isStreaming,
    error,
    devices,
    selectedDeviceId,
    startCamera,
    stopCamera,
    switchCamera,
    takePhoto,
    getDevices
  };
}