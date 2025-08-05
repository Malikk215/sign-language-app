<script setup lang="ts">
import { ref, computed } from 'vue'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Separator } from '@/components/ui/separator'
import { User, Mail, Calendar, Trophy, Target, Clock, Edit, Save, X } from 'lucide-vue-next'
import { useInitials } from '@/composables/useInitials'

// Mock user data - replace with actual user data from props/API
const user = ref({
  name: 'John Doe',
  email: 'john.doe@example.com',
  joinDate: '2024-01-15',
  avatar: null,
  bio: 'Learning sign language to communicate better with the deaf community.'
})

// Learning statistics - replace with actual data
const stats = ref({
  signsLearned: 15,
  totalSigns: 26,
  practiceHours: 24,
  currentStreak: 7,
  longestStreak: 12,
  practiceSessionsCompleted: 45
})

// Achievements - replace with actual data
const achievements = ref([
  { id: 1, title: 'First Steps', description: 'Completed your first practice session', earned: true, date: '2024-01-16' },
  { id: 2, title: 'Week Warrior', description: 'Practiced for 7 consecutive days', earned: true, date: '2024-01-22' },
  { id: 3, title: 'Alphabet Master', description: 'Learned all 26 letters', earned: false, progress: 15 },
  { id: 4, title: 'Speed Demon', description: 'Complete 10 signs in under 30 seconds', earned: false, progress: 0 },
  { id: 5, title: 'Dedicated Learner', description: 'Practice for 30 days straight', earned: false, progress: 7 }
])

const isEditing = ref(false)
const editForm = ref({ ...user.value })

const initials = computed(() => useInitials(user.value.name))
const progressPercentage = computed(() => Math.round((stats.value.signsLearned / stats.value.totalSigns) * 100))
const earnedAchievements = computed(() => achievements.value.filter(a => a.earned))
const upcomingAchievements = computed(() => achievements.value.filter(a => !a.earned))

const startEditing = () => {
  isEditing.value = true
  editForm.value = { ...user.value }
}

const cancelEditing = () => {
  isEditing.value = false
  editForm.value = { ...user.value }
}

const saveProfile = () => {
  // Here you would typically make an API call to save the profile
  user.value = { ...editForm.value }
  isEditing.value = false
  // Show success message
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<template>
  <div class="container mx-auto p-6 space-y-6">
    <!-- Page Header -->
    <div class="flex items-center gap-3 mb-6">
      <User class="h-8 w-8 text-blue-600" />
      <div>
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">Profile</h1>
        <p class="text-gray-600 dark:text-gray-400">Manage your account and track your progress</p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Profile Information -->
      <div class="lg:col-span-1">
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center justify-between">
              Profile Information
              <Button
                v-if="!isEditing"
                @click="startEditing"
                variant="ghost"
                size="sm"
              >
                <Edit class="h-4 w-4" />
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent class="space-y-6">
            <!-- Avatar -->
            <div class="flex flex-col items-center space-y-4">
              <Avatar class="h-24 w-24">
                <AvatarImage :src="user.avatar" :alt="user.name" />
                <AvatarFallback class="text-2xl">{{ initials }}</AvatarFallback>
              </Avatar>
              <Button v-if="isEditing" variant="outline" size="sm">
                Change Photo
              </Button>
            </div>

            <!-- Profile Form -->
            <div class="space-y-4">
              <div class="space-y-2">
                <Label for="name">Name</Label>
                <Input
                  v-if="isEditing"
                  id="name"
                  v-model="editForm.name"
                  placeholder="Enter your name"
                />
                <p v-else class="text-sm font-medium">{{ user.name }}</p>
              </div>

              <div class="space-y-2">
                <Label for="email">Email</Label>
                <Input
                  v-if="isEditing"
                  id="email"
                  v-model="editForm.email"
                  type="email"
                  placeholder="Enter your email"
                />
                <p v-else class="text-sm text-gray-600 dark:text-gray-400">{{ user.email }}</p>
              </div>

              <div class="space-y-2">
                <Label for="bio">Bio</Label>
                <textarea
                  v-if="isEditing"
                  id="bio"
                  v-model="editForm.bio"
                  class="flex min-h-[80px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                  placeholder="Tell us about yourself..."
                ></textarea>
                <p v-else class="text-sm text-gray-600 dark:text-gray-400">{{ user.bio }}</p>
              </div>

              <div class="flex items-center gap-2 text-sm text-gray-500">
                <Calendar class="h-4 w-4" />
                <span>Joined {{ formatDate(user.joinDate) }}</span>
              </div>
            </div>

            <!-- Action Buttons -->
            <div v-if="isEditing" class="flex gap-2">
              <Button @click="saveProfile" class="flex-1">
                <Save class="h-4 w-4 mr-2" />
                Save Changes
              </Button>
              <Button @click="cancelEditing" variant="outline">
                <X class="h-4 w-4" />
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      <!-- Statistics and Progress -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Learning Progress -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <Target class="h-5 w-5" />
              Learning Progress
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-4">
              <!-- Overall Progress -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <span class="text-sm font-medium">Signs Learned</span>
                  <span class="text-sm text-gray-600">{{ stats.signsLearned }}/{{ stats.totalSigns }}</span>
                </div>
                <div class="w-full bg-gray-200 rounded-full h-2 dark:bg-gray-700">
                  <div 
                    class="bg-blue-600 h-2 rounded-full transition-all duration-300" 
                    :style="{ width: `${progressPercentage}%` }"
                  ></div>
                </div>
                <p class="text-xs text-gray-500 mt-1">{{ progressPercentage }}% Complete</p>
              </div>

              <!-- Stats Grid -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
                <div class="text-center p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <div class="text-2xl font-bold text-blue-600">{{ stats.practiceHours }}</div>
                  <div class="text-sm text-blue-600">Practice Hours</div>
                </div>
                <div class="text-center p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <div class="text-2xl font-bold text-green-600">{{ stats.currentStreak }}</div>
                  <div class="text-sm text-green-600">Current Streak</div>
                </div>
                <div class="text-center p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
                  <div class="text-2xl font-bold text-purple-600">{{ stats.longestStreak }}</div>
                  <div class="text-sm text-purple-600">Longest Streak</div>
                </div>
                <div class="text-center p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg">
                  <div class="text-2xl font-bold text-orange-600">{{ stats.practiceSessionsCompleted }}</div>
                  <div class="text-sm text-orange-600">Sessions</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <!-- Achievements -->
        <Card>
          <CardHeader>
            <CardTitle class="flex items-center gap-2">
              <Trophy class="h-5 w-5" />
              Achievements
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div class="space-y-6">
              <!-- Earned Achievements -->
              <div>
                <h3 class="text-lg font-semibold mb-3">Earned ({{ earnedAchievements.length }})</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                  <div
                    v-for="achievement in earnedAchievements"
                    :key="achievement.id"
                    class="flex items-center gap-3 p-3 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800"
                  >
                    <Trophy class="h-8 w-8 text-yellow-600" />
                    <div class="flex-1">
                      <h4 class="font-medium text-yellow-900 dark:text-yellow-100">{{ achievement.title }}</h4>
                      <p class="text-sm text-yellow-700 dark:text-yellow-300">{{ achievement.description }}</p>
                      <p class="text-xs text-yellow-600 dark:text-yellow-400 mt-1">Earned {{ formatDate(achievement.date) }}</p>
                    </div>
                  </div>
                </div>
              </div>

              <Separator />

              <!-- Upcoming Achievements -->
              <div>
                <h3 class="text-lg font-semibold mb-3">In Progress ({{ upcomingAchievements.length }})</h3>
                <div class="space-y-3">
                  <div
                    v-for="achievement in upcomingAchievements"
                    :key="achievement.id"
                    class="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-800 rounded-lg"
                  >
                    <div class="h-8 w-8 rounded-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center">
                      <Trophy class="h-4 w-4 text-gray-600 dark:text-gray-400" />
                    </div>
                    <div class="flex-1">
                      <h4 class="font-medium text-gray-900 dark:text-gray-100">{{ achievement.title }}</h4>
                      <p class="text-sm text-gray-600 dark:text-gray-400">{{ achievement.description }}</p>
                      <div v-if="achievement.progress !== undefined" class="mt-2">
                        <div class="flex justify-between items-center mb-1">
                          <span class="text-xs text-gray-500">Progress</span>
                          <span class="text-xs text-gray-500">{{ achievement.progress }}/{{ achievement.id === 3 ? 26 : achievement.id === 4 ? 10 : 30 }}</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-1.5 dark:bg-gray-700">
                          <div 
                            class="bg-blue-600 h-1.5 rounded-full transition-all duration-300" 
                            :style="{ width: `${(achievement.progress / (achievement.id === 3 ? 26 : achievement.id === 4 ? 10 : 30)) * 100}%` }"
                          ></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  </div>
</template>