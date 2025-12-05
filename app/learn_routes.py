"""
Learn & Explore Routes
Personal development learning paths, quotes, patterns, and approaches.
"""

from flask import Blueprint, render_template
from flask_login import login_required

learn_bp = Blueprint('learn', __name__)


# Learning content data
LEARNING_CONTENT = {
    'quotes': [
        {
            'text': 'The only way to do great work is to love what you do.',
            'author': 'Steve Jobs',
            'category': 'Motivation'
        },
        {
            'text': 'Success is not final, failure is not fatal.',
            'author': 'Winston Churchill',
            'category': 'Resilience'
        },
        {
            'text': 'The best time to plant a tree was 20 years ago. The second best time is now.',
            'author': 'Chinese Proverb',
            'category': 'Growth'
        },
        {
            'text': 'Quality is not an act, it is a habit.',
            'author': 'Aristotle',
            'category': 'Excellence'
        },
        {
            'text': 'Your body keeps accurate account of all your thoughts.',
            'author': 'Deepak Chopra',
            'category': 'Mindfulness'
        },
        {
            'text': 'The future depends on what you do today.',
            'author': 'Mahatma Gandhi',
            'category': 'Action'
        },
    ],
    'approaches': [
        {
            'name': '5-Hour Rule',
            'description': 'Dedicate 5 hours every week to deliberate learning and skill development.',
            'icon': 'fa-clock',
            'tags': ['time-management', 'learning']
        },
        {
            'name': 'Atomic Habits',
            'description': 'Small, consistent habits compound over time to create major change.',
            'icon': 'fa-puzzle-piece',
            'tags': ['habits', 'growth']
        },
        {
            'name': 'The Pomodoro Technique',
            'description': 'Work in focused 25-minute intervals with 5-minute breaks.',
            'icon': 'fa-hourglass-half',
            'tags': ['productivity', 'focus']
        },
        {
            'name': 'Deep Work',
            'description': 'Engage in focused, distraction-free work on cognitively demanding tasks.',
            'icon': 'fa-brain',
            'tags': ['focus', 'quality']
        },
        {
            'name': 'Deliberate Practice',
            'description': 'Practice with clear goals, immediate feedback, and sustained effort.',
            'icon': 'fa-dumbbell',
            'tags': ['practice', 'mastery']
        },
    ],
    'patterns': [
        {
            'name': 'The 80/20 Rule (Pareto Principle)',
            'description': '80% of results come from 20% of efforts. Focus on high-impact activities.',
            'application': 'Identify and focus on the vital few tasks that drive most results.'
        },
        {
            'name': 'Systems Thinking',
            'description': 'View interconnected elements as a whole system rather than isolated parts.',
            'application': 'Design habit systems, not individual habits. Build supporting structures.'
        },
        {
            'name': 'Progressive Overload',
            'description': 'Gradually increase challenge to continue growth and prevent plateaus.',
            'application': 'Slowly increase difficulty, complexity, or volume of your quests.'
        },
        {
            'name': 'The Compounding Effect',
            'description': 'Small improvements compound exponentially over time.',
            'application': '1% daily improvement = 37x better in a year.'
        },
    ],
    'rules': [
        {
            'title': 'Rule #1: Show Up Consistently',
            'description': 'Consistency beats intensity. Small, regular actions are better than sporadic bursts.',
            'icon': 'fa-check-circle'
        },
        {
            'title': 'Rule #2: Track Your Progress',
            'description': 'What gets measured gets managed. Use metrics and streaks to stay accountable.',
            'icon': 'fa-chart-line'
        },
        {
            'title': 'Rule #3: Embrace the Struggle',
            'description': 'Discomfort is a sign of growth. Push beyond your comfort zone strategically.',
            'icon': 'fa-mountain'
        },
        {
            'title': 'Rule #4: Reflect and Adjust',
            'description': 'Regular reflection helps you learn from your journey and adapt your approach.',
            'icon': 'fa-mirror'
        },
        {
            'title': 'Rule #5: Focus on Systems, Not Goals',
            'description': 'Goals set direction; systems create momentum. Build the right habits.',
            'icon': 'fa-cogs'
        },
        {
            'title': 'Rule #6: Celebrate Small Wins',
            'description': 'Acknowledge progress along the way. Motivation comes from momentum.',
            'icon': 'fa-trophy'
        },
    ]
}


@learn_bp.route('/')
@login_required
def index():
    """Learn & Explore main page with quotes, approaches, patterns, and rules."""
    return render_template('learn_explore.html', 
                         content=LEARNING_CONTENT,
                         title='Learn & Explore')


@learn_bp.route('/quotes')
@login_required
def quotes():
    """Display inspirational quotes."""
    return render_template('learn/quotes.html',
                         quotes=LEARNING_CONTENT['quotes'],
                         title='Inspirational Quotes')


@learn_bp.route('/approaches')
@login_required
def approaches():
    """Display learning approaches and methodologies."""
    return render_template('learn/approaches.html',
                         approaches=LEARNING_CONTENT['approaches'],
                         title='Learning Approaches')


@learn_bp.route('/patterns')
@login_required
def patterns():
    """Display patterns and principles."""
    return render_template('learn/patterns.html',
                         patterns=LEARNING_CONTENT['patterns'],
                         title='Patterns & Principles')


@learn_bp.route('/rules')
@login_required
def rules():
    """Display personal development rules."""
    return render_template('learn/rules.html',
                         rules=LEARNING_CONTENT['rules'],
                         title='Personal Development Rules')
