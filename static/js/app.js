// Global JavaScript for LIFE RPG

async function apiFetch(url, options = {}) {
    // Default headers
    const headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': typeof csrfToken !== 'undefined' ? csrfToken : ''
    };
    
    // Add auth token if we transition fully to JWT, but since we use SessionAuth for templates:
    // This is primarily for endpoints that rely on Session authentication since it's a Django template app.
    
    const config = {
        ...options,
        headers: {
            ...headers,
            ...options.headers
        }
    };

    try {
        const response = await fetch(url, config);
        const data = await response.json().catch(() => ({}));
        
        if (!response.ok) {
            throw { status: response.status, data };
        }
        return data;
    } catch (error) {
        console.error("API Error:", error);
        throw error;
    }
}

// SoundManager (Web Audio API Synthesizer)
const SoundManager = {
    ctx: null,
    muted: false,
    init() {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        }
        if (window.USER_PREFS && window.USER_PREFS.reduced_motion) {
            this.muted = true;
        }
    },
    playTone(freq, type, duration, vol=0.1) {
        if (this.muted) return;
        if (!this.ctx) this.init();
        if (this.ctx.state === 'suspended') this.ctx.resume();
        
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);
        gain.gain.setValueAtTime(vol, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, this.ctx.currentTime + duration);
        osc.connect(gain);
        gain.connect(this.ctx.destination);
        osc.start();
        osc.stop(this.ctx.currentTime + duration);
    },
    playCoin() {
        this.playTone(987.77, 'sine', 0.1, 0.1); // B5
        setTimeout(() => this.playTone(1318.51, 'sine', 0.3, 0.1), 100); // E6
    },
    playLevelUp() {
        [523.25, 659.25, 783.99, 1046.50].forEach((freq, i) => {
            setTimeout(() => this.playTone(freq, 'square', 0.2, 0.1), i * 150);
        });
    },
    playHit() {
        this.playTone(100, 'sawtooth', 0.2, 0.2);
    },
    playEquip() {
        this.playTone(300, 'triangle', 0.1, 0.1);
        setTimeout(() => this.playTone(600, 'triangle', 0.2, 0.1), 50);
    }
};

// Reward Animation System
function showRewardAnimation(rewardData) {
    SoundManager.init();
    
    const overlay = document.getElementById('reward-overlay');
    const container = document.getElementById('reward-stats-container');
    const card = overlay.querySelector('.reward-card');
    
    container.innerHTML = '';
    
    // Play sounds
    if (rewardData.level_up) {
        SoundManager.playLevelUp();
        card.classList.add('shake');
        setTimeout(() => card.classList.remove('shake'), 500);
    } else {
        SoundManager.playCoin();
    }
    
    if (rewardData.level_up) {
        const lvlNode = document.createElement('div');
        lvlNode.className = 'reward-stat text-primary animate-popup';
        lvlNode.innerHTML = `LEVEL UP! <br><span style="font-size: 1.2rem;">LEVEL ${rewardData.new_level}</span>`;
        container.appendChild(lvlNode);
    }
    
    if (rewardData.xp_earned) {
        const xpNode = document.createElement('div');
        xpNode.className = 'reward-stat xp animate-popup';
        xpNode.style.animationDelay = '0.2s';
        xpNode.innerText = `+${rewardData.xp_earned} XP`;
        container.appendChild(xpNode);
    }
    
    if (rewardData.gold_earned) {
        const goldNode = document.createElement('div');
        goldNode.className = 'reward-stat gold animate-popup';
        goldNode.style.animationDelay = '0.4s';
        goldNode.innerText = `+${rewardData.gold_earned} GOLD`;
        container.appendChild(goldNode);
    }
    
    if (rewardData.attribute) {
        const attrNode = document.createElement('div');
        attrNode.className = 'reward-stat animate-popup';
        attrNode.style.color = 'var(--attr-int)';
        attrNode.style.animationDelay = '0.6s';
        attrNode.innerText = `+${rewardData.attribute_xp} ${rewardData.attribute}`;
        container.appendChild(attrNode);
    }
    
    overlay.classList.add('active');
    
    // Update global nav values
    const navXp = document.getElementById('nav-xp');
    const navGold = document.getElementById('nav-gold');
    if (navXp) navXp.innerText = rewardData.new_total_xp;
    if (navGold) {
        const currentGold = parseInt(navGold.innerText || '0');
        navGold.innerText = currentGold + rewardData.gold_earned;
    }
}

function closeRewardOverlay() {
    const overlay = document.getElementById('reward-overlay');
    overlay.classList.remove('active');
    window.location.reload();
}
