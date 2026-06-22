"""
PocketHub — Streamlit redesign  (run: streamlit run pockethub_app.py)
"""
import streamlit as st
from datetime import datetime
import random, uuid

st.set_page_config(page_title="PocketHub", page_icon="🗂", layout="wide",
                   initial_sidebar_state="collapsed")

C = dict(
    bg="#08090f", surface="#10121a", card="#14172280",
    border="#1e2235", borderBright="#2e3460",
    text="#eef0ff", textMuted="#5a6090", textSub="#9ba3d4",
    accent="#6366f1", accentSoft="#6366f118", accentGlow="#6366f133",
    success="#22c55e", error="#ef4444", warning="#f59e0b",
    info="#6366f1", birthday="#ec4899",
    purple="#8b5cf6", teal="#14b8a6", orange="#f97316",
)

TYPE_CFG = {
    "success":  {"color": C["success"],  "icon": "✅"},
    "error":    {"color": C["error"],    "icon": "❌"},
    "warning":  {"color": C["warning"],  "icon": "⚠️"},
    "info":     {"color": C["accent"],   "icon": "ℹ️"},
    "birthday": {"color": C["birthday"], "icon": "🎂"},
    "reminder": {"color": C["warning"],  "icon": "🔔"},
    "exam":     {"color": C["error"],    "icon": "📝"},
    "deadline": {"color": C["warning"],  "icon": "⏰"},
}

DEFAULT_FOLDERS = [
    {"id":"assignments","name":"Assignments","icon":"📚","color":C["warning"],"desc":"Homework, projects & submissions"},
    {"id":"credentials","name":"Credentials","icon":"🔐","color":C["success"],"desc":"Passwords, logins & access keys"},
    {"id":"notes","name":"Study Notes","icon":"📓","color":C["accent"],"desc":"Lectures, summaries & flashcards"},
    {"id":"exams","name":"Exam Prep","icon":"🎯","color":C["error"],"desc":"Mock tests, question banks & scores"},
]

DEMO_NOTIFS = [
    {"type":"success","title":"Note Saved","body":"Study notes for Chapter 7 saved."},
    {"type":"success","title":"Assignment Submitted","body":"Physics assignment submitted at 11:45 PM."},
    {"type":"error","title":"Login Failed","body":"Check your username and password."},
    {"type":"warning","title":"Due Tomorrow","body":"Maths Assignment 3 due at 11:59 PM."},
    {"type":"warning","title":"Exam in 2 Days","body":"Physics Unit Test — Thursday 9 AM."},
    {"type":"info","title":"Timetable Updated","body":"Wednesday lab moved to Room 204."},
    {"type":"birthday","title":"Priya's Birthday 🎂","body":"Don't forget to wish her!"},
    {"type":"reminder","title":"AFCAT Session 📚","body":"Study session at 6 PM tonight."},
    {"type":"exam","title":"Exam Alert 📝","body":"AFCAT mock test starts in 30 minutes!"},
]

FILE_EXT_ICONS = {"pdf":"📄","doc":"📝","docx":"📝","txt":"📃","png":"🖼️","jpg":"🖼️",
                  "jpeg":"🖼️","gif":"🖼️","mp4":"🎬","mp3":"🎵","zip":"📦",
                  "xlsx":"📊","xls":"📊","ppt":"📊","pptx":"📊","csv":"📊"}

FOLDER_ICONS = ["📁","📂","📚","🗂","🔐","📝","🎯","📓","🗄","💼","🧪","🏆","🎮","🔬","📊"]
FOLDER_COLORS = [C["accent"],C["success"],C["error"],C["warning"],C["birthday"],C["teal"],C["orange"],C["purple"]]
COLOR_NAMES = {"#6366f1":"Indigo","#22c55e":"Green","#ef4444":"Red","#f59e0b":"Amber",
               "#ec4899":"Pink","#14b8a6":"Teal","#f97316":"Orange","#8b5cf6":"Purple"}

def file_icon(n):
    ext = n.rsplit(".",1)[-1].lower() if "." in n else ""
    return FILE_EXT_ICONS.get(ext,"📎")

def fmt_size(b):
    if b<1024: return f"{b} B"
    if b<1_048_576: return f"{b/1024:.1f} KB"
    return f"{b/1_048_576:.1f} MB"

def now_full():
    return datetime.now().strftime("%b %d, %I:%M %p")

def new_notif(d):
    return {**d,"id":str(uuid.uuid4()),"read":False,"time":now_full()}

def push(d):
    st.session_state.notifs.insert(0, new_notif(d))
    cfg = TYPE_CFG.get(d["type"], TYPE_CFG["info"])
    st.toast(f"{cfg['icon']} **{d['title']}** — {d['body']}")

for k,v in [
    ("notifs",[]),
    ("folders",[dict(f) for f in DEFAULT_FOLDERS]),
    ("files",[]),
    ("open_folder",None),
    ("show_new_folder",False),
    ("notif_filter","all"),
    ("scribble_notes",""),
    ("note_entries",[]),
]:
    if k not in st.session_state:
        st.session_state[k] = v

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');
html,body,[class*="css"]{{font-family:'Plus Jakarta Sans',sans-serif!important;background:{C["bg"]}!important;color:{C["text"]}!important}}
#MainMenu,footer,header{{visibility:hidden}}
.block-container{{padding:1.5rem 2rem 4rem!important;max-width:1200px!important}}
.stTabs [role="tablist"]{{background:{C["surface"]};border-radius:14px;padding:5px;gap:4px;border:1px solid {C["border"]};width:fit-content}}
.stTabs [role="tab"]{{border-radius:10px!important;color:{C["textMuted"]}!important;font-weight:700!important;font-size:13px!important;padding:8px 18px!important;transition:all .2s!important}}
.stTabs [aria-selected="true"]{{background:linear-gradient(135deg,{C["accent"]},{C["purple"]})!important;color:#fff!important;box-shadow:0 4px 14px {C["accentGlow"]}!important}}
.stTabs [role="tabpanel"]{{background:transparent!important;padding:0!important}}
.stButton>button{{background:linear-gradient(135deg,{C["accent"]},{C["purple"]})!important;color:#fff!important;border:none!important;border-radius:10px!important;font-weight:700!important;font-size:13px!important;padding:9px 20px!important;box-shadow:0 4px 14px {C["accentGlow"]}!important;transition:all .2s!important;font-family:'Plus Jakarta Sans',sans-serif!important}}
.stButton>button:hover{{transform:translateY(-1px)!important;box-shadow:0 6px 20px {C["accentGlow"]}!important}}
.stTextInput>div>div>input,.stTextArea>div>div>textarea{{background:{C["surface"]}!important;color:{C["text"]}!important;border:1px solid {C["border"]}!important;border-radius:12px!important;font-size:13px!important;font-family:'Plus Jakarta Sans',sans-serif!important;padding:10px 14px!important}}
.stTextInput>div>div>input:focus,.stTextArea>div>div>textarea:focus{{border-color:{C["accent"]}!important;box-shadow:0 0 0 3px {C["accentGlow"]}!important}}
.stTextArea>div>div>textarea{{font-family:'JetBrains Mono',monospace!important;font-size:13px!important;line-height:1.7!important}}
.stSelectbox>div>div{{background:{C["surface"]}!important;color:{C["text"]}!important;border:1px solid {C["border"]}!important;border-radius:12px!important}}
.stFileUploader>div{{background:{C["surface"]}!important;border:2px dashed {C["border"]}!important;border-radius:16px!important;color:{C["textMuted"]}!important}}
.stFileUploader>div:hover{{border-color:{C["accent"]}!important}}
.streamlit-expanderHeader{{background:{C["surface"]}!important;color:{C["text"]}!important;border:1px solid {C["border"]}!important;border-radius:12px!important;font-weight:700!important;font-size:13px!important}}
.streamlit-expanderContent{{background:{C["surface"]}!important;border:1px solid {C["border"]}!important;border-top:none!important;border-radius:0 0 12px 12px!important}}
::-webkit-scrollbar{{width:5px}}::-webkit-scrollbar-track{{background:transparent}}::-webkit-scrollbar-thumb{{background:{C["border"]};border-radius:10px}}
hr{{border-color:{C["border"]}!important;margin:6px 0!important}}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="display:flex;align-items:center;gap:14px;padding:0 0 24px">
  <div style="width:46px;height:46px;border-radius:14px;background:linear-gradient(135deg,{C["accent"]},{C["purple"]});display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 6px 24px {C["accentGlow"]}">🗂</div>
  <div>
    <div style="font-size:22px;font-weight:900;color:{C["text"]};letter-spacing:-0.5px">PocketHub</div>
    <div style="font-size:11px;color:{C["textMuted"]};letter-spacing:0.5px;margin-top:1px">Files · Notes · Folders · Notifications</div>
  </div>
</div>
""", unsafe_allow_html=True)

tab_folders, tab_notes, tab_notifs = st.tabs(["📁  File Pockets","✏️  Notes & Scribble","🔔  Notifications"])

# ══ TAB 1 — FILE POCKETS ══════════════════════════════════════════════════════
with tab_folders:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    sc1,sc2 = st.columns([5,1])
    with sc1:
        search = st.text_input("","",placeholder="🔍  Search files across all folders…",label_visibility="collapsed",key="search_input")
    with sc2:
        if st.button("＋ New Folder"):
            st.session_state.show_new_folder = not st.session_state.show_new_folder

    if st.session_state.show_new_folder:
        st.markdown(f"<div style='background:{C['surface']};border:1px solid {C['borderBright']};border-radius:18px;padding:24px;margin:16px 0'><div style='font-size:15px;font-weight:800;color:{C['text']};margin-bottom:16px'>✨ New Folder</div></div>", unsafe_allow_html=True)
        nfc1,nfc2,nfc3 = st.columns([3,1,2])
        with nfc1: nf_name = st.text_input("Folder name",key="nf_name",placeholder="e.g. Chemistry")
        with nfc2: nf_icon = st.selectbox("Icon",FOLDER_ICONS,key="nf_icon")
        with nfc3: nf_color = st.selectbox("Colour",FOLDER_COLORS,key="nf_color",format_func=lambda c:COLOR_NAMES.get(c,c))
        ba,bb = st.columns(2)
        with ba:
            if st.button("✅ Create Folder",disabled=not (nf_name or "").strip()):
                st.session_state.folders.append({"id":f"f_{uuid.uuid4().hex[:8]}","name":nf_name.strip(),"icon":nf_icon,"color":nf_color,"desc":""})
                st.session_state.show_new_folder=False
                push({"type":"success","title":"Folder Created","body":f'"{nf_name}" is ready.'})
                st.rerun()
        with bb:
            if st.button("Cancel",key="nf_cancel"):
                st.session_state.show_new_folder=False; st.rerun()

    if search.strip():
        matches=[f for f in st.session_state.files if search.lower() in f["name"].lower()]
        st.markdown(f"<div style='color:{C['textMuted']};font-size:12px;margin:8px 0'>{len(matches)} result(s) for \"{search}\"</div>",unsafe_allow_html=True)
        if not matches:
            st.info("Nothing found — try a different name.")
        else:
            scols=st.columns(4)
            for i,f in enumerate(matches):
                fo=next((x for x in st.session_state.folders if x["id"]==f["folderId"]),None)
                fc=fo["color"] if fo else C["accent"]
                with scols[i%4]:
                    st.markdown(f"<div style='background:{C['surface']};border:1px solid {fc}44;border-radius:14px;padding:14px;text-align:center;margin-bottom:8px'><div style='font-size:34px;margin-bottom:6px'>{file_icon(f['name'])}</div><div style='font-size:11px;font-weight:700;color:{C['text']};overflow:hidden;text-overflow:ellipsis;white-space:nowrap'>{f['name']}</div><div style='font-size:9px;color:{C['textMuted']}'>{fmt_size(f['size'])}</div></div>",unsafe_allow_html=True)
                    if st.button("Remove",key=f"sdel_{f['id']}"):
                        st.session_state.files=[x for x in st.session_state.files if x["id"]!=f["id"]]; st.rerun()

    elif st.session_state.open_folder:
        folder=next((fo for fo in st.session_state.folders if fo["id"]==st.session_state.open_folder),None)
        if not folder: st.session_state.open_folder=None; st.rerun()
        bk,ti,rn=st.columns([1,5,1])
        with bk:
            if st.button("← Back"): st.session_state.open_folder=None; st.rerun()
        with ti:
            st.markdown(f"<div style='display:flex;align-items:center;gap:12px;padding:6px 0'><span style='font-size:32px'>{folder['icon']}</span><div><div style='font-size:18px;font-weight:900;color:{C['text']}'>{folder['name']}</div><div style='font-size:11px;color:{C['textMuted']}'>{folder.get('desc','')}</div></div></div>",unsafe_allow_html=True)
        with rn:
            with st.popover("✏️ Rename"):
                nn=st.text_input("New name",value=folder["name"],key="rf_inp")
                if st.button("Save",key="rf_save"):
                    for fo in st.session_state.folders:
                        if fo["id"]==folder["id"]: fo["name"]=nn.strip() or fo["name"]
                    st.rerun()
        uploaded=st.file_uploader("Upload files",accept_multiple_files=True,label_visibility="collapsed",key=f"up_{folder['id']}")
        if uploaded:
            for uf in uploaded:
                data=uf.read()
                st.session_state.files.append({"id":f"file_{uuid.uuid4().hex[:8]}","name":uf.name,"size":len(data),"folderId":folder["id"],"addedAt":datetime.now().isoformat(),"data":data})
            push({"type":"success","title":f"{len(uploaded)} File(s) Uploaded","body":f"Added to {folder['name']}."})
            st.rerun()
        folder_files=[f for f in st.session_state.files if f["folderId"]==folder["id"]]
        if not folder_files:
            st.markdown(f"<div style='text-align:center;padding:60px 20px;color:{C['textMuted']};font-size:13px;background:{C['surface']};border-radius:16px;border:1px solid {C['border']};margin-top:12px'><div style='font-size:52px;margin-bottom:12px'>{folder['icon']}</div><div style='font-weight:700;color:{C['textSub']};margin-bottom:4px'>Empty folder</div>Upload your first file above to get started.</div>",unsafe_allow_html=True)
        else:
            sc_s,_=st.columns([1,4])
            with sc_s: sort_by=st.selectbox("Sort","Date added,Name A→Z".split(","),label_visibility="collapsed",key=f"sort_{folder['id']}")
            folder_files=sorted(folder_files,key=lambda f:f["name"] if "Name" in sort_by else f["addedAt"],reverse="Name" not in sort_by)
            st.markdown(f"<div style='color:{C['textMuted']};font-size:11px;margin:4px 0 12px'>{len(folder_files)} file(s)</div>",unsafe_allow_html=True)
            fcols=st.columns(4)
            for i,f in enumerate(folder_files):
                with fcols[i%4]:
                    is_img=f["name"].rsplit(".",1)[-1].lower() in {"png","jpg","jpeg","gif","webp","svg"}
                    is_txt=f["name"].rsplit(".",1)[-1].lower() in {"txt","md","csv","json","py","js","html","css"}
                    st.markdown(f"<div style='background:{C['card']};border:1px solid {folder['color']}44;border-radius:14px;overflow:hidden;margin-bottom:8px'><div style='height:72px;display:flex;align-items:center;justify-content:center;background:{folder['color']}0d;font-size:34px;border-bottom:1px solid {C['border']}'>{file_icon(f['name'])}</div><div style='padding:10px 10px 8px'><div style='font-size:11px;font-weight:700;color:{C['text']};overflow:hidden;text-overflow:ellipsis;white-space:nowrap' title='{f['name']}'>{f['name']}</div><div style='font-size:9px;color:{C['textMuted']};margin-top:2px'>{fmt_size(f['size'])}</div></div></div>",unsafe_allow_html=True)
                    ac1,ac2,ac3=st.columns(3)
                    with ac1:
                        if is_img or is_txt:
                            with st.popover("👁"):
                                if is_img: st.image(f["data"],caption=f["name"])
                                else: st.code(f["data"].decode("utf-8","replace"))
                        else: st.download_button("⬇",data=f["data"],file_name=f["name"],key=f"dl_{f['id']}")
                    with ac2:
                        with st.popover("✏️"):
                            new_fn=st.text_input("Filename",value=f["name"],key=f"ren_{f['id']}")
                            if st.button("Save",key=f"rensave_{f['id']}"):
                                for fi in st.session_state.files:
                                    if fi["id"]==f["id"]: fi["name"]=new_fn.strip() or fi["name"]
                                push({"type":"success","title":"Renamed","body":f'→ "{new_fn}"'})
                                st.rerun()
                    with ac3:
                        if st.button("🗑",key=f"fdel_{f['id']}"):
                            st.session_state.files=[x for x in st.session_state.files if x["id"]!=f["id"]]
                            push({"type":"info","title":"File removed","body":f"{f['name']} deleted."})
                            st.rerun()
    else:
        folders=st.session_state.folders
        total_files=len(st.session_state.files)
        st.markdown(f"<div style='font-size:11px;color:{C['textMuted']};font-weight:700;text-transform:uppercase;letter-spacing:1.5px;margin:8px 0 18px'>{len(folders)} folders · {total_files} file{'s' if total_files!=1 else ''}</div>",unsafe_allow_html=True)
        gcols=st.columns(min(len(folders),4) or 1)
        for i,folder in enumerate(folders):
            fc=sum(1 for f in st.session_state.files if f["folderId"]==folder["id"])
            with gcols[i%4]:
                st.markdown(f"<div style='background:{C['surface']};border:1px solid {C['border']};border-radius:20px;padding:24px 20px 16px;margin-bottom:4px;position:relative;overflow:hidden'><div style='position:absolute;top:0;left:0;right:0;height:3px;background:linear-gradient(90deg,{folder['color']},{folder['color']}88)'></div><div style='font-size:40px;margin-bottom:14px'>{folder['icon']}</div><div style='font-size:15px;font-weight:800;color:{C['text']};margin-bottom:4px'>{folder['name']}</div><div style='font-size:11px;color:{C['textMuted']};margin-bottom:16px;line-height:1.5'>{folder.get('desc','')}</div><div style='display:flex;align-items:center;justify-content:space-between'><span style='font-size:10px;color:{folder['color']};font-weight:700;background:{folder['color']}18;border-radius:8px;padding:3px 10px'>{fc} file{'s' if fc!=1 else ''}</span><span style='color:{folder['color']};font-size:18px'>→</span></div></div>",unsafe_allow_html=True)
                oc1,oc2,oc3=st.columns([3,1,1])
                with oc1:
                    if st.button("Open",key=f"open_{folder['id']}"):
                        st.session_state.open_folder=folder["id"]; st.rerun()
                with oc2:
                    with st.popover("✏️"):
                        new_fn2=st.text_input("Name",value=folder["name"],key=f"rfold_{folder['id']}")
                        if st.button("Save",key=f"rfoldsv_{folder['id']}"):
                            for fo in st.session_state.folders:
                                if fo["id"]==folder["id"]: fo["name"]=new_fn2.strip() or fo["name"]
                            st.rerun()
                with oc3:
                    if st.button("🗑",key=f"dfold_{folder['id']}"):
                        st.session_state.folders=[fo for fo in st.session_state.folders if fo["id"]!=folder["id"]]
                        st.session_state.files=[f for f in st.session_state.files if f["folderId"]!=folder["id"]]
                        push({"type":"warning","title":"Folder deleted","body":f'"{folder['name']}" removed.'})
                        st.rerun()

# ══ TAB 2 — NOTES & SCRIBBLE ══════════════════════════════════════════════════
with tab_notes:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    left_notes,right_notes=st.columns([1.1,1])

    with left_notes:
        st.markdown(f"<div style='margin-bottom:10px'><div style='font-size:16px;font-weight:800;color:{C['text']}'>✏️ Scribble Pad</div><div style='font-size:12px;color:{C['textMuted']};margin-top:2px'>Quick scratch space — jot anything here, it persists all session.</div></div>",unsafe_allow_html=True)
        scribble=st.text_area("",value=st.session_state.scribble_notes,height=320,placeholder="Dump your thoughts here… equations, to-dos, random ideas, anything.",label_visibility="collapsed",key="scribble_area")
        st.session_state.scribble_notes=scribble
        sc_c1,sc_c2=st.columns(2)
        with sc_c1:
            wc=len(scribble.split()) if scribble.strip() else 0
            st.markdown(f"<div style='font-size:10px;color:{C['textMuted']};padding-top:6px'>{wc} words · {len(scribble)} chars</div>",unsafe_allow_html=True)
        with sc_c2:
            if st.button("🗑 Clear pad"):
                st.session_state.scribble_notes=""; st.rerun()
        st.markdown(f"<div style='margin-top:18px;font-size:12px;color:{C['textMuted']}'>Save as a note card →</div>",unsafe_allow_html=True)
        save_title=st.text_input("Note title",placeholder="e.g. Chapter 7 summary",key="save_note_title",label_visibility="collapsed")
        save_color_map={"Indigo":C["accent"],"Green":C["success"],"Amber":C["warning"],"Pink":C["birthday"],"Teal":C["teal"]}
        save_color_label=st.selectbox("Card colour",list(save_color_map.keys()),key="save_note_color",label_visibility="collapsed")
        if st.button("📌 Save as Note Card"):
            if scribble.strip():
                st.session_state.note_entries.insert(0,{"id":str(uuid.uuid4()),"title":save_title.strip() or "Untitled note","body":scribble.strip(),"color":save_color_map[save_color_label],"ts":now_full(),"attachment":None,"attachment_data":None})
                push({"type":"success","title":"Note saved","body":f'"{save_title or "Untitled note"}" added.'})
                st.rerun()
            else: st.warning("Scribble pad is empty — write something first.")

    with right_notes:
        st.markdown(f"<div style='margin-bottom:10px'><div style='font-size:16px;font-weight:800;color:{C['text']}'>📝 New Note</div><div style='font-size:12px;color:{C['textMuted']};margin-top:2px'>Compose a proper note with a title and optional attachment.</div></div>",unsafe_allow_html=True)
        nn_title=st.text_input("Title",placeholder="Note title…",key="nn_title",label_visibility="collapsed")
        nn_body=st.text_area("Body",placeholder="Write your note here…",height=200,key="nn_body",label_visibility="collapsed")
        nn_color_map={"Indigo":C["accent"],"Green":C["success"],"Amber":C["warning"],"Pink":C["birthday"],"Teal":C["teal"],"Purple":C["purple"]}
        nc1,nc2=st.columns(2)
        with nc1: nn_color_label=st.selectbox("Colour",list(nn_color_map.keys()),key="nn_color",label_visibility="collapsed")
        with nc2: nn_attach=st.file_uploader("Attach (optional)",key="nn_attach",label_visibility="collapsed")
        if st.button("📌 Add Note",key="add_note_btn"):
            if nn_body.strip() or nn_title.strip():
                entry={"id":str(uuid.uuid4()),"title":nn_title.strip() or "Untitled","body":nn_body.strip(),"color":nn_color_map[nn_color_label],"ts":now_full(),"attachment":nn_attach.name if nn_attach else None,"attachment_data":nn_attach.read() if nn_attach else None}
                st.session_state.note_entries.insert(0,entry)
                push({"type":"success","title":"Note added","body":f'"{entry['title']}" saved.'})
                st.rerun()
            else: st.warning("Add a title or body before saving.")

    notes=st.session_state.note_entries
    if notes:
        st.markdown(f"<div style='margin:28px 0 14px;display:flex;align-items:center;gap:10px'><div style='font-size:15px;font-weight:800;color:{C['text']}'>Your Notes</div><span style='font-size:11px;color:{C['textMuted']};background:{C['surface']};border-radius:8px;padding:2px 10px;border:1px solid {C['border']}'>{len(notes)} saved</span></div>",unsafe_allow_html=True)
        board_cols=st.columns(3)
        for i,note in enumerate(notes):
            with board_cols[i%3]:
                ab=f"<div style='font-size:10px;color:{C['textMuted']};margin-top:6px'>📎 {note['attachment']}</div>" if note.get("attachment") else ""
                st.markdown(f"<div style='background:{C['surface']};border:1px solid {note['color']}44;border-radius:16px;padding:18px;margin-bottom:10px;position:relative;overflow:hidden'><div style='position:absolute;top:0;left:0;width:100%;height:3px;background:linear-gradient(90deg,{note['color']},{note['color']}66)'></div><div style='font-size:13px;font-weight:800;color:{C['text']};margin-bottom:6px'>{note['title']}</div><div style='font-size:12px;color:{C['textSub']};line-height:1.6;white-space:pre-wrap;word-break:break-word'>{note['body'][:300]}{'…' if len(note['body'])>300 else ''}</div>{ab}<div style='font-size:9px;color:{C['textMuted']};margin-top:10px'>{note['ts']}</div></div>",unsafe_allow_html=True)
                d1,d2=st.columns(2)
                with d1:
                    if note.get("attachment_data"):
                        st.download_button("⬇ Attachment",data=note["attachment_data"],file_name=note["attachment"],key=f"ndl_{note['id']}")
                with d2:
                    if st.button("🗑 Delete",key=f"ndel_{note['id']}"):
                        st.session_state.note_entries=[n for n in st.session_state.note_entries if n["id"]!=note["id"]]; st.rerun()
    else:
        st.markdown(f"<div style='text-align:center;padding:50px 20px;color:{C['textMuted']};background:{C['surface']};border-radius:18px;border:1px solid {C['border']};margin-top:28px'><div style='font-size:48px;margin-bottom:12px'>📓</div><div style='font-weight:700;color:{C['textSub']};margin-bottom:4px'>No notes yet</div>Scribble something and pin it, or compose a note on the right.</div>",unsafe_allow_html=True)

# ══ TAB 3 — NOTIFICATIONS ════════════════════════════════════════════════════
with tab_notifs:
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    notifs=st.session_state.notifs
    unread_count=sum(1 for n in notifs if not n["read"])
    m1,m2,m3,m4=st.columns(4)
    for col,label,val,color in [(m1,"Total",len(notifs),C["accent"]),(m2,"✅ Success",sum(1 for n in notifs if n["type"]=="success"),C["success"]),(m3,"❌ Errors",sum(1 for n in notifs if n["type"]=="error"),C["error"]),(m4,"⚠️ Warnings",sum(1 for n in notifs if n["type"] in ("warning","deadline","exam")),C["warning"])]:
        with col:
            st.markdown(f"<div style='background:{C['surface']};border:1px solid {C['border']};border-radius:14px;padding:18px 16px;margin-bottom:20px;border-top:3px solid {color}'><div style='font-size:28px;font-weight:900;color:{color}'>{val}</div><div style='font-size:11px;color:{C['textMuted']};margin-top:3px'>{label}</div></div>",unsafe_allow_html=True)
    tl,tr=st.columns(2)
    with tl:
        with st.expander("✅ Success"):
            if st.button("Note Saved Successfully",key="ts1"): push({"type":"success","title":"Note Saved","body":"Study notes for Chapter 7 saved."}); st.rerun()
            if st.button("Assignment Submitted",key="ts2"): push({"type":"success","title":"Assignment Submitted","body":"Physics submitted at 11:45 PM."}); st.rerun()
            if st.button("Password Added",key="ts3"): push({"type":"success","title":"Password Added","body":"College Portal credential saved."}); st.rerun()
        with st.expander("❌ Errors"):
            if st.button("Invalid Login",key="te1"): push({"type":"error","title":"Login Failed","body":"Check username and password."}); st.rerun()
            if st.button("Failed to Save",key="te2"): push({"type":"error","title":"Save Failed","body":"Network timeout — changes lost."}); st.rerun()
        with st.expander("⚠️ Warnings"):
            if st.button("Assignment Due Tomorrow",key="tw1"): push({"type":"warning","title":"Due Tomorrow","body":"Maths Assignment 3 — 11:59 PM."}); st.rerun()
            if st.button("Exam in 2 Days",key="tw2"): push({"type":"warning","title":"Exam in 2 Days","body":"Physics Unit Test — Thursday 9 AM."}); st.rerun()
    with tr:
        with st.expander("ℹ️ Info & Reminders"):
            if st.button("Timetable Updated",key="ti1"): push({"type":"info","title":"Timetable Updated","body":"Wednesday lab → Room 204."}); st.rerun()
            if st.button("Good Morning ☀️",key="ti2"): push({"type":"reminder","title":"Good Morning ☀️","body":"3 classes today. First at 9:00 AM."}); st.rerun()
            if st.button("AFCAT Session 📚",key="ti3"): push({"type":"reminder","title":"AFCAT Session 📚","body":"Study session at 6 PM tonight."}); st.rerun()
            if st.button("Deadline in 4 Hours ⏰",key="ti4"): push({"type":"deadline","title":"Deadline ⏰","body":"Network Security — submit before 6 PM."}); st.rerun()
        with st.expander("🎉 Special"):
            if st.button("Priya's Birthday 🎂",key="tb1"): push({"type":"birthday","title":"Priya's Birthday 🎂","body":"Don't forget to wish her!"}); st.rerun()
            if st.button("Exam Alert 📝",key="tx1"): push({"type":"exam","title":"Exam Starting Soon 📝","body":"AFCAT mock test in 30 minutes!"}); st.rerun()
        with st.expander("⚡ Quick Fire"):
            if st.button("⚡ Fire 5 Random",key="tqf"):
                for p in random.sample(DEMO_NOTIFS,min(5,len(DEMO_NOTIFS))):
                    st.session_state.notifs.insert(0,new_notif(p))
                st.toast("⚡ Fired 5 random notifications!"); st.rerun()

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    if notifs:
        hc1,hc2,hc3=st.columns([3,1,1])
        with hc1:
            badge=(f" <span style='background:{C['error']};color:#fff;border-radius:20px;padding:2px 8px;font-size:10px;font-weight:700'>{unread_count} unread</span>" if unread_count else "")
            st.markdown(f"<div style='font-size:15px;font-weight:800;color:{C['text']}'>History{badge}</div>",unsafe_allow_html=True)
        with hc2:
            if unread_count and st.button("✓ Mark all read"):
                for n in st.session_state.notifs: n["read"]=True
                st.rerun()
        with hc3:
            if st.button("🗑 Clear all"):
                st.session_state.notifs=[]; st.rerun()
        flt_opts=["all","unread","success","error","warning","reminder"]
        sel=st.selectbox("Filter",flt_opts,index=flt_opts.index(st.session_state.notif_filter),label_visibility="collapsed",key="nfsel")
        st.session_state.notif_filter=sel
        filtered=notifs
        if sel=="unread": filtered=[n for n in notifs if not n["read"]]
        elif sel not in ("all","unread"): filtered=[n for n in notifs if n["type"]==sel]
        st.markdown(f"<div style='background:{C['surface']};border:1px solid {C['border']};border-radius:16px;padding:8px 14px;margin-top:10px'>",unsafe_allow_html=True)
        if not filtered:
            st.markdown(f"<div style='text-align:center;padding:28px;color:{C['textMuted']};font-size:13px'>🎉 All caught up!</div>",unsafe_allow_html=True)
        else:
            for n in filtered:
                cfg=TYPE_CFG.get(n["type"],TYPE_CFG["info"])
                dot="🔵 " if not n["read"] else ""
                r1,r2,r3,r4=st.columns([0.06,0.65,0.15,0.14])
                with r1: st.markdown(f"<div style='font-size:20px;padding-top:4px'>{cfg['icon']}</div>",unsafe_allow_html=True)
                with r2: st.markdown(f"<div style='padding:4px 0'><div style='font-size:12px;font-weight:700;color:{C['text']}'>{dot}{n['title']}</div><div style='font-size:11px;color:{C['textMuted']};line-height:1.4'>{n['body']}</div><div style='font-size:9px;color:{C['textMuted']};margin-top:2px'>{n['time']}</div></div>",unsafe_allow_html=True)
                with r3:
                    if not n["read"]:
                        if st.button("✓",key=f"r_{n['id']}"):
                            for x in st.session_state.notifs:
                                if x["id"]==n["id"]: x["read"]=True
                            st.rerun()
                with r4:
                    if st.button("✕",key=f"d_{n['id']}"):
                        st.session_state.notifs=[x for x in st.session_state.notifs if x["id"]!=n["id"]]; st.rerun()
                st.markdown(f"<hr style='border:none;border-top:1px solid {C['border']};margin:2px 0'>",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align:center;padding:50px;color:{C['textMuted']};background:{C['surface']};border-radius:18px;border:1px solid {C['border']};margin-top:12px'><div style='font-size:48px;margin-bottom:12px'>🔔</div><div style='font-weight:700;color:{C['textSub']};margin-bottom:4px'>No notifications yet</div>Fire some from the triggers above.</div>",unsafe_allow_html=True)
