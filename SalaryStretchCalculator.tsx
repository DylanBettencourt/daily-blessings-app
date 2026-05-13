"use client";

import { useState, useMemo } from "react";

// ── Types ────────────────────────────────────────────────────────────────────

interface Expense {
  key: string;
  icon: string;
  label: string;
  note: string;
  default: number;
  min: number;
  max: number;
  step: number;
}

// ── 2024 SA cost data ────────────────────────────────────────────────────────

const EXPENSES: Expense[] = [
  {
    key: "rent",
    icon: "🏠",
    label: "Rent / Bond",
    note: "1-bed in affordable township or flat",
    default: 4500,
    min: 1500,
    max: 20000,
    step: 250,
  },
  {
    key: "food",
    icon: "🛒",
    label: "Groceries & Food",
    note: "Monthly shop for 1 person",
    default: 2800,
    min: 800,
    max: 10000,
    step: 100,
  },
  {
    key: "transport",
    icon: "🚌",
    label: "Transport",
    note: "Taxi / bus / train commute",
    default: 1200,
    min: 200,
    max: 6000,
    step: 100,
  },
  {
    key: "electricity",
    icon: "💡",
    label: "Electricity",
    note: "Prepaid units (Eskom / municipal)",
    default: 650,
    min: 100,
    max: 3000,
    step: 50,
  },
  {
    key: "airtime",
    icon: "📱",
    label: "Airtime & Data",
    note: "Monthly bundle / prepaid top-ups",
    default: 350,
    min: 50,
    max: 2000,
    step: 50,
  },
];

// ── Colour helpers ────────────────────────────────────────────────────────────

function balanceColor(amount: number, takeHome: number): string {
  if (amount <= 0) return "#ff2222";
  const pct = amount / Math.max(takeHome, 1);
  if (pct > 0.35) return "#22cc88";
  if (pct > 0.2) return "#f0c040";
  if (pct > 0.08) return "#ff8800";
  return "#ff2222";
}

function balanceBg(amount: number, takeHome: number): string {
  return balanceColor(amount, takeHome) + "22"; // ~14 % alpha
}

function fmt(n: number): string {
  return "R " + Math.abs(n).toLocaleString("en-ZA", { maximumFractionDigits: 0 });
}

// ── Verdict ───────────────────────────────────────────────────────────────────

interface Verdict {
  bg: string;
  border: string;
  emoji: string;
  headline: string;
  sub: string;
}

function getVerdict(balance: number, pctLeft: number, takeHome: number): Verdict {
  if (balance <= 0) {
    return {
      bg: "#2a0000",
      border: "#ff2222",
      emoji: "🚨",
      headline: "You're already in the red.",
      sub: `Your expenses exceed your income by ${fmt(balance)}. Something has to give — or debt fills the gap.`,
    };
  }
  if (pctLeft < 8) {
    return {
      bg: "#1e0a00",
      border: "#ff6600",
      emoji: "😰",
      headline: `Only ${fmt(balance)} left. That's ${pctLeft.toFixed(0)}% of your salary.`,
      sub: "One taxi fare. One school fee. One load-shedding surge bill. Gone.",
    };
  }
  if (pctLeft < 20) {
    return {
      bg: "#1c1800",
      border: "#f0c040",
      emoji: "😬",
      headline: `${fmt(balance)} left — thin ice.`,
      sub: `That's ${pctLeft.toFixed(0)}% of your take-home. No buffer for emergencies, medical, or clothing.`,
    };
  }
  if (pctLeft < 40) {
    return {
      bg: "#001a10",
      border: "#22cc88",
      emoji: "😌",
      headline: `${fmt(balance)} left — workable, but tight.`,
      sub: `${pctLeft.toFixed(0)}% remaining. You can save a little, but lifestyle shocks can still derail you.`,
    };
  }
  return {
    bg: "#001a10",
    border: "#22cc88",
    emoji: "✅",
    headline: `${fmt(balance)} left — you have breathing room.`,
    sub: `${pctLeft.toFixed(0)}% of your income free. Build that emergency fund.`,
  };
}

// ── Sub-components ────────────────────────────────────────────────────────────

function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <div
      style={{
        fontSize: "0.72rem",
        letterSpacing: "0.15em",
        textTransform: "uppercase",
        color: "#555",
        margin: "28px 0 12px",
        borderBottom: "1px solid #222",
        paddingBottom: "6px",
      }}
    >
      {children}
    </div>
  );
}

interface ExpenseRowProps {
  exp: Expense;
  value: number;
  balance: number;
  takeHome: number;
  onChange: (v: number) => void;
}

function ExpenseRow({ exp, value, balance, takeHome, onChange }: ExpenseRowProps) {
  const color = balanceColor(balance, takeHome);
  const bg = balanceBg(balance, takeHome);
  const pct = ((value - exp.min) / (exp.max - exp.min)) * 100;

  return (
    <div style={{ marginBottom: "10px" }}>
      {/* Expense label + cost row */}
      <div
        style={{
          background: "#1a1a1a",
          borderLeft: "4px solid #2a2a2a",
          borderRadius: "6px",
          padding: "10px 16px",
          marginBottom: "4px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: "6px",
        }}
      >
        <span style={{ color: "#ccc", fontSize: "0.95rem" }}>
          {exp.icon} {exp.label}
          <span style={{ color: "#555", fontSize: "0.8rem", marginLeft: "8px" }}>
            − R{value.toLocaleString("en-ZA")}
          </span>
        </span>
        <span style={{ color: "#555", fontSize: "0.75rem" }}>{exp.note}</span>
      </div>

      {/* Slider */}
      <div
        style={{
          padding: "4px 16px 6px",
          background: "#131313",
          borderRadius: "6px",
          marginBottom: "4px",
          position: "relative",
        }}
      >
        <style>{`
          input[type=range].ssc-slider {
            -webkit-appearance: none;
            appearance: none;
            width: 100%;
            height: 4px;
            border-radius: 2px;
            outline: none;
            cursor: pointer;
            background: linear-gradient(
              to right,
              #ff4444 0%,
              #ff4444 ${pct}%,
              #2a2a2a ${pct}%,
              #2a2a2a 100%
            );
          }
          input[type=range].ssc-slider::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #ff4444;
            box-shadow: 0 0 6px rgba(255,68,68,0.5);
            cursor: pointer;
          }
          input[type=range].ssc-slider::-moz-range-thumb {
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: #ff4444;
            border: none;
            cursor: pointer;
          }
        `}</style>
        <input
          type="range"
          className="ssc-slider"
          min={exp.min}
          max={exp.max}
          step={exp.step}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
          aria-label={exp.label}
        />
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            fontSize: "0.68rem",
            color: "#444",
            marginTop: "2px",
          }}
        >
          <span>R{exp.min.toLocaleString("en-ZA")}</span>
          <span>R{exp.max.toLocaleString("en-ZA")}</span>
        </div>
      </div>

      {/* Running balance after this expense */}
      <div
        style={{
          background: bg,
          borderLeft: `4px solid ${color}`,
          borderRadius: "6px",
          padding: "12px 16px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <span
          style={{
            color,
            fontSize: "0.75rem",
            letterSpacing: "0.1em",
            textTransform: "uppercase",
            fontWeight: 600,
          }}
        >
          Remaining after {exp.label.toLowerCase()}
        </span>
        <span
          style={{
            color,
            fontSize: "1.9rem",
            fontWeight: 900,
            letterSpacing: "-0.02em",
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {balance < 0 ? "− " : ""}
          {fmt(balance)}
        </span>
      </div>
    </div>
  );
}

// ── Main component ────────────────────────────────────────────────────────────

export default function SalaryStretchCalculator() {
  const [takeHome, setTakeHome] = useState(8500);
  const [costs, setCosts] = useState<Record<string, number>>(
    Object.fromEntries(EXPENSES.map((e) => [e.key, e.default]))
  );

  const runningBalances = useMemo(() => {
    let balance = takeHome;
    return EXPENSES.map((exp) => {
      balance -= costs[exp.key];
      return balance;
    });
  }, [takeHome, costs]);

  const finalBalance = runningBalances[runningBalances.length - 1];
  const totalExpenses = Object.values(costs).reduce((a, b) => a + b, 0);
  const pctLeft = takeHome > 0 ? (finalBalance / takeHome) * 100 : 0;
  const verdict = getVerdict(finalBalance, pctLeft, takeHome);
  const finalColor = balanceColor(finalBalance, takeHome);

  const handleTakeHome = (e: React.ChangeEvent<HTMLInputElement>) => {
    const v = parseInt(e.target.value.replace(/\D/g, ""), 10);
    setTakeHome(isNaN(v) ? 0 : Math.min(v, 200000));
  };

  return (
    <div
      style={{
        background: "#0d0d0d",
        color: "#f0f0f0",
        minHeight: "100vh",
        fontFamily:
          '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
        padding: "0 16px 60px",
      }}
    >
      <div style={{ maxWidth: "680px", margin: "0 auto" }}>

        {/* ── Header ── */}
        <div style={{ textAlign: "center", padding: "40px 0 8px" }}>
          <div
            style={{
              fontSize: "clamp(2rem, 8vw, 2.8rem)",
              fontWeight: 900,
              letterSpacing: "-0.03em",
              lineHeight: 1.1,
              color: "#ffffff",
            }}
          >
            SALARY STRETCH
          </div>
          <div
            style={{
              fontSize: "clamp(2rem, 8vw, 2.8rem)",
              fontWeight: 900,
              letterSpacing: "-0.03em",
              lineHeight: 1.1,
              color: "#ff4444",
            }}
          >
            CALCULATOR
          </div>
          <div
            style={{
              color: "#555",
              fontSize: "0.8rem",
              marginTop: "8px",
              letterSpacing: "0.12em",
            }}
          >
            SOUTH AFRICA · 2024 REAL COSTS
          </div>
        </div>

        {/* ── Take-home input ── */}
        <SectionTitle>Your monthly take-home pay</SectionTitle>

        <div style={{ position: "relative" }}>
          <span
            style={{
              position: "absolute",
              left: "16px",
              top: "50%",
              transform: "translateY(-50%)",
              fontSize: "1.4rem",
              fontWeight: 900,
              color: "#666",
              pointerEvents: "none",
              userSelect: "none",
            }}
          >
            R
          </span>
          <input
            type="number"
            value={takeHome}
            onChange={handleTakeHome}
            min={0}
            max={200000}
            step={500}
            aria-label="Monthly take-home pay in Rand"
            style={{
              width: "100%",
              background: "#1a1a1a",
              border: "1px solid #333",
              borderRadius: "8px",
              color: "#fff",
              fontSize: "1.5rem",
              fontWeight: 700,
              padding: "14px 16px 14px 40px",
              outline: "none",
              boxSizing: "border-box",
              appearance: "textfield",
            }}
          />
        </div>

        <div
          style={{
            textAlign: "center",
            fontSize: "clamp(2.4rem, 10vw, 3.4rem)",
            fontWeight: 900,
            color: "#ffffff",
            letterSpacing: "-0.03em",
            margin: "10px 0 0",
            fontVariantNumeric: "tabular-nums",
          }}
        >
          {fmt(takeHome)}
        </div>
        <div
          style={{
            textAlign: "center",
            color: "#444",
            fontSize: "0.75rem",
            letterSpacing: "0.14em",
            marginBottom: "4px",
          }}
        >
          PER MONTH
        </div>

        {/* ── Expense sliders ── */}
        <SectionTitle>Monthly expenses</SectionTitle>
        <p style={{ color: "#444", fontSize: "0.78rem", margin: "0 0 16px" }}>
          Drag the sliders to match your actual spending.
        </p>

        {/* ── Brutal breakdown ── */}
        <SectionTitle>The brutal breakdown</SectionTitle>

        {EXPENSES.map((exp, i) => (
          <ExpenseRow
            key={exp.key}
            exp={exp}
            value={costs[exp.key]}
            balance={runningBalances[i]}
            takeHome={takeHome}
            onChange={(v) => setCosts((prev) => ({ ...prev, [exp.key]: v }))}
          />
        ))}

        {/* ── Verdict ── */}
        <div
          style={{
            background: verdict.bg,
            border: `2px solid ${verdict.border}`,
            borderRadius: "12px",
            padding: "24px 22px",
            textAlign: "center",
            marginTop: "20px",
          }}
        >
          <div style={{ fontSize: "3rem" }}>{verdict.emoji}</div>
          <div
            style={{
              fontSize: "1.25rem",
              fontWeight: 900,
              color: "#ffffff",
              marginTop: "10px",
              lineHeight: 1.4,
            }}
          >
            {verdict.headline}
          </div>
          <div
            style={{
              fontSize: "0.9rem",
              color: "#aaa",
              marginTop: "8px",
              lineHeight: 1.6,
            }}
          >
            {verdict.sub}
          </div>
        </div>

        {/* ── Summary chips ── */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(3, 1fr)",
            gap: "10px",
            marginTop: "20px",
          }}
        >
          {[
            { label: "Total out", value: `R${totalExpenses.toLocaleString("en-ZA")}`, color: "#ff4444" },
            { label: "Remaining", value: `R${Math.max(finalBalance, 0).toLocaleString("en-ZA")}`, color: finalColor },
            { label: "% free", value: `${Math.max(pctLeft, 0).toFixed(0)}%`, color: finalColor },
          ].map(({ label, value, color }) => (
            <div
              key={label}
              style={{
                background: "#111",
                border: "1px solid #222",
                borderRadius: "8px",
                padding: "14px 8px",
                textAlign: "center",
              }}
            >
              <div
                style={{
                  fontSize: "0.68rem",
                  color: "#555",
                  letterSpacing: "0.12em",
                  textTransform: "uppercase",
                  marginBottom: "6px",
                }}
              >
                {label}
              </div>
              <div
                style={{
                  fontSize: "clamp(1.2rem, 4vw, 1.7rem)",
                  fontWeight: 900,
                  color,
                  letterSpacing: "-0.02em",
                  fontVariantNumeric: "tabular-nums",
                }}
              >
                {value}
              </div>
            </div>
          ))}
        </div>

        {/* ── Data sources ── */}
        <div
          style={{
            marginTop: "28px",
            padding: "14px",
            background: "#111",
            borderRadius: "8px",
            border: "1px solid #1e1e1e",
          }}
        >
          <p
            style={{
              fontSize: "0.72rem",
              color: "#444",
              lineHeight: 1.7,
              margin: 0,
            }}
          >
            <strong style={{ color: "#333" }}>DATA SOURCES</strong>
            <br />
            Rent: StatsSA Housing Survey 2023 · Food: PMBEJD Basic Food Basket Dec 2024 ·
            Transport: SANTACO fare surveys 2024 · Electricity: Eskom tariff increase Apr 2024 ·
            Data: MyBroadband SA pricing index 2024. Defaults represent a single adult in a
            Gauteng township or affordable suburb.
          </p>
        </div>

      </div>
    </div>
  );
}
