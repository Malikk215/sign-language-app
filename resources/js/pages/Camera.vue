<script setup lang="ts">
import { useCamera } from '@/composables/useCamera';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Camera as CameraIcon, Square, RotateCcw } from 'lucide-vue-next';
import { ref } from 'vue';

const {
  videoRef,
  isStreaming,
  error,
  devices,
  selectedDeviceId,
  startCamera,
  stopCamera,
  switchCamera,
  takePhoto
} = useCamera();

const capturedPhoto = ref<string | null>(null);

const handleTakePhoto = () => {
  const photo = takePhoto();
  if (photo) {
    capturedPhoto.value = photo;
  }
};

const handleDeviceChange = (deviceId: string) => {
  switchCamera(deviceId);
};
</script>

<template>
  <div class="camera-container">
    <div class="flex items-center justify-between">
      <h1 class="text-3xl font-bold">Camera</h1>
    </div>

    <!-- Error Display -->
    <div v-if="error" class="bg-red-50 border border-red-200 rounded-lg p-4">
      <p class="text-red-800">{{ error }}</p>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <!-- Camera Feed -->
      <Card>
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <CameraIcon class="h-5 w-5" />
            Live Camera Feed
          </CardTitle>
        </CardHeader>
        <CardContent class="space-y-4">
          <!-- Video Element -->
          <div class="relative bg-gray-100 rounded-lg overflow-hidden aspect-video">
            <video
              ref="videoRef"
              class="w-full h-full object-cover"
              autoplay
              muted
              playsinline
            ></video>
            
            <!-- Camera Controls -->
            <div class="absolute bottom-4 left-0 right-0 flex justify-center gap-2">
              <Button v-if="!isStreaming" @click="startCamera()" variant="primary" size="sm">
                <CameraIcon class="h-4 w-4 mr-2" />
                Start Camera
              </Button>
              <Button v-else @click="stopCamera()" variant="destructive" size="sm">
                <Square class="h-4 w-4 mr-2" />
                Stop Camera
              </Button>
              <Button v-if="isStreaming" @click="handleTakePhoto()" variant="secondary" size="sm">
                <CameraIcon class="h-4 w-4 mr-2" />
                Take Photo
              </Button>
            </div>
          </div>
          
          <!-- Camera Selection -->
          <div v-if="devices.length > 1" class="mt-4">
            <Select :model-value="selectedDeviceId" @update:model-value="handleDeviceChange">
              <SelectTrigger class="w-full">
                <SelectValue placeholder="Select camera" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem v-for="device in devices" :key="device.deviceId" :value="device.deviceId">
                  {{ device.label || `Camera ${devices.indexOf(device) + 1}` }}
                </SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>
      
      <!-- Captured Photo -->
      <Card v-if="capturedPhoto">
        <CardHeader>
          <CardTitle class="flex items-center gap-2">
            <CameraIcon class="h-5 w-5" />
            Captured Photo
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div class="bg-gray-100 rounded-lg overflow-hidden aspect-video">
            <img :src="capturedPhoto" class="w-full h-full object-cover" alt="Captured photo" />
          </div>
          <Button @click="capturedPhoto = null" variant="outline" class="mt-4">
            <RotateCcw class="h-4 w-4 mr-2" />
            Clear Photo
          </Button>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<style scoped>
.debug-panel {
  position: fixed;
  top: 10px;
  right: 10px;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 10px;
  border-radius: 5px;
  font-size: 12px;
  max-width: 300px;
  word-wrap: break-word;
}

.detection-result {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(0, 255, 0, 0.9);
  color: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
}

.error-display {
  position: fixed;
  bottom: 10px;
  left: 10px;
  background: rgba(255, 0, 0, 0.8);
  color: white;
  padding: 10px;
  border-radius: 5px;
}
</style>