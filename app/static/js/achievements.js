// Achievement Definitions
const ACHIEVEMENTS = {
    BEGINNER_HUNTER: {
        id: 'beginner_hunter',
        title: 'Beginner Hunter',
        description: 'Complete your first quest',
        icon: 'fa-scroll'
    },
    DEDICATED_HUNTER: {
        id: 'dedicated_hunter',
        title: 'Dedicated Hunter',
        description: 'Complete 10 quests',
        icon: 'fa-trophy'
    },
    MEDITATION_MASTER: {
        id: 'meditation_master',
        title: 'Meditation Master',
        description: 'Maintain a meditation streak of 7 days',
        icon: 'fa-om'
    },
    BOOKWORM: {
        id: 'bookworm',
        title: 'Bookworm',
        description: 'Read 5 books',
        icon: 'fa-book'
    },
    HABIT_FORMER: {
        id: 'habit_former',
        title: 'Habit Former',
        description: 'Complete 20 daily habits',
        icon: 'fa-check-double'
    },
    GOAL_ACHIEVER: {
        id: 'goal_achiever',
        title: 'Goal Achiever',
        description: 'Achieve 5 personal goals',
        icon: 'fa-flag'
    }
};

// Experience Points for Activities
const XP_REWARDS = {
    COMPLETE_QUEST: 100,
    MEDITATION_DAILY: 50,
    READ_BOOK: 150,
    COMPLETE_HABIT: 30,
    ACHIEVE_GOAL: 200
};

// Leveling System
const LEVEL_THRESHOLDS = [
    0,      // Level 1
    1000,   // Level 2
    2500,   // Level 3
    5000,   // Level 4
    8000,   // Level 5
    12000,  // Level 6
    17000,  // Level 7
    23000,  // Level 8
    30000,  // Level 9
    38000   // Level 10
];

// Hunter Ranks
const HUNTER_RANKS = {
    1: 'E-Rank Hunter',
    3: 'D-Rank Hunter',
    5: 'C-Rank Hunter',
    7: 'B-Rank Hunter',
    9: 'A-Rank Hunter',
    10: 'S-Rank Hunter'
};

// Achievement System
function checkAchievements(stats) {
    const earnedAchievements = [];

    // Check Quests Achievement
    if (stats.quests_completed === 1) {
        earnedAchievements.push(ACHIEVEMENTS.BEGINNER_HUNTER);
    } else if (stats.quests_completed === 10) {
        earnedAchievements.push(ACHIEVEMENTS.DEDICATED_HUNTER);
    }

    // Check Meditation Achievement
    if (stats.meditation_streak >= 7) {
        earnedAchievements.push(ACHIEVEMENTS.MEDITATION_MASTER);
    }

    // Check Books Achievement
    if (stats.books_read >= 5) {
        earnedAchievements.push(ACHIEVEMENTS.BOOKWORM);
    }

    // Check Habits Achievement
    if (stats.habits_completed >= 20) {
        earnedAchievements.push(ACHIEVEMENTS.HABIT_FORMER);
    }

    // Check Goals Achievement
    if (stats.goals_achieved >= 5) {
        earnedAchievements.push(ACHIEVEMENTS.GOAL_ACHIEVER);
    }

    return earnedAchievements;
}

// Level System
function checkLevelUp(currentXp, currentLevel) {
    let newLevel = currentLevel;
    
    for (let level = currentLevel + 1; level < LEVEL_THRESHOLDS.length; level++) {
        if (currentXp >= LEVEL_THRESHOLDS[level]) {
            newLevel = level;
        } else {
            break;
        }
    }
    
    if (newLevel > currentLevel) {
        const newRank = HUNTER_RANKS[newLevel] || HUNTER_RANKS[Object.keys(HUNTER_RANKS).reverse().find(key => key <= newLevel)];
        return {
            newLevel,
            newRank,
            leveledUp: true
        };
    }
    
    return { leveledUp: false };
}

// Show Achievement Animation
function showAchievementNotification(achievement) {
    window.dispatchEvent(new CustomEvent('showAchievement', {
        detail: {
            message: `${achievement.title} - ${achievement.description}`,
            type: 'achievement'
        }
    }));
}

// Show Level Up Animation
function showLevelUpNotification(newLevel, newRank) {
    window.dispatchEvent(new CustomEvent('showAchievement', {
        detail: {
            message: `Advanced to Level ${newLevel}${newRank ? ` - ${newRank}` : ''}!`,
            type: 'levelup'
        }
    }));
}

// Update Stats with Animation
function updateStats(stats) {
    // Check for achievements
    const newAchievements = checkAchievements(stats);
    newAchievements.forEach(achievement => {
        showAchievementNotification(achievement);
    });

    // Check for level up
    const levelInfo = checkLevelUp(stats.xp, stats.level);
    if (levelInfo.leveledUp) {
        showLevelUpNotification(levelInfo.newLevel, levelInfo.newRank);
    }

    // Update UI elements smoothly
    updateStatBars(stats);
}

// Smoothly animate stat bars
function updateStatBars(stats) {
    const bars = document.querySelectorAll('[data-stat-bar]');
    bars.forEach(bar => {
        const stat = bar.dataset.statBar;
        const value = stats[stat] || 0;
        bar.style.transition = 'width 0.5s ease-out';
        bar.style.width = `${value}%`;
    });
}

// Listen for achievement events
window.addEventListener('achievement-earned', (event) => {
    const { achievement } = event.detail;
    showAchievementNotification(achievement);
});

// Listen for level up events
window.addEventListener('level-up', (event) => {
    const { level, rank } = event.detail;
    showLevelUpNotification(level, rank);
});