/**
 * WebdriverIO Configuration for Appium Mobile Web Testing
 * Target: Android Chrome via Appium
 * App: Skill-Gap AI Platform (https://skill-gap-ai.streamlit.app)
 */

const path = require('path');

const BASE_URL = process.env.BASE_URL || 'https://skill-gap-ai.streamlit.app';
const APPIUM_HOST = process.env.APPIUM_HOST || 'localhost';
const APPIUM_PORT = parseInt(process.env.APPIUM_PORT || '4723', 10);
const ANDROID_DEVICE = process.env.ANDROID_DEVICE || 'emulator-5554';
const ANDROID_VERSION = process.env.ANDROID_VERSION || '13.0';
const IMPLICIT_TIMEOUT = parseInt(process.env.IMPLICIT_TIMEOUT || '10000', 10);
const EXPLICIT_TIMEOUT = parseInt(process.env.EXPLICIT_TIMEOUT || '30000', 10);
const RESULTS_DIR = path.join(__dirname, 'results');

exports.config = {
  // ============================================================
  // Runner & Framework
  // ============================================================
  runner: 'local',

  // ============================================================
  // Specs
  // ============================================================
  specs: [
    './tests/**/*.js'
  ],
  exclude: [],

  // ============================================================
  // Capabilities
  // ============================================================
  maxInstances: 1,

  capabilities: [
    {
      platformName: 'Android',
      browserName: 'Chrome',
      'appium:automationName': 'UiAutomator2',
      'appium:deviceName': ANDROID_DEVICE,
      'appium:platformVersion': ANDROID_VERSION,
      'appium:chromedriverAutodownload': true,
      'appium:noReset': false,
      'appium:fullReset': false,
      'appium:newCommandTimeout': 120,
      'appium:adbExecTimeout': 60000,
      'appium:uiautomator2ServerLaunchTimeout': 60000,
      'appium:uiautomator2ServerInstallTimeout': 60000,
      'appium:nativeWebScreenshot': true,
      'goog:chromeOptions': {
        args: [
          '--disable-popup-blocking',
          '--disable-infobars',
          '--no-sandbox',
          '--disable-dev-shm-usage'
        ],
        mobileEmulation: {
          deviceMetrics: { width: 390, height: 844, pixelRatio: 3.0 },
          userAgent:
            'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
        }
      }
    }
  ],

  // ============================================================
  // Appium Service
  // ============================================================
  services: [
    [
      'appium',
      {
        command: 'appium',
        args: {
          address: APPIUM_HOST,
          port: APPIUM_PORT,
          relaxedSecurity: true,
          log: path.join(RESULTS_DIR, 'appium.log'),
          'log-level': 'info'
        }
      }
    ]
  ],

  // ============================================================
  // Appium Connection
  // ============================================================
  hostname: APPIUM_HOST,
  port: APPIUM_PORT,
  path: '/wd/hub',

  // ============================================================
  // Framework
  // ============================================================
  framework: 'mocha',

  mochaOpts: {
    ui: 'bdd',
    timeout: 120000,
    retries: 1
  },

  // ============================================================
  // Reporters
  // ============================================================
  reporters: [
    'spec',
    [
      'json',
      {
        outputDir: RESULTS_DIR,
        outputFileFormat: function (opts) {
          return `wdio-results-${opts.cid}-${Date.now()}.json`;
        }
      }
    ]
  ],

  // ============================================================
  // Timeouts
  // ============================================================
  connectionRetryTimeout: 120000,
  connectionRetryCount: 3,

  // ============================================================
  // Base URL (available in tests via browser.options.baseUrl)
  // ============================================================
  baseUrl: BASE_URL,

  // ============================================================
  // Hooks
  // ============================================================
  onPrepare: function (config, capabilities) {
    const fs = require('fs');
    if (!fs.existsSync(RESULTS_DIR)) {
      fs.mkdirSync(RESULTS_DIR, { recursive: true });
    }
    console.log(`\n[wdio.conf] Base URL: ${BASE_URL}`);
    console.log(`[wdio.conf] Appium: ${APPIUM_HOST}:${APPIUM_PORT}`);
    console.log(`[wdio.conf] Device: ${ANDROID_DEVICE} (Android ${ANDROID_VERSION})\n`);
  },

  before: async function (capabilities, specs) {
    const chai = require('chai');
    global.expect = chai.expect;
    global.assert = chai.assert;
    global.BASE_URL = BASE_URL;
    global.EXPLICIT_TIMEOUT = EXPLICIT_TIMEOUT;

    // Set implicit timeout
    await browser.setTimeout({ implicit: IMPLICIT_TIMEOUT });

    // Helper: navigate to app
    global.navigateToApp = async function () {
      await browser.url(BASE_URL);
      await browser.waitUntil(
        async () => {
          const state = await browser.execute(() => document.readyState);
          return state === 'complete';
        },
        { timeout: EXPLICIT_TIMEOUT, timeoutMsg: 'App did not load in time' }
      );
    };

    // Helper: perform login
    global.performLogin = async function (
      username = 'testuser',
      password = 'Test@1234'
    ) {
      await global.navigateToApp();
      try {
        const usernameInput = await browser.$('input[aria-label="Username"]');
        await usernameInput.waitForDisplayed({ timeout: EXPLICIT_TIMEOUT });
        await usernameInput.clearValue();
        await usernameInput.setValue(username);
        const passwordInput = await browser.$('input[aria-label="Password"]');
        await passwordInput.clearValue();
        await passwordInput.setValue(password);
        const loginBtn = await browser.$('button=Login');
        await loginBtn.click();
        await browser.pause(2000);
      } catch (e) {
        console.warn('[performLogin] Could not complete login:', e.message);
      }
    };

    // Helper: wait for element
    global.waitForEl = async function (selector, timeout = EXPLICIT_TIMEOUT) {
      const el = await browser.$(selector);
      await el.waitForDisplayed({ timeout });
      return el;
    };

    // Helper: safe click (scroll into view first)
    global.safeClick = async function (selector) {
      const el = await browser.$(selector);
      await el.waitForDisplayed({ timeout: EXPLICIT_TIMEOUT });
      await el.scrollIntoView();
      await el.click();
    };
  },

  afterTest: async function (test, context, { error, result, duration, passed }) {
    if (!passed) {
      const ts = new Date().toISOString().replace(/[:.]/g, '-');
      const screenshotDir = require('path').join(RESULTS_DIR, 'screenshots');
      const fs = require('fs');
      if (!fs.existsSync(screenshotDir)) {
        fs.mkdirSync(screenshotDir, { recursive: true });
      }
      const fileName = `${test.title.replace(/\s+/g, '_').substring(0, 60)}_${ts}.png`;
      await browser.saveScreenshot(require('path').join(screenshotDir, fileName));
    }
  },

  onComplete: function (exitCode, config, capabilities, results) {
    console.log('\n[wdio.conf] Test run complete.');
    console.log(`[wdio.conf] Results saved to: ${RESULTS_DIR}`);
  }
};
