# Hardcoded params used as seed inputs to run LDA and obtain nice output

r = 989  # Seed for reproducibility

smooth = 0.999  # Proportion of a single topic to split among initial seed words

genre_seed_words = [
    ('Adventure', [
        'demon',
        'evil',
        'hero',
        'journey',
        'king',
        'kingdom',
        'knight',
        'legend',
        'legendary',
        'magic',
        'magical',
        'quest',
        'sword',
        'warrior'
    ]),
    ('Mystery', [
        'blood',
        'crime',
        'criminal',
        'culprit',
        'detective',
        'ghost',
        'investigate',
        'investigation',
        'investigative',
        'investigator',
        'justice',
        'killer',
        'murder',
        'mystery',
        'mysterious',
        'police',
        'serial',
        'solve',
        'spirits',
        'supernatural',
        'witness',
        'youkai'
    ]),
    ('School', [
        'class',
        'classmate',
        'council',
        'high',
        'president',
        'school',
        'student',
        'teacher'
    ]),
    ('Sci-Fi', [
        'alien',
        'crew',
        'earth',
        'galaxy',
        'humanity',
        'planet',
        'robot',
        'space',
        'spaceship',
        'technological'
        'technology',
        'threat',
        'universe'
    ]),
    ('Slice of Life', [
        'boy',
        'boyfriend',
        'brother',
        'family',
        'father',
        'friend',
        'friendship',
        'girl',
        'girlfriend',
        'life',
        'love',
        'mother',
        'music',
        'parent',
        'sister',
        'summer'
    ]),
    ('Sports', [
        'baseball',
        'basketball',
        'champion',
        'competition',
        'competitive',
        'football',
        'game',
        'match',
        'national',
        'pitcher',
        'play',
        'player',
        'practice',
        'professional',
        'rival',
        'soccer',
        'team',
        'tournament',
        'training',
        'volleyball'
    ])
]
