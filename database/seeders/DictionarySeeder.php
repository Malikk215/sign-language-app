<?php

namespace Database\Seeders;

use App\Models\Dictionary;
use Illuminate\Database\Seeder;

class DictionarySeeder extends Seeder
{
    public function run(): void
    {
        $letters = [
            ['title' => 'A', 'link' => 'https://www.youtube.com/watch?v=example_A'],
            ['title' => 'B', 'link' => 'https://www.youtube.com/watch?v=example_B'],
            ['title' => 'C', 'link' => 'https://www.youtube.com/watch?v=example_C'],
            ['title' => 'D', 'link' => 'https://www.youtube.com/watch?v=example_D'],
            ['title' => 'E', 'link' => 'https://www.youtube.com/watch?v=example_E'],
            ['title' => 'F', 'link' => 'https://www.youtube.com/watch?v=example_F'],
            ['title' => 'G', 'link' => 'https://www.youtube.com/watch?v=example_G'],
            ['title' => 'H', 'link' => 'https://www.youtube.com/watch?v=example_H'],
            ['title' => 'I', 'link' => 'https://www.youtube.com/watch?v=example_I'],
            ['title' => 'J', 'link' => 'https://www.youtube.com/watch?v=example_J'],
            ['title' => 'K', 'link' => 'https://www.youtube.com/watch?v=example_K'],
            ['title' => 'L', 'link' => 'https://www.youtube.com/watch?v=example_L'],
            ['title' => 'M', 'link' => 'https://www.youtube.com/watch?v=example_M'],
            ['title' => 'N', 'link' => 'https://www.youtube.com/watch?v=example_N'],
            ['title' => 'O', 'link' => 'https://www.youtube.com/watch?v=example_O'],
            ['title' => 'P', 'link' => 'https://www.youtube.com/watch?v=example_P'],
            ['title' => 'Q', 'link' => 'https://www.youtube.com/watch?v=example_Q'],
            ['title' => 'R', 'link' => 'https://www.youtube.com/watch?v=example_R'],
            ['title' => 'S', 'link' => 'https://www.youtube.com/watch?v=example_S'],
            ['title' => 'T', 'link' => 'https://www.youtube.com/watch?v=example_T'],
            ['title' => 'U', 'link' => 'https://www.youtube.com/watch?v=example_U'],
            ['title' => 'V', 'link' => 'https://www.youtube.com/watch?v=example_V'],
            ['title' => 'W', 'link' => 'https://www.youtube.com/watch?v=example_W'],
            ['title' => 'X', 'link' => 'https://www.youtube.com/watch?v=example_X'],
            ['title' => 'Y', 'link' => 'https://www.youtube.com/watch?v=example_Y'],
            ['title' => 'Z', 'link' => 'https://www.youtube.com/watch?v=example_Z'],
        ];

        foreach ($letters as $letter) {
            Dictionary::create($letter);
        }
    }
}
