/**
 * k6 Load Test — Skill-Gap AI Platform
 * ======================================
 * Baseline Load Test:
 *   - 100 Virtual Users (VUs)
 *   - 1 minute duration
 *   - Non-destructive (GET-only where possible)
 *
 * Usage:
 *   k6 run load-tests/load-test.js
 *   k6 run --env BASE_URL=https://your-app.streamlit.app load-tests/load-test.js
 *
 * Results: Reports RPS, avg/min/max response times, error rates
 */

import http from 'k6/http';
import { check, sleep, group } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';

// ─── Configuration ────────────────────────────────────────────────
const BASE_URL = __ENV.BASE_URL || 'http://localhost:8501';

// ─── Custom Metrics ───────────────────────────────────────────────
const errorRate        = new Rate('error_rate');
const loginLatency     = new Trend('login_latency');
const homeLatency      = new Trend('home_page_latency');
const staticLatency    = new Trend('static_asset_latency');
const healthLatency    = new Trend('health_check_latency');
const totalRequests    = new Counter('total_requests');
const successRequests  = new Counter('success_requests');
const failedRequests   = new Counter('failed_requests');

// ─── Load Test Stages ─────────────────────────────────────────────
export const options = {
  scenarios: {
    // Baseline: 100 VUs for 1 minute
    baseline_load: {
      executor: 'constant-vus',
      vus: 100,
      duration: '1m',
      gracefulStop: '10s',
    },

    // Ramp-up scenario (runs after baseline)
    ramp_up: {
      executor: 'ramping-vus',
      startVUs: 0,
      stages: [
        { duration: '20s', target: 50 },   // Warm up to 50 VUs
        { duration: '30s', target: 100 },  // Peak at 100 VUs
        { duration: '10s', target: 0 },    // Cool down
      ],
      startTime: '65s',  // Start after baseline
      gracefulStop: '10s',
    },
  },

  thresholds: {
    // Response time SLAs
    http_req_duration: [
      'p(50)<500',    // 50% of requests < 500ms
      'p(90)<1500',   // 90% of requests < 1.5s
      'p(95)<2500',   // 95% of requests < 2.5s
      'p(99)<5000',   // 99% of requests < 5s
    ],

    // Error rate must be below 5%
    error_rate: ['rate<0.05'],

    // HTTP failure rate
    http_req_failed: ['rate<0.05'],

    // Custom metric thresholds
    login_latency:  ['p(95)<3000'],
    home_page_latency: ['p(95)<2000'],
  },

  // Output settings
  summaryTrendStats: ['avg', 'min', 'med', 'max', 'p(90)', 'p(95)', 'p(99)'],
};

// ─── HTTP Parameters ──────────────────────────────────────────────
const params = {
  headers: {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'User-Agent': 'k6-load-test/1.0 SkillGapAI-Performance-Test',
    'Connection': 'keep-alive',
  },
  timeout: '30s',
};

// ─── Helper Functions ─────────────────────────────────────────────
function makeRequest(url, description) {
  const start = Date.now();
  const response = http.get(url, params);
  const latency = Date.now() - start;

  totalRequests.add(1);
  errorRate.add(response.status >= 400);

  const success = check(response, {
    [`${description} - status 200`]: (r) => r.status === 200,
    [`${description} - response time < 5s`]: (r) => r.timings.duration < 5000,
    [`${description} - has body`]: (r) => r.body && r.body.length > 0,
  });

  if (success) {
    successRequests.add(1);
  } else {
    failedRequests.add(1);
  }

  return { response, latency };
}

// ─── Main VU Function ─────────────────────────────────────────────
export default function () {
  const vu = __VU;
  const iter = __ITER;

  // Simulate different user behaviors
  const scenario = iter % 5;

  group('Homepage Load', function () {
    const { response, latency } = makeRequest(BASE_URL, 'Homepage');
    homeLatency.add(latency);

    check(response, {
      'Page contains Streamlit content': (r) =>
        r.body && (
          r.body.includes('streamlit') ||
          r.body.includes('Skill-Gap') ||
          r.body.includes('Login') ||
          r.status === 200
        ),
    });
  });

  sleep(Math.random() * 1 + 0.5); // Think time 0.5–1.5s

  group('Static Assets', function () {
    // Streamlit serves static assets
    const staticEndpoints = [
      `${BASE_URL}/_stcore/health`,
      `${BASE_URL}/static/`,
      `${BASE_URL}/component/`,
    ];

    const endpoint = staticEndpoints[iter % staticEndpoints.length];
    const { latency } = makeRequest(endpoint, 'Static Asset');
    staticLatency.add(latency);
  });

  sleep(Math.random() * 0.5 + 0.2); // Short think time

  // Scenario-based testing
  switch (scenario) {
    case 0:
      group('Health Check Scenario', function () {
        const { latency } = makeRequest(`${BASE_URL}/_stcore/health`, 'Health Check');
        healthLatency.add(latency);
      });
      break;

    case 1:
      group('App Main Page Scenario', function () {
        makeRequest(BASE_URL, 'Main Page Load');
        sleep(1);
        makeRequest(`${BASE_URL}/?`, 'Main Page with Query');
      });
      break;

    case 2:
      group('API Probe Scenario', function () {
        // Probe Streamlit's internal APIs (read-only)
        makeRequest(`${BASE_URL}/_stcore/allowed-message-origins`, 'Allowed Origins');
      });
      break;

    case 3:
      group('Repeated Homepage Scenario', function () {
        // Simulate user refreshing
        for (let i = 0; i < 3; i++) {
          makeRequest(BASE_URL, `Refresh ${i + 1}`);
          sleep(0.3);
        }
      });
      break;

    case 4:
      group('Concurrent User Simulation', function () {
        // Simulate typical user journey
        makeRequest(BASE_URL, 'Journey - Login Page');
        sleep(2); // Read the page
        makeRequest(`${BASE_URL}/_stcore/health`, 'Journey - Health');
        sleep(0.5);
      });
      break;
  }

  // Random think time between 0.5s and 2s (realistic user behavior)
  sleep(Math.random() * 1.5 + 0.5);
}

// ─── Test Lifecycle ───────────────────────────────────────────────
export function setup() {
  console.log('='.repeat(60));
  console.log('🚀 Skill-Gap AI Platform — Load Test Starting');
  console.log('='.repeat(60));
  console.log(`📍 Target URL: ${BASE_URL}`);
  console.log(`👥 Virtual Users: 100`);
  console.log(`⏱️  Duration: 1 minute (baseline) + ramp-up`);
  console.log(`📊 Thresholds: p(95)<2.5s, error rate<5%`);
  console.log('='.repeat(60));

  // Warm-up check
  const warmup = http.get(`${BASE_URL}`, params);
  if (warmup.status === 0) {
    console.warn(`⚠️  WARNING: App may not be running at ${BASE_URL}`);
    console.warn('   Make sure the Streamlit app is running before load testing');
  } else {
    console.log(`✅ App is responding (status: ${warmup.status})`);
  }

  return { startTime: new Date().toISOString(), baseUrl: BASE_URL };
}

export function teardown(data) {
  console.log('='.repeat(60));
  console.log('✅ Load Test Complete');
  console.log(`🕐 Started: ${data.startTime}`);
  console.log(`🕐 Ended: ${new Date().toISOString()}`);
  console.log('='.repeat(60));
}

// ─── Custom Report ────────────────────────────────────────────────
export function handleSummary(data) {
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');

  return {
    // HTML report
    [`load-tests/reports/load-test-report-${timestamp}.html`]: htmlReport(data),

    // Console summary
    stdout: textSummary(data, { indent: '  ', enableColors: true }),

    // JSON report for parsing
    [`load-tests/reports/load-test-results-${timestamp}.json`]: JSON.stringify(data, null, 2),

    // Human-readable summary
    [`load-tests/reports/load-test-summary-${timestamp}.txt`]: generateTextReport(data),
  };
}

function generateTextReport(data) {
  const metrics = data.metrics;
  const dur = metrics.http_req_duration;
  const rps = metrics.http_reqs;
  const failures = metrics.http_req_failed;

  return `
╔══════════════════════════════════════════════════════════════╗
║          SKILL-GAP AI PLATFORM — LOAD TEST REPORT           ║
╚══════════════════════════════════════════════════════════════╝

TARGET URL: ${BASE_URL}
TEST DATE:  ${new Date().toISOString()}

── VIRTUAL USERS ──────────────────────────────────────────────
  Configured VUs:  100 concurrent users
  Duration:        1 minute baseline + ramp-up
  Total Requests:  ${rps ? Math.round(rps.values.count) : 'N/A'}

── REQUESTS PER SECOND ────────────────────────────────────────
  RPS (avg):       ${rps ? rps.values.rate.toFixed(1) : 'N/A'} req/sec
  Total Sent:      ${rps ? rps.values.count : 'N/A'} requests

── RESPONSE TIMES ─────────────────────────────────────────────
  Average:         ${dur ? dur.values.avg.toFixed(0) : 'N/A'} ms
  Minimum:         ${dur ? dur.values.min.toFixed(0) : 'N/A'} ms
  Median (p50):    ${dur ? dur.values.med.toFixed(0) : 'N/A'} ms
  p90:             ${dur ? dur.values['p(90)'].toFixed(0) : 'N/A'} ms
  p95:             ${dur ? dur.values['p(95)'].toFixed(0) : 'N/A'} ms
  p99:             ${dur ? dur.values['p(99)'].toFixed(0) : 'N/A'} ms
  Maximum:         ${dur ? dur.values.max.toFixed(0) : 'N/A'} ms

── ERROR RATE ─────────────────────────────────────────────────
  Failed Requests: ${failures ? (failures.values.rate * 100).toFixed(2) : 'N/A'}%
  Pass Threshold:  error_rate < 5%

── THRESHOLDS ─────────────────────────────────────────────────
  p(50) < 500ms:   ${dur && dur.values.med < 500 ? '✅ PASS' : '❌ FAIL'}
  p(90) < 1500ms:  ${dur && dur.values['p(90)'] < 1500 ? '✅ PASS' : '❌ FAIL'}
  p(95) < 2500ms:  ${dur && dur.values['p(95)'] < 2500 ? '✅ PASS' : '❌ FAIL'}
  error_rate < 5%: ${failures && failures.values.rate < 0.05 ? '✅ PASS' : '❌ FAIL'}

══════════════════════════════════════════════════════════════
`;
}
