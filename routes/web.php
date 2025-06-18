<?php

use Illuminate\Support\Facades\Route;
use Inertia\Inertia;

Route::get('/', function () {
    return Inertia::render('Home');
})->name('home');

Route::get('dashboard', function () {
    return Inertia::render('Dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

Route::get('dictionary', function () {
    return Inertia::render('DictionaryPage');
});

Route::get('profile', function () {
    return Inertia::render('ProfilePage');
});


require __DIR__.'/settings.php';
require __DIR__.'/auth.php';
