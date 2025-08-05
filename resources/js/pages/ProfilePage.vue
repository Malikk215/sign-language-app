
<script setup lang="ts">
import { ref, computed } from 'vue';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Button } from '@/components/ui/button';
import { User, History, Calendar, Award } from 'lucide-vue-next';

interface UserProfile {
  name: string;
  email: string;
  avatar?: string;
  joinDate: string;
  totalPracticed: number;
}

interface HistoryItem {
  letter: string;
  practicedAt: Date;
  accuracy: number;
}

const user = ref<UserProfile>({
  name: 'John Doe',
  email: 'johndoe@example.com',
  joinDate: '2024-01-15',
  totalPracticed: 25,
});

const practiceHistory = ref<HistoryItem[]>([
  { letter: 'A', practicedAt: new Date('2024-01-20'), accuracy: 95 },
  { letter: 'B', practicedAt: new Date('2024-01-21'), accuracy: 88 },
  { letter: 'D', practicedAt: new Date('2024-01-22'), accuracy: 92 },
  { letter: 'F', practicedAt: new Date('2024-01-23'), accuracy: 85 },
  { letter: 'G', practicedAt: new Date('2024-01-24'), accuracy: 90 },
]);

const triedAlphabets = computed(() => {
  return [...new Set(practiceHistory.value.map(item => item.letter))].sort();
});

const averageAccuracy = computed(() => {
  if (practiceHistory.value.length === 0) return 0;
  const total = practiceHistory.value.reduce((sum, item) => sum + item.accuracy, 0);
  return Math.round(total / practiceHistory.value.length);
});

const getInitials = (name: string) => {
  return name.split(' ').map(n => n[0]).join('').toUpperCase();
};

const getAccuracyColor = (accuracy: number) => {
  if (accuracy >= 90) return 'bg-green-500';
  if (accuracy >= 80) return 'bg-yellow-500';
  return 'bg-red-500';
};

const formatDate = (date: Date) => {
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
};
</script>

<template>
  <div class="container mx-auto p-6 space-y-6">
    <!-- Page Header -->
    <div class="flex items-center gap-3 mb-6">
      <User class="h-8 w-8 text-blue-600" />
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Profile</h1>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- User Profile Section -->
      <div class="lg:col-span-1">
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <User class="h-5 w-5" />
              User Profile
            </CardTitle>
          </CardHeader>
          <CardContent class="space-y-4">
            <div class="flex flex-col items-center text-center">
              <Avatar class="h-20 w-20 mb-4">
                <AvatarImage :src="user.avatar" :alt="user.name" />
                <AvatarFallback class="text-lg font-semibold">
                  {{ getInitials(user.name) }}
                </AvatarFallback>
              </Avatar>
              <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                {{ user.name }}
              </h3>
              <p class="text-gray-600 dark:text-gray-400">
                {{ user.email }}
              </p>
            </div>
            
            <div class="space-y-3 pt-4 border-t">
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400 flex items-center gap-2">
                  <Calendar class="h-4 w-4" />
                  Joined
                </span>
                <span class="text-sm font-medium">{{ formatDate(new Date(user.joinDate)) }}</span>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400 flex items-center gap-2">
                  <Award class="h-4 w-4" />
                  Total Practiced
                </span>
                <Badge variant="secondary">{{ user.totalPracticed }} letters</Badge>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-600 dark:text-gray-400">Average Accuracy</span>
                <Badge :class="getAccuracyColor(averageAccuracy)" class="text-white">
                  {{ averageAccuracy }}%
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- History and Statistics Section -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Alphabets Tried Overview -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <History class="h-5 w-5" />
              Alphabets Practiced ({{ triedAlphabets.length }}/26)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div class="flex flex-wrap gap-2">
              <Badge
                v-for="letter in triedAlphabets"
                :key="letter"
                variant="default"
                class="text-lg px-3 py-1 bg-blue-600 hover:bg-blue-700 text-white"
              >
                {{ letter }}
              </Badge>
            </div>
            <div class="mt-4 text-sm text-gray-600 dark:text-gray-400">
              Progress: {{ Math.round((triedAlphabets.length / 26) * 100) }}% complete
            </div>
          </CardContent>
        </Card>

        <!-- Detailed Practice History -->
        <Card>
          <CardHeader>
            <CardTitle>Recent Practice History</CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-3">
              <div
                v-for="(item, index) in practiceHistory.slice().reverse()"
                :key="index"
                class="flex items-center justify-between p-3 rounded-lg border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800 transition-colors"
              >
                <div class="flex items-center gap-3">
                  <Badge variant="outline" class="text-lg font-bold w-10 h-10 flex items-center justify-center">
                    {{ item.letter }}
                  </Badge>
                  <div>
                    <p class="font-medium text-gray-900 dark:text-white">
                      Letter {{ item.letter }}
                    </p>
                    <p class="text-sm text-gray-600 dark:text-gray-400">
                      {{ formatDate(item.practicedAt) }}
                    </p>
                  </div>
                </div>
                <Badge :class="getAccuracyColor(item.accuracy)" class="text-white">
                  {{ item.accuracy }}%
                </Badge>
              </div>
            </div>
            
            <div v-if="practiceHistory.length === 0" class="text-center py-8 text-gray-500 dark:text-gray-400">
              <History class="h-12 w-12 mx-auto mb-4 opacity-50" />
              <p>No practice history yet</p>
              <p class="text-sm">Start practicing to see your progress here!</p>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>
aza1qa1q5``a1qq1zd9