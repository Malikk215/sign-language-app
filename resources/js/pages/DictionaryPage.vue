<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Book, Search, Play, ExternalLink, Grid, List, Camera, X, CheckCircle, AlertCircle, Info } from 'lucide-vue-next';
import { useCamera } from '@/composables/useCamera';
import { useSignDetection } from '@/composables/useSignDetection';

interface Dictionary {
  id: number;
  title: string;
  link: string;
  created_at?: string;
  updated_at?: string;
}

interface Props {
  dictionaries: Dictionary[];
}

const props = defineProps<Props>();

const searchQuery = ref('');
const viewMode = ref<'grid' | 'list'>('grid');
const showCamera = ref(false);

// Camera composable
const {
  videoRef,
  isStreaming,
  error: cameraError,
  startCamera,
  stopCamera,
  takePhoto
} = useCamera();

const filteredDictionaries = computed(() => {
  if (!searchQuery.value) {
    return props.dictionaries;
  }
  
  return props.dictionaries.filter(item =>
    item.title.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

const alphabetProgress = computed(() => {
  return Math.round((props.dictionaries.length / 26) * 100);
});

const openSignVideo = (link: string) => {
  window.open(link, '_blank');
};

const getLetterColor = (letter: string) => {
  const colors = [
    'bg-blue-500', 'bg-green-500', 'bg-purple-500', 'bg-red-500', 
    'bg-yellow-500', 'bg-indigo-500', 'bg-pink-500', 'bg-teal-500'
  ];
  return colors[letter.charCodeAt(0) % colors.length];
};

// Camera functions
const {
  isDetecting,
  currentPrediction,
  currentConfidence, 
  currentAccuracy,
  error: detectionError,
  debugInfo,
  startDetection,
  stopDetection
} = useSignDetection();

// Tambahkan variabel untuk debug info
const showDebugInfo = ref(false);
const toggleDebugInfo = () => {
  showDebugInfo.value = !showDebugInfo.value;
};

// Update camera functions dengan debug
const openCamera = async () => {
  console.log('[DEBUG] Opening camera...');
  showCamera.value = true;
  
  try {
    console.log('[DEBUG] Starting camera...');
    await startCamera();
    
    console.log('[DEBUG] Camera started, waiting for video element...');
    // Tambahkan delay sebelum memulai deteksi
    setTimeout(() => {
      console.log('[DEBUG] Video ref:', videoRef.value);
      console.log('[DEBUG] Video ready state:', videoRef.value?.readyState);
      
      // Start real detection instead of mock
      if (videoRef.value) {
        console.log('[DEBUG] Starting detection with video element');
        startDetection(videoRef.value);
      } else {
        console.error('[DEBUG] Video element not available');
      }
    }, 1000); // Tunggu 1 detik untuk memastikan kamera sudah siap
  } catch (error) {
    console.error('[DEBUG] Error opening camera:', error);
  }
};

const closeCamera = () => {
  console.log('[DEBUG] Closing camera...');
  showCamera.value = false;
  stopCamera();
  stopDetection();
  console.log('[DEBUG] Camera closed');
};

// Tambahkan fungsi practiceDetectedLetter
const practiceDetectedLetter = () => {
  if (currentPrediction.value) {
    const letter = currentPrediction.value;
    const dictionary = props.dictionaries.find(item => item.title === letter);
    if (dictionary) {
      openSignVideo(dictionary.link);
    }
  }
};

// Update computed for detected letter
const detectedLetter = computed(() => currentPrediction.value || null);
const detectionConfidence = computed(() => currentConfidence.value || 0);
const letterAccuracy = computed(() => currentAccuracy.value || 0);
const isMirrored = ref(true); // Default mirror on

const toggleMirror = () => {
  isMirrored.value = !isMirrored.value;
};
</script>

<template>
  <div class="container mx-auto p-6 space-y-6">
    <!-- Page Header -->
    <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <Book class="h-8 w-8 text-blue-600" />
        <div>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Sign Language Dictionary</h1>
          <p class="text-gray-600 dark:text-gray-400">Learn and practice ASL alphabet signs</p>
        </div>
      </div>
      
      <!-- Progress Badge and Camera Button -->
      <div class="flex items-center gap-3">
        <Badge variant="info" class="text-lg px-4 py-2">
          {{ alphabetProgress }}% Complete ({{ dictionaries.length }}/26)
        </Badge>
        
        <!-- Camera Button -->
        <Button
          @click="openCamera"
          class="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white"
          size="lg"
        >
          <Camera class="h-5 w-5" />
          Practice with Camera
        </Button>
      </div>
    </div>

    <!-- Camera Modal -->
    <div 
      v-if="showCamera" 
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4"
    >
      <Card class="w-full max-w-4xl max-h-[90vh] overflow-hidden">
        <CardHeader class="flex flex-row items-center justify-between">
          <CardTitle class="flex items-center gap-2">
            <Camera class="h-6 w-6" />
            Sign Language Detection
          </CardTitle>
          <Button @click="closeCamera" variant="ghost" size="sm">
            <X class="h-4 w-4" />
          </Button>
        </CardHeader>
        
        <CardContent class="p-6">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Camera Feed -->
            <div class="lg:col-span-2">
              <div class="relative bg-gray-900 rounded-lg overflow-hidden aspect-video">
                <video
                  ref="videoRef"
                  class="w-full h-full object-cover"
                  :style="{ transform: isMirrored ? 'scaleX(-1)' : 'scaleX(1)' }"
                  autoplay
                  muted
                  playsinline
                ></video>
                
                <!-- Add mirror toggle button -->
                <div class="absolute top-4 right-4">
                  <Button 
                    @click="toggleMirror" 
                    variant="outline" 
                    size="sm"
                    class="bg-black bg-opacity-50 text-white border-white border-opacity-50 hover:bg-opacity-70"
                  >
                    {{ isMirrored ? '🔄 Mirror ON' : '↔️ Mirror OFF' }}
                  </Button>
                </div>
                
                <!-- Hand Position Guide -->
                <div class="absolute inset-0 pointer-events-none flex items-center justify-center">
                  <div class="w-64 h-64 border-2 border-white border-opacity-50 rounded-full flex items-center justify-center">
                    <div class="text-white text-opacity-70 text-sm text-center">
                      <div class="mb-2">✋</div>
                      <div>Posisikan tangan di sini</div>
                      <div class="text-xs mt-1">Pastikan pencahayaan cukup</div>
                    </div>
                  </div>
                </div>
                
                <!-- Detection Overlay -->
                <div 
                  v-if="detectedLetter" 
                  class="absolute top-4 left-4 bg-green-600 text-white px-4 py-2 rounded-lg shadow-lg"
                >
                  <div class="flex items-center gap-2">
                    <CheckCircle class="h-5 w-5" />
                    <div>
                      <div class="font-bold text-lg">{{ detectedLetter }}</div>
                      <div class="text-sm opacity-90">
                        {{ Math.round(detectionConfidence) }}% confidence | {{ letterAccuracy }}% accuracy
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Error State -->
                <div 
                  v-if="cameraError" 
                  class="absolute inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75"
                >
                  <div class="text-center text-white">
                    <AlertCircle class="h-12 w-12 mx-auto mb-4 text-red-400" />
                    <p class="text-lg font-semibold mb-2">Camera Error</p>
                    <p class="text-sm opacity-75">{{ cameraError }}</p>
                  </div>
                </div>
                
                <!-- Loading State -->
                <div 
                  v-if="!isStreaming && !cameraError" 
                  class="absolute inset-0 flex items-center justify-center bg-gray-800 bg-opacity-75"
                >
                  <div class="text-center text-white">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-white mx-auto mb-4"></div>
                    <p class="text-lg font-semibold">Starting Camera...</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Detection Panel -->
            <div class="space-y-4">
              <div>
                <h3 class="text-lg font-semibold mb-3">Detection Status</h3>
                <div class="space-y-3">
                  <div class="flex items-center gap-2">
                    <div :class="[
                      'w-3 h-3 rounded-full',
                      isDetecting ? 'bg-green-500 animate-pulse' : 'bg-gray-400'
                    ]"></div>
                    <span class="text-sm">
                      {{ isDetecting ? 'Detecting signs...' : 'Detection paused' }}
                    </span>
                  </div>
                  
                  <!-- Camera Status -->
                  <div class="flex items-center gap-2">
                    <div :class="[
                      'w-3 h-3 rounded-full',
                      isStreaming ? 'bg-blue-500' : 'bg-gray-400'
                    ]"></div>
                    <span class="text-sm">
                      {{ isStreaming ? 'Camera active' : 'Camera inactive' }}
                    </span>
                  </div>
                  
                  <!-- Error Display -->
                  <div v-if="detectionError || cameraError" class="p-3 bg-red-50 dark:bg-red-900/20 rounded-lg">
                    <div class="flex items-center gap-2 text-red-600 dark:text-red-400">
                      <AlertCircle class="h-4 w-4" />
                      <span class="text-sm font-medium">Error:</span>
                    </div>
                    <p class="text-sm text-red-600 dark:text-red-400 mt-1">
                      {{ detectionError || cameraError }}
                    </p>
                  </div>
                  
                  <!-- Detection Result -->
                  <div v-if="detectedLetter" class="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                    <div class="text-center">
                      <div 
                        :class="[
                          'w-16 h-16 mx-auto mb-3 rounded-full flex items-center justify-center text-white text-2xl font-bold shadow-lg',
                          getLetterColor(detectedLetter)
                        ]"
                      >
                        {{ detectedLetter }}
                      </div>
                      <p class="font-semibold text-green-800 dark:text-green-200 mb-2">
                        Detected: {{ detectedLetter }}
                      </p>
                      <p class="text-sm text-green-600 dark:text-green-400 mb-3">
                        Confidence: {{ Math.round(detectionConfidence) }}%
                      </p>
                      <Button 
                        @click="practiceDetectedLetter"
                        size="sm"
                        class="w-full"
                      >
                        <Play class="h-4 w-4 mr-2" />
                        Watch Tutorial
                      </Button>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Instructions -->
              <div>
                <h3 class="text-lg font-semibold mb-3">Instructions</h3>
                <div class="space-y-2 text-sm text-gray-600 dark:text-gray-400">
                  <p>• Position your hand clearly in the camera circle</p>
                  <p>• Ensure good lighting for better detection</p>
                  <p>• Hold the sign steady for 2-3 seconds</p>
                  <p>• Try different letters from the dictionary</p>
                  <p>• Make sure your hand fills the guide circle</p>
                  <p>• Keep background simple and uncluttered</p>
                </div>
              </div>
              
              <!-- Debug Information -->
              <div>
                <Button 
                  @click="toggleDebugInfo" 
                  variant="outline" 
                  size="sm"
                  class="w-full mb-2"
                >
                  <Info class="h-4 w-4 mr-2" />
                  {{ showDebugInfo ? 'Hide' : 'Show' }} Debug Info
                </Button>
                
                <div v-if="showDebugInfo" class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
                  <h4 class="text-sm font-medium mb-2">Debug Information:</h4>
                  <div class="text-xs text-gray-600 dark:text-gray-400 space-y-1">
                    <p>Camera Streaming: {{ isStreaming ? 'Yes' : 'No' }}</p>
                    <p>Detection Active: {{ isDetecting ? 'Yes' : 'No' }}</p>
                    <p v-if="videoRef">Video Dimensions: {{ videoRef.videoWidth }}x{{ videoRef.videoHeight }}</p>
                    <p>Debug Info: {{ debugInfo || 'No debug info' }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Quick Actions -->
              <div class="space-y-2">
                <Button 
                  v-if="!isDetecting && isStreaming" 
                  @click="startDetection(videoRef!)" 
                  variant="outline" 
                  class="w-full"
                >
                  Start Detection
                </Button>
                <Button 
                  v-if="isDetecting" 
                  @click="stopDetection" 
                  variant="outline" 
                  class="w-full"
                >
                  Stop Detection
                </Button>
                <Button 
                  @click="closeCamera" 
                  variant="outline" 
                  class="w-full"
                >
                  Close Camera
                </Button>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>

    <!-- Search and View Controls -->
    <Card>
      <CardContent class="p-4">
        <div class="flex flex-col sm:flex-row gap-4 items-center">
          <!-- Search Input -->
          <div class="relative flex-1 w-full sm:w-auto">
            <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            <Input
              v-model="searchQuery"
              placeholder="Search letters..."
              class="pl-10 w-full"
            />
          </div>
          
          <!-- View Mode Toggle -->
          <div class="flex gap-2">
            <Button
              @click="viewMode = 'grid'"
              :variant="viewMode === 'grid' ? 'default' : 'outline'"
              size="sm"
              class="flex items-center gap-2"
            >
              <Grid class="h-4 w-4" />
              Grid
            </Button>
            <Button
              @click="viewMode = 'list'"
              :variant="viewMode === 'list' ? 'default' : 'outline'"
              size="sm"
              class="flex items-center gap-2"
            >
              <List class="h-4 w-4" />
              List
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>

    <!-- Dictionary Content -->
    <div v-if="filteredDictionaries.length > 0">
      <!-- Grid View -->
      <div 
        v-if="viewMode === 'grid'" 
        class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4"
      >
        <Card 
          v-for="item in filteredDictionaries" 
          :key="item.id" 
          class="group hover:shadow-lg transition-all duration-200 cursor-pointer border-2 hover:border-blue-300"
          @click="openSignVideo(item.link)"
        >
          <CardContent class="p-6 text-center">
            <div 
              :class="[
                'w-20 h-20 mx-auto mb-4 rounded-full flex items-center justify-center text-white text-3xl font-bold shadow-lg group-hover:scale-110 transition-transform duration-200',
                getLetterColor(item.title)
              ]"
            >
              {{ item.title }}
            </div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Letter {{ item.title }}
            </h3>
            <div class="flex items-center justify-center gap-2 text-blue-600 dark:text-blue-400">
              <Play class="h-4 w-4" />
              <span class="text-sm font-medium">Watch Video</span>
              <ExternalLink class="h-3 w-3" />
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- List View -->
      <div v-else class="space-y-3">
        <Card 
          v-for="item in filteredDictionaries" 
          :key="item.id" 
          class="group hover:shadow-md transition-all duration-200 cursor-pointer border hover:border-blue-300"
          @click="openSignVideo(item.link)"
        >
          <CardContent class="p-4">
            <div class="flex items-center gap-4">
              <div 
                :class="[
                  'w-12 h-12 rounded-full flex items-center justify-center text-white text-xl font-bold shadow-md group-hover:scale-110 transition-transform duration-200',
                  getLetterColor(item.title)
                ]"
              >
                {{ item.title }}
              </div>
              <div class="flex-1">
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                  Letter {{ item.title }}
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  Learn the sign for letter {{ item.title }}
                </p>
              </div>
              <div class="flex items-center gap-2 text-blue-600 dark:text-blue-400">
                <Play class="h-5 w-5" />
                <span class="font-medium">Watch Video</span>
                <ExternalLink class="h-4 w-4" />
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <Book class="h-16 w-16 mx-auto text-gray-400 mb-4" />
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        No letters found
      </h3>
      <p class="text-gray-600 dark:text-gray-400">
        Try adjusting your search query
      </p>
    </div>
  </div>
</template>
