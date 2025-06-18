<script setup lang="ts">
import { type BreadcrumbItem } from '@/types';
import { Link } from '@inertiajs/vue3';
import { BookOpen, Camera, User } from 'lucide-vue-next';

interface NavItem {
    label: string;
    href: string;
    icon: any;
}

const breadcrumbs: BreadcrumbItem[] = [
    {
        title: 'Home',
        href: '/',
    },
];

// Bottom‑navigation items
const navItems: NavItem[] = [
    {
        label: 'Practice',
        href: '/practice',
        icon: Camera,
    },
    {
        label: 'Dictionary',
        href: '/dictionary',
        icon: BookOpen,
    },
    {
        label: 'Profile',
        href: '/profile',
        icon: User,
    },
];
</script>

<template>
    <div class="flex min-h-screen flex-col">
        <!-- Page Content -->
        <main class="flex-1 p-6">
            <!-- Hero Section -->
            <section class="py-12 text-center">
                <h1 class="mb-4 text-4xl font-bold text-gray-900 dark:text-white">Sign Language Learning App</h1>
                <p class="mb-8 text-lg text-gray-600 dark:text-gray-300">Learn and practice sign language with interactive tools</p>
            </section>

            <!-- Feature Cards – hidden on mobile, visible on md↑ -->
            <section class="hidden gap-6 md:grid md:grid-cols-3">
                <!-- Camera Feature -->
                <div class="rounded-lg bg-white p-6 shadow-md transition-shadow hover:shadow-lg dark:bg-gray-800">
                    <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-blue-100 dark:bg-blue-900">
                        <Camera class="h-6 w-6 text-blue-600 dark:text-blue-400" />
                    </div>
                    <h3 class="mb-2 text-xl font-semibold text-gray-900 dark:text-white">Camera Practice</h3>
                    <p class="mb-4 text-gray-600 dark:text-gray-300">Practice sign language using the camera with real‑time feedback</p>
                    <Link
                        :href="'/practice'"
                        class="inline-flex w-full items-center justify-center rounded-md bg-blue-600 px-4 py-2 font-medium text-white transition-colors hover:bg-blue-700"
                    >
                        Start Practice
                    </Link>
                </div>

                <!-- Dictionary Feature -->
                <div class="rounded-lg bg-white p-6 shadow-md transition-shadow hover:shadow-lg dark:bg-gray-800">
                    <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-green-100 dark:bg-green-900">
                        <BookOpen class="h-6 w-6 text-green-600 dark:text-green-400" />
                    </div>
                    <h3 class="mb-2 text-xl font-semibold text-gray-900 dark:text-white">Dictionary</h3>
                    <p class="mb-4 text-gray-600 dark:text-gray-300">Browse a comprehensive sign‑language dictionary</p>
                    <Link
                        :href="'/dictionary'"
                        class="inline-flex w-full items-center justify-center rounded-md bg-green-600 px-4 py-2 font-medium text-white transition-colors hover:bg-green-700"
                    >
                        Browse Dictionary
                    </Link>
                </div>

                <!-- Profile Feature -->
                <div class="rounded-lg bg-white p-6 shadow-md transition-shadow hover:shadow-lg dark:bg-gray-800">
                    <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-purple-100 dark:bg-purple-900">
                        <User class="h-6 w-6 text-purple-600 dark:text-purple-400" />
                    </div>
                    <h3 class="mb-2 text-xl font-semibold text-gray-900 dark:text-white">Profile</h3>
                    <p class="mb-4 text-gray-600 dark:text-gray-300">Track progress and manage the learning journey</p>
                    <Link
                        :href="'/profile'"
                        class="inline-flex w-full items-center justify-center rounded-md bg-purple-600 px-4 py-2 font-medium text-white transition-colors hover:bg-purple-700"
                    >
                        View Profile
                    </Link>
                </div>
            </section>

            <!-- Quick Stats -->
            <section class="mt-8 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600 p-6 text-white">
                <h2 class="mb-4 text-2xl font-bold">Your Learning Progress</h2>
                <div class="grid gap-4 md:grid-cols-3">
                    <div class="text-center">
                        <div class="text-3xl font-bold">0</div>
                        <div class="text-blue-100">Signs Learned</div>
                    </div>
                    <div class="text-center">
                        <div class="text-3xl font-bold">0</div>
                        <div class="text-blue-100">Practice Sessions</div>
                    </div>
                    <div class="text-center">
                        <div class="text-3xl font-bold">0</div>
                        <div class="text-blue-100">Days Streak</div>
                    </div>
                </div>
            </section>
        </main>

        <!-- Mobile‑first Bottom Navigation -->
        <nav
            class="fixed inset-x-0 bottom-0 z-50 flex justify-around border-t border-gray-200 bg-white py-2 md:static md:py-0 dark:border-gray-700 dark:bg-gray-800"
        >
            <Link
                v-for="item in navItems"
                :key="item.label"
                :href="item.href"
                class="flex flex-col items-center gap-1 text-sm font-medium md:flex-row md:px-4 md:py-2"
            >
                <component :is="item.icon" class="h-6 w-6" />
                <span class="text-xs md:ml-2 md:text-base">{{ item.label }}</span>
            </Link>
        </nav>
    </div>
</template>
