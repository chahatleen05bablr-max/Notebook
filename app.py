"""
PocketHub — Streamlit port of the React notification + folder management app.
Run with:  streamlit run pockethub_app.py
"""

import streamlit as st
from datetime import datetime
import random
import uuid

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="PocketHub",
    page_icon="🗂",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Theme colours (CSS variables injected once) ──────────────────────────────
THEME = dict(
    bg="#0B0D14", surface="#131620", surfaceHover="#1C2030", card="#181B28",
    border="#252A40", borderHover="#3A4060", text="#E8EAF6", textMuted="#6B72A8",
    textSub="#9BA3D4", success="#22C55E", successBg="#0A1F12",
    error="#EF4444", errorBg="#1F0A0A", warning="#F59E0B", warningBg="#1F180A",
    info="#6366F1", infoBg="#0E0F20", birthday="#EC4899", birthdayBg="#1F0A16",
    accent="#6366F1", purple="#8B5CF6", teal="#14B8A6", orange="#F97316",
)
C = THEME   # short alias

TYPE_CFG = {
    "success":  {"color": C["success"],  "bg": C["successBg"],  "icon": "✅", "label": "Success"},
    "error":    {"color": C["error"],    "bg": C["errorBg"],    "icon": "❌", "label": "Error"},
    "warning":  {"color": C["warning"],  "bg": C["warningBg"],  "icon": "⚠️", "label": "Warning"},
    "info":     {"color": C["info"],     "bg": C["infoBg"],     "icon": "ℹ️", "label": "Info"},
    "birthday": {"color": C["birthday"], "bg": C["birthdayBg"], "icon": "🎂", "label": "Birthday"},
    "reminder": {"color": C["warning"],  "bg": C["warningBg"],  "icon": "🔔", "label": "Reminder"},
    "exam":     {"color": C["error"],    "bg": C["errorBg"],    "icon": "📝", "label": "Exam"},
    "deadline": {"color": C["warning"],  "bg": C["warningBg"],  "icon": "⏰", "label": "Deadline"},
}

DEFAULT_FOLDERS = [
    {"id": "assignments", "name": "Assignments", "icon": "📚", "color": C["warning"],  "desc": "Homework, projects & submissions"},
    {"id": "credentials", "name": "Credentials", "icon": "🔐", "color": C["success"],  "desc": "Passwords, logins & access keys"},
    {"id": "notes",       "name": "Study Notes", "icon": "📓", "color": C["info"],     "desc": "Lectures, summaries & flashcards"},
    {"id": "exams",       "name": "Exam Prep",   "icon": "🎯", "color": C["error"],    "desc": "Mock tests, question banks & scores"},
]

DEMO_NOTIFS = [
    {"type": "success", "title": "Note Saved Successfully",     "body": "Study notes for Chapter 7 have been saved."},
    {"type": "success", "title": "Assignment Submitted",         "body": "Physics assignment submitted at 11:45 PM."},
    {"type": "success", "title": "Password Added",               "body": "Credential for 'College Portal' saved securely."},
    {"type": "error",   "title": "Invalid Login Credentials",    "body": "Check your username and password and try again."},
    {"type": "warning", "title": "Assignment Due Tomorrow",      "body": "Mathematics Assignment 3 is due at 11:59 PM tomorrow."},
    {"type": "warning", "title": "Exam in 2 Days",               "body": "Physics Unit Test — Thursday 9 AM."},
    {"type": "info",    "title": "Timetable Updated",            "body": "Wednesday's lab session moved to Room 204."},
    {"type": "birthday","title": "Today is Priya's Birthday 🎂", "body": "Don't forget to wish her!"},
    {"type": "reminder","title": "AFCAT Study Session 📚",       "body": "Don't forget your session at 6 PM tonight."},
    {"type": "exam",    "title": "Exam Alert 📝",                "body": "AFCAT mock test starts in 30 minutes. Best of luck!"},
]

FILE_ICONS = {
    "pdf": "📄", "doc": "📝", "docx": "📝", "txt": "📃", "png": "🖼️",
    "jpg": "🖼️", "jpeg": "🖼️", "gif": "🖼️", "mp4": "🎬", "mp3": "🎵",
    "zip": "📦", "xlsx": "📊", "xls": "📊", "ppt": "📊", "pptx": "📊", "csv": "📊",
}

FOLDER_ICONS = ["📁","📂","📚","🗂","🔐","📝","🎯","📓","🗄","💼","🧪","🏆","🎮","🔬","📊"]
FOLDER_COLORS = [C["accent"], C["success"], C["error"], C["warning"],
                 C["birthday"], C["teal"], C["orange"], C["purple"]]

# ─── Helpers ──────────────────────────────────────────────────────────────────

def file_icon(name: str) -> str:
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
    return FILE_ICONS.get(ext, "📎")

def fmt_size(b: int) -> str:
    if b < 1024:      return f"{b} B"
    if b < 1_048_576: return f"{b/1024:.1f} KB"
    return f"{b/1_048_576:.1f} MB"

def now_full() -> str:
    return datetime.now().strftime("%b %d, %I:%M %p")

def new_notif(data: dict) -> dict:
    return {**data, "id": str(uuid.uuid4()), "read": False, "time": now_full()}

# ─── Session state init ───────────────────────────────────────────────────────

def init_state():
    if "tab" not in st.session_state:
        st.session_state.tab = "folders"
    if "notifs" not in st.session_state:
        st.session_state.notifs = []
    if "folders" not in st.session_state:
        st.session_state.folders = [dict(f) for f in DEFAULT_FOLDERS]
    if "files" not in st.session_state:
        st.session_state.files = []
    if "open_folder" not in st.session_state:
        st.session_state.open_folder = None
    if "toast_msg" not in st.session_state:
        st.session_state.toast_msg = None
    if "search" not in st.session_state:
        st.session_state.search = ""
    if "show_new_folder" not in st.session_state:
        st.session_state.show_new_folder = False
    if "rename_folder_id" not in st.session_state:
        st.session_state.rename_folder_id = None
    if "rename_file_id" not in st.session_state:
        st.session_state.rename_file_id = None
    if "view_file_id" not in st.session_state:
        st.session_state.view_file_id = None
    if "notif_filter" not in st.session_state:
        st.session_state.notif_filter = "all"

init_state()

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {{
    font-family: 'Inter', sans-serif !important;
    background-color: {C['bg']} !important;
    color: {C['text']} !important;
}}

/* Hide Streamlit chrome */
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding-top: 1rem !important; max-width: 1100px; }}

/* Tabs styling */
.stTabs [role="tablist"] {{
    background: {C['card']};
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid {C['border']};
}}
.stTabs [role="tab"] {{
    border-radius: 8px !important;
    color: {C['textMuted']} !important;
    font-weight: 700 !important;
    font-size: 13px !important;
}}
.stTabs [aria-selected="true"] {{
    background: {C['accent']} !important;
    color: #fff !important;
}}
.stTabs [role="tabpanel"] {{ background: transparent !important; }}

/* Buttons */
.stButton > button {{
    background: {C['accent']} !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 13px !important;
    padding: 8px 18px !important;
}}
.stButton > button:hover {{
    background: #4F46E5 !important;
    border: none !important;
}}

/* Text input */
.stTextInput > div > div > input {{
    background: {C['card']} !important;
    color: {C['text']} !important;
    border: 1px solid {C['border']} !important;
    border-radius: 10px !important;
    font-size: 13px !important;
}}
.stTextInput > div > div > input:focus {{
    border-color: {C['accent']} !important;
    box-shadow: 0 0 0 2px {C['accent']}33 !important;
}}

/* Selectbox */
.stSelectbox > div > div {{
    background: {C['card']} !important;
    color: {C['text']} !important;
    border: 1px solid {C['border']} !important;
    border-radius: 10px !important;
}}

/* File uploader */
.stFileUploader > div {{
    background: {C['card']} !important;
    border: 2px dashed {C['border']} !important;
    border-radius: 12px !important;
    color: {C['textMuted']} !important;
}}

/* Metric */
[data-testid="metric-container"] {{
    background: {C['surface']} !important;
    border: 1px solid {C['border']} !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
}}

/* Scrollbar */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {C['border']}; border-radius: 10px; }}

/* Expander */
.streamlit-expanderHeader {{
    background: {C['surface']} !important;
    color: {C['text']} !important;
    border: 1px solid {C['border']} !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
}}
.streamlit-expanderContent {{
    background: {C['surface']} !important;
    border: 1px solid {C['border']} !important;
    border-top: none !important;
}}
</style>
""", unsafe_allow_html=True)

# ─── App Header ───────────────────────────────────────────────────────────────
col_logo, col_spacer = st.columns([1, 3])
with col_logo:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:10px;padding:8px 0 16px">
      <div style="width:40px;height:40px;border-radius:10px;
                  background:linear-gradient(135deg,{C['accent']},#818CF8);
                  display:flex;align-items:center;justify-content:center;font-size:20px;">🗂</div>
      <div>
        <div style="font-size:16px;font-weight:900;color:{C['text']}">PocketHub</div>
        <div style="font-size:10px;color:{C['textMuted']}">Files · Folders · Notifications</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Toast / banner helper ────────────────────────────────────────────────────
def show_toast(data: dict):
    """Push a notification and display a Streamlit toast."""
    notif = new_notif(data)
    st.session_state.notifs.insert(0, notif)
    cfg = TYPE_CFG.get(data["type"], TYPE_CFG["info"])
    st.toast(f"{cfg['icon']} **{data['title']}** — {data['body']}")

# ─── Render a single notification row ────────────────────────────────────────
def notif_row(n: dict):
    cfg = TYPE_CFG.get(n["type"], TYPE_CFG["info"])
    unread_dot = "🔵 " if not n["read"] else ""
    col1, col2, col3, col4 = st.columns([0.07, 0.65, 0.14, 0.14])
    with col1:
        st.markdown(f"<div style='font-size:22px;line-height:1'>{cfg['icon']}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div>
          <div style='font-size:12px;font-weight:700;color:{C['text']}'>{unread_dot}{n['title']}</div>
          <div style='font-size:11px;color:{C['textMuted']};line-height:1.4'>{n['body']}</div>
          <div style='font-size:10px;color:{C['textMuted']};margin-top:2px'>{n['time']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        if not n["read"]:
            if st.button("✓ Read", key=f"read_{n['id']}"):
                for notif in st.session_state.notifs:
                    if notif["id"] == n["id"]:
                        notif["read"] = True
                st.rerun()
    with col4:
        if st.button("✕", key=f"del_{n['id']}"):
            st.session_state.notifs = [x for x in st.session_state.notifs if x["id"] != n["id"]]
            st.rerun()
    st.markdown(f"<hr style='border:none;border-top:1px solid {C['border']};margin:4px 0'>", unsafe_allow_html=True)

# ─── Main tabs ────────────────────────────────────────────────────────────────
tab_folders, tab_notifs = st.tabs(["📁  File Pockets", "🔔  Notifications"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – FOLDER POCKETS
# ══════════════════════════════════════════════════════════════════════════════
with tab_folders:

    # --- Search bar + New Folder button ---------------------------------------
    sc1, sc2 = st.columns([4, 1])
    with sc1:
        search = st.text_input("", placeholder="🔍 Search files across all folders…",
                               value=st.session_state.search, label_visibility="collapsed",
                               key="search_input")
        st.session_state.search = search
    with sc2:
        if st.button("➕ New Folder"):
            st.session_state.show_new_folder = True

    # --- New folder dialog -------------------------------------------------------
    if st.session_state.show_new_folder:
        with st.expander("✨ Create New Folder", expanded=True):
            nf_col1, nf_col2 = st.columns(2)
            with nf_col1:
                nf_name = st.text_input("Folder Name", key="nf_name")
                nf_icon = st.selectbox("Icon", FOLDER_ICONS, key="nf_icon")
            with nf_col2:
                nf_color = st.selectbox("Color", FOLDER_COLORS, key="nf_color")
                if nf_name:
                    st.markdown(
                        f"<div style='padding:12px;background:{C['card']};border-radius:10px;"
                        f"border:1px solid {nf_color}55;display:flex;align-items:center;gap:10px;'>"
                        f"<span style='font-size:28px'>{nf_icon}</span>"
                        f"<span style='font-weight:700;color:{C['text']}'>{nf_name}</span></div>",
                        unsafe_allow_html=True)
            btn_c1, btn_c2 = st.columns(2)
            with btn_c1:
                if st.button("✅ Create Folder", disabled=not nf_name.strip()):
                    new_folder = {
                        "id": f"f_{uuid.uuid4().hex[:8]}",
                        "name": nf_name.strip(),
                        "icon": nf_icon,
                        "color": nf_color,
                        "desc": ""
                    }
                    st.session_state.folders.append(new_folder)
                    st.session_state.show_new_folder = False
                    show_toast({"type": "success", "title": "Folder Created",
                                "body": f'"{nf_name}" folder is ready.'})
                    st.rerun()
            with btn_c2:
                if st.button("Cancel", key="cancel_nf"):
                    st.session_state.show_new_folder = False
                    st.rerun()

    # --- Search results view --------------------------------------------------
    if search.strip():
        matches = [f for f in st.session_state.files
                   if search.lower() in f["name"].lower()]
        st.markdown(f"<div style='color:{C['textMuted']};font-size:12px;margin-bottom:8px'>"
                    f"{len(matches)} result{'s' if len(matches)!=1 else ''} for \"{search}\"</div>",
                    unsafe_allow_html=True)
        if not matches:
            st.info("No files found.")
        else:
            cols = st.columns(4)
            for i, f in enumerate(matches):
                folder = next((fo for fo in st.session_state.folders if fo["id"] == f["folderId"]), None)
                fc = folder["color"] if folder else C["accent"]
                with cols[i % 4]:
                    st.markdown(f"""
                    <div style="background:{C['card']};border:1px solid {fc}55;border-radius:12px;
                                padding:12px;text-align:center;">
                      <div style="font-size:32px">{file_icon(f['name'])}</div>
                      <div style="font-size:11px;font-weight:700;color:{C['text']};
                                  overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
                           title="{f['name']}">{f['name']}</div>
                      <div style="font-size:9px;color:{C['textMuted']}">{fmt_size(f['size'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("✕ Remove", key=f"srch_del_{f['id']}"):
                        st.session_state.files = [x for x in st.session_state.files if x["id"] != f["id"]]
                        st.rerun()
        st.stop()

    # --- Open a specific folder -----------------------------------------------
    if st.session_state.open_folder:
        folder = next((fo for fo in st.session_state.folders
                       if fo["id"] == st.session_state.open_folder), None)
        if not folder:
            st.session_state.open_folder = None
            st.rerun()

        # breadcrumb back button
        if st.button(f"← Back to All Folders"):
            st.session_state.open_folder = None
            st.rerun()

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;padding:16px 0 8px">
          <span style="font-size:36px">{folder['icon']}</span>
          <div>
            <div style="font-size:18px;font-weight:900;color:{C['text']}">{folder['name']}</div>
            <div style="font-size:11px;color:{C['textMuted']}">{folder.get('desc','')}</div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Rename folder inline
        rfcol1, rfcol2 = st.columns([3, 1])
        with rfcol2:
            with st.popover("✏️ Rename Folder"):
                new_name = st.text_input("New name", value=folder["name"], key="rf_input")
                if st.button("Save Name"):
                    for fo in st.session_state.folders:
                        if fo["id"] == folder["id"]:
                            fo["name"] = new_name.strip() or fo["name"]
                    st.rerun()

        # File uploader
        uploaded = st.file_uploader(
            "Upload files (drag & drop or click to browse)",
            accept_multiple_files=True,
            key=f"uploader_{folder['id']}"
        )
        if uploaded:
            added = 0
            for uf in uploaded:
                existing_ids = {f["id"] for f in st.session_state.files}
                fid = f"file_{uuid.uuid4().hex[:8]}"
                data = uf.read()
                new_file = {
                    "id": fid,
                    "name": uf.name,
                    "size": len(data),
                    "folderId": folder["id"],
                    "addedAt": datetime.now().isoformat(),
                    "data": data,
                }
                st.session_state.files.append(new_file)
                added += 1
            if added:
                show_toast({"type": "success", "title": f"{added} File(s) Uploaded",
                            "body": f"Added to {folder['name']}."})
                st.rerun()

        # Sort controls
        folder_files = [f for f in st.session_state.files if f["folderId"] == folder["id"]]
        if folder_files:
            sort_col1, sort_col2 = st.columns([3, 1])
            with sort_col2:
                sort_by = st.selectbox("Sort by", ["Date", "Name"], key=f"sort_{folder['id']}",
                                       label_visibility="collapsed")
            if sort_by == "Name":
                folder_files = sorted(folder_files, key=lambda f: f["name"])
            else:
                folder_files = sorted(folder_files, key=lambda f: f["addedAt"], reverse=True)

            with sort_col1:
                st.markdown(f"<div style='color:{C['textMuted']};font-size:11px;padding-top:8px'>"
                            f"{len(folder_files)} file(s)</div>", unsafe_allow_html=True)

            cols = st.columns(4)
            for i, f in enumerate(folder_files):
                with cols[i % 4]:
                    st.markdown(f"""
                    <div style="background:{C['card']};border:1px solid {folder['color']}44;
                                border-radius:12px;overflow:hidden;margin-bottom:8px">
                      <div style="height:70px;display:flex;align-items:center;justify-content:center;
                                  background:{folder['color']}10;font-size:32px;
                                  border-bottom:1px solid {C['border']}">{file_icon(f['name'])}</div>
                      <div style="padding:8px">
                        <div style="font-size:11px;font-weight:700;color:{C['text']};
                                    overflow:hidden;text-overflow:ellipsis;white-space:nowrap"
                             title="{f['name']}">{f['name']}</div>
                        <div style="font-size:9px;color:{C['textMuted']};margin-bottom:6px">{fmt_size(f['size'])}</div>
                      </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # View / Download
                    is_img = f["name"].rsplit(".", 1)[-1].lower() in {"png","jpg","jpeg","gif","webp","svg"}
                    is_text = f["name"].rsplit(".", 1)[-1].lower() in {"txt","md","csv","json","js","py","html","css"}
                    if is_img or is_text:
                        with st.popover("👁 View"):
                            if is_img:
                                st.image(f["data"], caption=f["name"])
                            else:
                                st.code(f["data"].decode("utf-8", errors="replace"),
                                        language=f["name"].rsplit(".",1)[-1] if "." in f["name"] else "text")
                    else:
                        st.download_button("⬇ Download", data=f["data"], file_name=f["name"],
                                           key=f"dl_{f['id']}")

                    # Rename
                    with st.popover("✏️ Rename"):
                        new_fn = st.text_input("New filename", value=f["name"], key=f"ren_{f['id']}")
                        if st.button("Save", key=f"saveren_{f['id']}"):
                            for fi in st.session_state.files:
                                if fi["id"] == f["id"]:
                                    fi["name"] = new_fn.strip() or fi["name"]
                            show_toast({"type": "success", "title": "File Renamed",
                                        "body": f'Renamed to "{new_fn}"'})
                            st.rerun()

                    # Delete
                    if st.button("🗑 Delete", key=f"fdel_{f['id']}"):
                        st.session_state.files = [x for x in st.session_state.files if x["id"] != f["id"]]
                        show_toast({"type": "info", "title": "File Removed", "body": f"{f['name']} deleted."})
                        st.rerun()
        else:
            st.markdown(f"""
            <div style="text-align:center;padding:40px;color:{C['textMuted']};font-size:13px">
              <div style="font-size:48px;margin-bottom:12px">{folder['icon']}</div>
              This folder is empty. Upload your first file above.
            </div>
            """, unsafe_allow_html=True)

    # --- Folder grid view -----------------------------------------------------
    else:
        folders = st.session_state.folders
        total_files = len(st.session_state.files)
        st.markdown(f"<div style='color:{C['textMuted']};font-size:11px;font-weight:700;"
                    f"text-transform:uppercase;letter-spacing:1px;margin-bottom:12px'>"
                    f"{len(folders)} folders · {total_files} files total</div>",
                    unsafe_allow_html=True)

        cols = st.columns(min(len(folders), 4) or 1)
        for i, folder in enumerate(folders):
            file_count = sum(1 for f in st.session_state.files if f["folderId"] == folder["id"])
            with cols[i % 4]:
                st.markdown(f"""
                <div style="background:{C['card']};border:1px solid {C['border']};
                            border-radius:16px;padding:20px;margin-bottom:8px;
                            border-top:3px solid {folder['color']}">
                  <div style="font-size:36px;margin-bottom:10px">{folder['icon']}</div>
                  <div style="font-size:14px;font-weight:800;color:{C['text']};margin-bottom:4px">
                    {folder['name']}</div>
                  <div style="font-size:11px;color:{C['textMuted']};margin-bottom:12px;line-height:1.4">
                    {folder.get('desc','')}</div>
                  <span style="font-size:10px;color:{folder['color']};font-weight:700;
                               background:{folder['color']}18;border-radius:6px;padding:3px 8px">
                    {file_count} file{'s' if file_count!=1 else ''}</span>
                </div>
                """, unsafe_allow_html=True)

                if st.button(f"📂 Open", key=f"open_{folder['id']}"):
                    st.session_state.open_folder = folder["id"]
                    st.rerun()

                # Rename / Delete via popover
                act1, act2 = st.columns(2)
                with act1:
                    with st.popover("✏️"):
                        new_fn = st.text_input("New name", value=folder["name"],
                                               key=f"rfold_{folder['id']}")
                        if st.button("Save", key=f"rfoldsave_{folder['id']}"):
                            for fo in st.session_state.folders:
                                if fo["id"] == folder["id"]:
                                    fo["name"] = new_fn.strip() or fo["name"]
                            st.rerun()
                with act2:
                    if st.button("🗑", key=f"delfold_{folder['id']}"):
                        st.session_state.folders = [fo for fo in st.session_state.folders
                                                     if fo["id"] != folder["id"]]
                        st.session_state.files = [f for f in st.session_state.files
                                                   if f["folderId"] != folder["id"]]
                        show_toast({"type": "warning", "title": "Folder Deleted",
                                    "body": f'"{folder["name"]}" and its files removed.'})
                        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – NOTIFICATIONS
# ══════════════════════════════════════════════════════════════════════════════
with tab_notifs:

    notifs = st.session_state.notifs
    unread_count = sum(1 for n in notifs if not n["read"])

    # ── Stats row ──────────────────────────────────────────────────────────
    m1, m2, m3, m4 = st.columns(4)
    metrics = [
        ("📊 Total",    len(notifs),                                   C["accent"]),
        ("✅ Success",  sum(1 for n in notifs if n["type"]=="success"), C["success"]),
        ("❌ Errors",   sum(1 for n in notifs if n["type"]=="error"),   C["error"]),
        ("⚠️ Warnings", sum(1 for n in notifs if n["type"] in
                          ("warning","deadline","exam")),               C["warning"]),
    ]
    for col, (label, val, color) in zip([m1,m2,m3,m4], metrics):
        with col:
            st.markdown(f"""
            <div style="background:{C['surface']};border:1px solid {C['border']};
                        border-radius:12px;padding:14px 16px;
                        border-top:3px solid {color};margin-bottom:16px">
              <div style="font-size:24px;font-weight:900;color:{color}">{val}</div>
              <div style="font-size:11px;color:{C['textMuted']};margin-top:2px">{label}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Trigger buttons ────────────────────────────────────────────────────
    st.markdown(f"<div style='font-size:12px;font-weight:800;color:{C['text']};"
                f"text-transform:uppercase;letter-spacing:1px;margin-bottom:10px'>"
                f"Fire Notifications</div>", unsafe_allow_html=True)

    left_col, right_col = st.columns(2)

    with left_col:
        # Success
        with st.expander("✅ Success", expanded=False):
            if st.button("Note Saved Successfully", key="t_s1"):
                show_toast({"type":"success","title":"Note Saved Successfully","body":"Study notes for Chapter 7 saved."})
                st.rerun()
            if st.button("Assignment Submitted", key="t_s2"):
                show_toast({"type":"success","title":"Assignment Submitted","body":"Physics assignment submitted at 11:45 PM."})
                st.rerun()
            if st.button("Password Added", key="t_s3"):
                show_toast({"type":"success","title":"Password Added","body":"Credential for 'College Portal' saved."})
                st.rerun()

        # Errors
        with st.expander("❌ Errors", expanded=False):
            if st.button("Invalid Login Credentials", key="t_e1"):
                show_toast({"type":"error","title":"Invalid Login Credentials","body":"Check your username and password."})
                st.rerun()
            if st.button("Failed to Save Data", key="t_e2"):
                show_toast({"type":"error","title":"Failed to Save","body":"Network timeout. Changes not saved."})
                st.rerun()

        # Warnings
        with st.expander("⚠️ Warnings", expanded=False):
            if st.button("Assignment Due Tomorrow", key="t_w1"):
                show_toast({"type":"warning","title":"Assignment Due Tomorrow","body":"Maths Assignment 3 due at 11:59 PM."})
                st.rerun()
            if st.button("Exam in 2 Days", key="t_w2"):
                show_toast({"type":"warning","title":"Exam in 2 Days","body":"Physics Unit Test — Thursday 9 AM."})
                st.rerun()

    with right_col:
        # Info
        with st.expander("ℹ️ Info", expanded=False):
            if st.button("New Update Available", key="t_i1"):
                show_toast({"type":"info","title":"New Update Available","body":"v2.4.1 — improved timetable sync."})
                st.rerun()
            if st.button("Timetable Updated", key="t_i2"):
                show_toast({"type":"info","title":"Timetable Updated","body":"Wednesday's lab moved to Room 204."})
                st.rerun()

        # Reminders / Special
        with st.expander("🔔 Reminders & Special", expanded=False):
            if st.button("Good Morning! 3 Classes", key="t_r1"):
                show_toast({"type":"reminder","title":"Good Morning! ☀️","body":"3 classes today. First at 9:00 AM."})
                st.rerun()
            if st.button("Deadline in 4 Hours ⏰", key="t_r2"):
                show_toast({"type":"deadline","title":"Deadline in 4 Hours ⏰","body":"Network Security — submit before 6 PM."})
                st.rerun()
            if st.button("AFCAT Session at 6 PM 📚", key="t_r3"):
                show_toast({"type":"reminder","title":"AFCAT Study Session 📚","body":"Study session at 6 PM tonight."})
                st.rerun()
            if st.button("Birthday — Priya 🎂", key="t_b1"):
                show_toast({"type":"birthday","title":"Today is Priya's Birthday 🎂","body":"Don't forget to wish her!"})
                st.rerun()
            if st.button("Exam Alert — AFCAT 📝", key="t_x1"):
                show_toast({"type":"exam","title":"Exam Starting Soon 📝","body":"AFCAT mock test in 30 minutes!"})
                st.rerun()

        # Quick fire
        with st.expander("⚡ Quick Fire", expanded=False):
            if st.button("⚡ Fire 5 Random Notifications", key="t_qf"):
                picks = random.sample(DEMO_NOTIFS, min(5, len(DEMO_NOTIFS)))
                for p in picks:
                    n = new_notif(p)
                    st.session_state.notifs.insert(0, n)
                st.toast("⚡ Fired 5 random notifications!")
                st.rerun()

    # ── History panel ─────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    if notifs:
        hdr1, hdr2, hdr3 = st.columns([2, 1, 1])
        with hdr1:
            badge = (f" <span style='background:{C['error']};color:#fff;border-radius:20px;"
                     f"padding:2px 7px;font-size:10px'>{unread_count} unread</span>"
                     if unread_count else "")
            st.markdown(f"<div style='font-size:14px;font-weight:800;color:{C['text']}'>"
                        f"History{badge}</div>", unsafe_allow_html=True)
        with hdr2:
            if unread_count and st.button("✓ Mark all read"):
                for n in st.session_state.notifs:
                    n["read"] = True
                st.rerun()
        with hdr3:
            if st.button("🗑 Clear all", key="clear_all_notifs"):
                st.session_state.notifs = []
                st.rerun()

        # Filter
        filter_options = ["all", "unread", "success", "error", "warning", "reminder"]
        selected_filter = st.selectbox(
            "Filter", filter_options,
            index=filter_options.index(st.session_state.notif_filter),
            label_visibility="collapsed", key="notif_filter_select"
        )
        st.session_state.notif_filter = selected_filter

        filtered = notifs
        if selected_filter == "unread":
            filtered = [n for n in notifs if not n["read"]]
        elif selected_filter not in ("all", "unread"):
            filtered = [n for n in notifs if n["type"] == selected_filter]

        st.markdown(f"<div style='background:{C['surface']};border:1px solid {C['border']};"
                    f"border-radius:14px;padding:8px 12px;margin-top:8px'>",
                    unsafe_allow_html=True)
        if not filtered:
            st.markdown(f"<div style='text-align:center;padding:24px;color:{C['textMuted']};font-size:13px'>"
                        f"🎉 All caught up!</div>", unsafe_allow_html=True)
        else:
            for n in filtered:
                notif_row(n)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:center;padding:40px;color:{C['textMuted']};font-size:13px'>"
                    f"No notifications yet. Fire some from above! 🚀</div>",
                    unsafe_allow_html=True)
