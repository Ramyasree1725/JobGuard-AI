/**
 * JobGuard AI - Main UI & Controller Application
 * Manages Tab Navigation, Chart.js Visualizations, Sample Loading, Quiz Logic, and Report Generation.
 */

document.addEventListener('DOMContentLoaded', () => {
    initThemeToggle();
    initLanguageSwitcher();
    initAuthSystem();
    initSubscriptionSystem();
    initNavigation();
    initSampleSelector();
    initJobScanner();
    initOcrScanner();
    initOfferAuditor();
    initSalaryCalculator();
    initRecruiterChecker();
    initLookupEngine();
    initComplaintGenerator();
    initUserHistory();
    initQuiz();
    initScamBoard();
    initReportScam();
    lucide.createIcons();
});

// Global state
let currentAnalysisResult = null;
let radarChartInstance = null;

/**
 * Light / Dark Theme Controller (Default: Crisp White)
 */
function initThemeToggle() {
    const themeBtn = document.getElementById('btn-theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const savedTheme = localStorage.getItem('jobguard_theme') || 'light';

    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark');
        if (themeIcon) themeIcon.setAttribute('data-lucide', 'sun');
    } else {
        document.documentElement.classList.remove('dark');
        if (themeIcon) themeIcon.setAttribute('data-lucide', 'moon');
    }

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const isDark = document.documentElement.classList.toggle('dark');
            localStorage.setItem('jobguard_theme', isDark ? 'dark' : 'light');
            if (themeIcon) {
                themeIcon.setAttribute('data-lucide', isDark ? 'sun' : 'moon');
                lucide.createIcons();
            }
        });
    }
}

/**
 * Authentication & Registration System (Local Session State)
 */
function initAuthSystem() {
    const openAuthBtn = document.getElementById('btn-open-auth');
    const tabLoginBtn = document.getElementById('tab-btn-login');
    const tabRegBtn = document.getElementById('tab-btn-register');
    const formLogin = document.getElementById('form-login');
    const formRegister = document.getElementById('form-register');
    const logoutBtn = document.getElementById('btn-logout');

    const guestControls = document.getElementById('auth-guest-controls');
    const userControls = document.getElementById('auth-user-controls');
    const userDisplayName = document.getElementById('user-display-name');
    const userDisplayRole = document.getElementById('user-display-role');
    const userInitials = document.getElementById('user-avatar-initials');

    // Check existing login session
    function checkUserSession() {
        const userJson = localStorage.getItem('jobguard_user');
        if (userJson) {
            try {
                const user = JSON.parse(userJson);
                guestControls.classList.add('hidden');
                userControls.classList.remove('hidden');
                userControls.classList.add('flex');
                if (userDisplayName) userDisplayName.textContent = user.name || 'User';
                if (userDisplayRole) userDisplayRole.textContent = user.role || 'Job Seeker';
                if (userInitials) {
                    const initials = (user.name || 'U').split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
                    userInitials.textContent = initials;
                }
            } catch (e) {
                console.error(e);
            }
        } else {
            guestControls.classList.remove('hidden');
            userControls.classList.add('hidden');
            userControls.classList.remove('flex');
        }
    }

    checkUserSession();

    // Open Auth Page
    if (openAuthBtn) {
        openAuthBtn.addEventListener('click', () => {
            document.querySelectorAll('.tab-section').forEach(s => s.classList.add('hidden'));
            document.querySelectorAll('.nav-tab-btn').forEach(b => {
                b.classList.remove('active', 'bg-amber-800', 'text-white');
                b.classList.add('text-stone-600', 'hover:text-stone-900', 'hover:bg-white');
            });
            const authSection = document.getElementById('tab-auth');
            if (authSection) {
                authSection.classList.remove('hidden');
                authSection.scrollIntoView({ behavior: 'smooth' });
            }
        });
    }

    // Toggle between Sign In & Register tabs
    if (tabLoginBtn && tabRegBtn) {
        tabLoginBtn.addEventListener('click', () => {
            tabLoginBtn.classList.add('bg-white', 'text-amber-800', 'font-bold', 'shadow-sm');
            tabLoginBtn.classList.remove('text-stone-500', 'font-semibold');
            tabRegBtn.classList.remove('bg-white', 'text-amber-800', 'font-bold', 'shadow-sm');
            tabRegBtn.classList.add('text-stone-500', 'font-semibold');

            formLogin.classList.remove('hidden');
            formRegister.classList.add('hidden');
            document.getElementById('auth-form-title').textContent = 'Welcome Back to JobGuard AI';
            document.getElementById('auth-form-subtitle').textContent = 'Sign in to access your scam audit history and candidate protection tools.';
        });

        tabRegBtn.addEventListener('click', () => {
            tabRegBtn.classList.add('bg-white', 'text-amber-800', 'font-bold', 'shadow-sm');
            tabRegBtn.classList.remove('text-stone-500', 'font-semibold');
            tabLoginBtn.classList.remove('bg-white', 'text-amber-800', 'font-bold', 'shadow-sm');
            tabLoginBtn.classList.add('text-stone-500', 'font-semibold');

            formRegister.classList.remove('hidden');
            formLogin.classList.add('hidden');
            document.getElementById('auth-form-title').textContent = 'Create New Account';
            document.getElementById('auth-form-subtitle').textContent = 'Join JobGuard AI to scan unlimited job postings and offer letters.';
        });
    }

    // Handle Login Submit
    if (formLogin) {
        formLogin.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = document.getElementById('login-email').value.trim();
            const name = email.split('@')[0].replace('.', ' ').replace(/^[a-z]/, c => c.toUpperCase());
            
            const userObj = {
                name: name || 'User',
                email: email,
                role: 'Candidate / Job Seeker',
                loginTime: new Date().toISOString()
            };

            localStorage.setItem('jobguard_user', JSON.stringify(userObj));
            checkUserSession();
            alert(`Welcome back, ${userObj.name}! You are now signed in.`);
            document.querySelector('[data-target=\'tab-scanner\']')?.click();
        });
    }

    // Handle Register Submit
    if (formRegister) {
        formRegister.addEventListener('submit', (e) => {
            e.preventDefault();
            const name = document.getElementById('reg-name').value.trim();
            const email = document.getElementById('reg-email').value.trim();
            const role = document.getElementById('reg-role').value;
            const pass = document.getElementById('reg-password').value;
            const passConfirm = document.getElementById('reg-password-confirm').value;

            if (pass !== passConfirm) {
                alert('Passwords do not match! Please check and try again.');
                return;
            }

            const userObj = {
                name: name,
                email: email,
                role: role,
                loginTime: new Date().toISOString()
            };

            localStorage.setItem('jobguard_user', JSON.stringify(userObj));
            checkUserSession();
            alert(`Registration successful! Welcome to JobGuard AI, ${name}.`);
            document.querySelector('[data-target=\'tab-scanner\']')?.click();
        });
    }

    // Handle Logout
    if (logoutBtn) {
        logoutBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to sign out?')) {
                localStorage.removeItem('jobguard_user');
                checkUserSession();
                alert('You have been signed out successfully.');
            }
        });
    }
}

function loginDemoUser(name, role) {
    const userObj = {
        name: name,
        email: `${name.toLowerCase().replace(' ', '.')}@example.com`,
        role: role,
        loginTime: new Date().toISOString()
    };
    localStorage.setItem('jobguard_user', JSON.stringify(userObj));
    location.reload();
}
window.loginDemoUser = loginDemoUser;

/**
 * Subscription & Scan Limit Management System (2 Free AI Scans Tier)
 */
const MAX_FREE_SCANS = 2;
let selectedPlan = 'annual';

function getScanCount() {
    return parseInt(localStorage.getItem('jobguard_scan_count') || '0', 10);
}

function setScanCount(val) {
    localStorage.setItem('jobguard_scan_count', Math.max(0, val).toString());
}

function isSubscribed() {
    return true; // 100% Free & Unlimited Full Access Enabled
}

function getRemainingFreeScans() {
    return 9999;
}

function initSubscriptionSystem() {
    localStorage.setItem('jobguard_subscription_active', 'true');
    updateSubscriptionUI();
}

function updateSubscriptionUI() {
    const pillBtn = document.getElementById('btn-subscription-pill');
    const pillText = document.getElementById('sub-pill-text');
    const pillIcon = document.getElementById('sub-pill-icon');
    const pillAction = document.getElementById('sub-pill-action');

    const scanRemainingText = document.getElementById('scan-remaining-text');
    const offerRemainingText = document.getElementById('offer-remaining-text');
    const scanBadge = document.getElementById('scan-remaining-badge');
    const offerBadge = document.getElementById('offer-remaining-badge');
    const subStatusAlert = document.getElementById('sub-status-alert');

    const dict = I18N_DICTIONARY[currentLang] || I18N_DICTIONARY.en;

    // Side Cards (Compact Free vs Full Pro)
    const sideFreeCard = document.getElementById('side-free-card');
    const sideProCard = document.getElementById('side-pro-card');
    const freeCardScansLeft = document.getElementById('free-card-scans-left');
    const freeCardTag = document.getElementById('free-card-tag');

    // Side Pro Card elements
    const sideProBadge = document.getElementById('side-pro-badge');
    const sideProSub = document.getElementById('side-pro-sub');
    const sideProTag = document.getElementById('side-pro-tag');
    const sideProStatusText = document.getElementById('side-pro-status-text');
    const sideProBtnText = document.getElementById('side-pro-btn-text');

    if (isSubscribed()) {
        const planName = localStorage.getItem('jobguard_subscription_plan') === 'monthly' ? 'Monthly' : 'Annual';
        if (pillBtn) {
            pillBtn.className = 'flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-gradient-to-r from-amber-600 to-amber-800 text-white border border-amber-700 text-xs font-bold transition-all shadow-xs';
        }
        if (pillIcon) pillIcon.setAttribute('data-lucide', 'crown');
        if (pillText) {
            pillText.textContent = dict.sub_pill_pro || `PRO Member (${planName})`;
        }
        if (pillAction) {
            pillAction.className = 'bg-yellow-400 text-amber-950 text-[10px] px-1.5 py-0.5 rounded font-extrabold uppercase';
            pillAction.textContent = 'ACTIVE';
        }

        if (scanRemainingText) scanRemainingText.textContent = dict.pro_unlimited || '👑 Pro: Unlimited AI Checks';
        if (offerRemainingText) offerRemainingText.textContent = dict.pro_unlimited || '👑 Pro: Unlimited AI Checks';
        if (scanBadge) scanBadge.className = 'inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-500/15 text-amber-900 text-[11px] font-bold border border-amber-300';
        if (offerBadge) offerBadge.className = 'inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-500/15 text-amber-900 text-[11px] font-bold border border-amber-300';

        if (subStatusAlert) {
            subStatusAlert.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-bold';
            subStatusAlert.innerHTML = '<i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-600"></i> <span>Pro Subscription Active • Unlimited AI Scans</span>';
        }

        // Hide compact free card and display full Pro card
        if (sideFreeCard) sideFreeCard.classList.add('hidden');
        if (sideProCard) sideProCard.classList.remove('hidden');

        // Update Side Pro Card (Active Pro)
        if (sideProBadge) {
            sideProBadge.textContent = '👑 PRO MEMBER';
            sideProBadge.className = 'px-1.5 py-0.5 rounded text-[9px] font-black uppercase bg-yellow-400 text-amber-950';
        }
        if (sideProSub) sideProSub.textContent = `Pro ${planName} Plan • Unlimited AI Scans & Audits`;
        if (sideProTag) {
            sideProTag.textContent = 'Pro Active';
            sideProTag.className = 'text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/30 text-emerald-200 border border-emerald-400/40 font-bold';
        }
        if (sideProStatusText) {
            sideProStatusText.innerHTML = '<i data-lucide="shield-check" class="w-3.5 h-3.5 text-emerald-300"></i> <span>Unlimited AI Access Active</span>';
        }
        if (sideProBtnText) sideProBtnText.textContent = 'Manage Plan';
    } else {
        const remaining = getRemainingFreeScans();

        if (pillBtn) {
            pillBtn.className = 'flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 text-xs font-bold transition-all shadow-xs';
        }
        if (pillIcon) pillIcon.setAttribute('data-lucide', 'zap');
        if (pillText) {
            pillText.textContent = `${dict.sub_pill_free || 'Free Scans'}: ${remaining}/${MAX_FREE_SCANS}`;
        }
        if (pillAction) {
            pillAction.className = 'bg-amber-800 text-white text-[10px] px-1.5 py-0.5 rounded font-extrabold uppercase';
            pillAction.textContent = 'Upgrade';
        }

        const scanRemainingMsg = `${remaining}/${MAX_FREE_SCANS} ${dict.free_scans_left || 'Free Scans Remaining'}`;
        if (scanRemainingText) scanRemainingText.textContent = scanRemainingMsg;
        if (offerRemainingText) offerRemainingText.textContent = scanRemainingMsg;

        if (remaining === 0) {
            if (scanBadge) scanBadge.className = 'inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-rose-100 text-rose-800 text-[11px] font-bold border border-rose-200';
            if (offerBadge) offerBadge.className = 'inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-rose-100 text-rose-800 text-[11px] font-bold border border-rose-200';
        } else {
            if (scanBadge) scanBadge.className = 'inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-100 text-amber-900 text-[11px] font-semibold border border-amber-200/80';
            if (offerBadge) offerBadge.className = 'inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-100 text-amber-900 text-[11px] font-semibold border border-amber-200/80';
        }

        if (subStatusAlert) {
            subStatusAlert.className = remaining === 0 ? 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-bold' : 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-amber-50 border border-amber-200 text-amber-800 text-xs font-bold';
            subStatusAlert.innerHTML = `<i data-lucide="${remaining === 0 ? 'alert-circle' : 'zap'}" class="w-4 h-4"></i> <span>${remaining === 0 ? 'Free Limit Reached (2/2 Used) • Upgrade to Continue' : `Free Tier: ${remaining} of 2 Checks Available`}</span>`;
        }

        // Show compact free teaser card and hide full Pro card
        if (sideFreeCard) sideFreeCard.classList.remove('hidden');
        if (sideProCard) sideProCard.classList.add('hidden');

        // Update Compact Free Card
        if (freeCardScansLeft) {
            freeCardScansLeft.textContent = remaining === 0 ? 'Free limit used (2/2 used)' : `${remaining} of 2 Free Checks Left`;
        }
        if (freeCardTag) {
            freeCardTag.textContent = remaining === 0 ? 'Limit Reached' : `${remaining} Free`;
            freeCardTag.className = remaining === 0 ? 'text-[10px] font-bold px-2 py-0.5 rounded-md bg-rose-100 text-rose-800 border border-rose-200' : 'text-[10px] font-bold px-2 py-0.5 rounded-md bg-amber-100 text-amber-900 border border-amber-200';
        }
    }

    lucide.createIcons();
}

/**
 * Gatekeeper function: Intercepts verification checks if limit is reached
 */
function checkScanLimitOrPrompt(actionType = 'Check') {
    return true; // Always allow unlimited scans and audits
}

function openSubscriptionModal() {
    const modal = document.getElementById('subscription-modal');
    if (modal) {
        modal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
        selectSubPlan(selectedPlan);
        updateSubscriptionUI();
        lucide.createIcons();
    }
}

function closeSubscriptionModal() {
    const modal = document.getElementById('subscription-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }
}

function selectSubPlan(plan) {
    selectedPlan = plan;
    const cardMonthly = document.getElementById('plan-card-monthly');
    const cardAnnual = document.getElementById('plan-card-annual');
    const btnLabel = document.getElementById('btn-sub-label');
    const radioMonthly = document.querySelector('input[name="sub_plan_choice"][value="monthly"]');
    const radioAnnual = document.querySelector('input[name="sub_plan_choice"][value="annual"]');

    if (plan === 'monthly') {
        if (cardMonthly) cardMonthly.className = 'cursor-pointer p-5 rounded-2xl border-2 border-amber-800 bg-amber-50/40 transition-all space-y-3 relative group shadow-sm';
        if (cardAnnual) cardAnnual.className = 'cursor-pointer p-5 rounded-2xl border-2 border-[#e8dfd2] hover:border-amber-700 bg-[#fbf9f5] transition-all space-y-3 relative group';
        if (radioMonthly) radioMonthly.checked = true;
        if (radioAnnual) radioAnnual.checked = false;
        if (btnLabel) btnLabel.textContent = 'Subscribe Now & Unlock Unlimited Checks (₹199/mo)';
    } else {
        if (cardAnnual) cardAnnual.className = 'cursor-pointer p-5 rounded-2xl border-2 border-amber-800 bg-amber-50/40 transition-all space-y-3 relative group shadow-sm';
        if (cardMonthly) cardMonthly.className = 'cursor-pointer p-5 rounded-2xl border-2 border-[#e8dfd2] hover:border-amber-700 bg-[#fbf9f5] transition-all space-y-3 relative group';
        if (radioAnnual) radioAnnual.checked = true;
        if (radioMonthly) radioMonthly.checked = false;
        if (btnLabel) btnLabel.textContent = 'Subscribe Now & Unlock Unlimited Checks (₹999/yr)';
    }
}

function applyPromoCode() {
    const code = document.getElementById('sub-promo-code')?.value.trim().toUpperCase();
    const msg = document.getElementById('promo-status-msg');
    const btnLabel = document.getElementById('btn-sub-label');

    if (!code) {
        if (msg) {
            msg.className = 'text-[11px] font-semibold text-rose-600 block';
            msg.textContent = 'Please enter a valid promo code.';
        }
        return;
    }

    if (['JOBGUARD', 'PROMO100', 'FREE', 'TEST', 'FREEDOM'].includes(code)) {
        if (msg) {
            msg.className = 'text-[11px] font-semibold text-emerald-600 block';
            msg.textContent = `✅ Promo code "${code}" applied! 100% Free Pro Access Unlocked.`;
        }
        if (btnLabel) {
            btnLabel.textContent = 'Activate 100% Free Pro Subscription (₹0)';
        }
    } else {
        if (msg) {
            msg.className = 'text-[11px] font-semibold text-rose-600 block';
            msg.textContent = '❌ Invalid or expired coupon code. Try promo code: JOBGUARD';
        }
    }
}

function processSubscriptionPayment() {
    const btn = document.getElementById('btn-subscribe-now');
    const originalContent = btn ? btn.innerHTML : '';

    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '<i data-lucide="loader" class="w-4 h-4 animate-spin"></i> <span>Processing Secure Subscription...</span>';
        lucide.createIcons();
    }

    setTimeout(() => {
        localStorage.setItem('jobguard_subscription_active', 'true');
        localStorage.setItem('jobguard_subscription_plan', selectedPlan);
        localStorage.setItem('jobguard_subscription_date', new Date().toISOString());

        if (btn) {
            btn.disabled = false;
            btn.innerHTML = originalContent;
        }

        closeSubscriptionModal();
        updateSubscriptionUI();

        const dict = I18N_DICTIONARY[currentLang] || I18N_DICTIONARY.en;
        alert(dict.sub_success_alert || '🎉 Congratulations! Your JobGuard AI Pro subscription is now active. You now have Unlimited AI Scam Verifications & Offer Audits!');

        lucide.createIcons();
    }, 800);
}

function resetSubscriptionDemo() {
    localStorage.removeItem('jobguard_subscription_active');
    localStorage.removeItem('jobguard_subscription_plan');
    localStorage.setItem('jobguard_scan_count', '0');
    updateSubscriptionUI();
    const msg = document.getElementById('promo-status-msg');
    if (msg) msg.classList.add('hidden');
    const promoInput = document.getElementById('sub-promo-code');
    if (promoInput) promoInput.value = '';
    alert('✅ Free checks reset to 2/2. You can test the 2-scan limit and subscription trigger again.');
}

window.openSubscriptionModal = openSubscriptionModal;
window.closeSubscriptionModal = closeSubscriptionModal;
window.selectSubPlan = selectSubPlan;
window.applyPromoCode = applyPromoCode;
window.processSubscriptionPayment = processSubscriptionPayment;
window.resetSubscriptionDemo = resetSubscriptionDemo;

/**
 * Tab Navigation Controller with Horizontal Auto-Scroll Support
 */
function scrollNavMenu(offset) {
    const mainNav = document.getElementById('main-nav-tabs');
    const mobNav = document.getElementById('mobile-nav-tabs');
    if (mainNav) {
        mainNav.scrollBy({ left: offset, behavior: 'smooth' });
    }
    if (mobNav) {
        mobNav.scrollBy({ left: offset, behavior: 'smooth' });
    }
}
window.scrollNavMenu = scrollNavMenu;

function initNavigation() {
    const navButtons = document.querySelectorAll('.nav-tab-btn');
    const sections = document.querySelectorAll('.tab-section');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const target = btn.getAttribute('data-target');

            navButtons.forEach(b => {
                if (b.getAttribute('data-target') === target) {
                    b.classList.add('active', 'bg-amber-800', 'text-white', 'shadow-xs');
                    b.classList.remove('text-stone-600', 'hover:text-stone-900', 'hover:bg-white', 'text-stone-700', 'bg-white');
                    // Ensure active button scrolls into view within horizontal container
                    b.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
                } else {
                    b.classList.remove('active', 'bg-amber-800', 'text-white', 'shadow-xs');
                    b.classList.add('text-stone-600', 'hover:text-stone-900', 'hover:bg-white');
                }
            });

            sections.forEach(sec => {
                if (sec.id === target) {
                    sec.classList.remove('hidden');
                    sec.classList.add('animate-fade-in');
                } else {
                    sec.classList.add('hidden');
                }
            });

            if (target === 'tab-history' && typeof renderUserHistory === 'function') {
                renderUserHistory();
            }
            if (target === 'tab-scambook' && typeof initScamBoard === 'function') {
                initScamBoard();
            }

            // Re-render icons after tab switch
            lucide.createIcons();
        });
    });
}

/**
 * Sample Job Loader
 */
function initSampleSelector() {
    const selector = document.getElementById('sample-job-select');
    if (!selector) return;

    selector.innerHTML = '<option value="">-- Load a Sample Job Posting --</option>';

    SAMPLE_JOBS.forEach(sample => {
        const opt = document.createElement('option');
        opt.value = sample.id;
        opt.textContent = `${sample.name} (${sample.company})`;
        selector.appendChild(opt);
    });

    selector.addEventListener('change', (e) => {
        const val = e.target.value;
        if (!val) return;

        const sample = SAMPLE_JOBS.find(j => j.id === val);
        if (sample) {
            document.getElementById('job-title').value = sample.title;
            document.getElementById('job-company').value = sample.company;
            document.getElementById('job-salary').value = sample.salary;
            document.getElementById('job-email').value = sample.email;
            document.getElementById('job-website').value = sample.website;
            document.getElementById('job-description').value = sample.description;
            
            // Hide output panel until user explicitly clicks the 'Run AI Scam Verification' button
            document.getElementById('scan-results-panel')?.classList.add('hidden');
        }
    });

    // Sample offer selector
    const offerSelector = document.getElementById('sample-offer-select');
    if (offerSelector) {
        offerSelector.innerHTML = '<option value="">-- Load Sample Offer Letter --</option>';
        SAMPLE_OFFER_LETTERS.forEach(off => {
            const opt = document.createElement('option');
            opt.value = off.id;
            opt.textContent = off.name;
            offerSelector.appendChild(opt);
        });

        offerSelector.addEventListener('change', (e) => {
            const val = e.target.value;
            if (!val) return;
            const off = SAMPLE_OFFER_LETTERS.find(o => o.id === val);
            if (off) {
                document.getElementById('offer-text').value = off.text;
                // Hide output panel until user explicitly clicks the 'Audit Selected Offer Letter' button
                document.getElementById('offer-results-panel')?.classList.add('hidden');
            }
        });
    }
}

/**
 * Job Scanner Trigger & UI Updates
 */
function initJobScanner() {
    const scanBtn = document.getElementById('btn-scan-job');
    const clearBtn = document.getElementById('btn-clear-job');

    if (scanBtn) {
        scanBtn.addEventListener('click', () => triggerJobScan());
    }

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            document.getElementById('job-title').value = '';
            document.getElementById('job-company').value = '';
            document.getElementById('job-salary').value = '';
            document.getElementById('job-email').value = '';
            document.getElementById('job-website').value = '';
            document.getElementById('job-description').value = '';
            document.getElementById('sample-job-select').value = '';
            document.getElementById('scan-results-panel').classList.add('hidden');
        });
    }
}

function triggerJobScan() {
    const jobData = {
        title: document.getElementById('job-title').value.trim(),
        company: document.getElementById('job-company').value.trim(),
        salary: document.getElementById('job-salary').value.trim(),
        email: document.getElementById('job-email').value.trim(),
        website: document.getElementById('job-website').value.trim(),
        description: document.getElementById('job-description').value.trim()
    };

    if (!jobData.description && !jobData.title) {
        alert('Please provide a job title or paste the job description to analyze.');
        return;
    }

    // Check scan limit (2 free scans allowed before subscription prompt)
    if (!checkScanLimitOrPrompt('Job Scan')) {
        return;
    }

    // Run Engine
    const result = DetectorEngine.analyzeJobPost(jobData);
    currentAnalysisResult = { ...result, jobData: jobData };

    renderJobResults(result);
}

function renderJobResults(res) {
    const panel = document.getElementById('scan-results-panel');
    panel.classList.remove('hidden');

    // Scroll smoothly to results
    panel.scrollIntoView({ behavior: 'smooth', block: 'start' });

    // Verdict Badge & Score
    const scoreVal = document.getElementById('result-score-val');
    const verdictTitle = document.getElementById('result-verdict-title');
    const verdictDesc = document.getElementById('result-summary-desc');
    const scoreProgress = document.getElementById('result-score-progress');
    const verdictBadge = document.getElementById('result-verdict-badge');

    scoreVal.textContent = `${res.score}%`;
    verdictTitle.textContent = res.verdict;
    verdictDesc.textContent = res.summaryStatement;
    scoreProgress.style.width = `${res.score}%`;

    // Reset color classes
    scoreVal.className = 'text-5xl font-extrabold tracking-tight';
    scoreProgress.className = 'h-3 rounded-full transition-all duration-700';
    verdictBadge.className = 'inline-flex items-center px-4 py-1.5 rounded-full text-xs font-bold uppercase tracking-wider mb-2';

    if (res.score >= 60) {
        scoreVal.classList.add('text-rose-500');
        scoreProgress.classList.add('bg-rose-500');
        verdictBadge.classList.add('bg-rose-500/20', 'text-rose-400', 'border', 'border-rose-500/30');
        verdictBadge.innerHTML = '<i data-lucide="alert-triangle" class="w-4 h-4 mr-1.5"></i> Danger: Fake Job / Scam';
    } else if (res.score >= 25) {
        scoreVal.classList.add('text-amber-400');
        scoreProgress.classList.add('bg-amber-400');
        verdictBadge.classList.add('bg-amber-500/20', 'text-amber-400', 'border', 'border-amber-500/30');
        verdictBadge.innerHTML = '<i data-lucide="alert-circle" class="w-4 h-4 mr-1.5"></i> Warning: Suspicious Indicators';
    } else {
        scoreVal.classList.add('text-emerald-400');
        scoreProgress.classList.add('bg-emerald-400');
        verdictBadge.classList.add('bg-emerald-500/20', 'text-emerald-400', 'border', 'border-emerald-500/30');
        verdictBadge.innerHTML = '<i data-lucide="check-circle-2" class="w-4 h-4 mr-1.5"></i> Verified: Likely Legitimate';
    }

    // Render Red Flags
    const redFlagsList = document.getElementById('red-flags-container');
    redFlagsList.innerHTML = '';
    if (res.detectedFlags.length === 0) {
        redFlagsList.innerHTML = `
            <div class="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-900 text-xs flex items-center gap-3">
                <i data-lucide="shield-check" class="w-5 h-5 text-emerald-600 shrink-0"></i>
                <span>No high-risk scam keywords or fraudulent phrases were detected in this job post.</span>
            </div>
        `;
    } else {
        res.detectedFlags.forEach(flag => {
            const card = document.createElement('div');
            card.className = 'p-3.5 rounded-xl bg-[#f7f4ed] border border-[#e8dfd2] hover:border-amber-700 transition-all space-y-1.5';
            
            const badgeBg = flag.severity === 'critical' ? 'bg-rose-100 text-rose-700 border border-rose-200' : 
                           flag.severity === 'high' ? 'bg-amber-100 text-amber-900 border border-amber-200' :
                           'bg-amber-50 text-amber-800 border border-amber-200';

            card.innerHTML = `
                <div class="flex items-center justify-between gap-3">
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold ${badgeBg}">${flag.category}</span>
                    <span class="text-[11px] text-rose-600 font-mono font-bold">+${flag.weight} Risk</span>
                </div>
                <div class="text-xs text-rose-800 font-mono bg-white px-2.5 py-1.5 rounded-lg border border-rose-200 font-medium break-all">
                    "${escapeHtml(flag.matchedPhrase)}"
                </div>
                <p class="text-xs text-stone-700 leading-relaxed">${escapeHtml(flag.explanation)}</p>
            `;
            redFlagsList.appendChild(card);
        });
    }

    // Render Safe Indicators
    const safeFlagsList = document.getElementById('safe-flags-container');
    safeFlagsList.innerHTML = '';
    if (res.safeFlags.length === 0) {
        safeFlagsList.innerHTML = '<p class="text-xs text-stone-500 italic">No standard corporate verification markers found.</p>';
    } else {
        res.safeFlags.forEach(sf => {
            const item = document.createElement('div');
            item.className = 'flex items-center gap-2 text-xs text-emerald-800 bg-emerald-50 border border-emerald-200 px-3 py-1.5 rounded-lg';
            item.innerHTML = `<i data-lucide="check" class="w-3.5 h-3.5 text-emerald-600 shrink-0"></i> <span>${escapeHtml(sf.label)}</span>`;
            safeFlagsList.appendChild(item);
        });
    }

    // Render Actionable Advice (Humanized Candidate Steps)
    const adviceList = document.getElementById('advice-container');
    adviceList.innerHTML = '';
    res.actionableAdvice.forEach(adv => {
        const item = document.createElement('li');
        item.className = 'flex items-start gap-2 text-xs text-stone-700 leading-relaxed';
        item.innerHTML = `<i data-lucide="arrow-right-circle" class="w-3.5 h-3.5 text-amber-800 shrink-0 mt-0.5"></i> <span>${escapeHtml(adv)}</span>`;
        adviceList.appendChild(item);
    });

    // Render Radar Risk Chart
    renderRiskChart(res.breakdown);

    lucide.createIcons();
}

/**
 * Chart.js Radar Chart
 */
function renderRiskChart(breakdown) {
    const ctx = document.getElementById('risk-radar-chart');
    if (!ctx) return;

    if (radarChartInstance) {
        radarChartInstance.destroy();
    }

    radarChartInstance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: Object.keys(breakdown),
            datasets: [{
                label: 'Risk Level %',
                data: Object.values(breakdown),
                backgroundColor: 'rgba(239, 68, 68, 0.25)',
                borderColor: 'rgba(239, 68, 68, 0.85)',
                pointBackgroundColor: '#ef4444',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#ef4444'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                    grid: { color: 'rgba(255, 255, 255, 0.08)' },
                    pointLabels: {
                        color: '#94a3b8',
                        font: { size: 10, family: 'Plus Jakarta Sans' }
                    },
                    ticks: {
                        backdropColor: 'transparent',
                        color: '#64748b',
                        stepSize: 25,
                        min: 0,
                        max: 100
                    }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

/**
 * Offer Letter Auditor Controller (with File & Folder Upload + PDF Extraction)
 */
let uploadedOfferFiles = [];

function initOfferAuditor() {
    const btn = document.getElementById('btn-audit-offer');
    const clearBtn = document.getElementById('btn-clear-offer');
    const fileInput = document.getElementById('offer-file-input');
    const folderInput = document.getElementById('offer-folder-input');
    const dropZone = document.getElementById('offer-drop-zone');
    const folderZone = document.getElementById('offer-folder-zone');
    const batchScanBtn = document.getElementById('btn-batch-scan');

    if (btn) btn.addEventListener('click', () => triggerOfferAudit());

    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            document.getElementById('offer-text').value = '';
            document.getElementById('offer-results-panel').classList.add('hidden');
            const indicator = document.getElementById('active-file-indicator');
            if (indicator) indicator.classList.add('hidden');
        });
    }

    // Single File Click & Drag
    if (dropZone && fileInput) {
        dropZone.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => handleOfferFiles(e.target.files));

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('border-indigo-500', 'bg-indigo-950/20');
        });
        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('border-indigo-500', 'bg-indigo-950/20');
        });
        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('border-indigo-500', 'bg-indigo-950/20');
            if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
                handleOfferFiles(e.dataTransfer.files);
            }
        });
    }

    // Folder Click & Input
    if (folderZone && folderInput) {
        folderZone.addEventListener('click', () => folderInput.click());
        folderInput.addEventListener('change', (e) => handleOfferFiles(e.target.files));
    }

    // Batch scan all
    if (batchScanBtn) {
        batchScanBtn.addEventListener('click', () => runBatchAudit());
    }
}

/**
 * Handle Single or Multiple Uploaded Offer Files / Folders
 */
async function handleOfferFiles(fileList) {
    if (!fileList || fileList.length === 0) return;

    const validFiles = Array.from(fileList).filter(f => {
        const name = f.name.toLowerCase();
        return name.endsWith('.pdf') || name.endsWith('.txt') || name.endsWith('.docx') || name.endsWith('.doc') || name.endsWith('.rtf');
    });

    if (validFiles.length === 0) {
        alert('No compatible document files found. Please upload PDF, TXT, or DOCX documents.');
        return;
    }

    const panel = document.getElementById('uploaded-files-panel');
    const countBadge = document.getElementById('uploaded-files-count');
    const listContainer = document.getElementById('uploaded-files-list');

    panel.classList.remove('hidden');
    countBadge.textContent = `${validFiles.length} file${validFiles.length > 1 ? 's' : ''}`;
    listContainer.innerHTML = '<div class="text-xs text-slate-400 py-2"><i data-lucide="loader" class="w-4 h-4 animate-spin inline mr-1"></i> Extracting document text...</div>';
    lucide.createIcons();

    uploadedOfferFiles = [];

    for (let i = 0; i < validFiles.length; i++) {
        const file = validFiles[i];
        try {
            const extractedText = await extractTextFromFile(file);
            uploadedOfferFiles.push({
                file: file,
                name: file.name,
                size: (file.size / 1024).toFixed(1) + ' KB',
                text: extractedText,
                auditResult: null
            });
        } catch (err) {
            console.error(`Error parsing ${file.name}:`, err);
            uploadedOfferFiles.push({
                file: file,
                name: file.name,
                size: (file.size / 1024).toFixed(1) + ' KB',
                text: `[Error reading document: ${err.message}]`,
                auditResult: null
            });
        }
    }

    renderUploadedFilesList();

    // Automatically load and audit first file if single file was uploaded
    if (uploadedOfferFiles.length === 1 && uploadedOfferFiles[0].text) {
        selectFileForAudit(0);
    }
}

/**
 * Render Uploaded Files List UI
 */
function renderUploadedFilesList() {
    const listContainer = document.getElementById('uploaded-files-list');
    if (!listContainer) return;
    listContainer.innerHTML = '';

    uploadedOfferFiles.forEach((item, index) => {
        const row = document.createElement('div');
        row.className = 'flex items-center justify-between p-2.5 rounded-xl bg-white border border-[#e8dfd2] hover:border-amber-700 transition-all shadow-xs';
        
        let statusBadge = '<span class="text-[10px] text-stone-500 font-mono px-2 py-0.5 rounded bg-stone-100">Ready</span>';
        if (item.auditResult) {
            if (item.auditResult.fraudScore >= 50) {
                statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-50 text-rose-700 border border-rose-200">🚨 ${item.auditResult.fraudScore}% Fake</span>`;
            } else if (item.auditResult.fraudScore >= 20) {
                statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-50 text-amber-800 border border-amber-200">⚠️ ${item.auditResult.fraudScore}% Warning</span>`;
            } else {
                statusBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-700 border border-emerald-200">🛡️ 0% Zero Risk</span>`;
            }
        }

        row.innerHTML = `
            <div class="flex items-center gap-2.5 overflow-hidden">
                <i data-lucide="file-text" class="w-4 h-4 text-amber-800 shrink-0"></i>
                <span class="font-semibold text-stone-800 truncate max-w-xs text-xs">${escapeHtml(item.name)}</span>
                <span class="text-[10px] text-stone-400 font-mono">(${item.size})</span>
            </div>
            <div class="flex items-center gap-2 shrink-0">
                ${statusBadge}
                <button type="button" class="px-3 py-1 rounded-lg bg-[#f7f4ed] hover:bg-amber-100 text-amber-900 border border-[#e8dfd2] text-[11px] font-bold transition-all" onclick="selectFileForAudit(${index})">
                    Audit Document
                </button>
            </div>
        `;
        listContainer.appendChild(row);
    });

    lucide.createIcons();
}

/**
 * Select single file from uploaded list to audit
 */
function selectFileForAudit(index) {
    if (!uploadedOfferFiles[index]) return;

    const fileItem = uploadedOfferFiles[index];
    const textarea = document.getElementById('offer-text');
    const indicator = document.getElementById('active-file-indicator');

    textarea.value = fileItem.text;
    if (indicator) {
        indicator.classList.remove('hidden');
        indicator.textContent = `📄 Active: ${fileItem.name}`;
    }

    // Automatically trigger audit for user convenience
    triggerOfferAudit(index);
}

/**
 * Batch Audit All Uploaded Files
 */
function runBatchAudit() {
    if (uploadedOfferFiles.length === 0) {
        alert('No files uploaded yet.');
        return;
    }

    // Check scan limit (2 free scans allowed before subscription prompt)
    if (!checkScanLimitOrPrompt('Batch Offer Audit')) {
        return;
    }

    uploadedOfferFiles.forEach((item, idx) => {
        item.auditResult = DetectorEngine.auditOfferLetter(item.text);
    });

    renderUploadedFilesList();

    // Select the one with highest fraud score to show details
    let highestIndex = 0;
    let maxScore = -1;
    uploadedOfferFiles.forEach((item, idx) => {
        if (item.auditResult && item.auditResult.fraudScore > maxScore) {
            maxScore = item.auditResult.fraudScore;
            highestIndex = idx;
        }
    });

    selectFileForAudit(highestIndex);
}

// Expose functions to window
window.selectFileForAudit = selectFileForAudit;
window.runBatchAudit = runBatchAudit;
window.exportAnalysisReport = exportAnalysisReport;

/**
 * Extract text from File object (supports PDF via PDF.js, and Plain Text)
 */
async function extractTextFromFile(file) {
    const name = file.name.toLowerCase();

    if (name.endsWith('.pdf')) {
        if (typeof pdfjsLib === 'undefined') {
            throw new Error('PDF.js library is not available.');
        }

        const arrayBuffer = await file.arrayBuffer();
        const loadingTask = pdfjsLib.getDocument({ data: arrayBuffer });
        const pdf = await loadingTask.promise;
        let fullText = '';

        for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
            const page = await pdf.getPage(pageNum);
            const textContent = await page.getTextContent();
            const pageStr = textContent.items.map(item => item.str).join(' ');
            fullText += `--- Page ${pageNum} ---\n` + pageStr + '\n\n';
        }

        return fullText.trim() || '[Empty PDF or scanned image without embedded text]';
    } else {
        // Plain text, rtf, or docx text reader
        return new Promise((resolve, reject) => {
            const reader = new FileReader();
            reader.onload = (e) => resolve(e.target.result);
            reader.onerror = (e) => reject(e);
            reader.readAsText(file);
        });
    }
}

function triggerOfferAudit(fileIndex = null) {
    const text = document.getElementById('offer-text').value.trim();
    if (!text) {
        alert('Please paste the offer letter text or upload a PDF/folder above.');
        return;
    }

    // Check scan limit (2 free scans allowed before subscription prompt)
    if (!checkScanLimitOrPrompt('Offer Letter Audit')) {
        return;
    }

    const audit = DetectorEngine.auditOfferLetter(text);
    
    if (fileIndex !== null && uploadedOfferFiles[fileIndex]) {
        uploadedOfferFiles[fileIndex].auditResult = audit;
        renderUploadedFilesList();
    }

    const resultsDiv = document.getElementById('offer-results-panel');
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });

    const statusBadge = document.getElementById('offer-status-badge');
    const zeroRiskTag = document.getElementById('offer-zero-risk-tag');
    const verdictTitle = document.getElementById('offer-verdict-title');
    const summaryDesc = document.getElementById('offer-summary-desc');
    const scoreVal = document.getElementById('offer-score-val');
    const scoreProgress = document.getElementById('offer-score-progress');
    const researchGrid = document.getElementById('offer-research-grid');
    const findingsContainer = document.getElementById('offer-findings-container');
    const safePointsContainer = document.getElementById('offer-safe-points-container');
    const tipsContainer = document.getElementById('offer-tips-container');

    scoreVal.textContent = `${audit.fraudScore}% Risk`;
    if (scoreProgress) scoreProgress.style.width = `${audit.fraudScore}%`;

    if (audit.fraudScore >= 50) {
        statusBadge.className = 'px-3.5 py-1 rounded-full text-xs font-bold uppercase bg-rose-50 text-rose-700 border border-rose-200 flex items-center gap-1.5';
        statusBadge.innerHTML = '<i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-rose-600"></i> <span>Fake / Fraudulent Offer Letter</span>';
        if (zeroRiskTag) zeroRiskTag.classList.add('hidden');
        if (verdictTitle) verdictTitle.textContent = 'High-Risk Counterfeit Offer Detected';
        if (summaryDesc) summaryDesc.textContent = audit.summaryStatement;
        scoreVal.className = 'text-3xl font-extrabold font-mono text-rose-600';
        if (scoreProgress) scoreProgress.className = 'h-full bg-rose-600 rounded-full transition-all duration-700';
    } else if (audit.fraudScore >= 20) {
        statusBadge.className = 'px-3.5 py-1 rounded-full text-xs font-bold uppercase bg-amber-50 text-amber-800 border border-amber-200 flex items-center gap-1.5';
        statusBadge.innerHTML = '<i data-lucide="alert-circle" class="w-3.5 h-3.5 text-amber-700"></i> <span>Suspicious Clauses Detected</span>';
        if (zeroRiskTag) zeroRiskTag.classList.add('hidden');
        if (verdictTitle) verdictTitle.textContent = 'Caution: Ambiguous or Suspicious Terms Found';
        if (summaryDesc) summaryDesc.textContent = audit.summaryStatement;
        scoreVal.className = 'text-3xl font-extrabold font-mono text-amber-600';
        if (scoreProgress) scoreProgress.className = 'h-full bg-amber-500 rounded-full transition-all duration-700';
    } else {
        statusBadge.className = 'px-3.5 py-1 rounded-full text-xs font-bold uppercase bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center gap-1.5';
        statusBadge.innerHTML = '<i data-lucide="shield-check" class="w-3.5 h-3.5 text-emerald-600"></i> <span>Verified Genuine Offer Letter</span>';
        if (zeroRiskTag) zeroRiskTag.classList.remove('hidden');
        if (verdictTitle) verdictTitle.textContent = '0% Risk - Authentic & Safe Employment Offer';
        if (summaryDesc) summaryDesc.textContent = audit.summaryStatement;
        scoreVal.className = 'text-3xl font-extrabold font-mono text-emerald-600';
        if (scoreProgress) {
            scoreProgress.className = 'h-full bg-emerald-600 rounded-full transition-all duration-700';
            scoreProgress.style.width = '0%';
        }
    }

    // Render Multi-Vector Deep Research Checklist
    if (researchGrid) {
        researchGrid.innerHTML = '';
        (audit.researchBreakdown || []).forEach(vector => {
            const card = document.createElement('div');
            const isSafe = vector.status === 'PASSED';
            card.className = `p-3.5 rounded-xl border transition-all ${
                isSafe 
                    ? 'bg-emerald-50/40 border-emerald-200/80 text-emerald-950' 
                    : 'bg-rose-50/40 border-rose-200/80 text-rose-950'
            }`;

            const badgeHtml = isSafe
                ? `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-extrabold uppercase bg-emerald-100 text-emerald-800 border border-emerald-300">
                     <i data-lucide="check" class="w-3 h-3 text-emerald-700"></i> Passed
                   </span>`
                : `<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[10px] font-extrabold uppercase bg-rose-100 text-rose-800 border border-rose-300">
                     <i data-lucide="x" class="w-3 h-3 text-rose-700"></i> ${vector.severity}
                   </span>`;

            card.innerHTML = `
                <div class="flex items-center justify-between gap-2 mb-1.5">
                    <span class="text-xs font-bold text-stone-800 flex items-center gap-1.5">
                        <i data-lucide="${vector.icon || 'shield'}" class="w-3.5 h-3.5 ${isSafe ? 'text-emerald-700' : 'text-rose-600'}"></i>
                        <span>${escapeHtml(vector.title)}</span>
                    </span>
                    ${badgeHtml}
                </div>
                <p class="text-[11px] text-stone-600 leading-snug">${escapeHtml(vector.summary)}</p>
            `;
            researchGrid.appendChild(card);
        });
    }

    // Render Red Flags Findings
    if (findingsContainer) {
        findingsContainer.innerHTML = '';
        if (audit.findings.length === 0) {
            findingsContainer.innerHTML = `
                <div class="p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs flex items-center gap-2.5">
                    <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-600 shrink-0"></i>
                    <span>No upfront fee requests, fake check schemes, or predatory clauses detected in this offer letter.</span>
                </div>
            `;
        } else {
            audit.findings.forEach(f => {
                const card = document.createElement('div');
                card.className = 'p-3 rounded-xl bg-rose-50/50 border border-rose-200 space-y-1.5';
                card.innerHTML = `
                    <div class="flex items-center justify-between">
                        <span class="text-xs font-bold text-rose-800">${escapeHtml(f.title)}</span>
                        <span class="text-[10px] px-2 py-0.5 rounded bg-rose-100 text-rose-800 font-extrabold uppercase">${f.severity}</span>
                    </div>
                    <div class="text-[11px] font-mono text-rose-900 bg-white p-2 rounded-lg border border-rose-200">"${escapeHtml(f.snippet)}"</div>
                    <p class="text-xs text-stone-600">${escapeHtml(f.description)}</p>
                `;
                findingsContainer.appendChild(card);
            });
        }
    }

    // Render Safe Points
    if (safePointsContainer) {
        safePointsContainer.innerHTML = '';
        if (audit.verifiedSafePoints && audit.verifiedSafePoints.length > 0) {
            audit.verifiedSafePoints.forEach(sp => {
                const item = document.createElement('div');
                item.className = 'flex items-center gap-2 text-xs text-emerald-800 bg-emerald-50/60 border border-emerald-200 px-3 py-1.5 rounded-lg';
                item.innerHTML = `<i data-lucide="check" class="w-3.5 h-3.5 text-emerald-600 shrink-0"></i> <span>${escapeHtml(sp.label)}</span>`;
                safePointsContainer.appendChild(item);
            });
        }
    }

    // Render Safety Tips
    if (tipsContainer) {
        tipsContainer.innerHTML = '';
        audit.safetyTips.forEach(tip => {
            const item = document.createElement('li');
            item.className = 'flex items-start gap-2 text-xs text-stone-700 leading-relaxed';
            item.innerHTML = `<i data-lucide="check-circle" class="w-3.5 h-3.5 text-amber-700 shrink-0 mt-0.5"></i> <span>${escapeHtml(tip)}</span>`;
            tipsContainer.appendChild(item);
        });
    }

    // Save Offer Audit to User History
    const fileName = (fileIndex !== null && uploadedOfferFiles[fileIndex]) ? uploadedOfferFiles[fileIndex].name : 'Offer Letter Document';
    saveAuditHistory({
        type: 'Offer Audit',
        title: `Offer Audit: ${fileName}`,
        company: 'Employment Offer / Contract',
        score: audit.fraudScore,
        verdict: audit.fraudScore >= 50 ? '🚨 Fake / Fraudulent Offer' : audit.fraudScore >= 20 ? '⚠️ Suspicious Clauses' : '🛡️ 0% Zero Risk Genuine Offer',
        details: audit.findings.length > 0 ? audit.findings.map(f => f.title).join(' • ') : 'Zero upfront money requested • 100% verified genuine corporate offer'
    });

    lucide.createIcons();
}

/**
 * Salary Sanity & Scam Bait Evaluator Controller
 */
const SALARY_BENCHMARKS = {
    data_entry: {
        name: 'Data Entry / Typing Clerk',
        ranges: {
            fresher: { min: 10000, max: 18000, avg: 14000 },
            entry: { min: 14000, max: 24000, avg: 19000 },
            mid: { min: 20000, max: 35000, avg: 26000 }
        },
        scamWarning: 'Legitimate companies pay ₹12,000–₹18,000 for full-time data entry. Offers exceeding ₹40,000/mo or ₹2,000/day for 1-2 hours of typing are 100% upfront registration fee traps.'
    },
    task_rating: {
        name: 'YouTube/Product Task Rating',
        ranges: {
            fresher: { min: 0, max: 2000, avg: 800 },
            entry: { min: 0, max: 3000, avg: 1200 },
            mid: { min: 0, max: 5000, avg: 2000 }
        },
        scamWarning: '🚨 EXTREME RISK: Legitimate tech firms DO NOT hire freelance individuals to like videos or rate hotels for ₹3,000–₹8,000/day. This is the notorious Telegram Prepaid Task Scam where victims are defrauded of USDT crypto deposits.'
    },
    customer_support: {
        name: 'Customer Support / Chat Agent',
        ranges: {
            fresher: { min: 15000, max: 25000, avg: 20000 },
            entry: { min: 22000, max: 35000, avg: 28000 },
            mid: { min: 30000, max: 55000, avg: 42000 }
        },
        scamWarning: 'Standard fresher BPO/Chat support ranges between ₹18,000–₹25,000/month. Unrealistic promises of ₹80,000+ without formal phone/video interview are fake.'
    },
    social_media: {
        name: 'Social Media Assistant',
        ranges: {
            fresher: { min: 15000, max: 28000, avg: 22000 },
            entry: { min: 25000, max: 42000, avg: 32000 },
            mid: { min: 38000, max: 65000, avg: 50000 }
        },
        scamWarning: 'Entry-level social media assistants earn standard local salaries. Avoid offers that require buying access to special influencer portals.'
    },
    content_writer: {
        name: 'Junior Content Writer',
        ranges: {
            fresher: { min: 14000, max: 25000, avg: 20000 },
            entry: { min: 24000, max: 40000, avg: 30000 },
            mid: { min: 35000, max: 60000, avg: 45000 }
        },
        scamWarning: 'Articles are paid per word (₹0.50 to ₹1.50/word) or fixed monthly stipend. Be careful of clients asking for "security deposit" before assigning writing projects.'
    },
    software_dev: {
        name: 'Junior Software Developer',
        ranges: {
            fresher: { min: 25000, max: 55000, avg: 38000 },
            entry: { min: 45000, max: 85000, avg: 62000 },
            mid: { min: 80000, max: 160000, avg: 110000 }
        },
        scamWarning: 'Real tech employers evaluate code through GitHub or technical interviews. Any tech role asking you to pay for training certification before joining is a fee scam.'
    },
    graphic_designer: {
        name: 'Junior Graphic Designer',
        ranges: {
            fresher: { min: 15000, max: 28000, avg: 22000 },
            entry: { min: 25000, max: 45000, avg: 34000 },
            mid: { min: 40000, max: 75000, avg: 55000 }
        },
        scamWarning: 'Always verify design job offers against the company portfolio. Beware of fake clients sending bad checks for graphic software purchases.'
    },
    package_handler: {
        name: 'Package Reshipper / Handler',
        ranges: {
            fresher: { min: 0, max: 0, avg: 0 },
            entry: { min: 0, max: 0, avg: 0 },
            mid: { min: 0, max: 0, avg: 0 }
        },
        scamWarning: '🚨 100% ILLEGAL MONEY/GOODS MULE SCAM: There is NO legitimate job where you receive parcels at home and reship them. Packages are bought with stolen credit cards. You will never be paid, and you will be held legally liable by police.'
    }
};

function initSalaryCalculator() {
    const btn = document.getElementById('btn-calc-salary');
    if (!btn) return;

    btn.addEventListener('click', () => {
        const roleKey = document.getElementById('calc-role').value;
        const expKey = document.getElementById('calc-exp').value;
        const timeKey = document.getElementById('calc-time').value;
        const offeredPay = parseFloat(document.getElementById('calc-offered-pay').value) || 0;

        const roleData = SALARY_BENCHMARKS[roleKey] || SALARY_BENCHMARKS.data_entry;
        let bench = roleData.ranges[expKey] || roleData.ranges.fresher;

        // Apply part-time adjustment (part-time is ~35% of full time)
        const timeFactor = (timeKey === 'part_time') ? 0.35 : 1.0;
        const adjMin = Math.round(bench.min * timeFactor);
        const adjMax = Math.round(bench.max * timeFactor);
        const adjAvg = Math.max(1, Math.round(bench.avg * timeFactor));

        const resultPanel = document.getElementById('salary-calc-result-panel');
        resultPanel.classList.remove('hidden');

        const verdictBadge = document.getElementById('salary-verdict-badge');
        const multVal = document.getElementById('salary-multiplier-val');
        const realRangeEl = document.getElementById('salary-real-range');
        const offeredValEl = document.getElementById('salary-offered-val');
        const devText = document.getElementById('salary-deviation-text');
        const analysisBox = document.getElementById('salary-analysis-box');

        realRangeEl.textContent = roleKey === 'package_handler' ? '₹0 (Illegal Operation)' : `₹${adjMin.toLocaleString('en-IN')} - ₹${adjMax.toLocaleString('en-IN')} / mo`;
        offeredValEl.textContent = `₹${offeredPay.toLocaleString('en-IN')} / mo`;

        const ratio = (adjAvg > 0) ? (offeredPay / adjAvg) : (offeredPay > 0 ? 10 : 1);

        if (roleKey === 'package_handler' || (roleKey === 'task_rating' && offeredPay > 5000)) {
            verdictBadge.className = 'px-3 py-1 rounded-full text-xs font-bold uppercase bg-rose-600 text-white shadow-xs';
            verdictBadge.textContent = '🚨 Extreme Fraud / Scam Trap Payout';
            multVal.textContent = `Scam Bait Multiplier: ${(ratio).toFixed(1)}x Normal Pay`;
            devText.className = 'text-[11px] font-bold text-rose-600';
            devText.textContent = `+${Math.round((ratio - 1) * 100)}% Exaggerated (Scam Bait)`;
            analysisBox.className = 'p-4 rounded-xl border border-rose-300 bg-rose-50 text-xs text-rose-900 leading-relaxed space-y-2';
            analysisBox.innerHTML = `
                <div class="font-bold text-sm text-rose-800 flex items-center gap-1.5">
                    <i data-lucide="alert-octagon" class="w-4 h-4 text-rose-600"></i>
                    <span>High Risk Scam Warning: Unrealistic Financial Bait</span>
                </div>
                <p>${roleData.scamWarning}</p>
                <div class="p-2.5 rounded-lg bg-white border border-rose-200 text-[11px] text-rose-800">
                    <strong>Why Scammers Do This:</strong> Scammers inflate the promised compensation to trigger excitement and lower your critical thinking, preparing you to pay "registration fees", "training fees", or "VIP merchant deposits".
                </div>
            `;
        } else if (ratio >= 2.2) {
            verdictBadge.className = 'px-3 py-1 rounded-full text-xs font-bold uppercase bg-rose-500 text-white shadow-xs';
            verdictBadge.textContent = '🚨 Unrealistic Scam Bait Rate';
            multVal.textContent = `Scam Bait Multiplier: ${(ratio).toFixed(1)}x Industry Standard`;
            devText.className = 'text-[11px] font-bold text-rose-600';
            devText.textContent = `+${Math.round((ratio - 1) * 100)}% Above Genuine Market Cap`;
            analysisBox.className = 'p-4 rounded-xl border border-rose-200 bg-rose-50/70 text-xs text-rose-900 leading-relaxed space-y-2';
            analysisBox.innerHTML = `
                <div class="font-bold text-sm text-rose-800 flex items-center gap-1.5">
                    <i data-lucide="alert-triangle" class="w-4 h-4 text-rose-600"></i>
                    <span>Suspicious Compensation Detected</span>
                </div>
                <p>The offered rate of <strong>₹${offeredPay.toLocaleString('en-IN')}/mo</strong> is <strong>${ratio.toFixed(1)} times higher</strong> than what verified companies pay for this role and experience.</p>
                <p class="text-stone-700">${roleData.scamWarning}</p>
            `;
        } else if (ratio >= 1.5) {
            verdictBadge.className = 'px-3 py-1 rounded-full text-xs font-bold uppercase bg-amber-500 text-white shadow-xs';
            verdictBadge.textContent = '⚠️ Elevated / Verify Authenticity';
            multVal.textContent = `Ratio: ${(ratio).toFixed(1)}x Average`;
            devText.className = 'text-[11px] font-bold text-amber-700';
            devText.textContent = `+${Math.round((ratio - 1) * 100)}% Above Average`;
            analysisBox.className = 'p-4 rounded-xl border border-amber-200 bg-amber-50/70 text-xs text-amber-900 leading-relaxed space-y-2';
            analysisBox.innerHTML = `
                <div class="font-bold text-sm text-amber-800 flex items-center gap-1.5">
                    <i data-lucide="info" class="w-4 h-4 text-amber-600"></i>
                    <span>Moderately High Salary Offer</span>
                </div>
                <p>This pay rate is slightly above average. Ensure you verify the employer's official website and never pay any pre-joining costs.</p>
            `;
        } else {
            verdictBadge.className = 'px-3 py-1 rounded-full text-xs font-bold uppercase bg-emerald-600 text-white shadow-xs';
            verdictBadge.textContent = '✅ Realistic Market Range';
            multVal.textContent = `Ratio: ${(ratio).toFixed(1)}x Standard`;
            devText.className = 'text-[11px] font-bold text-emerald-700';
            devText.textContent = 'Within Normal Industry Compensation Band';
            analysisBox.className = 'p-4 rounded-xl border border-emerald-200 bg-emerald-50/70 text-xs text-emerald-900 leading-relaxed space-y-2';
            analysisBox.innerHTML = `
                <div class="font-bold text-sm text-emerald-800 flex items-center gap-1.5">
                    <i data-lucide="check-circle" class="w-4 h-4 text-emerald-600"></i>
                    <span>Salary is Structurally Realistic</span>
                </div>
                <p>The offered salary of ₹${offeredPay.toLocaleString('en-IN')}/mo aligns with normal market benchmarks for ${roleData.name}. Continue to ensure all communication occurs via official corporate domains.</p>
            `;
        }

        // Save Salary Check to User History
        saveAuditHistory({
            type: 'Salary Check',
            title: `Salary Check: ${roleData.name}`,
            company: `Offered: ₹${offeredPay.toLocaleString('en-IN')}/mo`,
            score: ratio >= 2.2 ? 85 : ratio >= 1.5 ? 45 : 5,
            verdict: verdictBadge.textContent,
            details: `Offered ₹${offeredPay.toLocaleString('en-IN')}/mo vs Market standard ₹${adjMin.toLocaleString('en-IN')} - ₹${adjMax.toLocaleString('en-IN')}`
        });

        lucide.createIcons();
    });
}

/**
 * Recruiter & Domain Verifier Controller
 */
function initRecruiterChecker() {
    const btn = document.getElementById('btn-verify-recruiter');
    if (!btn) return;

    btn.addEventListener('click', () => {
        const email = document.getElementById('recruiter-email').value.trim();
        const company = document.getElementById('recruiter-company').value.trim();
        const website = document.getElementById('recruiter-website').value.trim();

        if (!email) {
            alert('Please enter a recruiter email address.');
            return;
        }

        // Check scan limit (2 free scans allowed before subscription prompt)
        if (!checkScanLimitOrPrompt('Recruiter Verification')) {
            return;
        }

        const res = DetectorEngine.evaluateRecruiterEmail(email, company, website);
        const out = document.getElementById('recruiter-results-panel');
        out.classList.remove('hidden');

        const badge = document.getElementById('recruiter-status-badge');
        const desc = document.getElementById('recruiter-eval-desc');

        if (res.flag && res.flag.severity === 'critical') {
            badge.className = 'px-3 py-1 rounded-full text-xs font-bold bg-rose-500/20 text-rose-400 border border-rose-500/40';
            badge.textContent = '🚨 LOOKALIKE / PHISHING DOMAIN';
            desc.textContent = res.flag.explanation;
        } else if (res.isFreeEmail) {
            badge.className = 'px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-400 border border-amber-500/40';
            badge.textContent = '⚠️ FREE PUBLIC EMAIL';
            desc.textContent = res.flag ? res.flag.explanation : 'Recruiter is using a free email provider rather than an official corporate domain.';
        } else if (res.isVerifiedCorporate) {
            badge.className = 'px-3 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40';
            badge.textContent = '✅ VERIFIED CORPORATE DOMAIN';
            desc.textContent = 'The domain belongs to a recognized, verified corporate domain repository.';
        } else {
            badge.className = 'px-3 py-1 rounded-full text-xs font-bold bg-slate-700 text-slate-300';
            badge.textContent = 'ℹ️ CUSTOM PRIVATE DOMAIN';
            desc.textContent = `Email domain: @${res.domain}. Verify that this domain matches the company's official public website.`;
        }

        // Save Recruiter Check to User History
        saveAuditHistory({
            type: 'Recruiter Check',
            title: `Recruiter Check: ${email}`,
            company: company || `@${res.domain}`,
            score: res.flag ? (res.flag.severity === 'critical' ? 90 : 60) : (res.isVerifiedCorporate ? 5 : 25),
            verdict: badge.textContent,
            details: desc.textContent
        });

        lucide.createIcons();
    });
}

/**
 * 60-Second Scam Assessment Quiz
 */
const QUIZ_QUESTIONS = [
    {
        q: "1. Did the recruiter contact you via WhatsApp or Telegram without any prior application on an official job portal?",
        risk: 25
    },
    {
        q: "2. Were you offered the job immediately with no video interview, background check, or formal technical assessment?",
        risk: 30
    },
    {
        q: "3. Does the employer ask you to pay any 'registration fee', 'training charges', or 'laptop insurance' before starting?",
        risk: 40
    },
    {
        q: "4. Are they sending you a check/payment to buy equipment from their 'designated IT vendor'?",
        risk: 35
    },
    {
        q: "5. Is the salary unusually high for entry-level work (e.g. $50+/hr for simple data entry or liking videos)?",
        risk: 25
    }
];

function initQuiz() {
    const container = document.getElementById('quiz-questions-container');
    if (!container) return;

    container.innerHTML = '';
    QUIZ_QUESTIONS.forEach((q, idx) => {
        const qBlock = document.createElement('div');
        qBlock.className = 'p-4 rounded-xl bg-slate-800/60 border border-slate-700/60 mb-3';
        qBlock.innerHTML = `
            <p class="text-xs sm:text-sm font-semibold text-slate-200 mb-3">${q.q}</p>
            <div class="flex items-center gap-6">
                <label class="flex items-center gap-2 cursor-pointer text-xs text-slate-300">
                    <input type="radio" name="quiz_q_${idx}" value="yes" class="accent-indigo-500 w-4 h-4">
                    <span>YES</span>
                </label>
                <label class="flex items-center gap-2 cursor-pointer text-xs text-slate-300">
                    <input type="radio" name="quiz_q_${idx}" value="no" checked class="accent-indigo-500 w-4 h-4">
                    <span>NO</span>
                </label>
            </div>
        `;
        container.appendChild(qBlock);
    });

    const submitBtn = document.getElementById('btn-eval-quiz');
    if (submitBtn) {
        submitBtn.addEventListener('click', () => {
            let totalRisk = 0;
            QUIZ_QUESTIONS.forEach((q, idx) => {
                const checked = document.querySelector(`input[name="quiz_q_${idx}"]:checked`);
                if (checked && checked.value === 'yes') {
                    totalRisk += q.risk;
                }
            });

            totalRisk = Math.min(100, totalRisk);
            const resPanel = document.getElementById('quiz-results-panel');
            resPanel.classList.remove('hidden');
            resPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });

            const scoreText = document.getElementById('quiz-score-val');
            const summaryText = document.getElementById('quiz-summary-text');
            scoreText.textContent = `${totalRisk}% Scam Risk`;

            if (totalRisk >= 50) {
                scoreText.className = 'text-2xl font-bold text-rose-500 mb-1';
                summaryText.textContent = '🚨 DANGER: Highly probable scam! Do NOT send money, cash checks, or share banking credentials with this contact.';
            } else if (totalRisk > 0) {
                scoreText.className = 'text-2xl font-bold text-amber-400 mb-1';
                summaryText.textContent = '⚠️ CAUTION: You have selected red flags associated with common employment fraud. Verify directly with the company HR.';
            } else {
                scoreText.className = 'text-2xl font-bold text-emerald-400 mb-1';
                summaryText.textContent = '✅ LOW RISK: None of the standard critical red flags were checked. Maintain standard privacy precautions.';
            }

            // Save Quiz Result to User History
            saveAuditHistory({
                type: 'Scam Quiz',
                title: '60s Scam Assessment Quiz',
                company: 'Candidate Risk Self-Assessment',
                score: totalRisk,
                verdict: scoreText.textContent,
                details: summaryText.textContent
            });
        });
    }
}

/**
 * Community Scam Board & Detailed Evidence Modal
 */
const SCAM_DATABASE = [
    {
        id: 'scam_1',
        title: 'Data Entry Assistant Telegram Trap',
        company: 'Global Cloud Logistics LLC',
        reporter: 'Priya K.',
        date: '2026-08-30',
        scamType: 'Payment Trap / Advance Fee',
        redFlag: 'Demanded ₹2,500 registration deposit on Telegram',
        financialLoss: '₹2,500 demanded (₹15,000 lost across group)',
        fakeContacts: 'Telegram: @Hiring_GlobalCloud, Email: globalcloud.hr@gmail.com, WhatsApp: +91 98765-43210',
        modusOperandi: 'Victims receive an SMS or WhatsApp stating they are selected for a ₹35,000/month remote data entry role. On Telegram, the scammer claims a ₹2,500 security deposit is compulsory for software license keys, promising a full refund on the first payday. After UPI transfer, the scammer immediately demands further "server access charges" or blocks the candidate.',
        evidence: [
            'Hiring conducted 100% via Telegram without voice/video call or HR interview',
            'Demanded ₹2,500 upfront registration & software security deposit',
            'Recruiter used free @gmail.com address rather than company domain',
            'Unrealistic compensation of ₹35,000/mo for basic copy-paste tasks'
        ],
        defenseAdvice: 'Legitimate employers NEVER ask for deposit or software fees. If paid via UPI, report immediately to Cyber Crime Helpline (1930) or cybercrime.gov.in and request an immediate UPI freeze with your bank.'
    },
    {
        id: 'scam_2',
        title: 'Counterfeit Equipment Check Fraud',
        company: 'Apex Horizon Tech Inc.',
        reporter: 'Alex M.',
        date: '2026-08-28',
        scamType: 'Fake Check Fraud',
        redFlag: 'Mailed $3,850 counterfeit cashier check for home office setup',
        financialLoss: '$3,200 out-of-pocket wire loss',
        fakeContacts: 'Email: hr@apex-horizon-careers.com (Lookalike domain), SMS: +1 (555) 321-9876',
        modusOperandi: 'Candidate received a fake offer letter via email for a Remote Admin position. Scammers mailed a paper cashier\'s check of $3,850 and asked the candidate to deposit it into their personal account and wire $3,200 to "Apex Certified IT Vendor" via Zelle to purchase an Apple MacBook. 4 days later, the bank bounced the counterfeit check, leaving the victim responsible for the $3,200 loss.',
        evidence: [
            'Employer sent a paper check and asked candidate to wire funds to a third-party vendor',
            'Used typosquatted lookalike domain (apex-horizon-careers.com instead of apexhorizon.com)',
            'Pressured victim with an urgent 24-hour deadline to wire funds',
            'No formal onboarding documents or I-9 verification completed'
        ],
        defenseAdvice: 'NEVER deposit checks from unknown employers or wire funds to their vendors. If deposited, inform your bank\'s fraud department immediately before the check bounces.'
    },
    {
        id: 'scam_3',
        title: 'YouTube Video & Product Rating VIP Task Scam',
        company: 'Nexus Digital Media Ltd',
        reporter: 'Ramesh B.',
        date: '2026-08-27',
        scamType: 'Crypto Task / Investment Trap',
        redFlag: 'Asked for USDT crypto recharge to unlock task earnings',
        financialLoss: '₹48,000 stolen in progressive crypto deposits',
        fakeContacts: 'Telegram: @Nexus_VIP_Mentor, Web: nexus-digital-vip.cc, WhatsApp: +91 88776-55443',
        modusOperandi: 'Candidates are paid ₹150 for liking 3 YouTube videos. Once trust is built, they are added to a VIP Telegram group and told to complete "prepaid merchant tasks" requiring ₹2,000 to ₹50,000 deposits in USDT crypto to unlock massive 30% returns. When the user tries to withdraw their balance, the platform claims the account is frozen and demands higher deposits.',
        evidence: [
            'Task involves liking videos, rating products, or clicking links for high daily returns',
            'Requires depositing personal money / crypto to unlock salary balances',
            'Conducted via unofficial APK apps and suspicious top-level domains (.cc / .vip)',
            'Employs shill accounts in Telegram groups displaying fake profit screenshots'
        ],
        defenseAdvice: 'Task-based pre-paid rating systems are 100% Ponzi scams. Cease sending funds immediately. Screenshot transaction hashes and report to cyber crime.'
    },
    {
        id: 'scam_4',
        title: 'Amazon Remote Reviewer Phishing Trap',
        company: 'Prime Solutions Ltd (Amazon Impersonator)',
        reporter: 'Sarah T.',
        date: '2026-08-25',
        scamType: 'Credential Phishing',
        redFlag: 'Phishing login link sent via unverified WhatsApp number',
        financialLoss: 'Compromised Amazon credentials & credit card details',
        fakeContacts: 'WhatsApp: +1 (202) 555-0198, Domain: http://amazon-review-portal-verify.site',
        modusOperandi: 'Scammer claimed to represent Amazon Recruiting and offered $30/hr to test and review products from home. Sent a fake Amazon login portal link requiring candidates to log in with their real Amazon account credentials and enter their credit card OTP to "verify buyer status".',
        evidence: [
            'Fake Amazon domain (amazon-review-portal-verify.site) trying to steal credentials',
            'Requested credit card CVV and OTP for candidate identity verification',
            'Unsolicited WhatsApp message from international non-business phone number'
        ],
        defenseAdvice: 'Never enter account passwords or OTPs on non-amazon.com domains. Change passwords immediately and enable 2-Factor Authentication.'
    },
    {
        id: 'scam_5',
        title: 'Federal Luxury Package Reshipping Mule Ring',
        company: 'Express Global Mailers',
        reporter: 'David L.',
        date: '2026-08-20',
        scamType: 'Reshipping / Money Mule',
        redFlag: 'Instructed candidate to reship stolen goods from residence',
        financialLoss: 'Candidate faced criminal investigation as an unwitting parcel mule',
        fakeContacts: 'Email: support@fedex-global-reship.org, Phone: +1 (312) 555-7890',
        modusOperandi: 'Offered work-from-home "Quality Assurance Package Forwarder" role. Victim received packages of high-end electronics purchased by criminals using stolen credit cards, inspected them, and reprinted shipping labels to send overseas. Candidate never received their promised $3,500 monthly paycheck.',
        evidence: [
            'Job requires receiving packages at home and reshipping to international addresses',
            'Employer promises monthly salary but never requires formal tax forms',
            'Involves handling stolen merchandise under candidate\'s personal name'
        ],
        defenseAdvice: 'Package reshipping from residential addresses is virtually always criminal mule activity. Refuse deliveries, do not open packages, and notify local law enforcement.'
    }
];

function initScamBoard() {
    const list = document.getElementById('scam-board-list');
    const searchInput = document.getElementById('scam-search-input');
    const modal = document.getElementById('scam-details-modal');
    const closeModalBtn1 = document.getElementById('btn-close-scam-modal');
    const closeModalBtn2 = document.getElementById('btn-close-scam-modal-2');

    if (!list) return;

    function renderScams(items) {
        list.innerHTML = '';
        if (items.length === 0) {
            list.innerHTML = '<div class="p-6 text-center text-xs text-slate-400">No matching scam reports found in the database.</div>';
            return;
        }

        items.forEach(item => {
            const card = document.createElement('div');
            card.className = 'p-4 rounded-xl bg-white border border-[#e8dfd2] hover:border-amber-700 shadow-xs transition-all flex flex-col sm:flex-row sm:items-center justify-between gap-4';
            card.innerHTML = `
                <div>
                    <div class="flex items-center gap-2 mb-1 flex-wrap">
                        <span class="px-2 py-0.5 rounded text-[10px] font-bold uppercase bg-rose-100 text-rose-700 border border-rose-200">${item.scamType}</span>
                        <span class="text-xs text-stone-500">${item.date} • Reported by ${item.reporter}</span>
                    </div>
                    <h4 class="text-sm font-bold text-stone-900">${escapeHtml(item.title)}</h4>
                    <p class="text-xs text-stone-600 font-mono mt-0.5">Company Impersonated: <span class="text-amber-800 font-bold">${escapeHtml(item.company)}</span></p>
                    <p class="text-xs text-rose-600 mt-1"><i data-lucide="alert-octagon" class="w-3.5 h-3.5 inline mr-1"></i>${escapeHtml(item.redFlag)}</p>
                </div>
                <button type="button" class="px-3.5 py-1.5 rounded-lg text-xs font-bold bg-amber-800/10 hover:bg-amber-800 text-amber-900 hover:text-white border border-amber-800/20 shrink-0 self-start sm:self-center transition-all flex items-center gap-1.5" onclick="openScamDetailsModal('${item.id}')">
                    <i data-lucide="eye" class="w-3.5 h-3.5"></i>
                    <span>View Details</span>
                </button>
            `;
            list.appendChild(card);
        });
        lucide.createIcons();
    }

    renderScams(SCAM_DATABASE);

    if (searchInput) {
        searchInput.addEventListener('input', (e) => {
            const q = e.target.value.toLowerCase();
            const filtered = SCAM_DATABASE.filter(s => 
                s.title.toLowerCase().includes(q) || 
                s.company.toLowerCase().includes(q) || 
                s.scamType.toLowerCase().includes(q) ||
                (s.modusOperandi && s.modusOperandi.toLowerCase().includes(q))
            );
            renderScams(filtered);
        });
    }

    // Modal Close events
    if (closeModalBtn1) closeModalBtn1.addEventListener('click', closeScamDetailsModal);
    if (closeModalBtn2) closeModalBtn2.addEventListener('click', closeScamDetailsModal);
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeScamDetailsModal();
        });
    }
}

/**
 * Open Detailed Evidence Modal for a specific Scam
 */
function openScamDetailsModal(scamId) {
    const item = SCAM_DATABASE.find(s => s.id === scamId);
    if (!item) return;

    const modal = document.getElementById('scam-details-modal');
    if (!modal) return;

    document.getElementById('modal-scam-type').textContent = item.scamType;
    document.getElementById('modal-report-date').textContent = `Reported: ${item.date} by ${item.reporter}`;
    document.getElementById('modal-scam-title').textContent = item.title;
    document.getElementById('modal-company-name').textContent = item.company;
    document.getElementById('modal-scam-modus').textContent = item.modusOperandi || item.redFlag;
    document.getElementById('modal-financial-trap').textContent = item.financialLoss || 'Financial exploitation reported';
    document.getElementById('modal-fake-contact').textContent = item.fakeContacts || 'Unverified contact channels';
    document.getElementById('modal-defense-advice').textContent = item.defenseAdvice || 'Cease all communication and report to cyber crime helpline (1930).';

    const evidenceList = document.getElementById('modal-evidence-list');
    evidenceList.innerHTML = '';
    
    if (item.evidence && item.evidence.length > 0) {
        item.evidence.forEach(ev => {
            const li = document.createElement('li');
            li.className = 'flex items-start gap-2 text-slate-300';
            li.innerHTML = `<i data-lucide="x-circle" class="w-4 h-4 text-rose-400 shrink-0 mt-0.5"></i> <span>${escapeHtml(ev)}</span>`;
            evidenceList.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.className = 'flex items-start gap-2 text-slate-300';
        li.innerHTML = `<i data-lucide="x-circle" class="w-4 h-4 text-rose-400 shrink-0 mt-0.5"></i> <span>${escapeHtml(item.redFlag)}</span>`;
        evidenceList.appendChild(li);
    }

    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
    lucide.createIcons();
}

function closeScamDetailsModal() {
    const modal = document.getElementById('scam-details-modal');
    if (modal) {
        modal.classList.add('hidden');
        document.body.style.overflow = 'auto';
    }
}

// Global expose
window.openScamDetailsModal = openScamDetailsModal;
window.closeScamDetailsModal = closeScamDetailsModal;

/**
 * Report Scam Form Controller
 */
function initReportScam() {
    const form = document.getElementById('report-scam-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const comp = document.getElementById('report-company').value.trim();
        const title = document.getElementById('report-title').value.trim();
        const details = document.getElementById('report-details').value.trim();
        const contact = document.getElementById('report-contact').value.trim();

        if (!comp || !title || !details) {
            alert('Please fill out all required fields.');
            return;
        }

        const newId = 'user_scam_' + Date.now();
        SCAM_DATABASE.unshift({
            id: newId,
            title: title,
            company: comp,
            reporter: 'Community User',
            date: 'Today',
            scamType: 'Community Report',
            redFlag: details.substring(0, 100) + '...',
            financialLoss: 'Investigating financial impact',
            fakeContacts: contact || 'Not specified',
            modusOperandi: details,
            evidence: [
                'Reported directly by job seeker community member',
                'Unverified recruitment communication pattern'
            ],
            defenseAdvice: 'Verify with the company\'s official careers portal directly before sending documents or money.'
        });

        alert('Thank you! Your scam report has been submitted to the community database to protect other job seekers.');
        form.reset();
        initScamBoard();
    });
}

/**
 * 1. Multi-Language Switcher (English / Telugu / Hindi)
 */
const I18N_DICTIONARY = {
    en: {
        ticker_badge: 'LIVE SCAM RADAR',
        tagline: 'Online Job Scam & Fraud Detection',
        nav_scanner: 'Job Scanner',
        nav_offer: 'Offer Auditor',
        nav_salary: 'Salary Checker',
        nav_recruiter: 'Recruiter Check',
        nav_quiz: '60s Scam Quiz',
        nav_lookup: 'Phone/UPI Lookup',
        nav_complaint: 'Cyber Complaint',
        nav_scam_db: 'Scam Database',
        nav_report: 'Report Scam',
        nav_history: 'My History',
        btn_signin: 'Sign In / Register',
        hero_badge: 'AI Heuristics & 150+ Scam Pattern Detection Active',
        hero_title_1: 'Detect Fake Job Postings & ',
        hero_title_2: 'Employment Scams',
        hero_desc: 'Paste suspicious job descriptions, upload WhatsApp/Telegram chat screenshots (OCR), or check salary realism.',
        form_title: 'Job Posting Details',
        ocr_title: '📸 Upload WhatsApp / Telegram Chat Screenshot (OCR Scan)',
        ocr_desc: 'Upload PNG/JPG photo to automatically extract chat text',
        label_job_title: 'Job Title',
        label_company: 'Company Name',
        label_salary: 'Offered Salary / Rate',
        label_email: 'Contact Email',
        label_website: 'Company Website',
        label_desc: 'Job Description or Recruitment Message *',
        btn_clear: 'Clear Fields',
        btn_run_scan: 'Run AI Scam Verification',
        red_flags_title: 'Top 5 Red Flags of Online Job Scams',
        sub_pill_free: 'Free Scans',
        sub_pill_pro: 'PRO Member (Unlimited)',
        free_scans_left: 'Free Scans Remaining',
        pro_unlimited: '👑 Pro: Unlimited AI Checks',
        sub_modal_title: 'Unlock Unlimited AI Job Scam Protection',
        sub_modal_subtitle: 'You have used your 2 free AI scam checks. Subscribe to JobGuard AI Pro to unlock unlimited job scans, offer audits, OCR chat analysis, and legal complaint drafts.',
        sub_limit_reached_tag: 'Free Check Limit Reached (2 / 2 Used)',
        plan_monthly_title: 'Pro Monthly',
        plan_yearly_title: 'Pro Annual',
        btn_subscribe_now: 'Subscribe Now & Unlock Unlimited Checks',
        sub_success_alert: '🎉 Congratulations! Your JobGuard AI Pro subscription is now active. You now have Unlimited AI Scam Verifications & Offer Audits!'
    },
    te: {
        ticker_badge: 'లైవ్ స్కామ్ అలర్ట్',
        tagline: 'ఆన్‌లైన్ జాబ్ స్కామ్ & ఫ్రాడ్ డిటెక్షన్',
        nav_scanner: 'జాబ్ స్కానర్',
        nav_offer: 'ఆఫర్ లెటర్ ఆడిటర్',
        nav_salary: 'జీతం చెకర్',
        nav_recruiter: 'రిక్యూటర్ చెక్',
        nav_quiz: '60సె. స్కామ్ క్విజ్',
        nav_lookup: 'ఫోన్/UPI లుకప్',
        nav_complaint: 'పోలీస్ ఫిర్యాదు పత్రం',
        nav_scam_db: 'స్కామ్ డేటాబేస్',
        nav_report: 'స్కామ్ రిపోర్ట్ చేయండి',
        nav_history: 'నా స్కాన్ హిస్టరీ',
        btn_signin: 'లాగిన్ / రిజిస్టర్',
        hero_badge: 'AI మోడల్ & 150+ స్కామ్ ప్యాటర్న్స్ యాక్టివ్‌గా ఉన్నాయి',
        hero_title_1: 'నకిలీ ఉద్యోగ ప్రకటనలు & ',
        hero_title_2: 'స్కామ్‌లను గుర్తించండి',
        hero_desc: 'అనుమానాస్పద జాబ్ వివరాలను పేస్ట్ చేయండి లేదా వాట్సాప్/టెలిగ్రామ్ స్క్రీన్‌షాట్ అప్‌లోడ్ చేసి స్కామ్ ఉందో లేదో క్షణాల్లో తెలుసుకోండి.',
        form_title: 'ఉద్యోగ ప్రకటన వివరాలు',
        ocr_title: '📸 వాట్సాప్ / టెలిగ్రామ్ చాట్ స్క్రీన్‌షాట్ అప్‌లోడ్ (OCR స్కానర్)',
        ocr_desc: 'ఫొటో అప్‌లోడ్ చేస్తే అందులోని టెక్స్ట్‌ను ఆటోమేటిక్‌గా రీడ్ చేస్తుంది',
        label_job_title: 'ఉద్యోగ హోదా (Job Title)',
        label_company: 'కంపెనీ పేరు',
        label_salary: 'ఆఫర్ చేసిన జీతం',
        label_email: 'కాంటాక్ట్ ఈమెయిల్',
        label_website: 'కంపెనీ వెబ్‌సైట్',
        label_desc: 'జాబ్ వివరణ లేదా రిక్రూటర్ మెసేజ్ *',
        btn_clear: 'క్లియర్ చేయండి',
        btn_run_scan: 'AI స్కామ్ వెరిఫికేషన్ చేయండి',
        red_flags_title: 'ఆన్‌లైన్ జాబ్ స్కామ్స్ టాప్ 5 రెడ్ ఫ్లాగ్స్',
        sub_pill_free: 'ఉచిత స్కాన్లు',
        sub_pill_pro: 'ప్రో మెంబర్ (అపరిమిత)',
        free_scans_left: 'ఉచిత స్కాన్లు మిగిలి ఉన్నాయి',
        pro_unlimited: '👑 ప్రో: అపరిమిత AI స్కాన్‌లు',
        sub_modal_title: 'అపరిమిత AI జాబ్ స్కామ్ ప్రొటెక్షన్ పొందండి',
        sub_modal_subtitle: 'మీరు మీ 2 ఉచిత AI స్కాన్‌లను ఉపయోగించారు. అపరిమిత జాబ్ చెక్స్, ఆఫర్ లెటర్ ఆడిట్ మరియు లీగల్ డ్రాఫ్ట్స్ కోసం ప్రో సబ్‌స్క్రిప్షన్ తీసుకోండి.',
        sub_limit_reached_tag: 'ఉచిత స్కాన్ పరిమితి ముగిసింది (2/2 వాడారు)',
        plan_monthly_title: 'ప్రో నెలవారీ ప్లాన్',
        plan_yearly_title: 'ప్రో వార్షిక ప్లాన్',
        btn_subscribe_now: 'ఇప్పుడే సబ్‌స్క్రయిబ్ చేసుకోండి (అపరిమిత స్కాన్లు)',
        sub_success_alert: '🎉 అభినందనలు! మీ JobGuard AI ప్రో సబ్‌స్క్రిప్షన్ యాక్టివేట్ అయింది. ఇప్పుడు మీరు అపరిమితంగా చెక్ చేసుకోవచ్చు!'
    },
    hi: {
        ticker_badge: 'लाइव स्कैम रडार',
        tagline: 'ऑनलाइन जॉब स्कैम एवं फ्रॉड डिटेक्शन',
        nav_scanner: 'जॉब स्कैनर',
        nav_offer: 'ऑफर लेटर ऑडिटर',
        nav_salary: 'सैलरी चेकर',
        nav_recruiter: 'रिक्रूटर चेक',
        nav_quiz: '60s फ्रॉड क्विज',
        nav_lookup: 'फोन/UPI लुकअप',
        nav_complaint: 'साइबर पुलिस शिकायत',
        nav_scam_db: 'स्कैम डेटाबेस',
        nav_report: 'स्कैम रिपोर्ट करें',
        nav_history: 'मेरा इतिहास',
        btn_signin: 'लॉग इन / रजिस्टर',
        hero_badge: 'AI मॉडल एवं 150+ स्कैम पैटर्न सक्रिय',
        hero_title_1: 'फर्जी जॉब पोस्टिंग एवं ',
        hero_title_2: 'नौकरी घोटालों को पहचानें',
        hero_desc: 'संदेहास्पद नौकरी विवरण पेस्ट करें या व्हाट्सएप/टेलीग्राम चैट स्क्रीनशॉट अपलोड कर तुरंत फ्रॉड का पता लगाएं।',
        form_title: 'नौकरी विवरण (Job Posting)',
        ocr_title: '📸 व्हाट्सएप / टेलीग्राम चैट स्क्रीनशॉट अपलोड (OCR)',
        ocr_desc: 'फोटो अपलोड करें और चैट टेक्स्ट को तुरंत स्कैन करें',
        label_job_title: 'पद / जॉब टाइटल',
        label_company: 'कंपनी का नाम',
        label_salary: 'वेतन / सैलरी',
        label_email: 'ईमेल पता',
        label_website: 'कंपनी वेबसाइट',
        label_desc: 'नौकरी विवरण या संदेश *',
        btn_clear: 'साफ़ करें',
        btn_run_scan: 'AI स्कैम वेरिफिकेशन शुरू करें',
        red_flags_title: 'ऑनलाइन जॉब स्कैम के 5 बड़े खतरे',
        sub_pill_free: 'फ्री स्कैन',
        sub_pill_pro: 'प्रो मेंबर (अनलिमिटेड)',
        free_scans_left: 'फ्री स्कैन शेष हैं',
        pro_unlimited: '👑 प्रो: अनलिमिटेड AI चेक्स',
        sub_modal_title: 'अनलिमिटेड AI जॉब स्कैम सुरक्षा अनलॉक करें',
        sub_modal_subtitle: 'आपने अपने 2 फ्री AI स्कैन उपयोग कर लिए हैं। अनलिमिटेड जॉब स्कैन, ऑफर ऑडिट और लीगल ड्राफ्ट के लिए प्रो सब्सक्रिप्शन लें।',
        sub_limit_reached_tag: 'फ्री स्कैन सीमा समाप्त (2/2 उपयोग)',
        plan_monthly_title: 'प्रो मासिक प्लान',
        plan_yearly_title: 'प्रो वार्षिक प्लान',
        btn_subscribe_now: 'अभी सब्सक्राइब करें और अनलिमिटेड चेक्स अनलॉक करें',
        sub_success_alert: '🎉 बधाई! आपका JobGuard AI प्रो सब्सक्रिप्शन सक्रिय हो गया है। अब आप अनलिमिटेड चेक्स कर सकते हैं!'
    }
};

let currentLang = 'en';

function initLanguageSwitcher() {
    const toggleBtn = document.getElementById('btn-language-toggle');
    const menu = document.getElementById('lang-dropdown-menu');

    if (toggleBtn && menu) {
        toggleBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            menu.classList.toggle('hidden');
        });

        document.addEventListener('click', (e) => {
            if (!menu.contains(e.target) && e.target !== toggleBtn) {
                menu.classList.add('hidden');
            }
        });
    }

    // Apply default language
    const savedLang = localStorage.getItem('jobguard_lang') || 'en';
    selectLanguage(savedLang);
}

function selectLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('jobguard_lang', lang);

    const dict = I18N_DICTIONARY[lang];
    if (!dict) return;

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (dict[key]) {
            el.textContent = dict[key];
        }
    });

    // Update label on dropdown button
    const label = document.getElementById('current-lang-label');
    if (label) {
        label.textContent = lang === 'te' ? 'తెలుగు' : lang === 'hi' ? 'हिन्दी' : 'English';
    }

    // Update Checkmarks in dropdown
    ['en', 'te', 'hi'].forEach(l => {
        const checkIcon = document.getElementById(`check-lang-${l}`);
        if (checkIcon) {
            if (l === lang) {
                checkIcon.classList.remove('hidden');
            } else {
                checkIcon.classList.add('hidden');
            }
        }
    });

    // Hide dropdown menu
    const menu = document.getElementById('lang-dropdown-menu');
    if (menu) menu.classList.add('hidden');

    if (typeof updateSubscriptionUI === 'function') {
        updateSubscriptionUI();
    }

    lucide.createIcons();
}
window.selectLanguage = selectLanguage;

/**
 * 2. WhatsApp / Telegram Chat Screenshot OCR Scanner
 */
function initOcrScanner() {
    const ocrBox = document.getElementById('ocr-drop-box');
    const ocrInput = document.getElementById('ocr-file-input');
    const ocrStatusPill = document.getElementById('ocr-status-pill');

    if (!ocrBox || !ocrInput) return;

    ocrBox.addEventListener('click', () => ocrInput.click());

    ocrInput.addEventListener('change', async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        if (ocrStatusPill) {
            ocrStatusPill.innerHTML = '<i data-lucide="loader" class="w-3.5 h-3.5 animate-spin inline mr-1"></i> Scanning Image...';
            lucide.createIcons();
        }

        try {
            if (typeof Tesseract === 'undefined') {
                throw new Error('Tesseract OCR library not loaded.');
            }

            const { data: { text } } = await Tesseract.recognize(file, 'eng');
            
            if (ocrStatusPill) {
                ocrStatusPill.innerHTML = '✅ Extracted';
                ocrStatusPill.className = 'text-[10px] px-2.5 py-1 rounded-lg bg-emerald-600 text-white font-bold shrink-0';
            }

            const descTextarea = document.getElementById('job-description');
            if (descTextarea) {
                descTextarea.value = text.trim();
                // Hide old output until user clicks 'Run AI Scam Verification'
                document.getElementById('scan-results-panel')?.classList.add('hidden');
            }
        } catch (err) {
            console.error('OCR Error:', err);
            if (ocrStatusPill) {
                ocrStatusPill.textContent = 'Upload Photo';
            }
            alert('Failed to extract text from screenshot: ' + err.message);
        }
    });
}

/**
 * 3. Scammer Phone / Telegram / UPI Blacklist Lookup
 */
const KNOWN_SCAM_LOOKUP_DB = [
    { query: '+919876543210', formatted: '+91 98765-43210', type: 'WhatsApp Phone', category: 'Crypto VIP Task Fraud', complaints: 14, risk: 'CRITICAL', desc: 'Used to send bulk WhatsApp messages promising ₹12,000/day for liking videos. Trapped victims in Telegram VIP groups.' },
    { query: '@nexus_vip_mentor', formatted: '@Nexus_VIP_Mentor', type: 'Telegram Handle', category: 'Prepaid Merchant Task Scam', complaints: 28, risk: 'CRITICAL', desc: 'Demands cryptocurrency (USDT) deposits to unlock fake rating salary.' },
    { query: 'hr.globalcloud@okaxis', formatted: 'hr.globalcloud@okaxis', type: 'UPI VPA ID', category: 'Upfront Registration Fee Trap', complaints: 9, risk: 'CRITICAL', desc: 'Collected ₹2,500 "refundable security deposits" for fake data entry jobs.' },
    { query: '+15553219876', formatted: '+1 (555) 321-9876', type: 'US SMS Number', category: 'Counterfeit Check Equipment Scam', complaints: 6, risk: 'CRITICAL', desc: 'Mailed fake cashier checks and instructed victims to wire funds to IT vendors.' }
];

function initLookupEngine() {
    const btn = document.getElementById('btn-run-lookup');
    const input = document.getElementById('lookup-query-input');

    if (btn && input) {
        btn.addEventListener('click', () => runLookupQuery(input.value.trim()));
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') runLookupQuery(input.value.trim());
        });
    }
}

function searchLookupNumber(val) {
    const input = document.getElementById('lookup-query-input');
    if (input) {
        input.value = val;
        runLookupQuery(val);
    }
}
window.searchLookupNumber = searchLookupNumber;

function runLookupQuery(q) {
    if (!q) {
        alert('Please enter a phone number, Telegram handle, or UPI ID.');
        return;
    }

    const cleanQ = q.toLowerCase().replace(/[\s\-\(\)]/g, '');
    const found = KNOWN_SCAM_LOOKUP_DB.find(item => item.query.includes(cleanQ) || cleanQ.includes(item.query));
    const box = document.getElementById('lookup-results-box');
    box.classList.remove('hidden');

    if (found) {
        box.className = 'rounded-xl p-5 border border-rose-300 bg-rose-50 text-slate-800 space-y-3';
        box.innerHTML = `
            <div class="flex items-center justify-between border-b border-rose-200 pb-3">
                <div class="flex items-center gap-2">
                    <span class="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase bg-rose-600 text-white">🚨 KNOWN SCAMMER BLACKLISTED</span>
                    <span class="text-xs font-mono font-semibold text-rose-800">${found.formatted}</span>
                </div>
                <span class="text-xs font-bold text-rose-700 bg-rose-200/60 px-2 py-0.5 rounded-lg">${found.complaints} Community Reports</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                <div>
                    <span class="text-slate-500 font-semibold block">Channel Type:</span>
                    <span class="text-slate-800 font-bold">${found.type}</span>
                </div>
                <div>
                    <span class="text-slate-500 font-semibold block">Fraud Classification:</span>
                    <span class="text-rose-700 font-bold">${found.category}</span>
                </div>
            </div>
            <p class="text-xs text-slate-700 bg-white p-3 rounded-lg border border-rose-200 leading-relaxed">${found.desc}</p>
            <div class="text-xs text-rose-900 font-semibold">
                ⚠️ Action Required: Block this contact immediately. Do NOT send money or UPI payments under any circumstances!
            </div>
        `;
    } else {
        box.className = 'rounded-xl p-5 border border-emerald-300 bg-emerald-50 text-slate-800 space-y-2';
        box.innerHTML = `
            <div class="flex items-center gap-2">
                <i data-lucide="shield-check" class="w-5 h-5 text-emerald-600"></i>
                <span class="text-sm font-bold text-emerald-900">No Direct Blacklist Match for "${escapeHtml(q)}"</span>
            </div>
            <p class="text-xs text-slate-600 leading-relaxed">
                This specific phone number, handle, or UPI ID has not been reported in our scam database yet. However, always exercise caution if an employer asks for payments, deposit checks, or interviews solely via text chat.
            </p>
        `;
    }

    // Save Blacklist Lookup to User History
    saveAuditHistory({
        type: 'Phone Lookup',
        title: `Blacklist Lookup: ${q}`,
        company: found ? `${found.type} (${found.category})` : `Query: ${q}`,
        score: found ? 95 : 5,
        verdict: found ? '🚨 Blacklisted Scammer' : '✅ No Blacklist Match',
        details: found ? `${found.desc} (${found.complaints} community reports)` : `Queried "${q}" - no direct reports found in database`
    });

    lucide.createIcons();
}

/**
 * 4. Official Cyber Crime Complaint Draft Generator
 */
function initComplaintGenerator() {
    const form = document.getElementById('complaint-generator-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        const victimName = document.getElementById('comp-victim-name').value.trim();
        const victimPhone = document.getElementById('comp-victim-phone').value.trim();
        const victimCity = document.getElementById('comp-victim-city').value.trim();
        const suspectName = document.getElementById('comp-suspect-name').value.trim() || 'Unknown Scammer / Impersonated Company';
        const suspectContact = document.getElementById('comp-suspect-contact').value.trim() || 'Not Provided';
        const lossAmount = document.getElementById('comp-loss-amount').value.trim() || 'Nil / Sensitive Data Compromise';
        const incidentDesc = document.getElementById('comp-incident-desc').value.trim();

        const currentDate = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'long', year: 'numeric' });

        const draft = `FORMAL COMPLAINT REGARDING ONLINE EMPLOYMENT / CYBER FRAUD
To,
The Cyber Crime Police Station / National Cyber Crime Reporting Portal (cybercrime.gov.in)
Helpline: 1930

Date: ${currentDate}

SUBJECT: Formal complaint against fraudulent recruitment operation under Section 66D of Information Technology Act, 2000 and Section 420 of Indian Penal Code (IPC).

RESPECTED CYBER CRIME CELL / INVESTIGATING OFFICER,

I am submitting this formal complaint regarding an online fraudulent job recruitment racket that has defrauded/targeted me under the guise of an employment opportunity.

1. COMPLAINANT PARTICULARS:
   - Full Name: ${victimName}
   - Contact Number: ${victimPhone}
   - Residence / Location: ${victimCity || 'Provided in official KYC'}

2. SUSPECT / ACCUSED ENTITY DETAILS:
   - Impersonated Company / Scammer Name: ${suspectName}
   - Suspect Phone / Telegram / UPI Handle: ${suspectContact}
   - Financial Loss Demanded / Incurred: ${lossAmount}

3. INCIDENT SUMMARY & MODUS OPERANDI:
${incidentDesc}

4. PRAYER / RELIEF SOUGHT:
In light of the above cyber fraud, I respectfully request the Cyber Crime Investigation Cell to:
a) Immediately initiate an inquiry into the suspect phone numbers, Telegram channels, and UPI Virtual Payment Addresses (VPAs).
b) Instruct the concerned bank / intermediary to freeze fraudulent UPI receiver accounts to prevent further misappropriation of funds.
c) Take strict legal action against the culprits in accordance with the IT Act and criminal law.

I declare that the information stated above is true and accurate to the best of my knowledge.

Sincerely,

${victimName}
Phone: ${victimPhone}
Generated via JobGuard AI Legal Assistance Tool`;

        const previewBox = document.getElementById('generated-complaint-box');
        const previewText = document.getElementById('complaint-letter-text');
        
        previewText.textContent = draft;
        previewBox.classList.remove('hidden');
        previewBox.scrollIntoView({ behavior: 'smooth' });

        // Save Complaint Generation to User History
        saveAuditHistory({
            type: 'Police Complaint',
            title: `Police Complaint Draft: ${suspectName}`,
            company: `Target: ${suspectContact}`,
            score: 100,
            verdict: '⚖️ Legal Draft Ready',
            details: `Complaint prepared for Cyber Crime Helpline 1930 • Loss Claim: ${lossAmount}`
        });
    });
}

function copyComplaintDraft() {
    const text = document.getElementById('complaint-letter-text')?.textContent;
    if (text) {
        navigator.clipboard.writeText(text);
        alert('Police complaint draft copied to clipboard!');
    }
}
window.copyComplaintDraft = copyComplaintDraft;

/**
 * 5. User Audit History ("My Scans") - Complete Deletion & Filter Controls
 */
let currentHistoryFilter = 'all';
let selectedHistoryItemIds = new Set();

function filterHistory(filterType) {
    currentHistoryFilter = filterType;
    selectedHistoryItemIds.clear();
    updateBatchDeleteUI();

    document.querySelectorAll('.history-filter-btn').forEach(btn => {
        if (btn.getAttribute('onclick')?.includes(filterType)) {
            btn.className = 'history-filter-btn active px-3 py-1.5 rounded-lg font-bold bg-amber-800 text-white shadow-xs transition-all cursor-pointer';
        } else {
            btn.className = 'history-filter-btn px-3 py-1.5 rounded-lg font-semibold bg-[#f2eee6] text-stone-700 hover:bg-[#e8dfd2] transition-all cursor-pointer';
        }
    });
    renderUserHistory();
}
window.filterHistory = filterHistory;

function toggleHistoryItemSelect(id, isChecked) {
    if (isChecked) {
        selectedHistoryItemIds.add(id);
    } else {
        selectedHistoryItemIds.delete(id);
    }
    updateBatchDeleteUI();
}
window.toggleHistoryItemSelect = toggleHistoryItemSelect;

function toggleSelectAllHistory(isChecked) {
    const allHistory = JSON.parse(localStorage.getItem('jobguard_history') || '[]');
    const filtered = currentHistoryFilter === 'all' 
        ? allHistory 
        : allHistory.filter(item => item.type === currentHistoryFilter);

    if (isChecked) {
        filtered.forEach(item => selectedHistoryItemIds.add(item.id));
    } else {
        selectedHistoryItemIds.clear();
    }

    document.querySelectorAll('.history-item-checkbox').forEach(cb => {
        cb.checked = isChecked;
    });

    updateBatchDeleteUI();
}
window.toggleSelectAllHistory = toggleSelectAllHistory;

function updateBatchDeleteUI() {
    const btn = document.getElementById('btn-delete-selected');
    const countEl = document.getElementById('selected-count');
    const count = selectedHistoryItemIds.size;

    if (countEl) countEl.textContent = count;
    if (btn) {
        if (count > 0) {
            btn.classList.remove('hidden');
            btn.classList.add('flex');
        } else {
            btn.classList.add('hidden');
            btn.classList.remove('flex');
        }
    }
}

function deleteSelectedHistory() {
    if (selectedHistoryItemIds.size === 0) return;

    if (confirm(`మీరు సెలెక్ట్ చేసిన ${selectedHistoryItemIds.size} టెస్ట్ రికార్డులను ఖచ్చితంగా తొలగించాలనుకుంటున్నారా? (Delete ${selectedHistoryItemIds.size} selected test records?)`)) {
        try {
            let history = JSON.parse(localStorage.getItem('jobguard_history') || '[]');
            history = history.filter(item => !selectedHistoryItemIds.has(item.id));
            localStorage.setItem('jobguard_history', JSON.stringify(history));
            selectedHistoryItemIds.clear();
            updateBatchDeleteUI();
            renderUserHistory();
        } catch (e) {
            console.error(e);
        }
    }
}
window.deleteSelectedHistory = deleteSelectedHistory;

function deleteAuditHistory(id) {
    if (confirm('ఈ టెస్ట్ రికార్డును తొలగించాలనుకుంటున్నారా? (Delete this test record?)')) {
        try {
            let history = JSON.parse(localStorage.getItem('jobguard_history') || '[]');
            history = history.filter(item => item.id !== id);
            selectedHistoryItemIds.delete(id);
            localStorage.setItem('jobguard_history', JSON.stringify(history));
            updateBatchDeleteUI();
            renderUserHistory();
        } catch (e) {
            console.error(e);
        }
    }
}
window.deleteAuditHistory = deleteAuditHistory;

function initUserHistory() {
    renderUserHistory();

    const clearBtn = document.getElementById('btn-clear-history');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            const history = JSON.parse(localStorage.getItem('jobguard_history') || '[]');
            if (history.length === 0) {
                alert('మీ హిస్టరీ ఇప్పటికే ఖాళీగా ఉంది. (Your test history is already empty.)');
                return;
            }
            if (confirm('మీరు మొత్తం టెస్ట్ స్కాన్ హిస్టరీని క్లియర్ చేయాలనుకుంటున్నారా? (Are you sure you want to clear your entire test history?)')) {
                localStorage.removeItem('jobguard_history');
                selectedHistoryItemIds.clear();
                updateBatchDeleteUI();
                renderUserHistory();
            }
        });
    }
}

function saveAuditHistory(item) {
    try {
        let history = JSON.parse(localStorage.getItem('jobguard_history') || '[]');
        const newItem = {
            id: 'test_' + Date.now() + '_' + Math.random().toString(36).substring(2, 6),
            date: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }) + ' • ' + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            title: item.title || 'Untitled Verification',
            company: item.company || 'Direct Verification',
            score: typeof item.score === 'number' ? item.score : 0,
            verdict: item.verdict || 'Completed',
            type: item.type || 'Job Scan',
            details: item.details || ''
        };
        history.unshift(newItem);
        // Keep up to 50 genuine test scans
        history = history.slice(0, 50);
        localStorage.setItem('jobguard_history', JSON.stringify(history));
        renderUserHistory();
    } catch (e) {
        console.error(e);
    }
}
window.saveAuditHistory = saveAuditHistory;

function renderUserHistory() {
    const list = document.getElementById('user-history-list');
    const countBadge = document.getElementById('history-count-badge');
    const selectAllWrap = document.getElementById('history-select-all-wrap');
    if (!list) return;

    const allHistory = JSON.parse(localStorage.getItem('jobguard_history') || '[]');
    if (countBadge) {
        countBadge.textContent = `${allHistory.length} Test${allHistory.length === 1 ? '' : 's'}`;
    }

    const filtered = currentHistoryFilter === 'all' 
        ? allHistory 
        : allHistory.filter(item => item.type === currentHistoryFilter);

    if (allHistory.length === 0) {
        if (selectAllWrap) selectAllWrap.classList.add('hidden');
        list.innerHTML = `
            <div class="p-10 text-center text-xs text-stone-500 border border-dashed border-[#e8dfd2] rounded-2xl bg-[#f7f4ed]/50 space-y-2">
                <div class="w-12 h-12 rounded-2xl bg-white border border-[#e8dfd2] flex items-center justify-center mx-auto text-amber-800 shadow-xs">
                    <i data-lucide="clipboard-list" class="w-6 h-6"></i>
                </div>
                <h4 class="font-bold text-stone-800 text-sm">మీరు ఇంకా ఏ టెస్ట్ చేయలేదు (No Test History Yet)</h4>
                <p class="max-w-md mx-auto text-stone-500 text-[11px] leading-relaxed">
                    మీరు జాబ్ పోస్ట్ స్కాన్, ఆఫర్ లెటర్ ఆడిట్, రిక్రూటర్ వెరిఫికేషన్ లేదా ఫోన్/UPI లుకప్ చేసినప్పుడు మాత్రమే ఆ ఫలితాలు ఇక్కడ ఆటోమేటిక్‌గా రికార్డ్ అవుతాయి.
                </p>
                <div class="pt-2">
                    <button type="button" onclick="document.querySelector('[data-target=\\'tab-scanner\\']')?.click()" class="px-4 py-2 rounded-xl text-xs font-bold bg-amber-800 hover:bg-amber-900 text-white shadow-xs transition-all cursor-pointer">
                        🔍 మొదటి జాబ్ స్కాన్ చేయండి (Run First Job Scan)
                    </button>
                </div>
            </div>
        `;
        lucide.createIcons();
        return;
    }

    if (selectAllWrap) {
        selectAllWrap.classList.remove('hidden');
        selectAllWrap.classList.add('flex');
    }

    if (filtered.length === 0) {
        list.innerHTML = `
            <div class="p-8 text-center text-xs text-stone-500 border border-dashed border-[#e8dfd2] rounded-xl bg-white space-y-1">
                <p>No tests found under the "<strong>${currentHistoryFilter}</strong>" category.</p>
                <button type="button" onclick="filterHistory('all')" class="text-amber-800 font-bold hover:underline text-[11px] cursor-pointer">View All Tests (${allHistory.length})</button>
            </div>
        `;
        lucide.createIcons();
        return;
    }

    list.innerHTML = '';
    filtered.forEach(item => {
        const row = document.createElement('div');
        row.className = 'flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl bg-white border border-[#e8dfd2] hover:border-amber-700/40 transition-all shadow-xs gap-3.5 group';

        const typeIcon = item.type === 'Job Scan' ? 'scan-search' :
                         item.type === 'Offer Audit' ? 'file-check-2' :
                         item.type === 'Salary Check' ? 'badge-dollar-sign' :
                         item.type === 'Recruiter Check' ? 'user-check' :
                         item.type === 'Phone Lookup' ? 'phone-call' :
                         item.type === 'Scam Quiz' ? 'help-circle' :
                         item.type === 'Police Complaint' ? 'file-warning' : 'shield-alert';

        const badgeColor = item.score >= 50 ? 'bg-rose-100 text-rose-800 border-rose-200' :
                           item.score >= 20 ? 'bg-amber-100 text-amber-800 border-amber-200' :
                           'bg-emerald-100 text-emerald-800 border-emerald-200';

        const isChecked = selectedHistoryItemIds.has(item.id);

        row.innerHTML = `
            <div class="flex items-start gap-3 flex-1 min-w-0">
                <!-- Checkbox -->
                <div class="pt-1 shrink-0">
                    <input type="checkbox" onchange="toggleHistoryItemSelect('${item.id}', this.checked)" class="history-item-checkbox w-4 h-4 rounded text-amber-800 accent-amber-800 cursor-pointer" ${isChecked ? 'checked' : ''}>
                </div>

                <!-- Icon -->
                <div class="w-10 h-10 rounded-xl bg-amber-50 border border-amber-200/80 text-amber-800 flex items-center justify-center shrink-0 shadow-2xs mt-0.5">
                    <i data-lucide="${typeIcon}" class="w-5 h-5"></i>
                </div>

                <!-- Details -->
                <div class="flex-1 min-w-0 space-y-0.5">
                    <div class="flex items-center gap-2 flex-wrap">
                        <span class="px-2 py-0.5 rounded-md text-[10px] font-extrabold uppercase bg-stone-100 text-stone-700 border border-stone-200">${item.type}</span>
                        <span class="px-2 py-0.5 rounded-md text-[10px] font-extrabold uppercase border ${badgeColor}">${item.score}% Risk</span>
                        <span class="text-[11px] text-stone-400 font-mono">${item.date}</span>
                    </div>
                    <h4 class="font-bold text-xs sm:text-sm text-stone-900 truncate">${escapeHtml(item.title)}</h4>
                    <p class="text-[11px] text-stone-500 truncate"><strong class="text-stone-700">Entity/Target:</strong> ${escapeHtml(item.company)}</p>
                    ${item.details ? `<p class="text-[11px] text-stone-600 bg-[#f7f4ed] px-2.5 py-1 rounded-lg border border-[#e8dfd2] mt-1 line-clamp-2">${escapeHtml(item.details)}</p>` : ''}
                </div>
            </div>

            <!-- Action: Verdict & Delete Button -->
            <div class="flex sm:flex-col items-center sm:items-end justify-between sm:justify-center gap-2 shrink-0 border-t sm:border-t-0 border-[#e8dfd2] pt-2 sm:pt-0">
                <span class="text-xs font-bold px-2.5 py-1 rounded-lg bg-[#f2eee6] text-stone-800 border border-[#e8dfd2]">${escapeHtml(item.verdict)}</span>
                <button type="button" onclick="deleteAuditHistory('${item.id}')" class="px-2.5 py-1 rounded-lg text-xs font-semibold text-rose-600 hover:bg-rose-50 border border-rose-200/80 flex items-center gap-1 transition-all cursor-pointer" title="Delete this test record">
                    <i data-lucide="trash" class="w-3.5 h-3.5"></i>
                    <span>Delete</span>
                </button>
            </div>
        `;
        list.appendChild(row);
    });

    lucide.createIcons();
}

/**
 * Hook into Job Scan result to save to history
 */
const originalRenderJobResults = renderJobResults;
renderJobResults = function(res) {
    originalRenderJobResults(res);
    saveAuditHistory({
        title: currentAnalysisResult?.jobData?.title || 'Job Posting Scan',
        company: currentAnalysisResult?.jobData?.company || 'Analyzed Employer',
        score: res.score,
        verdict: (typeof res.verdict === 'string' ? res.verdict : res.verdict?.label) || `${res.score}% Risk`,
        type: 'Job Scan',
        details: res.summaryStatement || res.summary || 'Job posting heuristic evaluation completed'
    });
};

/**
 * Utility functions
 */
function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

function exportAnalysisReport() {
    if (!currentAnalysisResult) {
        alert('Please run a job scan first before exporting the report.');
        return;
    }
    window.print();
}

// JobGuard AI Frontend Suite v2.5.0 
