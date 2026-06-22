import { useState, useEffect, useRef, useCallback } from "react";

// ─── Theme ────────────────────────────────────────────────────────────────────
const C = {
  bg: "#0B0D14",
  surface: "#131620",
  surfaceHover: "#1C2030",
  card: "#181B28",
  border: "#252A40",
  borderHover: "#3A4060",
  text: "#E8EAF6",
  textMuted: "#6B72A8",
  textSub: "#9BA3D4",
  success: "#22C55E", successBg: "#0A1F12",
  error: "#EF4444",   errorBg: "#1F0A0A",
  warning: "#F59E0B", warningBg: "#1F180A",
  info: "#6366F1",    infoBg: "#0E0F20",
  birthday: "#EC4899",birthdayBg: "#1F0A16",
  accent: "#6366F1",
  accentSoft: "rgba(99,102,241,0.15)",
  purple: "#8B5CF6",
  teal: "#14B8A6",
  orange: "#F97316",
};

const TYPE_CFG = {
  success:  { color: C.success,  bg: C.successBg,  icon: "✓",  label: "Success" },
  error:    { color: C.error,    bg: C.errorBg,    icon: "✕",  label: "Error" },
  warning:  { color: C.warning,  bg: C.warningBg,  icon: "⚠",  label: "Warning" },
  info:     { color: C.info,     bg: C.infoBg,     icon: "ℹ",  label: "Info" },
  birthday: { color: C.birthday, bg: C.birthdayBg, icon: "🎂", label: "Birthday" },
  reminder: { color: C.warning,  bg: C.warningBg,  icon: "🔔", label: "Reminder" },
  exam:     { color: C.error,    bg: C.errorBg,    icon: "📝", label: "Exam" },
  deadline: { color: C.warning,  bg: C.warningBg,  icon: "⏰", label: "Deadline" },
};

// ─── Default Folders ─────────────────────────────────────────────────────────
const DEFAULT_FOLDERS = [
  { id: "assignments", name: "Assignments", icon: "📚", color: C.warning,  desc: "Homework, projects & submissions" },
  { id: "credentials", name: "Credentials", icon: "🔐", color: C.success,  desc: "Passwords, logins & access keys" },
  { id: "notes",       name: "Study Notes", icon: "📓", color: C.info,     desc: "Lectures, summaries & flashcards" },
  { id: "exams",       name: "Exam Prep",   icon: "🎯", color: C.error,    desc: "Mock tests, question banks & scores" },
];

// ─── File type icons ──────────────────────────────────────────────────────────
const fileIcon = (name) => {
  const ext = name.split(".").pop().toLowerCase();
  const map = { pdf: "📄", doc: "📝", docx: "📝", txt: "📃", png: "🖼", jpg: "🖼", jpeg: "🖼", gif: "🖼", mp4: "🎬", mp3: "🎵", zip: "📦", xlsx: "📊", xls: "📊", ppt: "📊", pptx: "📊", csv: "📊" };
  return map[ext] || "📎";
};
const fmtSize = (b) => b < 1024 ? `${b} B` : b < 1048576 ? `${(b/1024).toFixed(1)} KB` : `${(b/1048576).toFixed(1)} MB`;
const fmtDate = (d) => new Date(d).toLocaleDateString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });

let _uid = 1;
const uid = () => _uid++;
const nowFull = () => new Date().toLocaleString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
const nowTime = () => new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

const DEMO_NOTIFS = [
  { type: "success", title: "Note Saved Successfully", body: "Study notes for Chapter 7 have been saved." },
  { type: "success", title: "Assignment Submitted", body: "Physics assignment submitted at 11:45 PM." },
  { type: "success", title: "Password Added", body: "Credential for 'College Portal' saved securely." },
  { type: "error",   title: "Invalid Login Credentials", body: "Check your username and password and try again." },
  { type: "warning", title: "Assignment Due Tomorrow", body: "Mathematics Assignment 3 is due at 11:59 PM tomorrow." },
  { type: "warning", title: "Exam in 2 Days", body: "Physics Unit Test — Thursday 9 AM." },
  { type: "info",    title: "Timetable Updated", body: "Wednesday's lab session moved to Room 204." },
  { type: "birthday",title: "Today is Priya's Birthday 🎂", body: "Don't forget to wish her!" },
  { type: "reminder",title: "AFCAT Study Session 📚", body: "Don't forget your session at 6 PM tonight." },
  { type: "exam",    title: "Exam Alert 📝", body: "AFCAT mock test starts in 30 minutes. Best of luck!" },
];

// ══════════════════════════════════════════════════════════════════════════════
// TOAST
// ══════════════════════════════════════════════════════════════════════════════
function Toast({ notif, onDismiss }) {
  const cfg = TYPE_CFG[notif.type] || TYPE_CFG.info;
  const [vis, setVis] = useState(false);
  const [exit, setExit] = useState(false);

  useEffect(() => {
    requestAnimationFrame(() => setVis(true));
    const t = setTimeout(dismiss, 4800);
    return () => clearTimeout(t);
  }, []);

  const dismiss = useCallback(() => {
    setExit(true);
    setTimeout(() => onDismiss(notif.id), 320);
  }, [notif.id, onDismiss]);

  return (
    <div onClick={dismiss} style={{
      position: "relative", display: "flex", gap: 12, alignItems: "flex-start",
      background: C.surface, border: `1px solid ${cfg.color}44`,
      borderLeft: `4px solid ${cfg.color}`, borderRadius: 12,
      padding: "13px 15px 17px", cursor: "pointer",
      boxShadow: `0 8px 32px rgba(0,0,0,0.6), 0 0 0 1px ${cfg.color}18`,
      overflow: "hidden", minWidth: 300, maxWidth: 360,
      transform: vis && !exit ? "translateX(0) scale(1)" : "translateX(110%) scale(0.96)",
      opacity: vis && !exit ? 1 : 0,
      transition: "transform 0.3s cubic-bezier(0.34,1.56,0.64,1), opacity 0.3s ease",
    }}>
      <div style={{
        width: 30, height: 30, borderRadius: "50%",
        background: cfg.bg, border: `1.5px solid ${cfg.color}55`,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 13, color: cfg.color, flexShrink: 0, fontWeight: 700,
      }}>{cfg.icon}</div>
      <div style={{ flex: 1 }}>
        <div style={{ fontSize: 12, fontWeight: 700, color: C.text, marginBottom: 2 }}>{notif.title}</div>
        <div style={{ fontSize: 11, color: C.textMuted, lineHeight: 1.4 }}>{notif.body}</div>
      </div>
      <div style={{ fontSize: 10, color: C.textMuted, flexShrink: 0 }}>{nowTime()}</div>
      <div style={{ position: "absolute", bottom: 0, left: 0, height: 3, background: cfg.color, width: "100%", transformOrigin: "left", animation: "toastBar 4.8s linear forwards" }} />
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// CENTER MODAL
// ══════════════════════════════════════════════════════════════════════════════
function CenterModal({ notif, onClose }) {
  const cfg = TYPE_CFG[notif.type] || TYPE_CFG.info;
  const [in_, setIn] = useState(false);
  useEffect(() => { requestAnimationFrame(() => setIn(true)); }, []);

  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,0.75)",
      backdropFilter: "blur(6px)", display: "flex", alignItems: "center",
      justifyContent: "center", zIndex: 9999,
      opacity: in_ ? 1 : 0, transition: "opacity 0.2s",
    }} onClick={onClose}>
      <div onClick={e => e.stopPropagation()} style={{
        background: C.surface, border: `1px solid ${cfg.color}44`,
        borderRadius: 20, padding: "36px 40px", maxWidth: 420, width: "90%",
        boxShadow: `0 32px 80px rgba(0,0,0,0.7), 0 0 60px ${cfg.color}14`,
        transform: in_ ? "scale(1) translateY(0)" : "scale(0.88) translateY(24px)",
        transition: "transform 0.3s cubic-bezier(0.34,1.56,0.64,1)",
        textAlign: "center",
      }}>
        <div style={{
          width: 60, height: 60, borderRadius: "50%",
          background: cfg.bg, border: `2px solid ${cfg.color}`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 26, margin: "0 auto 18px",
          boxShadow: `0 0 28px ${cfg.color}44`,
        }}>{cfg.icon}</div>
        <div style={{ fontSize: 10, letterSpacing: 2, color: cfg.color, fontWeight: 800, marginBottom: 6, textTransform: "uppercase" }}>{cfg.label}</div>
        <div style={{ fontSize: 18, fontWeight: 800, color: C.text, marginBottom: 8 }}>{notif.title}</div>
        <div style={{ fontSize: 13, color: C.textMuted, lineHeight: 1.6, marginBottom: 24 }}>{notif.body}</div>
        <button onClick={onClose} style={{
          background: cfg.color, color: "#fff", border: "none", borderRadius: 10,
          padding: "10px 30px", fontSize: 13, fontWeight: 700, cursor: "pointer",
          boxShadow: `0 4px 16px ${cfg.color}55`,
        }}>Got it</button>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// NOTIFICATION BELL PANEL
// ══════════════════════════════════════════════════════════════════════════════
function NotifPanelItem({ n, onRead, onDelete }) {
  const cfg = TYPE_CFG[n.type] || TYPE_CFG.info;
  return (
    <div style={{
      display: "flex", gap: 10, alignItems: "flex-start",
      padding: "11px 14px", borderBottom: `1px solid ${C.border}`,
      background: n.read ? "transparent" : `${cfg.color}08`,
    }}>
      <div style={{
        width: 32, height: 32, borderRadius: "50%",
        background: cfg.bg, border: `1.5px solid ${cfg.color}44`,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 13, color: cfg.color, flexShrink: 0,
      }}>{cfg.icon}</div>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 5, marginBottom: 2 }}>
          {!n.read && <span style={{ width: 6, height: 6, borderRadius: "50%", background: cfg.color, display: "inline-block", flexShrink: 0 }} />}
          <span style={{ fontSize: 11, fontWeight: 700, color: C.text }}>{n.title}</span>
        </div>
        <div style={{ fontSize: 10, color: C.textMuted, lineHeight: 1.4, marginBottom: 3 }}>{n.body}</div>
        <div style={{ fontSize: 9, color: C.textMuted }}>{n.time}</div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 3, flexShrink: 0 }}>
        {!n.read && <button onClick={() => onRead(n.id)} style={{ background: "none", border: `1px solid ${C.border}`, color: C.textMuted, borderRadius: 5, padding: "2px 5px", fontSize: 9, cursor: "pointer" }}>✓</button>}
        <button onClick={() => onDelete(n.id)} style={{ background: "none", border: `1px solid ${C.border}`, color: C.error, borderRadius: 5, padding: "2px 5px", fontSize: 9, cursor: "pointer" }}>✕</button>
      </div>
    </div>
  );
}

function NotifBell({ notifs, onRead, onDelete, onClearAll }) {
  const [open, setOpen] = useState(false);
  const [filter, setFilter] = useState("all");
  const ref = useRef();
  const unread = notifs.filter(n => !n.read).length;

  useEffect(() => {
    const h = e => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    document.addEventListener("mousedown", h);
    return () => document.removeEventListener("mousedown", h);
  }, []);

  const filtered = filter === "all" ? notifs : filter === "unread" ? notifs.filter(n => !n.read) : notifs.filter(n => n.type === filter);

  return (
    <div ref={ref} style={{ position: "relative" }}>
      <button onClick={() => setOpen(o => !o)} style={{
        position: "relative", background: open ? C.surfaceHover : C.surface,
        border: `1px solid ${open ? C.accent : C.border}`,
        borderRadius: 10, width: 40, height: 40, cursor: "pointer",
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 18, transition: "all 0.2s",
        boxShadow: open ? `0 0 0 3px ${C.accentSoft}` : "none",
      }}>
        🔔
        {unread > 0 && (
          <span style={{
            position: "absolute", top: -4, right: -4,
            background: C.error, color: "#fff", borderRadius: "50%",
            width: 17, height: 17, fontSize: 9, fontWeight: 800,
            display: "flex", alignItems: "center", justifyContent: "center",
            border: `2px solid ${C.bg}`, animation: "pulse 2s infinite",
          }}>{unread > 9 ? "9+" : unread}</span>
        )}
      </button>

      {open && (
        <div style={{
          position: "absolute", top: 48, right: 0,
          width: 340, maxHeight: 500,
          background: C.surface, border: `1px solid ${C.border}`,
          borderRadius: 14, boxShadow: "0 20px 60px rgba(0,0,0,0.7)",
          display: "flex", flexDirection: "column", overflow: "hidden",
          zIndex: 500, animation: "slideDown 0.18s ease",
        }}>
          <div style={{ padding: "14px 14px 10px", borderBottom: `1px solid ${C.border}` }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
              <span style={{ fontSize: 13, fontWeight: 800, color: C.text }}>Notifications</span>
              <div style={{ display: "flex", gap: 8 }}>
                {unread > 0 && <button onClick={() => notifs.filter(n => !n.read).forEach(n => onRead(n.id))} style={{ fontSize: 10, color: C.accent, background: "none", border: "none", cursor: "pointer", fontWeight: 700 }}>Mark all read</button>}
                <button onClick={onClearAll} style={{ fontSize: 10, color: C.error, background: "none", border: "none", cursor: "pointer", fontWeight: 700 }}>Clear all</button>
              </div>
            </div>
            <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
              {["all", "unread", "success", "error", "warning", "reminder"].map(f => (
                <button key={f} onClick={() => setFilter(f)} style={{
                  padding: "3px 9px", borderRadius: 20, fontSize: 9, fontWeight: 700,
                  border: "none", cursor: "pointer", textTransform: "capitalize",
                  background: filter === f ? C.accent : C.surfaceHover,
                  color: filter === f ? "#fff" : C.textMuted,
                }}>{f}</button>
              ))}
            </div>
          </div>
          <div style={{ overflowY: "auto", flex: 1 }}>
            {filtered.length === 0
              ? <div style={{ padding: 28, textAlign: "center", color: C.textMuted, fontSize: 12 }}>🎉 All caught up!</div>
              : filtered.map(n => <NotifPanelItem key={n.id} n={n} onRead={onRead} onDelete={onDelete} />)
            }
          </div>
        </div>
      )}
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// FOLDER POCKET SYSTEM
// ══════════════════════════════════════════════════════════════════════════════

function RenameModal({ value, onSave, onClose }) {
  const [val, setVal] = useState(value);
  const ref = useRef();
  useEffect(() => { ref.current?.focus(); ref.current?.select(); }, []);
  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,0.7)",
      backdropFilter: "blur(4px)", display: "flex", alignItems: "center",
      justifyContent: "center", zIndex: 8000,
    }} onClick={onClose}>
      <div onClick={e => e.stopPropagation()} style={{
        background: C.surface, border: `1px solid ${C.border}`,
        borderRadius: 16, padding: "28px 28px 24px",
        width: 360, boxShadow: "0 24px 60px rgba(0,0,0,0.6)",
      }}>
        <div style={{ fontSize: 14, fontWeight: 800, color: C.text, marginBottom: 16 }}>Rename</div>
        <input
          ref={ref}
          value={val}
          onChange={e => setVal(e.target.value)}
          onKeyDown={e => { if (e.key === "Enter") onSave(val); if (e.key === "Escape") onClose(); }}
          style={{
            width: "100%", background: C.card, border: `1px solid ${C.border}`,
            borderRadius: 8, padding: "10px 12px", fontSize: 13, color: C.text,
            outline: "none", marginBottom: 16,
          }}
        />
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
          <button onClick={onClose} style={{ padding: "8px 18px", borderRadius: 8, background: "none", border: `1px solid ${C.border}`, color: C.textMuted, fontSize: 12, cursor: "pointer" }}>Cancel</button>
          <button onClick={() => onSave(val)} style={{ padding: "8px 18px", borderRadius: 8, background: C.accent, border: "none", color: "#fff", fontSize: 12, fontWeight: 700, cursor: "pointer" }}>Save</button>
        </div>
      </div>
    </div>
  );
}

function NewFolderModal({ onSave, onClose }) {
  const [name, setName] = useState("");
  const [icon, setIcon] = useState("📁");
  const [color, setColor] = useState(C.accent);
  const icons = ["📁","📂","📚","🗂","🔐","📝","🎯","📓","🗄","💼","🧪","🏆","🎮","🔬","📊"];
  const colors = [C.accent, C.success, C.error, C.warning, C.birthday, C.teal, C.orange, C.purple];
  const ref = useRef();
  useEffect(() => { ref.current?.focus(); }, []);
  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,0.75)",
      backdropFilter: "blur(6px)", display: "flex", alignItems: "center",
      justifyContent: "center", zIndex: 8000,
    }} onClick={onClose}>
      <div onClick={e => e.stopPropagation()} style={{
        background: C.surface, border: `1px solid ${C.border}`,
        borderRadius: 18, padding: "28px", width: 400,
        boxShadow: "0 24px 60px rgba(0,0,0,0.6)",
      }}>
        <div style={{ fontSize: 15, fontWeight: 800, color: C.text, marginBottom: 20 }}>New Folder</div>
        {/* Preview */}
        <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 20, padding: "14px 16px", background: C.card, borderRadius: 12, border: `1px solid ${color}44` }}>
          <div style={{ fontSize: 28 }}>{icon}</div>
          <div>
            <div style={{ fontSize: 14, fontWeight: 700, color: C.text }}>{name || "Folder Name"}</div>
            <div style={{ fontSize: 10, color: C.textMuted }}>0 files</div>
          </div>
        </div>
        {/* Name */}
        <input ref={ref} value={name} onChange={e => setName(e.target.value)} placeholder="Folder name..."
          onKeyDown={e => { if (e.key === "Enter" && name.trim()) onSave({ name, icon, color }); if (e.key === "Escape") onClose(); }}
          style={{ width: "100%", background: C.card, border: `1px solid ${C.border}`, borderRadius: 8, padding: "9px 12px", fontSize: 13, color: C.text, outline: "none", marginBottom: 14 }} />
        {/* Icons */}
        <div style={{ fontSize: 10, color: C.textMuted, marginBottom: 8, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }}>Icon</div>
        <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 14 }}>
          {icons.map(i => (
            <button key={i} onClick={() => setIcon(i)} style={{
              fontSize: 18, background: icon === i ? C.accentSoft : "none",
              border: `1px solid ${icon === i ? C.accent : C.border}`,
              borderRadius: 8, padding: "4px 6px", cursor: "pointer",
            }}>{i}</button>
          ))}
        </div>
        {/* Colors */}
        <div style={{ fontSize: 10, color: C.textMuted, marginBottom: 8, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }}>Color</div>
        <div style={{ display: "flex", gap: 8, marginBottom: 20 }}>
          {colors.map(col => (
            <button key={col} onClick={() => setColor(col)} style={{
              width: 24, height: 24, borderRadius: "50%", background: col, border: "none",
              cursor: "pointer", boxShadow: color === col ? `0 0 0 3px ${C.surface}, 0 0 0 5px ${col}` : "none",
            }} />
          ))}
        </div>
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
          <button onClick={onClose} style={{ padding: "8px 18px", borderRadius: 8, background: "none", border: `1px solid ${C.border}`, color: C.textMuted, fontSize: 12, cursor: "pointer" }}>Cancel</button>
          <button onClick={() => name.trim() && onSave({ name, icon, color })} style={{ padding: "8px 18px", borderRadius: 8, background: name.trim() ? C.accent : C.border, border: "none", color: "#fff", fontSize: 12, fontWeight: 700, cursor: "pointer" }}>Create Folder</button>
        </div>
      </div>
    </div>
  );
}

function FileViewer({ file, onClose }) {
  const isImg = /\.(png|jpg|jpeg|gif|webp|svg)$/i.test(file.name);
  const isText = /\.(txt|md|csv|json|js|py|html|css)$/i.test(file.name);
  const [textContent, setTextContent] = useState("");
  const [in_, setIn] = useState(false);
  useEffect(() => {
    requestAnimationFrame(() => setIn(true));
    if (isText && file.dataUrl) {
      fetch(file.dataUrl).then(r => r.text()).then(setTextContent).catch(() => setTextContent("Could not read file content."));
    }
  }, []);

  return (
    <div style={{ position: "fixed", inset: 0, background: "rgba(0,0,0,0.85)", backdropFilter: "blur(8px)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 8500, opacity: in_ ? 1 : 0, transition: "opacity 0.2s" }} onClick={onClose}>
      <div onClick={e => e.stopPropagation()} style={{ background: C.surface, border: `1px solid ${C.border}`, borderRadius: 18, width: "min(720px, 94vw)", maxHeight: "80vh", display: "flex", flexDirection: "column", overflow: "hidden", transform: in_ ? "scale(1)" : "scale(0.9)", transition: "transform 0.25s cubic-bezier(0.34,1.56,0.64,1)" }}>
        <div style={{ padding: "16px 20px", borderBottom: `1px solid ${C.border}`, display: "flex", alignItems: "center", gap: 12 }}>
          <span style={{ fontSize: 22 }}>{fileIcon(file.name)}</span>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 13, fontWeight: 700, color: C.text }}>{file.name}</div>
            <div style={{ fontSize: 10, color: C.textMuted }}>{fmtSize(file.size)} · {fmtDate(file.addedAt)}</div>
          </div>
          <button onClick={onClose} style={{ background: "none", border: "none", color: C.textMuted, fontSize: 20, cursor: "pointer" }}>✕</button>
        </div>
        <div style={{ flex: 1, overflow: "auto", padding: 20 }}>
          {isImg && file.dataUrl && <img src={file.dataUrl} alt={file.name} style={{ maxWidth: "100%", borderRadius: 8 }} />}
          {isText && <pre style={{ fontSize: 12, color: C.textSub, lineHeight: 1.6, whiteSpace: "pre-wrap", margin: 0 }}>{textContent || "Loading..."}</pre>}
          {!isImg && !isText && (
            <div style={{ textAlign: "center", padding: 40 }}>
              <div style={{ fontSize: 64, marginBottom: 16 }}>{fileIcon(file.name)}</div>
              <div style={{ color: C.textMuted, fontSize: 13 }}>Preview not available for this file type.</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function FolderView({ folder, files, onUpload, onRename, onDelete, onBack, onRenameFolder, showToast }) {
  const inputRef = useRef();
  const [dragOver, setDragOver] = useState(false);
  const [renaming, setRenaming] = useState(null); // file id
  const [viewing, setViewing] = useState(null);
  const [sort, setSort] = useState("date");

  const folderFiles = files.filter(f => f.folderId === folder.id);
  const sorted = [...folderFiles].sort((a, b) => sort === "date" ? b.addedAt - a.addedAt : a.name.localeCompare(b.name));

  const handleFiles = (fileList) => {
    Array.from(fileList).forEach(file => {
      const reader = new FileReader();
      reader.onload = (e) => {
        onUpload({ id: uid(), name: file.name, size: file.size, folderId: folder.id, dataUrl: e.target.result, addedAt: Date.now() });
        showToast({ type: "success", title: "File Uploaded", body: `${file.name} added to ${folder.name}` });
      };
      reader.readAsDataURL(file);
    });
  };

  return (
    <div>
      {/* Breadcrumb */}
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 20 }}>
        <button onClick={onBack} style={{ background: "none", border: `1px solid ${C.border}`, color: C.textMuted, borderRadius: 8, padding: "6px 12px", fontSize: 12, cursor: "pointer" }}>← Folders</button>
        <span style={{ color: C.textMuted, fontSize: 12 }}>/</span>
        <span style={{ fontSize: 14, fontWeight: 700, color: folder.color }}>{folder.icon} {folder.name}</span>
        <button onClick={() => { const name = prompt("Rename folder:", folder.name); if (name?.trim()) onRenameFolder(folder.id, name.trim()); }}
          style={{ marginLeft: "auto", background: "none", border: `1px solid ${C.border}`, color: C.textMuted, borderRadius: 7, padding: "4px 10px", fontSize: 11, cursor: "pointer" }}>✏ Rename Folder</button>
      </div>

      {/* Drop Zone / Upload */}
      <div
        onDragOver={e => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={e => { e.preventDefault(); setDragOver(false); handleFiles(e.dataTransfer.files); }}
        onClick={() => inputRef.current?.click()}
        style={{
          border: `2px dashed ${dragOver ? folder.color : C.border}`,
          borderRadius: 14, padding: "28px",
          textAlign: "center", cursor: "pointer",
          background: dragOver ? `${folder.color}0A` : C.card,
          transition: "all 0.2s", marginBottom: 20,
        }}
      >
        <div style={{ fontSize: 32, marginBottom: 8 }}>📤</div>
        <div style={{ fontSize: 13, fontWeight: 700, color: dragOver ? folder.color : C.text }}>
          {dragOver ? "Drop files here" : "Click or drag files to upload"}
        </div>
        <div style={{ fontSize: 11, color: C.textMuted, marginTop: 4 }}>PDF, images, documents, any file</div>
        <input ref={inputRef} type="file" multiple onChange={e => handleFiles(e.target.files)} style={{ display: "none" }} />
      </div>

      {/* Toolbar */}
      {sorted.length > 0 && (
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <div style={{ fontSize: 12, color: C.textMuted }}>{sorted.length} file{sorted.length !== 1 ? "s" : ""}</div>
          <div style={{ display: "flex", gap: 6 }}>
            {["date", "name"].map(s => (
              <button key={s} onClick={() => setSort(s)} style={{ padding: "4px 10px", borderRadius: 7, fontSize: 10, fontWeight: 700, border: "none", cursor: "pointer", background: sort === s ? C.accent : C.surfaceHover, color: sort === s ? "#fff" : C.textMuted, textTransform: "capitalize" }}>{s}</button>
            ))}
          </div>
        </div>
      )}

      {/* Files */}
      {sorted.length === 0 ? (
        <div style={{ textAlign: "center", padding: "40px 20px", color: C.textMuted, fontSize: 13 }}>
          <div style={{ fontSize: 40, marginBottom: 12 }}>{folder.icon}</div>
          This folder is empty. Upload your first file above.
        </div>
      ) : (
        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 10 }}>
          {sorted.map(file => (
            <FileCard key={file.id} file={file} folderColor={folder.color}
              onRename={() => setRenaming(file.id)}
              onDelete={() => { onDelete(file.id); showToast({ type: "info", title: "File Removed", body: `${file.name} deleted.` }); }}
              onView={() => setViewing(file)}
            />
          ))}
        </div>
      )}

      {renaming && (
        <RenameModal
          value={files.find(f => f.id === renaming)?.name || ""}
          onSave={(newName) => { onRename(renaming, newName); showToast({ type: "success", title: "File Renamed", body: `Renamed to "${newName}"` }); setRenaming(null); }}
          onClose={() => setRenaming(null)}
        />
      )}
      {viewing && <FileViewer file={viewing} onClose={() => setViewing(null)} />}
    </div>
  );
}

function FileCard({ file, folderColor, onRename, onDelete, onView }) {
  const [hover, setHover] = useState(false);
  return (
    <div
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: hover ? C.surfaceHover : C.card,
        border: `1px solid ${hover ? folderColor + "55" : C.border}`,
        borderRadius: 12, overflow: "hidden", cursor: "pointer",
        transition: "all 0.18s", boxShadow: hover ? `0 4px 16px rgba(0,0,0,0.3)` : "none",
      }}
    >
      {/* Thumbnail */}
      <div onClick={onView} style={{
        height: 80, display: "flex", alignItems: "center", justifyContent: "center",
        background: `${folderColor}10`, fontSize: 36, borderBottom: `1px solid ${C.border}`,
      }}>
        {fileIcon(file.name)}
      </div>
      {/* Info */}
      <div style={{ padding: "10px 10px 8px" }}>
        <div onClick={onView} style={{ fontSize: 11, fontWeight: 700, color: C.text, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap", marginBottom: 3 }} title={file.name}>{file.name}</div>
        <div style={{ fontSize: 9, color: C.textMuted, marginBottom: 8 }}>{fmtSize(file.size)}</div>
        <div style={{ display: "flex", gap: 5 }}>
          <button onClick={onRename} style={{ flex: 1, background: "none", border: `1px solid ${C.border}`, color: C.textMuted, borderRadius: 6, padding: "4px", fontSize: 9, cursor: "pointer" }}>✏ Rename</button>
          <button onClick={onDelete} style={{ background: "none", border: `1px solid ${C.border}`, color: C.error, borderRadius: 6, padding: "4px 6px", fontSize: 9, cursor: "pointer" }}>✕</button>
        </div>
      </div>
    </div>
  );
}

function FolderCard({ folder, fileCount, onClick, onRename, onDelete }) {
  const [hover, setHover] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const menuRef = useRef();

  useEffect(() => {
    const h = e => { if (menuRef.current && !menuRef.current.contains(e.target)) setMenuOpen(false); };
    document.addEventListener("mousedown", h);
    return () => document.removeEventListener("mousedown", h);
  }, []);

  return (
    <div
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: hover ? C.surfaceHover : C.card,
        border: `1px solid ${hover ? folder.color + "66" : C.border}`,
        borderRadius: 16, padding: "20px", cursor: "pointer",
        transition: "all 0.2s", position: "relative",
        boxShadow: hover ? `0 8px 24px rgba(0,0,0,0.3), 0 0 0 1px ${folder.color}22` : "none",
      }}
    >
      {/* Menu */}
      <div ref={menuRef} style={{ position: "absolute", top: 12, right: 12 }} onClick={e => e.stopPropagation()}>
        <button onClick={() => setMenuOpen(o => !o)} style={{ background: "none", border: "none", color: C.textMuted, fontSize: 16, cursor: "pointer", padding: "2px 6px", borderRadius: 6, display: hover || menuOpen ? "block" : "none" }}>⋯</button>
        {menuOpen && (
          <div style={{ position: "absolute", top: 28, right: 0, background: C.surface, border: `1px solid ${C.border}`, borderRadius: 10, overflow: "hidden", minWidth: 130, boxShadow: "0 8px 24px rgba(0,0,0,0.4)", zIndex: 10 }}>
            <button onClick={() => { onRename(); setMenuOpen(false); }} style={{ display: "block", width: "100%", padding: "9px 14px", background: "none", border: "none", color: C.text, fontSize: 11, cursor: "pointer", textAlign: "left" }}>✏ Rename folder</button>
            <button onClick={() => { onDelete(); setMenuOpen(false); }} style={{ display: "block", width: "100%", padding: "9px 14px", background: "none", border: "none", color: C.error, fontSize: 11, cursor: "pointer", textAlign: "left" }}>🗑 Delete folder</button>
          </div>
        )}
      </div>

      <div onClick={onClick}>
        <div style={{ fontSize: 36, marginBottom: 12 }}>{folder.icon}</div>
        <div style={{ fontSize: 14, fontWeight: 800, color: C.text, marginBottom: 4 }}>{folder.name}</div>
        <div style={{ fontSize: 11, color: C.textMuted, marginBottom: 12, lineHeight: 1.4 }}>{folder.desc}</div>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
          <span style={{ fontSize: 10, color: folder.color, fontWeight: 700, background: `${folder.color}18`, borderRadius: 6, padding: "3px 8px" }}>
            {fileCount} file{fileCount !== 1 ? "s" : ""}
          </span>
          <span style={{ fontSize: 18, color: folder.color, opacity: hover ? 1 : 0, transition: "opacity 0.2s" }}>→</span>
        </div>
      </div>
    </div>
  );
}

function FolderPockets({ showToast }) {
  const [folders, setFolders] = useState(DEFAULT_FOLDERS);
  const [files, setFiles] = useState([]);
  const [openFolder, setOpenFolder] = useState(null);
  const [showNewFolder, setShowNewFolder] = useState(false);
  const [renamingFolder, setRenamingFolder] = useState(null);
  const [search, setSearch] = useState("");

  const addFile = useCallback((file) => setFiles(prev => [...prev, file]), []);
  const renameFile = useCallback((id, name) => setFiles(prev => prev.map(f => f.id === id ? { ...f, name } : f)), []);
  const deleteFile = useCallback((id) => setFiles(prev => prev.filter(f => f.id !== id)), []);

  const addFolder = ({ name, icon, color }) => {
    const f = { id: `f_${uid()}`, name, icon, color, desc: "" };
    setFolders(prev => [...prev, f]);
    setShowNewFolder(false);
    showToast({ type: "success", title: "Folder Created", body: `"${name}" folder is ready.` });
  };

  const renameFolder = (id, name) => setFolders(prev => prev.map(f => f.id === id ? { ...f, name } : f));
  const deleteFolder = (id) => { setFolders(prev => prev.filter(f => f.id !== id)); setFiles(prev => prev.filter(f => f.folderId !== id)); };

  const searchResults = search.trim()
    ? files.filter(f => f.name.toLowerCase().includes(search.toLowerCase()))
    : null;

  const currentFolder = folders.find(f => f.id === openFolder);

  return (
    <div>
      {/* Header row */}
      <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 20 }}>
        <div style={{ flex: 1, position: "relative" }}>
          <span style={{ position: "absolute", left: 10, top: "50%", transform: "translateY(-50%)", fontSize: 14, color: C.textMuted }}>🔍</span>
          <input value={search} onChange={e => setSearch(e.target.value)} placeholder="Search files across all folders..."
            style={{ width: "100%", background: C.card, border: `1px solid ${C.border}`, borderRadius: 10, padding: "9px 12px 9px 34px", fontSize: 12, color: C.text, outline: "none" }} />
        </div>
        <button onClick={() => setShowNewFolder(true)} style={{
          background: C.accent, border: "none", color: "#fff",
          borderRadius: 10, padding: "9px 16px", fontSize: 12, fontWeight: 700,
          cursor: "pointer", whiteSpace: "nowrap", flexShrink: 0,
        }}>+ New Folder</button>
      </div>

      {/* Search results */}
      {searchResults && (
        <div style={{ marginBottom: 20 }}>
          <div style={{ fontSize: 11, color: C.textMuted, marginBottom: 10 }}>{searchResults.length} result{searchResults.length !== 1 ? "s" : ""} for "{search}"</div>
          {searchResults.length === 0
            ? <div style={{ color: C.textMuted, fontSize: 12, padding: 16, background: C.card, borderRadius: 10 }}>No files found.</div>
            : <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: 10 }}>
                {searchResults.map(f => {
                  const folder = folders.find(fo => fo.id === f.folderId);
                  return <FileCard key={f.id} file={f} folderColor={folder?.color || C.accent}
                    onRename={() => { const n = prompt("Rename:", f.name); if (n?.trim()) renameFile(f.id, n.trim()); }}
                    onDelete={() => deleteFile(f.id)}
                    onView={() => {}} />;
                })}
              </div>
          }
        </div>
      )}

      {/* Folder view */}
      {!searchResults && openFolder && currentFolder ? (
        <FolderView
          folder={currentFolder}
          files={files}
          onUpload={addFile}
          onRename={renameFile}
          onDelete={deleteFile}
          onBack={() => setOpenFolder(null)}
          onRenameFolder={renameFolder}
          showToast={showToast}
        />
      ) : !searchResults && (
        <>
          <div style={{ fontSize: 11, color: C.textMuted, marginBottom: 12, fontWeight: 700, textTransform: "uppercase", letterSpacing: 1 }}>{folders.length} folders · {files.length} files total</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(200px, 1fr))", gap: 14 }}>
            {folders.map(f => (
              <FolderCard key={f.id} folder={f}
                fileCount={files.filter(fi => fi.folderId === f.id).length}
                onClick={() => setOpenFolder(f.id)}
                onRename={() => setRenamingFolder(f.id)}
                onDelete={() => deleteFolder(f.id)}
              />
            ))}
          </div>
        </>
      )}

      {showNewFolder && <NewFolderModal onSave={addFolder} onClose={() => setShowNewFolder(false)} />}
      {renamingFolder && (
        <RenameModal
          value={folders.find(f => f.id === renamingFolder)?.name || ""}
          onSave={(name) => { renameFolder(renamingFolder, name); setRenamingFolder(null); }}
          onClose={() => setRenamingFolder(null)}
        />
      )}
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// NOTIFICATION TRIGGER BUTTONS (compact)
// ══════════════════════════════════════════════════════════════════════════════
function TrigBtn({ label, type, onClick, icon }) {
  const cfg = TYPE_CFG[type] || TYPE_CFG.info;
  const [hover, setHover] = useState(false);
  return (
    <button onClick={onClick} onMouseEnter={() => setHover(true)} onMouseLeave={() => setHover(false)}
      style={{ display: "flex", alignItems: "center", gap: 7, padding: "8px 12px", borderRadius: 9, background: hover ? cfg.bg : "transparent", border: `1px solid ${hover ? cfg.color : C.border}`, color: hover ? cfg.color : C.textMuted, fontSize: 11, fontWeight: 600, cursor: "pointer", transition: "all 0.18s", textAlign: "left" }}>
      <span>{icon || cfg.icon}</span>{label}
    </button>
  );
}

function NotifSection({ title, color, children }) {
  return (
    <div style={{ background: C.surface, border: `1px solid ${C.border}`, borderRadius: 12, marginBottom: 12, overflow: "hidden" }}>
      <div style={{ padding: "10px 14px", borderBottom: `1px solid ${C.border}`, fontSize: 10, fontWeight: 800, color, letterSpacing: 0.5, textTransform: "uppercase", background: `${color}08` }}>{title}</div>
      <div style={{ padding: "8px 10px", display: "flex", flexDirection: "column", gap: 5 }}>{children}</div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════════════════════
// MAIN APP
// ══════════════════════════════════════════════════════════════════════════════
export default function App() {
  const [tab, setTab] = useState("folders");   // "folders" | "notifications"
  const [toasts, setToasts] = useState([]);
  const [modal, setModal] = useState(null);
  const [notifs, setNotifs] = useState([]);
  const [stats, setStats] = useState({ total: 0, success: 0, error: 0, warning: 0 });

  useEffect(() => {
    const s = document.createElement("style");
    s.textContent = `
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
      * { box-sizing: border-box; font-family: 'Inter', sans-serif; margin: 0; padding: 0; }
      @keyframes toastBar { from { transform: scaleX(1); } to { transform: scaleX(0); } }
      @keyframes pulse { 0%,100% { box-shadow: 0 0 0 0 rgba(239,68,68,0.5); } 50% { box-shadow: 0 0 0 6px rgba(239,68,68,0); } }
      @keyframes slideDown { from { opacity:0; transform: translateY(-8px); } to { opacity:1; transform: translateY(0); } }
      ::-webkit-scrollbar { width: 5px; } ::-webkit-scrollbar-track { background: transparent; } ::-webkit-scrollbar-thumb { background: #252A40; border-radius: 10px; }
    `;
    document.head.appendChild(s);
    return () => document.head.removeChild(s);
  }, []);

  const addNotif = useCallback((data, showToast = true, showModal = false) => {
    const n = { ...data, id: uid(), read: false, time: nowFull() };
    setNotifs(prev => [n, ...prev]);
    setStats(prev => ({
      total: prev.total + 1,
      success: prev.success + (n.type === "success" ? 1 : 0),
      error: prev.error + (n.type === "error" ? 1 : 0),
      warning: prev.warning + (["warning", "deadline", "exam"].includes(n.type) ? 1 : 0),
    }));
    if (showToast) setToasts(prev => [...prev.slice(-4), { ...n, id: uid() }]);
    if (showModal) setModal(n);
  }, []);

  const showToast = useCallback((data) => addNotif(data, true, false), [addNotif]);

  const fire = (data, asModal = false) => addNotif(data, true, asModal);
  const dismissToast = useCallback((id) => setToasts(prev => prev.filter(t => t.id !== id)), []);
  const markRead = useCallback((id) => setNotifs(prev => prev.map(n => n.id === id ? { ...n, read: true } : n)), []);
  const deleteNotif = useCallback((id) => setNotifs(prev => prev.filter(n => n.id !== id)), []);
  const clearAll = useCallback(() => setNotifs([]), []);
  const unread = notifs.filter(n => !n.read).length;

  const TABS = [
    { id: "folders",       label: "📁 File Pockets" },
    { id: "notifications", label: "🔔 Notifications" },
  ];

  return (
    <div style={{ minHeight: "100vh", background: C.bg, color: C.text, paddingBottom: 80 }}>
      {/* Header */}
      <div style={{ background: C.surface, borderBottom: `1px solid ${C.border}`, padding: "0 24px", position: "sticky", top: 0, zIndex: 100, display: "flex", alignItems: "center", justifyContent: "space-between", height: 60 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{ width: 34, height: 34, borderRadius: 9, background: `linear-gradient(135deg, ${C.accent}, #818CF8)`, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16 }}>🗂</div>
          <div>
            <div style={{ fontSize: 14, fontWeight: 800, color: C.text }}>PocketHub</div>
            <div style={{ fontSize: 9, color: C.textMuted }}>Files · Folders · Notifications</div>
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          {/* Tab nav */}
          <div style={{ display: "flex", gap: 4, background: C.card, borderRadius: 10, padding: 4, border: `1px solid ${C.border}` }}>
            {TABS.map(t => (
              <button key={t.id} onClick={() => setTab(t.id)} style={{
                padding: "6px 14px", borderRadius: 7, fontSize: 11, fontWeight: 700, border: "none", cursor: "pointer",
                background: tab === t.id ? C.accent : "transparent",
                color: tab === t.id ? "#fff" : C.textMuted,
                transition: "all 0.2s",
              }}>{t.label}</button>
            ))}
          </div>
          <NotifBell notifs={notifs} onRead={markRead} onDelete={deleteNotif} onClearAll={clearAll} />
        </div>
      </div>

      <div style={{ maxWidth: 960, margin: "0 auto", padding: "24px 20px" }}>
        {/* ── FOLDER POCKETS TAB ── */}
        {tab === "folders" && <FolderPockets showToast={showToast} />}

        {/* ── NOTIFICATIONS TAB ── */}
        {tab === "notifications" && (
          <>
            {/* Stats */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 10, marginBottom: 24 }}>
              {[
                { label: "Total", value: stats.total,   color: C.accent,   icon: "📊" },
                { label: "Success", value: stats.success, color: C.success, icon: "✓" },
                { label: "Errors",  value: stats.error,   color: C.error,   icon: "✕" },
                { label: "Warnings",value: stats.warning, color: C.warning, icon: "⚠" },
              ].map(s => (
                <div key={s.label} style={{ background: C.surface, border: `1px solid ${C.border}`, borderRadius: 12, padding: "14px 16px", borderTop: `3px solid ${s.color}` }}>
                  <div style={{ fontSize: 20, fontWeight: 900, color: s.color }}>{s.value}</div>
                  <div style={{ fontSize: 10, color: C.textMuted, marginTop: 2 }}>{s.icon} {s.label}</div>
                </div>
              ))}
            </div>

            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
              <div>
                <NotifSection title="✓ Success" color={C.success}>
                  <TrigBtn label="Note Saved Successfully" type="success" onClick={() => fire({ type: "success", title: "Note Saved Successfully", body: "Study notes for Chapter 7 saved." })} />
                  <TrigBtn label="Assignment Submitted" type="success" onClick={() => fire({ type: "success", title: "Assignment Submitted", body: "Physics assignment submitted at 11:45 PM." })} />
                  <TrigBtn label="Password Added" type="success" onClick={() => fire({ type: "success", title: "Password Added", body: "Credential for 'College Portal' saved." })} />
                  <TrigBtn label="Show as Modal" type="success" icon="⊞" onClick={() => fire({ type: "success", title: "File Uploaded ✅", body: "Your document was saved to Assignments folder." }, true)} />
                </NotifSection>
                <NotifSection title="✕ Errors" color={C.error}>
                  <TrigBtn label="Invalid Login Credentials" type="error" onClick={() => fire({ type: "error", title: "Invalid Login Credentials", body: "Check your username and password." })} />
                  <TrigBtn label="Failed to Save Data" type="error" onClick={() => fire({ type: "error", title: "Failed to Save", body: "Network timeout. Changes not saved." })} />
                  <TrigBtn label="Show as Modal" type="error" icon="⊞" onClick={() => fire({ type: "error", title: "Login Failed", body: "Invalid credentials. Reset your password." }, true)} />
                </NotifSection>
                <NotifSection title="⚠ Warnings" color={C.warning}>
                  <TrigBtn label="Assignment Due Tomorrow" type="warning" onClick={() => fire({ type: "warning", title: "Assignment Due Tomorrow", body: "Maths Assignment 3 is due at 11:59 PM." })} />
                  <TrigBtn label="Exam in 2 Days" type="warning" onClick={() => fire({ type: "warning", title: "Exam in 2 Days", body: "Physics Unit Test — Thursday 9 AM." })} />
                  <TrigBtn label="Show as Modal" type="warning" icon="⊞" onClick={() => fire({ type: "warning", title: "Deadline in 2 Hours!", body: "Submit your assignment before 6 PM." }, true)} />
                </NotifSection>
              </div>
              <div>
                <NotifSection title="ℹ Info" color={C.info}>
                  <TrigBtn label="New Update Available" type="info" onClick={() => fire({ type: "info", title: "New Update Available", body: "v2.4.1 — improved timetable sync." })} />
                  <TrigBtn label="Timetable Updated" type="info" onClick={() => fire({ type: "info", title: "Timetable Updated", body: "Wednesday's lab moved to Room 204." })} />
                </NotifSection>
                <NotifSection title="🔔 Reminders" color={C.warning}>
                  <TrigBtn label="Good Morning! 3 Classes" type="reminder" onClick={() => fire({ type: "reminder", title: "Good Morning! ☀️", body: "3 classes today. First at 9:00 AM." })} />
                  <TrigBtn label="Deadline in 4 Hours" type="deadline" onClick={() => fire({ type: "deadline", title: "Deadline in 4 Hours ⏰", body: "Network Security — submit before 6 PM." })} />
                  <TrigBtn label="AFCAT Session at 6 PM" type="reminder" onClick={() => fire({ type: "reminder", title: "AFCAT Study Session 📚", body: "Study session at 6 PM tonight." })} />
                  <TrigBtn label="Log Your Mood" type="reminder" onClick={() => fire({ type: "reminder", title: "Log Your Mood 💭", body: "You haven't logged your mood today." })} />
                </NotifSection>
                <NotifSection title="🎉 Special" color={C.birthday}>
                  <TrigBtn label="Birthday — Priya 🎂" type="birthday" onClick={() => fire({ type: "birthday", title: "Today is Priya's Birthday 🎂", body: "Don't forget to wish her!" }, false, true)} />
                  <TrigBtn label="Exam Alert — AFCAT" type="exam" onClick={() => fire({ type: "exam", title: "Exam Starting Soon 📝", body: "AFCAT mock test in 30 minutes!" })} />
                </NotifSection>
                <NotifSection title="⚡ Quick Fire" color={C.accent}>
                  <TrigBtn label="Fire 5 Random Notifications" type="info" icon="⚡"
                    onClick={() => {
                      const picks = [...DEMO_NOTIFS].sort(() => Math.random() - 0.5).slice(0, 5);
                      picks.forEach((n, i) => setTimeout(() => addNotif(n, true, false), i * 600));
                    }} />
                </NotifSection>
              </div>
            </div>

            {/* History */}
            {notifs.length > 0 && (
              <div style={{ marginTop: 24 }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
                  <div style={{ fontSize: 13, fontWeight: 800, color: C.text }}>
                    History
                    {unread > 0 && <span style={{ marginLeft: 8, background: C.error, color: "#fff", borderRadius: 20, padding: "2px 7px", fontSize: 10 }}>{unread} unread</span>}
                  </div>
                  <div style={{ display: "flex", gap: 7 }}>
                    <button onClick={() => notifs.filter(n => !n.read).forEach(n => markRead(n.id))} style={{ fontSize: 11, color: C.accent, background: "none", border: `1px solid ${C.border}`, borderRadius: 7, padding: "5px 11px", cursor: "pointer", fontWeight: 600 }}>Mark all read</button>
                    <button onClick={clearAll} style={{ fontSize: 11, color: C.error, background: "none", border: `1px solid ${C.border}`, borderRadius: 7, padding: "5px 11px", cursor: "pointer", fontWeight: 600 }}>Clear all</button>
                  </div>
                </div>
                <div style={{ background: C.surface, border: `1px solid ${C.border}`, borderRadius: 14, overflow: "hidden" }}>
                  {notifs.map(n => <NotifPanelItem key={n.id} n={n} onRead={markRead} onDelete={deleteNotif} />)}
                </div>
              </div>
            )}
          </>
        )}
      </div>

      {/* Toast stack */}
      <div style={{ position: "fixed", bottom: 20, right: 20, display: "flex", flexDirection: "column-reverse", gap: 8, zIndex: 9998, pointerEvents: "none" }}>
        {toasts.map(t => <div key={t.id} style={{ pointerEvents: "auto" }}><Toast notif={t} onDismiss={dismissToast} /></div>)}
      </div>

      {/* Center modal */}
      {modal && <CenterModal notif={modal} onClose={() => setModal(null)} />}
    </div>
  );
}
