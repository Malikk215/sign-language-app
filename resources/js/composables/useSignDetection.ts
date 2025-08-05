import { ref, computed } from 'vue';
import axios from 'axios';

export interface DetectionResult {
  prediction: string;
  confidence: number;
  accuracy: number;
}

export function useSignDetection() {
  const isDetecting = ref(false);
  const currentPrediction = ref<string>('');
  const currentConfidence = ref<number>(0);
  const currentAccuracy = ref<number>(0);
  const debugInfo = ref<string>('');
  const confidenceHistory = ref<number[]>([]);
  const detectionTips = ref<string>('');

  let detectionInterval: number | null = null;
  let videoElement: HTMLVideoElement | null = null;
  let canvasElement: HTMLCanvasElement | null = null;
  let contextElement: CanvasRenderingContext2D | null = null;

  // Tambahkan lastDetection untuk kompatibilitas
  const lastDetection = computed(() => ({
    prediction: currentPrediction.value,
    confidence: currentConfidence.value,
    accuracy: currentAccuracy.value
  }));

  const averageConfidence = computed(() => {
    if (confidenceHistory.value.length === 0) return 0;
    const sum = confidenceHistory.value.reduce((acc, conf) => acc + conf, 0);
    return sum / confidenceHistory.value.length;
  });

  const initializeCamera = async (): Promise<MediaStream | null> => {
    try {
      console.log('[DEBUG] Initializing camera...');
      debugInfo.value = 'Initializing camera...';
      
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          width: { ideal: 1280 },
          height: { ideal: 720 },
          facingMode: 'user'
        }
      });
      
      console.log('[DEBUG] Camera initialized successfully');
      debugInfo.value = 'Camera initialized successfully';
      return stream;
    } catch (error) {
      console.error('[DEBUG] Camera error:', error);
      debugInfo.value = `Camera error: ${error}`;
      return null;
    }
  };

  const enhanceImage = (imageData: ImageData): ImageData => {
    const data = imageData.data;
    
    // Increase brightness and contrast
    for (let i = 0; i < data.length; i += 4) {
      // Increase brightness
      data[i] = Math.min(255, data[i] * 1.2 + 20);     // Red
      data[i + 1] = Math.min(255, data[i + 1] * 1.2 + 20); // Green
      data[i + 2] = Math.min(255, data[i + 2] * 1.2 + 20); // Blue
      // Alpha channel (data[i + 3]) remains unchanged
    }
    
    return imageData;
  };

  async function captureAndPredict() {
    // Perbaikan: hapus .value karena videoElement dan canvasElement bukan ref
    if (!videoElement || !canvasElement) {
      console.error('[DEBUG] Video or canvas element not available');
      return;
    }
  
    try {
      const startTime = Date.now();
      console.log('[DEBUG] Starting capture and predict...');
      
      // Capture frame from video
      // Perbaikan: hapus .value
      const context = canvasElement.getContext('2d');
      if (!context) {
        console.error('[DEBUG] Could not get canvas context');
        return;
      }
      
      // Perbaikan: hapus .value dari kedua elemen
      context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
      
      console.log('[DEBUG] Converting to base64...');
      // Convert to base64 with higher quality for better detection
      // Perbaikan: hapus .value
      const base64Image = canvasElement.toDataURL('image/jpeg', 0.9);
      
      debugInfo.value = `Sending image: ${base64Image.length} bytes`;
      console.log('[DEBUG] Sending to backend...');
      
      // Send to backend with longer timeout and retry logic
      const maxRetries = 2;
      let lastError;
      let response; // Declare response variable outside the loop
      
      for (let attempt = 1; attempt <= maxRetries; attempt++) {
        try {
          console.log(`[DEBUG] Attempt ${attempt}/${maxRetries}`);
          
          response = await axios.post('/api/predict-sign', {
            image: base64Image
          }, {
            timeout: 120000, // Increase timeout to 2 minutes
            onUploadProgress: (progressEvent) => {
              console.log('[DEBUG] Upload progress:', progressEvent.loaded, '/', progressEvent.total);
            }
          });
          
          const endTime = Date.now();
          console.log(`[DEBUG] Request completed in ${endTime - startTime}ms`);
          
          console.log('[DEBUG] Response received:', response.data);
          
          if (response.data && response.data.prediction) {
            currentPrediction.value = response.data.prediction;
            currentConfidence.value = response.data.confidence || 0;
            currentAccuracy.value = response.data.accuracy || 0;
            
            // Update confidence history
            confidenceHistory.value.push(currentConfidence.value);
            if (confidenceHistory.value.length > 10) {
              confidenceHistory.value.shift();
            }
            
            debugInfo.value = `Prediction: ${response.data.prediction}, Confidence: ${response.data.confidence}%`;
            console.log('[DEBUG] Prediction updated:', { prediction: response.data.prediction, confidence: response.data.confidence });
            
            // Update detection tips based on response
            if (response.data.prediction) {
              detectionTips.value = 'Hand detected successfully!';
            }
            
            return; // Success, exit retry loop
          } else {
            console.log('[DEBUG] No prediction received');
            debugInfo.value = 'No prediction received';
            return;
          }
        } catch (error: any) {
          lastError = error;
          console.error(`[DEBUG] Attempt ${attempt} failed:`, error.message);
          
          if (attempt < maxRetries) {
            console.log(`[DEBUG] Retrying in 2 seconds...`);
            await new Promise(resolve => setTimeout(resolve, 2000));
          }
        }
      }
      
      // All retries failed
      throw lastError;
      
    } catch (error: any) {
      console.error('[DEBUG] Prediction error:', error);
      
      if (error.code === 'ECONNABORTED') {
        debugInfo.value = 'Server timeout - backend is taking too long to respond. Check if Laravel server is running.';
      } else if (error.response?.status === 404) {
        debugInfo.value = 'API endpoint not found - check if route exists';
      } else if (error.response?.status === 500) {
        debugInfo.value = 'Server error - check Laravel logs';
      } else {
        debugInfo.value = `Error: ${error.message || 'Unknown error'}`;
      }
      
      // Set appropriate detection tips based on error
      detectionTips.value = 'Tips: Pastikan tangan terlihat jelas, pencahayaan cukup, dan posisi tangan di tengah frame';
    }
  }

  const startDetection = async (video: HTMLVideoElement, canvas?: HTMLCanvasElement): Promise<boolean> => {
    try {
      console.log('[DEBUG] Starting detection...');
      console.log('[DEBUG] Video element:', video);
      console.log('[DEBUG] Canvas element:', canvas);
      
      debugInfo.value = 'Starting detection...';
      
      videoElement = video;
      
      // Create canvas if not provided
      if (!canvas) {
        console.log('[DEBUG] Creating canvas element...');
        canvasElement = document.createElement('canvas');
        // Set canvas dimensions to match video
        canvasElement.width = video.videoWidth || 640;
        canvasElement.height = video.videoHeight || 480;
      } else {
        canvasElement = canvas;
      }
      
      console.log('[DEBUG] Getting canvas context...');
      // Perbaikan: gunakan canvasElement bukan canvas
      const context = canvasElement.getContext('2d', { willReadFrequently: true });
      
      // Perbaikan: gunakan context bukan contextElement
      if (!context) {
        console.error('[DEBUG] Failed to get canvas context');
        debugInfo.value = 'Failed to get canvas context';
        return false;
      }
      
      // Simpan context untuk digunakan nanti
      contextElement = context;
      
      console.log('[DEBUG] Initializing camera...');
      const stream = await initializeCamera();
      if (!stream) {
        console.error('[DEBUG] Failed to initialize camera');
        return false;
      }
      
      console.log('[DEBUG] Setting video source...');
      videoElement.srcObject = stream;
      
      await new Promise<void>((resolve) => {
        videoElement!.onloadedmetadata = () => {
          console.log('[DEBUG] Video metadata loaded');
          resolve();
        };
      });
      
      console.log('[DEBUG] Playing video...');
      await videoElement.play();
      isDetecting.value = true;
      
      console.log('[DEBUG] Starting detection interval...');
      // Start detection loop
      detectionInterval = window.setInterval(captureAndPredict, 1200);
      
      debugInfo.value = 'Detection started successfully';
      console.log('[DEBUG] Detection started successfully');
      return true;
    } catch (error: any) {
      console.error('[DEBUG] Failed to start detection:', error);
      debugInfo.value = `Failed to start: ${error.message}`;
      return false;
    }
  };

  const stopDetection = (): void => {
    console.log('[DEBUG] Stopping detection...');
    isDetecting.value = false;
    
    if (detectionInterval) {
      clearInterval(detectionInterval);
      detectionInterval = null;
      console.log('[DEBUG] Detection interval cleared');
    }
    
    if (videoElement && videoElement.srcObject) {
      const stream = videoElement.srcObject as MediaStream;
      stream.getTracks().forEach(track => track.stop());
      videoElement.srcObject = null;
      console.log('[DEBUG] Video stream stopped');
    }
    
    // Reset values
    currentPrediction.value = '';
    currentConfidence.value = 0;
    currentAccuracy.value = 0;
    confidenceHistory.value = [];
    debugInfo.value = 'Detection stopped';
    console.log('[DEBUG] Detection stopped and values reset');
  };

  const resetHistory = (): void => {
    confidenceHistory.value = [];
    debugInfo.value = 'History reset';
    console.log('[DEBUG] History reset');
  };

  return {
    isDetecting,
    currentPrediction,
    currentConfidence,
    currentAccuracy,
    lastDetection, // Tambahkan untuk kompatibilitas
    debugInfo,
    confidenceHistory,
    averageConfidence,
    startDetection,
    stopDetection,
    resetHistory,
    detectionTips
  };
}
