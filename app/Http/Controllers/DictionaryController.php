<?php

namespace App\Http\Controllers;

use App\Models\Dictionary;
use Illuminate\Http\Request;
use Inertia\Inertia;

class DictionaryController extends Controller
{
    public function index()
    {
        $dictionary = Dictionary::all();

        return Inertia::render('DictionaryPage', [
            'dictionaries' => $dictionary,
        ]);
    }
}
