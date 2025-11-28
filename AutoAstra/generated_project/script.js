// Pomodoro Timer Script
// This script implements timer state management, UI updates, task handling, statistics persistence, and settings.

/* =============================
   1. State Management
   ============================= */
const timerState = {
    mode: 'focus', // 'focus' or 'break'
    focusDuration: 25 * 60, // seconds
    breakDuration: 5 * 60, // seconds
    remaining: 25 * 60, // seconds
    isRunning: false,
    completedPomodoros: 0,
    totalFocus: 0, // seconds
    totalBreak: 0, // seconds
    soundEnabled: true,
};

/* =============================
   2. DOM References
   ============================= */
const timeEl = document.getElementById('timeEl');
const progressRing = document.getElementById('progressRing'); // assumed <circle> element
const startPauseBtn = document.getElementById('startPauseBtn');
const resetBtn = document.getElementById('resetBtn');
const taskInput = document.getElementById('taskInput');
const taskList = document.getElementById('taskList');
const statsElements = {
    pomodoros: document.getElementById('statPomodoros'),
    focusTime: document.getElementById('statFocusTime'),
    breakTime: document.getElementById('statBreakTime'),
};
const settingsModal = document.getElementById('settingsModal');
const focusInput = document.getElementById('focusInput');
const breakInput = document.getElementById('breakInput');
const soundToggle = document.getElementById('soundToggle');
const settingsBtn = document.getElementById('settingsBtn');

/* =============================
   3. Sound Handling
   ============================= */
const startSound = new Audio('assets/start.mp3');
const endSound = new Audio('assets/end.mp3');

function playSound(type) {
    if (!timerState.soundEnabled) return;
    if (type === 'start') {
        startSound.currentTime = 0;
        startSound.play();
    } else if (type === 'end') {
        endSound.currentTime = 0;
        endSound.play();
    }
}

/* =============================
   4. Timer Functions
   ============================= */
let intervalId = null;

function startTimer() {
    if (timerState.isRunning) return;
    timerState.isRunning = true;
    startPauseBtn.textContent = 'Pause';
    playSound('start');
    intervalId = setInterval(tick, 1000);
}

function pauseTimer() {
    if (!timerState.isRunning) return;
    timerState.isRunning = false;
    startPauseBtn.textContent = 'Start';
    clearInterval(intervalId);
    intervalId = null;
}

function resetTimer() {
    pauseTimer();
    // Reset remaining based on current mode
    timerState.remaining = timerState.mode === 'focus' ? timerState.focusDuration : timerState.breakDuration;
    updateTimeDisplay();
    updateProgressRing();
}

function tick() {
    if (timerState.remaining > 0) {
        timerState.remaining--;
        // Accumulate total time for stats
        if (timerState.mode === 'focus') {
            timerState.totalFocus++;
        } else {
            timerState.totalBreak++;
        }
        updateTimeDisplay();
        updateProgressRing();
    } else {
        // Mode finished
        playSound('end');
        if (timerState.mode === 'focus') {
            timerState.completedPomodoros++;
        }
        switchMode();
    }
}

/* =============================
   5. Mode Transition
   ============================= */
function switchMode() {
    // Toggle mode
    timerState.mode = timerState.mode === 'focus' ? 'break' : 'focus';
    // Set remaining to appropriate duration
    timerState.remaining = timerState.mode === 'focus' ? timerState.focusDuration : timerState.breakDuration;
    // Update UI colors via CSS variable
    const modeColor = timerState.mode === 'focus' ? '#ff6b6b' : '#4ecca3'; // example colors
    document.documentElement.style.setProperty('--mode-color', modeColor);
    // Reset progress ring animation (handled in updateProgressRing)
    updateTimeDisplay();
    updateProgressRing();
    // Persist stats after a mode change
    saveStats();
}

/* =============================
   6. UI Update Functions
   ============================= */
function formatTime(seconds) {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}

function updateTimeDisplay() {
    if (timeEl) timeEl.textContent = formatTime(timerState.remaining);
}

function updateProgressRing() {
    if (!progressRing) return;
    const radius = progressRing.r.baseVal.value;
    const circumference = 2 * Math.PI * radius;
    const duration = timerState.mode === 'focus' ? timerState.focusDuration : timerState.breakDuration;
    const offset = circumference * (1 - timerState.remaining / duration);
    progressRing.style.strokeDasharray = `${circumference} ${circumference}`;
    progressRing.style.strokeDashoffset = offset;
}

function updateStatsPanel() {
    if (!statsElements) return;
    if (statsElements.pomodoros) statsElements.pomodoros.textContent = timerState.completedPomodoros;
    if (statsElements.focusTime) statsElements.focusTime.textContent = formatTime(timerState.totalFocus);
    if (statsElements.breakTime) statsElements.breakTime.textContent = formatTime(timerState.totalBreak);
}

/* =============================
   7. Task List Management
   ============================= */
function loadTasks() {
    const stored = localStorage.getItem('pomodoroTasks');
    let tasks = [];
    try {
        tasks = stored ? JSON.parse(stored) : [];
    } catch (e) {
        console.error('Failed to parse tasks from localStorage', e);
        tasks = [];
    }
    taskList.innerHTML = '';
    tasks.forEach(renderTask);
}

function saveTasks(tasks) {
    localStorage.setItem('pomodoroTasks', JSON.stringify(tasks));
}

function renderTask(task) {
    const li = document.createElement('li');
    li.dataset.id = task.id;
    li.className = task.completed ? 'completed' : '';
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.checked = task.completed;
    checkbox.addEventListener('change', () => toggleTask(task.id));
    const span = document.createElement('span');
    span.textContent = task.text;
    const removeBtn = document.createElement('button');
    removeBtn.textContent = '✕';
    removeBtn.addEventListener('click', () => removeTask(task.id));
    li.appendChild(checkbox);
    li.appendChild(span);
    li.appendChild(removeBtn);
    taskList.appendChild(li);
}

function addTask(text) {
    if (!text) return;
    const tasks = getTasks();
    const newTask = { id: Date.now(), text, completed: false };
    tasks.push(newTask);
    saveTasks(tasks);
    renderTask(newTask);
    taskInput.value = '';
}

function toggleTask(id) {
    const tasks = getTasks();
    const task = tasks.find(t => t.id === id);
    if (!task) return;
    task.completed = !task.completed;
    saveTasks(tasks);
    loadTasks(); // re-render list
}

function removeTask(id) {
    let tasks = getTasks();
    tasks = tasks.filter(t => t.id !== id);
    saveTasks(tasks);
    loadTasks();
}

function getTasks() {
    const stored = localStorage.getItem('pomodoroTasks');
    try {
        return stored ? JSON.parse(stored) : [];
    } catch (e) {
        console.error('Failed to parse tasks', e);
        return [];
    }
}

/* =============================
   8. Statistics Persistence
   ============================= */
function loadStats() {
    const stored = localStorage.getItem('pomodoroStats');
    if (!stored) return;
    try {
        const data = JSON.parse(stored);
        timerState.completedPomodoros = data.completedPomodoros || 0;
        timerState.totalFocus = data.totalFocus || 0;
        timerState.totalBreak = data.totalBreak || 0;
    } catch (e) {
        console.error('Failed to load stats', e);
    }
    updateStatsPanel();
}

function saveStats() {
    const data = {
        completedPomodoros: timerState.completedPomodoros,
        totalFocus: timerState.totalFocus,
        totalBreak: timerState.totalBreak,
    };
    localStorage.setItem('pomodoroStats', JSON.stringify(data));
}

/* =============================
   9. Settings Modal
   ============================= */
function openSettings() {
    if (settingsModal) settingsModal.style.display = 'block';
    // Populate inputs with current values
    if (focusInput) focusInput.value = timerState.focusDuration / 60;
    if (breakInput) breakInput.value = timerState.breakDuration / 60;
    if (soundToggle) soundToggle.checked = timerState.soundEnabled;
}

function closeSettings() {
    if (settingsModal) settingsModal.style.display = 'none';
}

function saveSettings() {
    const focusVal = parseInt(focusInput.value, 10);
    const breakVal = parseInt(breakInput.value, 10);
    if (!isNaN(focusVal) && focusVal > 0) {
        timerState.focusDuration = focusVal * 60;
    }
    if (!isNaN(breakVal) && breakVal > 0) {
        timerState.breakDuration = breakVal * 60;
    }
    timerState.soundEnabled = soundToggle.checked;
    // Persist settings
    localStorage.setItem('pomodoroSettings', JSON.stringify({
        focusDuration: timerState.focusDuration,
        breakDuration: timerState.breakDuration,
        soundEnabled: timerState.soundEnabled,
    }));
    // Apply new remaining time if timer not running
    if (!timerState.isRunning) {
        timerState.remaining = timerState.mode === 'focus' ? timerState.focusDuration : timerState.breakDuration;
        updateTimeDisplay();
        updateProgressRing();
    }
    closeSettings();
}

function loadSettings() {
    const stored = localStorage.getItem('pomodoroSettings');
    if (!stored) return;
    try {
        const data = JSON.parse(stored);
        if (typeof data.focusDuration === 'number') timerState.focusDuration = data.focusDuration;
        if (typeof data.breakDuration === 'number') timerState.breakDuration = data.breakDuration;
        if (typeof data.soundEnabled === 'boolean') timerState.soundEnabled = data.soundEnabled;
    } catch (e) {
        console.error('Failed to load settings', e);
    }
    // Ensure remaining aligns with possibly loaded durations
    timerState.remaining = timerState.mode === 'focus' ? timerState.focusDuration : timerState.breakDuration;
}

/* =============================
   10. Gradient by Time
   ============================= */
function setGradientByTime() {
    const hour = new Date().getHours();
    // Simple example: morning (5-12) light, afternoon (12-18) warm, night (18-5) dark
    let gradient = '';
    if (hour >= 5 && hour < 12) {
        gradient = 'linear-gradient(to right, #ff9a9e, #fad0c4)';
    } else if (hour >= 12 && hour < 18) {
        gradient = 'linear-gradient(to right, #a1c4fd, #c2e9fb)';
    } else {
        gradient = 'linear-gradient(to right, #434343, #000000)';
    }
    document.body.style.background = gradient;
}

/* =============================
   11. Initialization
   ============================= */
function init() {
    // Load persisted data
    loadSettings();
    loadStats();
    loadTasks();
    setGradientByTime();
    // Initial UI sync
    updateTimeDisplay();
    updateProgressRing();
    updateStatsPanel();
    // Event listeners
    if (startPauseBtn) {
        startPauseBtn.addEventListener('click', () => {
            timerState.isRunning ? pauseTimer() : startTimer();
        });
    }
    if (resetBtn) {
        resetBtn.addEventListener('click', resetTimer);
    }
    if (taskInput) {
        taskInput.addEventListener('keypress', e => {
            if (e.key === 'Enter') {
                addTask(taskInput.value.trim());
            }
        });
    }
    if (settingsBtn) {
        settingsBtn.addEventListener('click', openSettings);
    }
    // Assuming modal has close button with class 'close-modal'
    const closeModalBtn = settingsModal ? settingsModal.querySelector('.close-modal') : null;
    if (closeModalBtn) closeModalBtn.addEventListener('click', closeSettings);
    // Save settings button inside modal
    const saveSettingsBtn = settingsModal ? settingsModal.querySelector('.save-settings') : null;
    if (saveSettingsBtn) saveSettingsBtn.addEventListener('click', saveSettings);
    // Ensure progress ring has proper dasharray initially
    if (progressRing) {
        const radius = progressRing.r.baseVal.value;
        const circumference = 2 * Math.PI * radius;
        progressRing.style.strokeDasharray = `${circumference} ${circumference}`;
        progressRing.style.strokeDashoffset = circumference;
    }
}

document.addEventListener('DOMContentLoaded', init);
