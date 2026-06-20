import streamlit as st
import random

# ---------- 页面配置 ----------
st.set_page_config(page_title="普通话练习", page_icon="📖")

# ---------- 获取汉字拼音 ----------
def get_pinyin(char):
    """获取单个汉字的拼音（带声调）"""
    result = pinyin(char, style=Style.TONE)
    return result[0][0] if result and result[0] else ""

# ---------- 随机汉字生成函数 ----------
def get_random_char(exclude_char=None):
    """
    从Unicode基本汉字区间(0x4E00 ~ 0x9FFF)中随机抽取一个汉字。
    如果提供了 exclude_char,则确保返回的汉字与之不同。
    """
    # 基本汉字区间共有 20992 个字符，足够随机且不易重复
    if exclude_char is None:
        return chr(random.randint(0x4E00, 0x9FFF))
    else:
        # 循环直到抽中与 exclude_char 不同的汉字（区间很大，几乎不会死循环）
        while True:
            candidate = chr(random.randint(0x4E00, 0x9FFF))
            if candidate != exclude_char:
                return candidate

# ---------- 初始化 session_state ----------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False      # 用户是否已登录
if 'username' not in st.session_state:
    st.session_state.username = ""              # 用户名
if 'current_char' not in st.session_state:
    st.session_state.current_char = None        # 当前显示的汉字
if 'previous_char' not in st.session_state:
    st.session_state.previous_char = None       # 上一次生成的汉字（用于避免重复）

# ---------- 侧边栏：切换用户（辅助功能） ----------
st.sidebar.markdown("### 账号管理")
if st.sidebar.button("🔄 切换用户"):
    # 重置所有状态，回到登录界面
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.session_state.current_char = None
    st.session_state.previous_char = None
    st.rerun()

# ---------- 主界面 ----------
st.title("📖 普通话练习")

# 情况1：未登录 -> 显示用户名输入表单
if not st.session_state.authenticated:
    with st.form("login_form"):
        username = st.text_input("请输入您的姓名", placeholder="例如：张三")
        submitted = st.form_submit_button("✅ 确认")
        if submitted:
            if username and username.strip():
                st.session_state.authenticated = True
                st.session_state.username = username.strip()
                # 清空历史汉字，重新开始练习
                st.session_state.current_char = None
                st.session_state.previous_char = None
                st.rerun()   # 立即刷新页面，进入主练习区
            else:
                st.error("用户名不能为空，请重新输入。")

# 情况2：已登录 -> 显示练习主界面
else:
    # 欢迎信息
    st.success(f"👋 欢迎，{st.session_state.username}！请开始您的普通话练习。")
    st.balloons()

    # ---- 核心按钮：随机生成汉字 ----
    if st.button("✨ 随机生成一个汉字", use_container_width=True):
        # 生成新汉字，保证不与上一个重复
        new_char = get_random_char(st.session_state.previous_char)
        st.session_state.current_char = new_char
        st.session_state.previous_char = new_char
        # 按钮点击后会自动重新运行脚本，无需额外 rerun

    # ---- 显示当前汉字 ----
    st.markdown("---")  # 分割线
    if st.session_state.current_char is not None:
        # 获取当前汉字的拼音
        pinyin = get_pinyin(st.session_state.current_char)
        # 显示拼音（在上方，大字体）
        st.markdown(
            f"<h2 style='text-align: center; font-size: 48px; margin: 10px 0; color: #666;'>{pinyin}</h2>",
            unsafe_allow_html=True
        )
        # 用超大字体展示汉字，便于练习
        st.markdown(
            f"<h1 style='text-align: center; font-size: 120px; margin: 20px 0;'>{st.session_state.current_char}</h1>",
            unsafe_allow_html=True
        )
        # 显示上一个汉字（辅助信息）
        st.caption(f"📌 上一个汉字：{st.session_state.previous_char}")
    else:
        st.info("👆 请点击上方按钮，生成第一个汉字。")
        st.caption("每次点击都会随机出现一个新汉字，并且不会与上一次的汉字重复。")

    # 额外提示（规则说明）
    st.markdown("---")
    st.caption("💡 规则：每次生成的汉字均不会与上一个重复，但可以隔代重复出现。")
