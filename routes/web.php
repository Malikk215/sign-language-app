<?php

use App\Http\Controllers\DictionaryController;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;
use App\Http\Controllers\SignLanguageController;

Route::get('/', function () {
    return Inertia::render('Home');
})->name('home');

Route::get('dashboard', function () {
    return Inertia::render('Dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

Route::get('dictionary', [DictionaryController::class, 'index']);

Route::get('/profile', function () {
    return Inertia::render('Profile');
})->name('profile');

// Add the practice route for camera functionality
Route::get('practice', function () {
    return Inertia::render('Camera');
});

require __DIR__.'/settings.php';
require __DIR__.'/auth.php';

Route::post('/api/predict-sign', [SignLanguageController::class, 'predict']);
Route::get('/api/accuracy-data', [SignLanguageController::class, 'getAccuracyData']);
